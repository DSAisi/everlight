# 通用宿主钩子契约

这是逻辑接线而非插件清单。H00–H20 可由同一进程部署；具有同一个 trace，但每轮和尝试必须分开。生产批准=false。输入的逗号项描述依赖：可信证据被消费时必验；并非每条 turn/job 都必须产生所有可选输入。空分支用显式 none/partial/not_applicable，并带原因。R18/R24 对相关路径常驻，不能被宿主未触发的可选 hook 替代。

最低可见链：H00→H01→H03/H04→H06–H10。独立生成输出还是执行任务由宿主决定；动作 H11 必须在任何副作用之前，实际结果 H12 随后回流。H14 的反馈事件回到 H01 走幂等入口；H18 恢复指针交下一轮 H04，水位交 H15；H19 补查回到 H06，建议作为同一个 H11 的新意图；H20 的策略候选经隔离批准后才由宿主切换配置。H16 在治理/前台修订后处理派生，逻辑失效在对应提交时即生效。

| Hook / 负责模块 | 输入 → 输出 | 故障语义 | 验收名称 |
|---|---|---|---|
| H00 接入与能力握手（R21 R18 R24） | authenticated_request, capability_probe → trusted_scope, capability_set | 认证失败拒绝；缺能力只降低接入档位 | capability_degrade |
| H01 入账与原文保全（R01 R19） | trusted_scope, host_event → event_receipt, source_ref | 未写入不报已保存；断网持久队列需显式状态 | transaction_reopen |
| H02 局部线索与人物绑定（R02 R07） | source_ref, trusted_scope → cue_set, identity_candidates | 引用、同名和否定有歧义则只给候选，不合并身份 | same_name |
| H03 当轮时态纠错（R05 R01 R18） | event_receipt, cue_set, identity_candidates, verified_patch → claim_heads, dispute_fence | 版本冲突重新核证；可界定则标时段争议，未绑定先保留原话 | targeted_correction |
| H04 工作台更新与恢复（R03 R12 R13） | event_receipt, claim_heads, dispute_fence, focus_hint, trusted_scope → work_snapshot | 读取依赖版本；同名任务需澄清；未知送达不得继续发送 | resume_v2 |
| H05 经历与认知提案（R04 R08 R09 R07） | source_ref, identity_candidates, work_snapshot → state_candidates, episode_ref | 事实、表达和推断分开；没有证据可以不更新 | affect_repair |
| H06 召回规划与查找（R15 R24） | work_snapshot, cue_set, state_candidates, claim_heads, dispute_fence, trusted_scope, capability_set → recall_candidates | 索引落后回规范库；时间/字节有界；无历史需要仍做最低检查 | stale_index |
| H07 原文、反证与覆盖（R16 R10 R12） | recall_candidates, source_ref, trusted_scope → evidence_bundle, coverage | 原文不可读标缺口；闭包不完整整组不装配 | partial_evidence |
| H08 请求前装配与替换（R22 R21 R18 R24） | evidence_bundle, coverage, work_snapshot, request_draft, capability_set → prepared_request, attempt_binding | 只替宿主所有的动态块；移除过期块；相关不足仍可普通对话 | replace_messages |
| H09 实际请求读回（R21 R23） | prepared_request, attempt_binding, actual_provider_request → request_receipt | 读不到就记 unverified；不以组装副本替代；真实输出另验 | provider_readback |
| H10 实际输出观察（R21 R19） | request_receipt, actual_host_output, attempt_binding → output_receipt | 输出按 run/attempt 绑定；无绑定记 unverified 不提交自我变化 | visible_output |
| H11 动作前门禁（R14 R18 R21） | action_intent, work_snapshot, claim_heads, dispute_fence, trusted_scope, capability_set → action_decision | 权限未知/缺钩子/范围错则拒；发送结果未知只能查询状态 | unknown_delivery |
| H12 实际行动回执（R14 R01 R03） | action_decision, actual_executor_event → action_receipt, receipt_event | 拟议/尝试/已接受/送达分开；未知不重发 | receipt_binding |
| H13 认知状态提交（R08 R09 R19 R21） | state_candidates, output_receipt, trusted_scope → state_commit_receipt | CAS 或绑定失败只落待核记录；不写第二份当前状态 | stale_state |
| H14 反馈闭环再入账（R01 R03 R11） | receipt_event, output_receipt, action_receipt, state_commit_receipt, optional_user_feedback → feedback_event | 没有真实反馈则未知；反馈不是成功的默认值 | false_success |
| H15 后台领取与做梦（R17 R11 R06 R24） | event_receipt, feedback_event, episode_ref, committed_cursor, trusted_scope → validated_patch | 租约/版本失效不提交；旧事件修订按水位补扫；候选可拒 | dream_stale |
| H16 派生失效、投影与 Wiki（R17 R12 R15 R19） | validated_patch, claim_heads, state_commit_receipt, governance_change → projection_receipt | 提交前重核授权和 CAS；立即阻旧使用；投影失败可重试并保水位 | projection_fail |
| H17 治理与撤回（R18 R19） | trusted_scope, authorized_governance_cmd → governance_change | 当轮 tombstone 阻用；跨存储失效异步对账，阻所有复活路径 | delete_restore |
| H18 恢复、迁移与对账（R19 R20 R13） | governance_change, authorized_recovery_cmd, projection_receipt → restored_cursor, restored_focus | 先加载最新删除账；引用不齐标部分；未知外部动作不重做 | restart_no_repeat |
| H19 持续需求观察与主动建议（R03 R14 R17 R24） | work_snapshot, coverage, feedback_event, capability_set → action_intent, followup_query | 节流、暂停及撤销有权；建议不等于执行；前台注入不靠提醒分数 | proactive_permission |
| H20 对照评估与受控 RSI（R23 R17 R15 R22） | request_receipt, output_receipt, action_receipt, projection_receipt, frozen_cases → evaluation_receipt, strategy_candidate | 候选无法改验收、授权和发布；失败保反例；回退策略不回滚事实 | rsi_holdout |

## 出站合同与证据
观测位置是宿主实际序列化后至网络/供应商 SDK 调用的最后可读边界。H08 必须标编排器拥有的唯一块、保留其余消息顺序和工具调用完整性。H09 保存请求摘要与脱敏差异，至少包含 run、attempt、request digest、旧动态块是否移除、新块范围和来源版本；记录失败不能冒成验证成功。H10 按同一尝试对应实际外显结果；流式输出如果已发片段，不宣称撤回，后续停止或澄清并记回执。有权限的真实请求/结果抽样与脱敏审计分开存。

## 四档有限检索：无召回强度硬门槛
宿主先做必需身份/权限、焦点、可见和动作检查。其后按工作量选择：L0 不注入历史；L1 精确键与当前时态；L2 附加类型/词法/语义候选和必需回读；L3 有界关联和补取原件。档位由问题的证据义务与能力决定，不以情绪强弱触发。面向未结任务可供应“未结总数 + 最相关前两条”，这不是完整清单，不能省去必要纠错或动作限制。
