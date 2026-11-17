import sys,unittest,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'implementation_reference'))
from guarded_projection import Source,Candidate,project,AffectStream
class ProjectionTests(unittest.TestCase):
 def setUp(self):
  self.s={'s':Source('先别发送','doc'),'fix':Source('现在只保存草稿','doc'),'trip':Source('周末去旅行','trip')}
  self.c=Candidate('c','s','send',1,'先别发送')
 def test_exact_negative(self):
  r=project('doc',[self.c],self.s); self.assertEqual(r['selected'],['c']); self.assertIn('先别发送',r['block'])
 def test_historical_wrong_route(self):
  c=Candidate('bad','trip','x',1,'周末去旅行',route_label='doc')
  self.assertEqual(project('doc',[c],self.s)['rejected'],{'bad':'not_needed'})
 def test_historical_polarity_flip(self):
  c=Candidate('bad','s','send',1,'立即发送')
  self.assertEqual(project('doc',[c],self.s)['rejected'],{'bad':'unverified_summary'})
 def test_zero_history(self): self.assertEqual(project(None,[self.c],self.s)['block'],'')
 def test_missing_source(self): self.assertEqual(project('doc',[self.c],{})['status'],'partial')
 def test_deleted_source(self):
  self.s['s']=Source('先别发送','doc',deleted=True)
  self.assertEqual(project('doc',[self.c],self.s)['selected'],[])
 def test_stale_revision(self):
  self.s['s']=Source('先别发送','doc',revision=2)
  self.assertEqual(project('doc',[self.c],self.s)['selected'],[])
 def test_budget_atomic(self): self.assertEqual(project('doc',[self.c],self.s,budget=1)['block'],'')
 def test_exact_byte_budget(self):
  r=project('doc',[self.c],self.s); n=len(r['block'].encode())
  self.assertEqual(project('doc',[self.c],self.s,budget=n)['selected'],['c'])
  self.assertEqual(project('doc',[self.c],self.s,budget=n-1)['selected'],[])
 def test_missing_correction(self):
  c=Candidate('c','s','send',1,'先别发送',required=('missing',))
  self.assertEqual(project('doc',[c],self.s)['selected'],[])
 def test_correction_closure(self):
  c=Candidate('c','s','send',1,'先别发送',required=('f',)); f=Candidate('f','fix','update',1,'现在只保存草稿')
  self.assertEqual(set(project('doc',[c,f],self.s)['selected']),{'c','f'})
 def test_cycle_bounded(self):
  c=Candidate('c','s','send',1,'先别发送',required=('c',))
  self.assertEqual(project('doc',[c],self.s)['selected'],['c'])
 def test_same_root_different_claim(self):
  c=Candidate('other','s','different',1,'先别发送')
  self.assertEqual(len(project('doc',[self.c,c],self.s)['selected']),2)
 def test_same_claim_dedup(self):
  c=Candidate('other','s','send',1,'先别发送')
  self.assertEqual(len(project('doc',[self.c,c],self.s)['selected']),1)
 def test_duplicate_id_rejected(self):
  with self.assertRaises(ValueError): project('doc',[self.c,self.c],self.s)
 def test_invalid_budget(self):
  with self.assertRaises(ValueError): project('doc',[self.c],self.s,-1)
class AffectTests(unittest.TestCase):
 def setUp(self): self.a=AffectStream('user','progress','D')
 def apply(self,e,labels,rev,**kw): return self.a.apply(e,self.a.key,labels,rev,**kw)
 def test_explicit_correction(self):
  self.apply('one',['生气'],0); self.apply('two',['担心'],1)
  self.assertEqual(self.a.labels,('担心',)); self.assertEqual(len(self.a.events),2)
 def test_mixed(self): self.apply('one',['亲近','不满'],0); self.assertEqual(len(self.a.labels),2)
 def test_network_no_emotion(self):
  self.apply('one',['担心'],0); self.apply('net',['冷淡'],1,kind='network_fault')
  self.assertEqual(self.a.labels,('担心',)); self.assertEqual(self.a.revision,1)
 def test_delivery_not_satisfaction(self):
  self.apply('delivery',['满意'],0,kind='delivery_receipt'); self.assertEqual(self.a.labels,())
 def test_repeat_no_reinforcement(self):
  self.apply('one',['担心'],0); self.assertEqual(self.apply('one',['担心'],0),'replayed'); self.assertEqual(self.a.revision,1)
 def test_idempotency_conflict(self):
  self.apply('one',['担心'],0)
  with self.assertRaises(ValueError): self.apply('one',['满意'],1)
 def test_cas_conflict(self):
  self.apply('one',['担心'],0)
  with self.assertRaises(ValueError): self.apply('two',['满意'],0)
 def test_owner_separation(self):
  with self.assertRaises(ValueError): self.a.apply('one',('other','progress','D'),['担心'],0)
 def test_restore_last_known(self): self.assertEqual(self.a.restore()['observation'],'last_known')
if __name__=='__main__':
 suite=unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
 result=unittest.TextTestRunner(verbosity=2).run(suite)
 report={'scope':'isolated exact projection and explicit affect reducer; author-written fixtures',
 'tests_run':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),
 'real_host_tests_run':0,'open_semantic_tests_run':0,'production_approved':False}
 Path(__file__).with_name('reference_results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
 sys.exit(not result.wasSuccessful())
