"""Validate delivery structure and target SQLite constraints, not DSH behavior."""
from pathlib import Path
import re,json,sqlite3,hashlib
ROOT=Path(__file__).resolve().parents[1]
checks=[]
def ck(name,passed,detail=None):
    checks.append(dict(check=name,passed=bool(passed),detail=detail))

mods=sorted((ROOT/'modules').glob('R*.md'))
ck('24 module files', [p.stem for p in mods]==[f'R{i:02}' for i in range(1,25)])
for p in mods:
 s=p.read_text()
 nums=re.findall(r'^## (\d+)\. ',s,re.M)
 ck(p.stem+' 18 sections', nums==[str(i) for i in range(1,19)])
 ids=re.findall(r'\| (R\d\d-T\d\d) ',s)
 ck(p.stem+' 36 unique cases',ids==[p.stem+f'-T{i:02}' for i in range(1,37)])
ck('module registry all 24 modules',len(json.loads((ROOT/'contracts/module_registry.json').read_text()))==24)
cases=json.loads((ROOT/'verification/acceptance_cases.json').read_text())
ck('864 cases all not_run',len(cases)==864 and len({x['id'] for x in cases})==864 and all(x['status']=='not_run' for x in cases))
chains=json.loads((ROOT/'verification/integration_cases.json').read_text())
ck('40 chain cases all not_run',len(chains)==40 and all(x['status']=='not_run' for x in chains))
ck('all 24 modules covered by chain cases',set(sum((x['modules'] for x in chains),[]))=={f'R{i:02}' for i in range(1,25)})
unknown=[];table_errors=[];json_errors=[]
for p in sorted(ROOT.rglob('*.md')):
 s=p.read_text()
 unknown +=[(str(p.relative_to(ROOT)),n) for n in re.findall(r'\bR(\d\d)\b',s) if not 1<=int(n)<=24]
 for block in re.findall(r'```json\n(.*?)\n```',s,re.S):
  try:json.loads(block)
  except Exception:json_errors.append(str(p))
 cur=[]
 for line in s.splitlines()+['']:
  if line.startswith('|'):cur.append(line)
  elif cur:
   counts={len(re.sub(r'`[^`]*`','X',x).split('|')) for x in cur}
   if len(counts)!=1:table_errors.append((str(p),cur[0]))
   cur=[]
ck('valid module references',not unknown,unknown)
ck('markdown table widths',not table_errors,table_errors)
ck('JSON examples parse',not json_errors,json_errors)

db=sqlite3.connect(':memory:')
db.executescript((ROOT/'contracts/memory_schema.sql').read_text())
ck('DDL executes and foreign keys on',db.execute('PRAGMA foreign_keys').fetchone()[0]==1)
kinds=['working','episodic','semantic','procedural','relational','emotional','identity','metamemory','reflective','atlas']
tables=['working_memory','episodic_memory','semantic_memory','procedural_memory','relational_memory','emotional_memory','identity_memory','metamemory','reflective_memory','atlas_memory']
def base(id,kind,rev=1):
 db.execute('INSERT INTO memory_objects VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)',
 (id,kind,'demo','agent','session','channel',rev,'everlight/6','candidate',0,'2026-11-08T12:00:00+08:00','validator','demo-digest'))
def detail(table,id,kind,override=None):
 values={}
 for _,name,typ,notnull,default,_ in db.execute('PRAGMA table_info('+table+')'):
  if name=='object_id':values[name]=id
  elif name=='kind':values[name]=kind
  elif notnull:
   values[name]=('[]' if name.endswith('_json') else {'state':'active','record_type':'relation','change_mode':'unknown','axis':'work','index_state':'available'}.get(name,'demo'))
 values.update(override or {})
 db.execute('INSERT INTO '+table+'('+','.join(values)+') VALUES('+','.join('?' for _ in values)+')',list(values.values()))
for kind,table in zip(kinds,tables):
 base('ok-'+kind,kind); detail(table,'ok-'+kind,kind)
 ck('typed insert '+kind,db.execute('SELECT count(*) FROM '+table).fetchone()[0]==1)
db.commit()
def reject(name,fn,expected):
 db.execute('SAVEPOINT probe')
 try:
  fn();passed=False;message='unexpected acceptance'
 except sqlite3.IntegrityError as e:message=str(e);passed=expected in message
 finally:db.execute('ROLLBACK TO probe');db.execute('RELEASE probe')
 ck(name,passed,message)
for i,(kind,table) in enumerate(zip(kinds,tables)):
 wrong=kinds[(i+1)%10]
 def wrong_type(kind=kind,wrong=wrong,table=table):
  base('bad-type-'+kind,wrong);detail(table,'bad-type-'+kind,kind)
 reject('cross-kind write rejected '+kind,wrong_type,'FOREIGN KEY')
 jcols=[r[1] for r in db.execute('PRAGMA table_info('+table+')') if r[1].endswith('_json')]
 if jcols:
  def bad_json(kind=kind,table=table,col=jcols[0]):
   base('bad-json-'+kind,kind);detail(table,'bad-json-'+kind,kind,{col:'not-json'})
  reject('invalid JSON rejected '+kind,bad_json,'CHECK')
reject('unknown kind rejected',lambda:base('bad-kind','pretend-fact'),'CHECK')
reject('negative revision rejected',lambda:base('bad-rev','semantic',-1),'CHECK')
db.execute("INSERT INTO memory_versions VALUES('ok-working',1,'{}','hash','commit-demo')")
db.execute("INSERT INTO source_registry VALUES('source-demo','1','demo','event','hash',9,'acl',0)")
reject('invalid source range rejected',lambda:db.execute("INSERT INTO source_refs VALUES('ok-working',1,'source-demo','1','hash',5,2,'supports')"),'CHECK')
db.commit()
one=db.execute("UPDATE memory_objects SET revision=revision+1 WHERE id='ok-working' AND revision=1").rowcount
two=db.execute("UPDATE memory_objects SET revision=revision+1 WHERE id='ok-working' AND revision=1").rowcount
ck('CAS SQL pattern one winner',one==1 and two==0)
db.commit()
db.execute('BEGIN')
base('rolled-back','working');detail('working_memory','rolled-back','working')
db.rollback()
ck('base/detail rollback consistent',db.execute("SELECT count(*) FROM memory_objects WHERE id='rolled-back'").fetchone()[0]==0 and db.execute("SELECT count(*) FROM working_memory WHERE object_id='rolled-back'").fetchone()[0]==0)
ck('no foreign-key violations',not db.execute('PRAGMA foreign_key_check').fetchall())

r=json.loads((ROOT/'evidence/results.json').read_text());bad=json.loads((ROOT/'evidence/semantic_challenges.json').read_text())
ck('historical failed semantic challenges retained',r['passed']==21 and r['variant_passed']==210 and bad['semantic_failures']==2)
report=dict(scope='document structure and target DDL only',sqlite_version=sqlite3.sqlite_version,
            checks_passed=sum(c['passed'] for c in checks),checks_total=len(checks),checks=checks,
            module_acceptance_executed=0,integration_acceptance_executed=0,production_approved=False)
(ROOT/'verification/static_check_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps({k:v for k,v in report.items() if k!='checks'},ensure_ascii=False))
failed=[c for c in checks if not c['passed']]
if failed:print(json.dumps(failed,ensure_ascii=False,indent=2));raise SystemExit(1)
