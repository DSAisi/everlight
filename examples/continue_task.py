"""Run a complete offline task-memory example without keeping a local database."""
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'reference'))
from replay import Replay
from ingress import ingest


def scenario(path):
    scope, task = 'demo-workspace', 'design'
    key = f'artifact:{task}'
    store = Replay(path)
    try:
        seed = store.write(scope, 'turn-1', '草稿为第三版，第三版禁止发送。', [
            dict(op='set', key=key, value='v3', lo=1),
            dict(op='set', key=f'allow:{task}:v3', value=False, lo=1),
        ], task=task, work=dict(expected=0, artifact_key=key, decision_keys=[],
                               pending=['确认最终版本'], completed=['撰写草稿']))
        target = store.db.execute(
            'SELECT id FROM facts WHERE scope=? AND key=? AND src=?', (scope,key,seed)
        ).fetchone()[0]
        ingest(store, scope, 'turn-2', '刚才记错了，改回第二版。', dict(
            kind='explicit_correction', key=key, target=target, value='v2',
            expected=1, support_verified=True, quote='改回第二版', lo=1
        ), task=task, work=dict(expected=1, artifact_key=key, decision_keys=[],
                               pending=['查送达'], completed=['确认最终版本']))
        store.write(scope, 'turn-3', '只许可第二版走后续状态检查。', [
            dict(op='set', key=f'allow:{task}:v2', value=True, lo=2),
        ])
    finally:
        store.db.close()
    reopened = Replay(path)
    try:
        return {
            'work': reopened.read_work(scope, task, 3),
            'stale_index_read': reopened.current(scope,key,3,index_revision=1),
            'third_version_permission': reopened.current(scope,f'allow:{task}:v3',3),
            'resume': reopened.resume(scope,task,3,{(scope,task,'v3'):'confirmed'}),
        }
    finally:
        reopened.db.close()


if __name__ == '__main__':
    with TemporaryDirectory() as tmp:
        print(json.dumps(scenario(Path(tmp)/'demo.sqlite'), ensure_ascii=False, indent=2))
