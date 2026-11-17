from pathlib import Path
import json,hashlib
p=Path(__file__).resolve().parent
doc=json.loads((p/'hooks.json').read_text())
hooks={h['id']:h for h in doc['hooks']}
ids=set(hooks); assert ids=={f'H{i:02}' for i in range(21)}
module_ids={f'R{i:02}' for i in range(1,25)}
assert {m for h in hooks.values() for m in h['modules']}==module_ids
assert len(list((p/'baseline/modules').glob('R*.md')))==24
prod={s:h['id'] for h in hooks.values() for s in h['outputs']}
assert len(prod)==sum(len(h['outputs']) for h in hooks.values())
ext=set(doc['external_inputs'])
edges={(prod[s],h['id'],s) for h in hooks.values() for s in h['inputs'] if s in prod}
assert all(s in prod or s in ext for h in hooks.values() for s in h['inputs'])
assert all(h['failure'] and h['acceptance'] for h in hooks.values())
man=json.loads((p/'wiring.json').read_text())
for edge in man['boundary_bridges']:
 assert edge['from'] in ids and edge['to'] in ids
 edges.add((edge['from'],edge['to'], edge['event']))
def reachable(a,b):
 found={a}
 while True:
  more=found|{y for x,y,_ in edges if x in found}
  if more==found:return b in found
  found=more
for a,b in man['required_paths']:
 assert reachable(a,b),(a,b)
cases=json.loads((p/'fixtures/hook_acceptance.json').read_text())
assert len(cases)==len(hooks)
assert {c['id'] for c in cases}=={h['acceptance'] for h in hooks.values()}
assert all(c['state']=='not_run_on_real_host' for c in cases)
print(f'PASS: {len(hooks)} hooks, {len(module_ids)} modules, {len(edges)} declared edges, {len(cases)} real-host acceptance entries (not run)')
for fn in ('HANDOVER.md','HOOKS.md','PORTABLE_API.md','research/START_HERE.md','research/AFFECT_SOURCE_EXTRACT.md'):
 assert (p/fn).stat().st_size>0
f=p/'manifest.json'
if f.exists():
 m=json.loads(f.read_text())
 for n,digest in m['sha256'].items():
  assert hashlib.sha256((p/n).read_bytes()).hexdigest()==digest,n
 print(f"PASS: {len(m['sha256'])} manifest digests")
