# 全系统公共契约 v6

日期：2026-11-08。各R规格引用本文件的字段、状态与故障语义，但每个模块仍须实现其专属规则。所有接口为目标设计，不声称现役DSH已有对应端口。

## 1. 不可破坏的不变量

1. 原始事件、可修订主张、解释、当前状态、执行结果分开；源存在不等于支持某个结论。
2. 每个规范字段只有一个写入责任服务。其他模块可写自己的候选/投影，不私改别类真源。
3. 人物ID、scope、有效时期、记录时期、来源版本必须传递；关系边不传递访问权。
4. 用户输入/明确更正先入账；D依赖实际输出的认知状态须强观察绑定后CAS提交。
5. 记忆数量不等于成长；召回不等于读到；读到不等于实际供给；供给不等于模型采用；输出不等于送达。
6. 十类store分开校验、索引和查询；后台共享原始来源，不能把反思/情绪洗成事实。
7. 一个动态注入出口；允许零动态历史；源错/服务失败不能伪装不需要。
8. 单库事务原子不代表文件、两库和外部动作全局原子；unknown必须可查询/对账。
9. 删除先阻使用，再传播清理；恢复/迁移先用最新删除/撤回账，不能复活内容。
10. 工程资源阈值不是情感阈值；允许不变、矛盾、混合、暂缓、未知；不编造生理和内心测量。

## 2. 调用包络

CallEnvelope必需：schema_version=everlight-call/1，request_id，module，operation，trusted_context_ref，scope，deadline，cancel_token_ref。写操作有expected_revision与operation_key；读取有filter、snapshot_ref、limit/cursor。trusted_context由宿主签发或经认证通道建立，不由模型填一个principal字符串取得权限。

Scope必需namespace/agent_id/session_id/channel_id；跨会话来源的导入/后台读取另带真实source_scope与授权引用。project/task/environment可空，空不是通配。认证principal、原发话actor、命题主体subject、观点holder、感受owner、关系target、动作recipient分别命名，不得用一个user_id包办。

Instant为带时区ISO8601字符串，发生时间不明可null并记precision。索引/事件水位由其源契约定义，不把wall clock或ingest_seq冒上游连续序列。Revision对象内单调整数，更新携expected_revision，不能按时间最新或任意last-writer-wins覆写高影响事实。

ResultEnvelope含request_id/operation_id/module、disposition、object_refs、source_refs、coverage、gaps、receipt_ref和evidence_level。纯读committed_revision=null；proposed不是committed；no_result不是unavailable。无持久写的模块不能生成虚假提交回执。

ErrorEnvelope含code、retryable、commit_outcome、request_id、可公开reason、current_revision（有权才给）。code固定分类，私密查找用NOT_FOUND_OR_HIDDEN，不泄漏对象存在。未知提交先按操作键查询；重试不得悄悄换新动作键。

## 3. 来源与解释契约

SourceRef={source_id,source_revision,source_type,source_hash,start_byte?,end_byte?}，文本范围UTF-8半开且必须落字符边界；无范围引用指整个登记对象，不能冒全文已供给。PDF页/媒体时间另存；所有具体引文必须在本轮supplied_ranges内。

source_roots追到原始独立事件/可信外部结果；同一事件被总结10次仍一个根源。epistemic=self_report/other_report/observation/inference/unknown；review_status与change_mode/business_state分开。直接表达只支持谁当时说过/表达过，不必然支持客观事实、永久偏好或他人内心。

Dependency边区分derived_from/supports/contradicts/continuation/associated_with。关联导航不是支持或因果。更正/删除沿反向依赖使旧派生invalid_for_use，再重算；多源结论需核余下支持，不能只删引文保留旧结论。

## 4. 三条提交线与两库

输入线：R01在memory.sqlite内保存event/source/outbox/receipt；回复失败不回滚已保存输入。明确纠正先阻止旧推测当当前已证事实；匹配不清标争议。

认知线：control.sqlite保存run/proposal/实际观察和SelfState/八域版本；同库强绑定CAS可原子提交。对应历史Affect/Lesson在memory.sqlite的物化标projection_of_commit，并引用control commit ID，不充当第二份独立真源。投影滞后时查询当前状态须读规范control并保projection_pending，不能回旧索引冒最新。

行动线：R14先记录意图/尝试，授权门禁后调用执行器，回执/远端查询确认具体效果。独立事件回放不重做动作。外部不支持幂等且结果未知则待查，不能保证自动重试既不丢又不重复。

跨库桥：canonical_commit_id+target_projection_type+schema_version确定桥幂等键；源库事务写提交及本库outbox，消费者写目标并留receipt。源ACK前目标可能已成功，重投查询receipt；两侧水位和pending项可对账。不能把memory与control各自commit说成同一事务。

## 5. 当前状态与策略的真源

Work/Claim/Episode等规范记忆对象在memory typed stores；当前SelfState/八域协议前态在control。身份认证与授权来自宿主/PolicyEngine，身份记忆只是角色/事实视图。Checkpoint只指版本/水位，不能再维护另一套事实；Wiki是规范对象只读导出，不给模型并发改规范库的权限。

当前机器尚未知的DSH版本、插件、桥、模型、tokenizer、目录权限均填unverified；历史DSH0.1.5-rc.1/dsh-memory0.9.3或容器名不能代填现场。

## 6. 统一幂等与任务

幂等必须针对同一业务事件/操作，不吞用户重复说的真实话。处理键含scope、source ID/revision、目的、processor/schema版本；同键异实质输入冲突。查询可缓存但版本/策略/删除/实际问题变化须失效。

Job pending→leased→succeeded；暂错retry、永久错dead、源无效/撤回cancelled。lease带单调fencing，失约写者不得提交。重试上限/deadline/取消共享，客户端与内部不无限放大。模型调用在事务外，提交前核前态、来源、权限、取消和删除。

## 7. 能力与结果状态分轴

每个host hook为verified/present_unverified/missing；每route为available/partial/stale/unavailable/disabled/denied/unknown。Run、retrieval、read、supply、generation、commit、delivery、action、index、wiki发布分别记，不设遮盖一切的success。

evidence_level=design/static/synthetic_process/real_host/storage_fault/production。本文864个模块验收和全链验收初始not_run；文档结构检查、DDL约束实验不升级真实业务成绩。生产许可仍false。

## 8. 兼容与发布

新增字段通过everlight/6版本化适配，C032旧profile继续严格校验。Citation形状以旧版本真实schema为准，本稿SourceRef必须显式映射。grounding为非空数组；counterEvidence为数组可空；旧supersedes仅引用本轮合法可见同domain/subject条目。无法映射的字段明确unsupported，不能静默删掉实质内容或随意装入旧顶层。

off/shadow/on是适配模式：shadow不改业务请求；on只替换旧动态出口；off清本补丁拥有块，不关闭宿主原规则。切换需隔离回归、manifest、回退及用户已有授权；本次只交设计，不执行生产变更。
