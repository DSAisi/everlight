"""Offline reference: trusted structured commands, no model, no network."""
import json
import sqlite3
from contextlib import contextmanager

SCHEMA = """
CREATE TABLE IF NOT EXISTS events(
 seq INTEGER PRIMARY KEY, scope TEXT NOT NULL, event_id TEXT NOT NULL,
 payload TEXT NOT NULL, UNIQUE(scope,event_id));
CREATE TABLE IF NOT EXISTS heads(
 scope TEXT, key TEXT, rev INTEGER NOT NULL, PRIMARY KEY(scope,key));
CREATE TABLE IF NOT EXISTS facts(
 id INTEGER PRIMARY KEY, scope TEXT, key TEXT, val TEXT NOT NULL,
 lo INTEGER NOT NULL, hi INTEGER, state TEXT NOT NULL CHECK(state IN ('accepted','corrected')),
 src INTEGER NOT NULL REFERENCES events(seq), replaced_by INTEGER REFERENCES events(seq),
 CHECK(hi IS NULL OR hi>lo));
CREATE TABLE IF NOT EXISTS disputes(
 id INTEGER PRIMARY KEY, scope TEXT, key TEXT, lo INTEGER NOT NULL, hi INTEGER,
 src INTEGER NOT NULL REFERENCES events(seq), resolved INTEGER REFERENCES events(seq),
 CHECK(hi IS NULL OR hi>lo));
CREATE TABLE IF NOT EXISTS jobs(seq INTEGER PRIMARY KEY REFERENCES events(seq));
CREATE TABLE IF NOT EXISTS work(
 scope TEXT, task TEXT, rev INTEGER NOT NULL, state TEXT NOT NULL,
 source INTEGER NOT NULL REFERENCES events(seq), PRIMARY KEY(scope,task));
"""
class Conflict(Exception):
    pass

class Replay:
    def __init__(self,path):
        self.db=sqlite3.connect(path,isolation_level=None,timeout=5)
        self.db.execute('PRAGMA foreign_keys=ON')
        self.db.executescript(SCHEMA)

    @contextmanager
    def tx(self,write=False):
        self.db.execute('BEGIN IMMEDIATE' if write else 'BEGIN')
        try:
            yield
            self.db.commit()
        except BaseException:
            self.db.rollback()
            raise

    def _head(self,scope,key):
        row=self.db.execute('SELECT rev FROM heads WHERE scope=? AND key=?',(scope,key)).fetchone()
        return row[0] if row else 0

    def _view(self,scope,key,t,index_revision=None):
        rev=self._head(scope,key)
        route='canonical_fallback' if index_revision is not None and index_revision!=rev else 'canonical'
        args=(scope,key,t,t)
        fence=self.db.execute('SELECT id FROM disputes WHERE scope=? AND key=? AND resolved IS NULL AND lo<=? AND (hi IS NULL OR hi>?)',args).fetchall()
        if fence:return ('disputed',None,route)
        vals=self.db.execute("SELECT val FROM facts WHERE scope=? AND key=? AND state='accepted' AND lo<=? AND (hi IS NULL OR hi>?)",args).fetchall()
        if len(vals)==1:return ('known',json.loads(vals[0][0]),route)
        return ('disputed' if vals else 'unknown',None,route)

    def current(self,scope,key,t,index_revision=None):
        with self.tx():return self._view(scope,key,t,index_revision)

    def write(self,scope,event_id,body,commands,*,task=None,work=None,ingress_identity=None):
        """Trusted ingress only. Each command may carry a CAS revision.
        Work stores verified progress and references, never duplicated fact values.
        """
        allowed={'set','correct','dispute','resolve'}
        if not scope or not event_id or not isinstance(body,str) or not body:
            raise ValueError('invalid event identity/source')
        if (task is None)!=(work is None):raise ValueError('task/work pair required')
        if work is not None:
            if set(work)!={'expected','artifact_key','decision_keys','pending','completed'}:
                raise ValueError('invalid work shape')
            if not task or not work['artifact_key'] or not isinstance(work['expected'],int):
                raise ValueError('invalid work identity/revision')
            for k in ('decision_keys','pending','completed'):
                if not isinstance(work[k],list) or not all(isinstance(v,str) and v for v in work[k]):
                    raise ValueError('invalid work list')
            if set(work['pending'])&set(work['completed']):raise ValueError('inconsistent work')
        keys=set()
        for c in commands:
            op=c.get('op');key=c.get('key')
            schema={'set':{'op','key','lo','value'},'correct':{'op','key','target','value','expected'},
                    'dispute':{'op','key','lo'},'resolve':{'op','key','target','support','expected'}}
            optional={'set':{'expected'},'dispute':{'hi','expected'},'correct':set(),'resolve':set()}
            if op not in allowed or not key or key in keys:raise ValueError('invalid/duplicate operation')
            if not schema[op]<=c.keys() or c.keys()-(schema[op]|optional[op]):raise ValueError('invalid command fields')
            for f in ('lo','hi','target','support','expected'):
                if f in c and (type(c[f]) is not int or c[f]<0):raise ValueError('invalid numeric field')
            if 'hi' in c and c['hi']<=c['lo']:raise ValueError('invalid interval')
            keys.add(key)
        payload=json.dumps([body,commands,task,work] if ingress_identity is None else
                           [body,ingress_identity],ensure_ascii=False,sort_keys=True,allow_nan=False)
        with self.tx(write=True):
            old=self.db.execute('SELECT seq,payload FROM events WHERE scope=? AND event_id=?',(scope,event_id)).fetchone()
            if old:
                if old[1]!=payload:raise Conflict('event id reused with different payload')
                return old[0]
            seq=self.db.execute('INSERT INTO events(scope,event_id,payload) VALUES(?,?,?)',(scope,event_id,payload)).lastrowid
            for c in commands:self._apply(scope,seq,c)
            if work is not None:
                row=self.db.execute('SELECT rev FROM work WHERE scope=? AND task=?',(scope,task)).fetchone()
                rev=row[0] if row else 0
                if work['expected']!=rev:raise Conflict('work revision changed')
                state={k:v for k,v in work.items() if k!='expected'}
                self.db.execute('INSERT INTO work VALUES(?,?,?,?,?) ON CONFLICT(scope,task) DO UPDATE SET rev=excluded.rev,state=excluded.state,source=excluded.source',
                    (scope,task,rev+1,json.dumps(state,ensure_ascii=False),seq))
            self.db.execute('INSERT INTO jobs VALUES(?)',(seq,))
            return seq

    def _apply(self,scope,seq,c):
        key,op=c['key'],c['op'];rev=self._head(scope,key)
        if 'expected' in c and c['expected']!=rev:raise Conflict('claim revision changed')
        enc=lambda v:json.dumps(v,ensure_ascii=False,allow_nan=False)
        if op=='set':
            lo=c['lo']
            newer=self.db.execute("SELECT 1 FROM facts WHERE scope=? AND key=? AND state='accepted' AND (lo>=? OR (hi IS NOT NULL AND hi>?))",(scope,key,lo,lo)).fetchone()
            if newer:raise Conflict('overlap or out-of-order: use explicit dispute')
            self.db.execute("UPDATE facts SET hi=? WHERE scope=? AND key=? AND state='accepted' AND hi IS NULL",(lo,scope,key))
            self.db.execute("INSERT INTO facts(scope,key,val,lo,hi,state,src) VALUES(?,?,?,?,NULL,'accepted',?)",(scope,key,enc(c['value']),lo,seq))
        elif op=='correct':
            old=self.db.execute("SELECT lo,hi FROM facts WHERE id=? AND scope=? AND key=? AND state='accepted'",(c['target'],scope,key)).fetchone()
            if not old:raise Conflict('target revision not accepted in scope')
            self.db.execute("UPDATE facts SET state='corrected',replaced_by=? WHERE id=?",(seq,c['target']))
            self.db.execute("INSERT INTO facts(scope,key,val,lo,hi,state,src) VALUES(?,?,?,?,?,'accepted',?)",(scope,key,enc(c['value']),*old,seq))
        elif op=='dispute':
            self.db.execute('INSERT INTO disputes(scope,key,lo,hi,src) VALUES(?,?,?,?,?)',(scope,key,c['lo'],c.get('hi'),seq))
        elif op=='resolve':
            f=self.db.execute('SELECT lo,hi,src FROM disputes WHERE id=? AND scope=? AND key=? AND resolved IS NULL',(c['target'],scope,key)).fetchone()
            v=self.db.execute("SELECT lo,hi,src FROM facts WHERE id=? AND scope=? AND key=? AND state='accepted'",(c['support'],scope,key)).fetchone()
            if not f or not v or v[2]<=f[2] or v[0]>f[0] or (v[1] is not None and (f[1] is None or v[1]<f[1])):
                raise Conflict('new accepted evidence must cover disputed interval')
            self.db.execute('UPDATE disputes SET resolved=? WHERE id=?',(seq,c['target']))
        self.db.execute('INSERT INTO heads VALUES(?,?,?) ON CONFLICT(scope,key) DO UPDATE SET rev=excluded.rev',(scope,key,rev+1))

    def read_work(self,scope,task,t):
        with self.tx():return self._work(scope,task,t)

    def _work(self,scope,task,t):
        row=self.db.execute('SELECT rev,state FROM work WHERE scope=? AND task=?',(scope,task)).fetchone()
        if not row:return None
        rev,state=row[0],json.loads(row[1])
        # Decisions are canonical references resolved at read time, even when work.rev
        # did not change; a consumer cache must include dependency revisions.
        keys=[state['artifact_key'],*state['decision_keys']]
        return {**state,'rev':rev,'values':{k:self._view(scope,k,t)[:2] for k in keys},
                'claim_revs':{k:self._head(scope,k) for k in keys}}

    def resume(self,scope,task,t,delivery_lookup):
        with self.tx():
            view=self._work(scope,task,t)
            if not view:return 'clarify',None
            status,artifact=view['values'][view['artifact_key']]
            if status!='known':return 'clarify',None
            if self._view(scope,f'allow:{task}:{artifact}',t)[:2]!=('known',True):return 'blocked',artifact
            # Fixture receipts are identified by scope, task and exact artifact.
            delivery=delivery_lookup.get((scope,task,artifact))
            if delivery=='confirmed':return 'already_delivered',artifact
            return 'lookup_delivery',artifact
