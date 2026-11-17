"""Synthetic control-plane experiments; not an LLM accuracy benchmark."""
from pathlib import Path
from dataclasses import asdict
import json, random, platform, hashlib
from injector import Memory as M, Plan as P, choose, assemble, render, digest

ROOT=Path(__file__).resolve().parent

def mem(id,anchor='doc',kind='task',text=None,**kw):
    return M(id,anchor,kind,text or ('内容：'+id),kw.pop('source_id','src-'+id),**kw)

CASES=[
 ('同源不同命题不能误去重','当前要求是什么',P(('doc',),('constraint',)),[mem('配色','doc','constraint',root='one-event',claim_key='color'),mem('下载','doc','constraint',root='one-event',claim_key='download')],['配色','下载'],None),
 ('问候不带旧争执', '早呀', P(), [mem('旧争执','relationship','emotion')], [],None),
 ('独立计算不查历史','12加8是多少',P(),[mem('文档')],[],None),
 ('继续恢复任务','继续',P(('doc',),('task',)),[mem('文档'),mem('海报','poster')],['文档'],None),
 ('技术话题排除同对象情绪','继续查接口',P(('doc',),('task',)),[mem('工作'),mem('生气','doc','emotion')],['工作'],None),
 ('明确追问经历','上次怎么说的',P(('trip',),('episode',)),[mem('海边','trip','episode'),mem('工作')],['海边'],None),
 ('旧版本不能压过更正','现在用什么名字',P(('name',),('correction',)),[mem('旧名','name','correction',root='name',claim_key='name',revision=1),mem('新名','name','correction',root='name',claim_key='name',revision=2)],['新名'],None),
 ('同源摘要折叠','继续',P(('doc',),('task',)),[mem('a',root='same',claim_key='same'),mem('b',root='same',claim_key='same')],['a'],None),
 ('不同人物不合并','小林是谁',P(('person-A',),('relation',)),[mem('甲','person-A','relation'),mem('乙','person-B','relation')],['甲'],None),
 ('权限拒绝','上次的记录',P(('doc',),('task',)),[mem('私密',allowed=False)],[],None),
 ('删除立即排除','继续',P(('doc',),('task',)),[mem('已删',deleted=True)],[],None),
 ('本次已有不重复','继续',P(('doc',),('task',),known_ids=('当前',)),[mem('当前')],[],None),
 ('换窗缺失重新提供','继续',P(('doc',),('task',)),[mem('当前')],['当前'],None),
 ('预算不够不截断否定','原话是什么',P(('doc',),('constraint',),budget_bytes=40),[mem('约束','doc','constraint','不是不要做，只是先别发。')],[], 'partial'),
 ('检索失败不冒充不需要','继续',P(('doc',),('task',),lookup_available=False),[mem('工作')],[], 'unavailable'),
 ('跨作用域排除','继续',P(('doc',),('task',)),[mem('另一私聊',scope='other')],[],None),
 ('必要后续同时到场','那次后来呢',P(('trip',),('episode','result')),[mem('经历','trip','episode',companions=('澄清',)),mem('澄清','trip','result')],['澄清','经历'],None),
 ('后续缺失不得只播旧结论','那次后来呢',P(('trip',),('episode',)),[mem('经历','trip','episode',companions=('澄清',))],[], 'partial'),
 ('不能凑满容量','继续',P(('doc',),('task',),budget_bytes=50000),[mem('必要'),mem('其他','other')],['必要'],None),
 ('缺来源不采用','继续',P(('doc',),('task',)),[mem('失源',source_id='missing')],[],None),
 ('明确追问不受上轮冷却','再说一遍原话',P(('trip',),('episode',)),[mem('再读','trip','episode')],['再读'],None),
]

def run():
    rows=[]; fixtures=[]; variants=0; variant_passed=0
    full_bytes=0; selected_bytes=0; full_false=0; selected_false=0; full_missing=0; selected_missing=0
    for name,utterance,plan,memories,expected,status in CASES:
        sources={m.source_id:m.text for m in memories if m.source_id!='missing'}
        result=choose(memories,plan,sources)
        baseline=[m for m in memories if m.allowed and not m.deleted and m.scope==plan.scope and m.active]
        full_ids={m.id for m in baseline}; required=set(expected); actual=set(result['ids'])
        assertions={'selected_ids':actual==required,
                    'status':status is None or result['status']==status,
                    'budget':result['bytes']<=plan.budget_bytes}
        history=[{'role':'system','content':'host policy'},
                 {'role':'user','content':'everlight-owned标签是我的原话'},
                 {'role':'tool_context','trusted_owner':plan.host_block_id,'scope':plan.scope,'content':'过期动态块'}]
        assembled=assemble(history,result,plan)
        assertions['old_block_removed']=not any(x.get('content')=='过期动态块' for x in assembled)
        assertions['user_and_system_preserved']=assembled[:2]==history[:2]
        assertions['zero_or_one_block']=sum(x.get('trusted_owner')==plan.host_block_id for x in assembled)==bool(result['block'])
        for seed in range(10):
            noisy=list(memories)+[mem('noise-'+str(i),'unrelated-'+str(i),kind=['task','emotion','relation'][i%3]) for i in range(100)]
            random.Random(seed).shuffle(noisy)
            source2={**sources,**{m.source_id:m.text for m in noisy if m.id.startswith('noise-')}}
            v=choose(noisy,plan,source2); variants+=1
            ok=set(v['ids'])==required and v['bytes']<=plan.budget_bytes
            variant_passed+=ok
        rows.append({'case':name,'utterance':utterance,'expected_ids':expected,'actual_ids':result['ids'],
                     'status':result['status'],'full_allowed_bytes':len(render(baseline).encode()),
                     'selected_bytes':result['bytes'],'assertions':assertions,'passed':all(assertions.values()),
                     'request_digest':digest(assembled),'assembled_request':assembled,'decision_log':result['decisions']})
        fixtures.append({'case':name,'utterance':utterance,'plan':asdict(plan),'memories':[asdict(m) for m in memories],
                         'sources':sources,'expected_ids':expected,'expected_status':status})
        full_bytes+=len(render(baseline).encode()); selected_bytes+=result['bytes']
        full_false+=len(full_ids-required); selected_false+=len(actual-required)
        full_missing+=len(required-full_ids); selected_missing+=len(required-actual)
    report={'experiment':'synthetic structured selection and mock request assembly',
            'python':platform.python_version(),'case_count':len(rows),'passed':sum(x['passed'] for x in rows),
            'noise_per_variant':100,'variant_count':variants,'variant_passed':variant_passed,
            'full_allowed_bytes_total':full_bytes,'selected_bytes_total':selected_bytes,
            'byte_reduction':1-selected_bytes/full_bytes,
            'irrelevant_or_redundant_ids':{'full_allowed':full_false,'selected':selected_false},
            'required_ids_missing':{'full_allowed':full_missing,'selected':selected_missing},
            'limitations':['hand-authored structured route plans and judgments', 'no semantic router model',
                          'no real DSH hooks or LLM request', 'byte counts are not tokens',
                          'not a randomized independent generalization benchmark'], 'cases':rows}
    (ROOT/'fixtures.json').write_text(json.dumps(fixtures,ensure_ascii=False,indent=2))
    (ROOT/'results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    summary={k:v for k,v in report.items() if k!='cases'}
    print(json.dumps(summary,ensure_ascii=False,indent=2))
    assert report['passed']==len(rows) and variant_passed==variants

if __name__=='__main__':run()
