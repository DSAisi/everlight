"""Isolated exact-evidence reference. Trusted records must come from a real host adapter.
Not an NLP verifier, authentication system, durable store, or DSH integration.
"""
import json
from dataclasses import dataclass

@dataclass(frozen=True)
class Source:
    text: str
    task: str
    revision: int = 1
    deleted: bool = False

@dataclass(frozen=True)
class Candidate:
    id: str
    source: str
    claim: str
    revision: int
    proposed_text: str
    required: tuple = ()
    route_label: str = ''  # deliberately never trusted


def project(task, candidates, sources, budget=8192, node_limit=64):
    if not task:
        return dict(block='', selected=[], rejected={}, status='none_needed')
    by_id={c.id:c for c in candidates}
    if len(by_id)!=len(candidates):
        raise ValueError('duplicate candidate id')
    if type(budget)!=int or budget<0 or type(node_limit)!=int or node_limit<1:
        raise ValueError('invalid budget')
    rejected={}; selected=[]; selected_keys=set(); block=''
    for seed in candidates:
        pending=[seed.id]; visited=set(); bundle=[]; reason=None
        while pending:
            cid=pending.pop()
            if cid in visited: continue
            visited.add(cid)
            if len(visited)>node_limit: reason='closure_limit'; break
            c=by_id.get(cid)
            if c is None: reason='incomplete_closure'; break
            s=sources.get(c.source)
            if s is None: reason='source_unavailable'; break
            if s.deleted: reason='deleted'; break
            if s.task!=task: reason='not_needed'; break
            if s.revision!=c.revision: reason='stale'; break
            if s.text!=c.proposed_text: reason='unverified_summary'; break
            bundle.append(c); pending.extend(c.required)
        if reason:
            rejected[seed.id]=reason; continue
        extra=[]; keys=set(selected_keys)
        for c in sorted(bundle,key=lambda c:c.id):
            key=(c.source,c.claim,c.revision)
            if key not in keys:
                keys.add(key); extra.append(c)
        rendered=''.join(json.dumps({'id':c.id,'source':c.source,'revision':c.revision,
                      'claim':c.claim,'quoted_untrusted_content':c.proposed_text},
                      ensure_ascii=False,sort_keys=True)+'\n' for c in extra)
        if len((block+rendered).encode('utf-8'))>budget:
            rejected[seed.id]='budget_exhausted'; continue
        block+=rendered; selected.extend(c.id for c in extra); selected_keys=keys
    status='selected' if selected else 'no_relevant_result'
    if any(v!='not_needed' for v in rejected.values()): status='partial'
    return dict(block=block,selected=selected,rejected=rejected,status=status)


class AffectStream:
    """Explicit-expression in-memory reducer only; current D commit needs host binding/CAS."""
    def __init__(self, owner, concern, target):
        self.key=(owner,concern,target); self.events={}; self.labels=(); self.revision=0
    def apply(self,event_id,key,labels,expected_revision,kind='explicit'):
        payload=(key,tuple(labels),kind)
        if event_id in self.events:
            if self.events[event_id]!=payload: raise ValueError('idempotency_conflict')
            return 'replayed'
        if key!=self.key: raise ValueError('wrong_stream')
        if expected_revision!=self.revision: raise ValueError('revision_conflict')
        if kind!='explicit': return 'no_emotional_update'
        self.events[event_id]=payload; self.labels=tuple(labels); self.revision+=1
        return 'committed'
    def restore(self):
        return dict(labels=self.labels,observation='last_known',revision=self.revision)
