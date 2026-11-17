# 通用接入合同｜Everlight/1

主机适配器负责可信身份、回执和实际请求。可先把以下操作映射到本地 SDK/进程，HTTP 只是同构的传输形式。单一 API 密钥不能代替用户与 workspace 的细粒度授权。接入合成环境不需要 DSH 插件。

| 操作 | 适配输入 | 响应 / 处理约束 |
|---|---|---|
| POST /v1/events | event_id、actor/source，原文或已验证回执 | 201 committed；相同键相同载荷 200 duplicate；相同键不同载荷 409 conflict |
| PATCH /v1/tasks/{id} | expected_revision、带来源的进度增量、事实/产物引用 | 200 新版本；409 版本冲突；任务不唯一先澄清 |
| POST /v1/claims/revise | expected_revision、canonical_key、目标修订/范围、证据 | 200 committed 或 disputed；拒绝未授权或伪证据，原始消息通过 events 入账 |
| POST /v1/memory/query | 任务、人、用途、有效时刻、可选已知水位、预算 | 200 + complete/partial/unavailable；source_refs、依赖水位、缺口，禁止伪装空结果 |
| POST /v1/evidence/read | source_ref、版本与范围 | actual_range、内容/哈希与 partial；没有权限不泄露是否存在 |
| POST /v1/context/prepare | run/attempt、scope、请求草案、版本、预算 | 单块候选及 digest，未读回为 unverified |
| POST /v1/context/observe | 宿主真实请求读回、绑定和出处 | matched / mismatch / unverified；不可让模型代报 |
| POST /v1/output/observe | 实际外显输出/流事件、attempt 绑定 | 按输出真实范围和状态记录 |
| POST /v1/actions/check | 规范对象、意图、权限、目标、幂等键 | allow/deny/check_existing；allow 是当次决定，不是永久许可 |
| POST /v1/actions/observe | 执行器回执与动作/尝试 ID | 区分 attempted、accepted、delivered、failed、unknown |
| POST /v1/maintenance/jobs | 授权调度器调用，水位、目的、预算 | 候选/拒绝/投影回执；任务重试取相同作业身份 |
| POST /v1/governance/erase | 授权删除请求，目标及范围 | 先阻用，再异步清理；分列不可控的外部副本 |
| POST /v1/restore | 有权恢复的备份及最新删除水位 | 完整、部分或拒绝；未知动作不重做 |

API 实例所有操作都须有调用身份。超预算或不可用输出可继续普通对话，返回证据缺口；禁止在动作链把不可用当允许。输入真实权限由验签/会话绑定产生，以下字段只是调用形状示例。

```json
{
  "schema": "everlight.event/1",
  "event_id": "msg-008",
  "operation_id": "op-008",
  "run_id": "run-003",
  "attempt_id": "turn-012",
  "scope": {"tenant": "tenant-demo", "workspace": "project-demo", "channel": "chat", "task": "task-12"},
  "actor_id": "actor-demo",
  "subject_id": "subject-demo",
  "source": {"kind": "host_message", "id": "msg-008", "revision": 1},
  "body": "刚才记错了，这次改回第二版；第三版还是别发。",
  "observed_at": "2026-11-17T05:35:00Z"
}
```

同一兼容版本只新增可选字段；枚举及行为改变升版本，接入握手协商。传输超时查询 operation_id 再决定重试，尤其是动作。当前没有部署这些路由；它们是可移植的接口规范。受限参考代码在 reference/。
