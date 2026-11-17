"""Deterministic decision for trusted, preclassified host events."""
from replay import Conflict

def ingest(store,scope,event_id,body,signal,*,task=None,work=None):
    # Host must verify actor, canonical scope, and structured provenance before calling.
    if signal is None:
        return store.write(scope,event_id,body,[],task=task,work=work)
    identity=[signal,task,work]
    kind,key=signal['kind'],signal['key']
    if kind=='explicit_correction' and signal.get('target') is not None and signal.get('support_verified') is True:
        quote=signal.get('quote')
        if not quote or quote not in body:raise ValueError('missing original span')
        cmd=dict(op='correct',key=key,target=signal['target'],value=signal['value'],expected=signal['expected'])
    elif kind=='explicit_correction' or kind=='contradiction':
        # The key is bound by the host; only the target version may be unclear.
        cmd=dict(op='dispute',key=key,lo=signal['lo'])
        if 'hi' in signal:cmd['hi']=signal['hi']
        # Do not promote draft work based on a disputed claim.
        task=work=None
    elif kind=='confirmed_change' and signal.get('support_verified') is True:
        cmd=dict(op='set',key=key,lo=signal['lo'],value=signal['value'])
        if 'expected' in signal:cmd['expected']=signal['expected']
    else:
        raise ValueError('unsupported signal')
    try:
        return store.write(scope,event_id,body,[cmd],task=task,work=work,ingress_identity=identity)
    except Conflict:
        # The failed atomic update must never lose the raw message. Hold the scope/key
        # in dispute instead of guessing a replacement based on a stale snapshot.
        # A background proposal should call write() directly, not this ingress path.
        if 'lo' not in signal:raise
        fence=dict(op='dispute',key=key,lo=signal['lo'])
        if 'hi' in signal:fence['hi']=signal['hi']
        return store.write(scope,event_id,body,[fence],ingress_identity=identity)
