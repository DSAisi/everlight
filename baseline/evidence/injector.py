"""Isolated deterministic selection core. No model, network or DSH access."""
from dataclasses import dataclass, field
import hashlib
import json

@dataclass
class Memory:
    id: str
    anchor: str
    kind: str
    text: str
    source_id: str
    root: str = ''
    claim_key: str = ''
    revision: int = 1
    scope: str = 'private'
    allowed: bool = True
    deleted: bool = False
    active: bool = True
    companions: tuple = ()

@dataclass
class Plan:
    anchors: tuple = ()
    kinds: tuple = ()
    known_ids: tuple = ()
    budget_bytes: int = 2000
    scope: str = 'private'
    lookup_available: bool = True
    host_block_id: str = 'everlight-owned'

PRIORITY = {'correction':0, 'constraint':1, 'task':2, 'result':3,
            'episode':4, 'emotion':5, 'relation':6, 'knowledge':7}

def render(items):
    if not items:
        return ''
    # JSON encodes text as data; it does not make prompt injection impossible.
    return json.dumps({'memory_evidence':[{'id':m.id,'text':m.text,
        'source_id':m.source_id,'revision':m.revision} for m in items]},
        ensure_ascii=False,separators=(',',':'))

def choose(memories, plan, sources):
    if plan.budget_bytes < 0:
        raise ValueError('budget_bytes must be nonnegative')
    decisions={}; gaps=[]; eligible={}
    if not plan.lookup_available:
        return {'ids':[], 'block':'','mode':'NONE','status':'unavailable',
                'gaps':['lookup_unavailable'],'decisions':{},'bytes':0}
    latest={}
    for m in memories:
        key=(m.scope,m.root or m.id,m.claim_key or m.id)
        latest[key]=max(latest.get(key,0),m.revision)
    for m in memories:
        reason=None
        if m.scope!=plan.scope or not m.allowed: reason='scope_or_acl'
        elif m.deleted or not m.active: reason='invalidated'
        elif m.revision<latest[(m.scope,m.root or m.id,m.claim_key or m.id)]: reason='old_revision'
        elif m.source_id not in sources: reason='source_unavailable'
        elif m.anchor not in plan.anchors: reason='no_current_anchor'
        elif m.kind not in plan.kinds: reason='no_current_need'
        if reason: decisions[m.id]=reason
        else: eligible[m.id]=m
    # Fold only identical root and revision. Separate sources stay separate.
    representatives={}
    for m in sorted(eligible.values(),key=lambda m:(PRIORITY.get(m.kind,99),m.id)):
        key=(m.root or m.id,m.revision,m.claim_key or m.id)
        if key in representatives: decisions[m.id]='same_root_duplicate'
        else: representatives[key]=m
    candidates=sorted(representatives.values(),key=lambda m:(PRIORITY.get(m.kind,99),m.id))
    selected=[]; selected_ids=set()
    for m in candidates:
        if m.id in selected_ids: continue
        # Companions are required qualifiers, corrections or later outcomes.
        bundle=[m]; unavailable=[]
        for cid in m.companions:
            if cid in plan.known_ids: continue
            if cid not in eligible: unavailable.append(cid)
            elif cid not in selected_ids: bundle.append(eligible[cid])
        if unavailable:
            decisions[m.id]='required_companion_missing'
            gaps.append('missing_companion:'+m.id)
            continue
        if m.id in plan.known_ids:
            bundle=[x for x in bundle if x.id!=m.id]
            decisions[m.id]='already_in_actual_request'
        unique={x.id:x for x in selected+bundle}
        proposed=list(unique.values())
        if len(render(proposed).encode('utf-8'))>plan.budget_bytes:
            decisions[m.id]='budget_exhausted'
            gaps.append('budget_exhausted:'+m.id)
            continue
        for x in bundle:
            if x.id not in selected_ids:
                selected.append(x); selected_ids.add(x.id)
                decisions[x.id]='include'
    block=render(selected)
    status='partial' if gaps else ('selected' if selected else 'none_needed' if not plan.anchors else 'no_relevant_result')
    return {'ids':[m.id for m in selected],'block':block,
            'mode':'BRIEF' if selected else 'NONE','status':status,
            'gaps':gaps,'decisions':decisions,'bytes':len(block.encode('utf-8'))}

def assemble(history, result, plan):
    # Real adapters must supply trusted metadata, never parse user text as ownership.
    kept=[dict(m) for m in history if not (m.get('trusted_owner')==plan.host_block_id
          and m.get('scope')==plan.scope)]
    if result['block']:
        kept.append({'role':'tool_context','trusted_owner':plan.host_block_id,
                     'scope':plan.scope,'content':result['block']})
    return kept

def digest(value):
    return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True).encode()).hexdigest()
