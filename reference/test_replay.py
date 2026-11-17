import tempfile, threading, unittest
from pathlib import Path
from replay import Replay, Conflict
from ingress import ingest

def cmd(key,value,lo,**kw):return dict(op='set',key=key,value=value,lo=lo,**kw)
def work(rev,**kw):return dict(expected=rev,artifact_key='artifact:p',decision_keys=['color:p'],
                                  pending=['verify'],completed=['draft'],**kw)
class Suite(unittest.TestCase):
    def setUp(self):
        box=tempfile.TemporaryDirectory();self.addCleanup(box.cleanup)
        self.path=Path(box.name)/'isolated.sqlite';self.r=Replay(self.path);self.addCleanup(self.r.db.close)
    def put(self,e,*c,**kw):return self.r.write('s',e,e,list(c),**kw)
    def city(self,t,v=None):return self.r.current('s','city',t,v)
    def own(self):return self.r.db.execute("SELECT id FROM facts WHERE scope='s' AND key='city' ORDER BY id DESC LIMIT 1").fetchone()[0]
    def start(self):
        self.put('old',cmd('city','Boston',1))
    def fence(self):
        self.put('unclear',dict(op='dispute',key='city',lo=5))
    def test_old_index_no_worker(self):
        self.start();self.put('move',cmd('city','Seattle',5))
        self.assertEqual(self.city(6,1),('known','Seattle','canonical_fallback'))
        self.assertEqual(self.city(4)[1],'Boston')
        self.assertEqual(self.r.db.execute('SELECT count(*) FROM jobs').fetchone()[0],2)
    def test_targeted_auto_correction_retains_unrelated_history(self):
        self.start();self.put('move',cmd('city','Seattle',5));target=self.own()
        ingest(self.r,'s','fix','是波特兰，不是西雅图',dict(kind='explicit_correction',key='city',
               target=target,value='Portland',expected=2,support_verified=True,quote='是波特兰，不是西雅图',lo=5))
        self.assertEqual(self.city(4)[1],'Boston');self.assertEqual(self.city(5)[1],'Portland')
        self.assertEqual(self.r.db.execute('SELECT state FROM facts WHERE id=?',(target,)).fetchone()[0],'corrected')
    def test_future_without_dispute(self):
        self.start();self.put('plan',cmd('city','Portland',10))
        self.assertEqual(self.city(9)[1],'Boston');self.assertEqual(self.city(10)[1],'Portland')
    def test_future_does_not_clear_dispute(self):
        self.start();self.fence();self.put('plan',cmd('city','Portland',10))
        self.assertEqual(self.city(6)[:2],('disputed',None));self.assertEqual(self.city(4)[1],'Boston')
        with self.assertRaises(Conflict):
            self.put('bad-resolve',dict(op='resolve',key='city',target=1,support=self.own(),expected=3))
    def test_explicit_resolution(self):
        self.start();self.fence();self.put('known',cmd('city','Seattle',5))
        self.assertEqual(self.city(5)[0],'disputed')
        self.put('resolve',dict(op='resolve',key='city',target=1,support=self.own(),expected=3))
        self.assertEqual(self.city(5)[:2],('known','Seattle'))
    def test_typo_leaves_dispute_and_event_count(self):
        self.start();self.fence()
        with self.assertRaises(ValueError):self.put('bad',dict(op='typo',key='city',lo=7))
        self.assertEqual(self.city(8)[0],'disputed')
        self.assertEqual(self.r.db.execute('SELECT count(*) FROM events').fetchone()[0],2)
    def test_late_observation_not_current(self):
        self.put('now',cmd('city','Seattle',5))
        with self.assertRaises(Conflict):self.put('late',cmd('city','Boston',1))
        self.assertEqual(self.city(6)[1],'Seattle')
    def test_scope_and_idempotency(self):
        self.start();seq=self.put('old',cmd('city','Boston',1))
        self.assertEqual(seq,1)
        with self.assertRaises(Conflict):self.put('old',cmd('city','Seattle',1))
        self.r.write('other','old','other',[cmd('city','Seattle',1)])
        self.assertEqual(self.city(2)[1],'Boston')
    def test_ambiguous_correction_blocks(self):
        self.start()
        ingest(self.r,'s','fix','地点记错了',dict(kind='explicit_correction',key='city',lo=4))
        self.assertEqual(self.city(4)[0],'disputed')
    def test_stale_auto_correction_preserves_input_and_replays(self):
        self.start();target=self.own();self.put('move',cmd('city','Seattle',5))
        sig=dict(kind='explicit_correction',key='city',target=target,value='Portland',
                 expected=1,support_verified=True,quote='是波特兰',lo=1,hi=5)
        seq=ingest(self.r,'s','fix','是波特兰',sig)
        self.assertEqual(ingest(self.r,'s','fix','是波特兰',sig),seq)
        self.assertEqual(self.city(3)[0],'disputed')
        self.assertEqual(self.city(6)[1],'Seattle')
        self.assertEqual(self.r.db.execute('SELECT count(*) FROM events').fetchone()[0],3)
    def test_invalid_quote_does_not_write_claim(self):
        self.start()
        with self.assertRaises(ValueError):
            ingest(self.r,'s','fix','？',dict(kind='explicit_correction',key='city',
                   target=self.own(),value='X',expected=1,support_verified=True,quote='另一句话',lo=1))
        self.assertEqual(self.city(2)[1],'Boston')
    def test_work_update_and_receipt_identity(self):
        self.put('task',cmd('artifact:p','v3',1),cmd('allow:p:v3',False,1),cmd('color:p','red',1),task='p',work=work(0))
        self.put('update',cmd('artifact:p','v2',2),cmd('allow:p:v2',True,2),cmd('color:p','purple',2),
                 task='p',work=dict(expected=1,artifact_key='artifact:p',decision_keys=['color:p'],pending=['check receipt'],completed=['write','review']))
        view=self.r.read_work('s','p',3)
        self.assertEqual((view['rev'],view['pending'],view['completed']), (2,['check receipt'],['write','review']))
        self.assertEqual(view['values']['color:p'],('known','purple'))
        self.assertEqual(self.r.resume('s','p',3,{('s','p','v3'):'confirmed'}),('lookup_delivery','v2'))
        self.assertEqual(self.r.resume('s','p',3,{('s','p','v2'):'confirmed'}),('already_delivered','v2'))
        self.assertEqual(self.r.current('s','allow:p:v3',3)[1],False)
    def test_work_cached_revision_dependency_changes(self):
        self.put('task',cmd('artifact:p','v2',1),cmd('color:p','red',1),task='p',work=work(0))
        a=self.r.read_work('s','p',2)
        self.put('new-color',cmd('color:p','purple',2))
        b=self.r.read_work('s','p',2)
        self.assertEqual(a['rev'],b['rev'])
        self.assertNotEqual(a['claim_revs'],b['claim_revs'])
        self.assertEqual(b['values']['color:p'][1],'purple')
    def test_atomic_failure_and_reopen(self):
        self.put('good',cmd('artifact:p','v2',1),task='p',work=work(0))
        with self.assertRaises(Conflict):
            self.put('bad',cmd('artifact:p','v3',2),task='p',work=work(0))
        conn=Replay(self.path)
        try:
            self.assertEqual(conn.read_work('s','p',3)['values']['artifact:p'][1],'v2')
            self.assertEqual(conn.db.execute('SELECT count(*) FROM events').fetchone()[0],1)
            self.assertEqual(conn.db.execute('SELECT count(*) FROM jobs').fetchone()[0],1)
        finally:conn.db.close()
    def test_two_writers_same_revision_only_one_wins(self):
        self.start();barrier=threading.Barrier(2);results=[]
        def writer(i):
            c=Replay(self.path)
            try:
                barrier.wait(timeout=3)
                c.write('s',str(i),'update',[cmd('city',str(i),2,expected=1)])
                results.append('committed')
            except Conflict:results.append('stale')
            finally:c.db.close()
        ts=[threading.Thread(target=writer,args=(i,)) for i in (1,2)]
        for t in ts:t.start()
        for t in ts:t.join(timeout=8)
        self.assertEqual(sorted(results),['committed','stale'])
        self.assertEqual(self.r.db.execute('SELECT count(*) FROM jobs').fetchone()[0],2)
        self.assertIn(self.city(3)[1],('1','2'))
    def test_error_after_fact_insert_rolls_back_all(self):
        self.r.db.execute("CREATE TRIGGER fail BEFORE INSERT ON jobs BEGIN SELECT RAISE(ABORT,'fault'); END")
        import sqlite3
        with self.assertRaises(sqlite3.IntegrityError):
            self.put('attempt',cmd('artifact:p','v2',1),task='p',work=work(0))
        for t in ('events','heads','facts','work','jobs'):
            self.assertEqual(self.r.db.execute('SELECT count(*) FROM '+t).fetchone()[0],0)

if __name__=='__main__':unittest.main(verbosity=2)
