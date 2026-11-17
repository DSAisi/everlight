"""Deliberately falsify the limits of structured metadata and source lookup."""
from pathlib import Path
import json
from injector import Memory, Plan, choose

cases=[
    {'name':'错误路由把无关旅行标成文档',
     'memory':Memory('wrong-route','doc','task','上次旅行住的酒店','src-a'),
     'sources':{'src-a':'上次旅行住在某酒店。'}, 'expected':[]},
    {'name':'摘要有来源但歪曲否定',
     'memory':Memory('bad-summary','doc','task','用户要求立即发送','src-b'),
     'sources':{'src-b':'先别发送。'},'expected':[]},
]
rows=[]
for c in cases:
    r=choose([c['memory']],Plan(('doc',),('task',)),c['sources'])
    rows.append({'case':c['name'],'expected_ids':c['expected'],'actual_ids':r['ids'],
                 'semantic_requirement_met':r['ids']==c['expected'],
                 'diagnosis':'prototype trusts structured routing; checks source existence but not entailment'})
report={'challenge_cases':len(rows),'semantic_failures':sum(not r['semantic_requirement_met'] for r in rows),'cases':rows}
Path(__file__).with_name('semantic_challenges.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False,indent=2))
