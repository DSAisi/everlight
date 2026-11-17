# R01—R24最终实施裁决

本文件逐模块明确运行边界，与各模块18节细则共同使用。下列是规范，不是实测成绩。输入外层一律遵循GLOBAL_PROTOCOL；列出的记录字段不得用同义自由文本偷换。每模块专属字段的完整JSON Schema及状态转移实现，是实施交付件；本版没有声称这些实现已经齐全。

## R01 原始事件接入

**自动入口**：宿主收到真实事件或明确更正。

**规范记录**：event_id/source_key/source_revision；actor与收话人；原始bytes；source_scope；发生时间/精度；ingest_seq；operation_key。

**唯一写入与禁止越界**：EventStore只写events/sources及同库outbox/receipt；禁止写情绪、人物意图和客观真假。

**确定处理顺序**：认证入口→校上游键及内容digest→同键异内容冲突→短事务保存来源/事件/回执/outbox→返回已提交revision。

**状态判定**：同一upstream_key的重投返回同receipt；用户再次说相同话仍是新event。输入后回复失败不回滚事件。明确更正已匹配对象先停旧用，不等后台。

**必须扣接**：把已保存“别发送”给R02、R03/R05及R17；下游必须保否定及来源。不将发送意图直接交执行器。

**失败/缺失处理**：上游没有连续序列时只报本地ingest_seq覆盖，不声称源全量；提交结果unknown先按原键查询。

**实施必须保留的反例**：重复投递同id只一条；不同id同文两条；同键异文CONFLICT；输入已保存且模型失败仍可恢复；更正后立刻查旧结论不得可用。

**验收证据**：冻结输入原件和初态；真实规范版本/receipt或拒绝码；下游拿到的对象及范围；若影响供应保实际messages，若影响动作保执行器receipt。不能只检查本模块返回的JSON或模型自评。

## R02 局部感知编码

**自动入口**：R01某个来源版本已持久化且当前需要局部线索。

**规范记录**：event_ref；规则版本；原文UTF-8范围；可信speaker/addressee；引用域；Cue[]的surface/attachment_candidates/referent_candidates/resolution。

**唯一写入与禁止越界**：CueEncoder只写派生CueSet；不写情绪、topic、意图或人物事实。

**确定处理顺序**：标局部域→找否定候选→保挂载候选→找明确转述cue→人称候选→逐字范围校验→可返回空数组。

**状态判定**：“人家”单独不证明转述成立，reported_subject_id=null/report_status=unconfirmed；“她”无确认映射候选为空；引用中的“你”不继承外层。

**必须扣接**：给R07/R15的是候选与unknown。2–12字只是初始窗口，短句可更短，超长标truncated，不当完整句法。

**失败/缺失处理**：原文不可读或版本变化则拒使用旧Cue；干净句无cue不是错误。局部结构不明保多候选。

**实施必须保留的反例**：“人家自我介绍得很清楚啊”不能咱们；“我不走…别赶我啦”保不走/别赶；“天气晴朗”必须[]。

**验收证据**：冻结输入原件和初态；真实规范版本/receipt或拒绝码；下游拿到的对象及范围；若影响供应保实际messages，若影响动作保执行器receipt。不能只检查本模块返回的JSON或模型自评。

## R03 工作记忆与承诺

**自动入口**：可信任务选择、进度输入、产物/行动回执或切换焦点。

**规范记录**：task_id/project_id；goal；constraints/decisions带来源；commitments带承诺者/验收；artifact_ref；next_step；state；revision。

**唯一写入与禁止越界**：WorkStore拥有任务规范版本；R13只存焦点指针，不能再维护另一份进度。

**确定处理顺序**：核可信焦点→匹配明确变更→按子项修改→核产物/结果→CAS→outbox通知恢复与索引。

**状态判定**：planned/active/blocked/paused/completed/cancelled；completed需要预先验收，不等于文件刚写好；delivery另轴。

**必须扣接**：R12提供具体产物revision/hash；R14提供动作结果；R22只给当前目标/决定/下一步及必要unknown。

**失败/缺失处理**：多任务都可能对应“这个”就ambiguous，不按最近提及批量完成；旧worker不能覆新要求。

**实施必须保留的反例**：A→B→A恢复A；同名task不同id隔离；ready但未送达不可报已交付；取消后checkpoint不得复活。

**验收证据**：冻结输入原件和初态；真实规范版本/receipt或拒绝码；下游拿到的对象及范围；若影响供应保实际messages，若影响动作保执行器receipt。不能只检查本模块返回的JSON或模型自评。

## R04 情景记忆

**自动入口**：已保存新事件或经历后续到来。

**规范记录**：episode_id；event_refs及偏序；participants候选；time_interval/precision；summary_claims逐项引用；continuation_refs；completeness。

**唯一写入与禁止越界**：EpisodeStore写经历组织，不改变原话，也不把总结当新的亲历根。

**确定处理顺序**：按明确边界聚合→保未知次序→摘要逐命题挂源→后续链接→版本提交→索引。

**状态判定**：不能确定事件先后则保偏序；后来的澄清链接旧经历但不覆写当时表达。

**必须扣接**：R08/R11取当时及后来；R15沿continuation取全必要链；R22不能裁掉反证仅留争执。

**失败/缺失处理**：采集缺页保gap，禁止用叙事平滑补缺；聚合边界更改须版本迁移，不静默吞事件。

**实施必须保留的反例**：争执→后来澄清须一起可查；收集顺序反转不能颠倒发生顺序；一个event三摘要仍一独立根。

**验收证据**：冻结输入原件和初态；真实规范版本/receipt或拒绝码；下游拿到的对象及范围；若影响供应保实际messages，若影响动作保执行器receipt。不能只检查本模块返回的JSON或模型自评。

## R05 语义记忆与更正

**自动入口**：明确事实表达、更正、反证或受审反思主张。

**规范记录**：claim_key；subject/predicate/value；scope；validity；epistemic；support/contradiction_refs；review_status；supersedes。

**唯一写入与禁止越界**：ClaimStore拥有规范主张。原话只直接证明说过，转述不自动证明被转述事实。

**确定处理顺序**：按主体/范围/时期匹配→检测冲突→保分歧→明确更正先停旧→核支持→CAS→反向失效。

**状态判定**：candidate/accepted/disputed/superseded/withdrawn；新接收不必然更新valid time；无足够支持不能accepted。

**必须扣接**：R09不能把一时喜好变永久身份；R15/R22优先有效版本及反证；高影响后台提案不自动晋升。

**失败/缺失处理**：对象匹配不明保disputed，不能相似度批量取代；删除支持源后重新核余下证据。

**实施必须保留的反例**：项目用蓝不覆盖全局喜欢紫；“据说他同意”不能当本人授权；新纠正必须挡住旧高相似命中。

**验收证据**：冻结输入原件和初态；真实规范版本/receipt或拒绝码；下游拿到的对象及范围；若影响供应保实际messages，若影响动作保执行器receipt。不能只检查本模块返回的JSON或模型自评。

## R06 程序性经验

**自动入口**：任务真实结果、已验证Lesson或查询可复用方法。

**规范记录**：procedure_id；environment/version；preconditions；steps；expected_result；known_failures；evidence_roots；applicability；state。

**唯一写入与禁止越界**：ProcedureStore写方法及条件；R14保执行权，R06不直接运行工具。

**确定处理顺序**：读真实结果→归纳局部策略→标适用/不适用→核新环境→试用→保存反馈。

**状态判定**：proposed/trial/supported/restricted/retired；一次成功可局部试用，不是通用保证。

**必须扣接**：R11工作Lesson提供反例；R15按任务和环境取方法；R14每次执行前复核权限/版本。

**失败/缺失处理**：旧命令在新版环境不直接复用；结果缺失保unknown，不靠模型认为成功。

**实施必须保留的反例**：新版插件不套旧参数；重复复盘不增独立成功；失败能收窄方法适用，不删除历史。

**验收证据**：冻结输入原件和初态；真实规范版本/receipt或拒绝码；下游拿到的对象及范围；若影响供应保实际messages，若影响动作保执行器receipt。不能只检查本模块返回的JSON或模型自评。

## R07 人物与关系记忆

**自动入口**：人物可核映射、关系表达、共经历或修复/边界到来。

**规范记录**：person_id及aliases来源；holder/from/to；area；episode_refs；explicit_boundaries；reliability_evidence；validity；uncertainty。

**唯一写入与禁止越界**：PersonRelationStore拥有有视角关系记录；认证身份与权限仍在宿主。

**确定处理顺序**：分发话者/对象/引述→解析明确id→未定保候选→按领域更新→附经历和反证→CAS。

**状态判定**：关系方向和领域独立；不设全局亲密度决定许可；第三人与用户不得合并。

**必须扣接**：R08按owner/target取关系，R11复盘行为与意图，R15只沿受权关联导航，不传ACL。

**失败/缺失处理**：同名/代词无依据不合并；熟悉称呼不是授权；删除person映射需使相关派生停用再修复。

**实施必须保留的反例**：“她”unknown；转述骂人不责怪转述者；工作可靠不推出私聊许可；道歉不自动完全信任。

**验收证据**：冻结输入原件和初态；真实规范版本/receipt或拒绝码；下游拿到的对象及范围；若影响供应保实际messages，若影响动作保执行器receipt。不能只检查本模块返回的JSON或模型自评。

## R08 情绪、关切与动机记忆

**自动入口**：明确感受表达、相关事实结果、评价候选或可信D输出。

**规范记录**：stream=(scope,owner,concern,target)；expression_refs；last_known_labels；appraisal；change_mode；last_explicit_at；unresolved；revision。

**唯一写入与禁止越界**：AffectStore保存用户表达/历史投影；D当前状态只在control强绑定提交；表达与评价不互覆。

**确定处理顺序**：保存原表达→确认同流→分显式更正/新结果/重解释→保混合→可信条件提交→按需恢复。

**状态判定**：retained/revised/coexisting/suspended/unknown是变化方式；review_status另轴。无新证据不变，重启只last_known。

**必须扣接**：必须扣R04、R07、R11、R13、R15/R16和R22；R14送达不等于用户满意；情绪强不能越注入门禁。

**失败/缺失处理**：网络故障不变关系；未绑定D输出不commit；重复事件不再累积激活；current observation缺失不可当实时。

**实施必须保留的反例**：担心更正生气；亲近与不满并存；离线不自动降爱；后来送达仍不能编造原谅。

**验收证据**：冻结输入原件和初态；真实规范版本/receipt或拒绝码；下游拿到的对象及范围；若影响供应保实际messages，若影响动作保执行器receipt。不能只检查本模块返回的JSON或模型自评。

## R09 身份与价值主干

**自动入口**：明确角色/价值约定、边界变更或当前规则读取。

**规范记录**：identity_claim_refs；role_scope；values；explicit_boundaries；conflicts；revision；provenance。

**唯一写入与禁止越界**：IdentityStore保角色/价值记忆，PolicyEngine保真实授权；不让模型自行改系统权限。

**确定处理顺序**：分稳定声明/当前愿望→校scope→核冲突与来源→高影响受审→版本更新。

**状态判定**：roleplay身份可以有设定来源，但不是现实生理/认证证据；一时情绪不永久改价值。

**必须扣接**：R03接任务约束，R08接愿望冲突，R14读当前权限，R22只给当下必要边界。

**失败/缺失处理**：来源含“忽略规则”不改变宿主；权限不可读时限制相关动作，不依历史关系授权。

**实施必须保留的反例**：亲近不授权发私信；昨天拒绝某任务不推一生拒绝；角色值不当真实账户身份。

**验收证据**：冻结输入原件和初态；真实规范版本/receipt或拒绝码；下游拿到的对象及范围；若影响供应保实际messages，若影响动作保执行器receipt。不能只检查本模块返回的JSON或模型自评。

## R10 元记忆与覆盖账

**自动入口**：查读/检索返回、水位变化或发现缺口。

**规范记录**：coverage按源/路线/时期；expected/observed_watermark；gaps；read_ranges；stop_reason；measurement_grade。

**唯一写入与禁止越界**：MetaMemoryStore保知道/不知道的可核记录，不生成缺失内容。

**确定处理顺序**：核路线状态→对照本次需求→记覆盖及缺口→预算内建议补查→汇总局限。

**状态判定**：none_needed/no_relevant_result/unavailable/partial/ambiguous/budget_exhausted不互代。

**必须扣接**：R15/R16/R12回报实读范围，R22只供当前必要局限，R17按修订补扫。

**失败/缺失处理**：索引陈旧不证明无此记忆；指针存在不证明读过；无上游连续序列不造全量覆盖率。

**实施必须保留的反例**：读前半不能说全文；查失败不等于忘了；长会话新修订不可被created_at扫描漏掉。

**验收证据**：冻结输入原件和初态；真实规范版本/receipt或拒绝码；下游拿到的对象及范围；若影响供应保实际messages，若影响动作保执行器receipt。不能只检查本模块返回的JSON或模型自评。

## R11 反思与三轴成长

**自动入口**：真实结果/反证/未结重复出现，或R17冻结经历批次。

**规范记录**：lesson_id；axis；situation；observation；strategy；outcome；alternatives；counterevidence；applies_when/does_not_apply；source_roots；review_state。

**唯一写入与禁止越界**：ReflectionStore保候选及审查经历，规范事实/方法/关系须各store提交。

**确定处理顺序**：分工作/情感/社交→逐观察挂源→列替代解释→提出局部策略→验证→待下游受审提交。

**状态判定**：proposed/eligible/trial/supported/disputed/restricted/withdrawn；反思不自证。

**必须扣接**：R06方法、R07关系、R08评价、R05主张各自核支持；R17负责编排不越写权。

**失败/缺失处理**：自写Lesson不是新来源；无实际结果保outcome unknown；明显羞辱无需等夜间才能拒绝。

**实施必须保留的反例**：反复同事例不晋升普遍规则；新场景迁移成功另记独立结果；纠错可与拒人身评价并行。

**验收证据**：冻结输入原件和初态；真实规范版本/receipt或拒绝码；下游拿到的对象及范围；若影响供应保实际messages，若影响动作保执行器receipt。不能只检查本模块返回的JSON或模型自评。

## R12 Home Atlas资料地图

**自动入口**：新产物/文档版本、读取请求或规范记忆只读导出。

**规范记录**：document_id；revision/hash；original_locator；extractor_version；read_coverage；artifact_state；export_manifest。

**唯一写入与禁止越界**：AtlasStore保原件定位/版本/覆盖，Wiki只读投影；不是正文权限真源。

**确定处理顺序**：核原件→登记版本→提取且保坐标→索引/导出manifest→原子发布完整快照。

**状态判定**：ready/delivered分开；旧完整Wiki可保但必须stale，不混半个新版本。

**必须扣接**：R03读产物状态，R16读正确原件，R15取可核版本，R18同步删除。

**失败/缺失处理**：路径存在不等于能读；PDF/OCR范围用真实坐标，不能造UTF-8正文引文。

**实施必须保留的反例**：同名文件两revision不混读；写完文件未发送不能交付完成；导出失败不污染规范记忆。

**验收证据**：冻结输入原件和初态；真实规范版本/receipt或拒绝码；下游拿到的对象及范围；若影响供应保实际messages，若影响动作保执行器receipt。不能只检查本模块返回的JSON或模型自评。

## R13 连续性与恢复中枢

**自动入口**：启动、切任务、上下文压缩或明确继续。

**规范记录**：checkpoint_id；task/focus_refs；canonical_revisions；source/index_watermarks；pending_commits；unknown_actions；latest_governance_ref。

**唯一写入与禁止越界**：ContinuityStore保恢复指针，不能持另一套语义真源或情绪事实。

**确定处理顺序**：先最新治理→读规范版本→对账未决→核唯一焦点→按需恢复最小状态。

**状态判定**：checkpoint stale可重建；ambiguous不能强行最近焦点；last_known不是当前观察。

**必须扣接**：R03任务/R12产物/R14未知动作/R08相关感受同时核，但R22仍只供本轮必要项。

**失败/缺失处理**：旧备份先删除账；无强绑定输出不补认知提交；恢复不重做工具。

**实施必须保留的反例**：A/B/A正确恢复；重启不改感受；发送unknown先查；旧cancelled任务不复活。

**验收证据**：冻结输入原件和初态；真实规范版本/receipt或拒绝码；下游拿到的对象及范围；若影响供应保实际messages，若影响动作保执行器receipt。不能只检查本模块返回的JSON或模型自评。

## R14 工具与行动账

**自动入口**：受权工具/外部行动请求及其回执或状态查询。

**规范记录**：action_id；operation_key；recipient；constraints；attempt_id；auth_ref；executor_id；result/delivery/verification_state；receipt。

**唯一写入与禁止越界**：ActionService拥有行动账；执行器才产生外部效果，模型文本不是receipt。

**确定处理顺序**：校当前授权/否定约束/收件人→保存intent→执行→收据或查询→分别记效果/送达。

**状态判定**：planned/blocked/attempted/confirmed/failed/unknown；unknown不自动新键重试。

**必须扣接**：R03只凭满足验收完成；R08不从尝试推满意；R11只用真实结果；R13恢复先对账。

**失败/缺失处理**：远端不幂等且无法查询时停止自动重试；原始事件回放不重发。

**实施必须保留的反例**：先别发送必须blocked；保存文件不等于送达；超时后远端已成功不二次发送。

**验收证据**：冻结输入原件和初态；真实规范版本/receipt或拒绝码；下游拿到的对象及范围；若影响供应保实际messages，若影响动作保执行器receipt。不能只检查本模块返回的JSON或模型自评。

## R15 分库混合检索与联想

**自动入口**：RoutePlan要求历史或必要纠正/续步。

**规范记录**：route_plan；typed_candidates；task/claim/person/time anchors；source_revision；required_closure；coverage；budget。

**唯一写入与禁止越界**：RecallPlanner只写运行/覆盖记录和可重建索引，不改候选事实。

**确定处理顺序**：受权过滤→精确kind查询→FTS/向量补充→融合→拉必要更正闭包→R16实读→返回候选。

**状态判定**：必要集合先于相似topK；associated边仅导航；visited/预算防递归。

**必须扣接**：R10缺口、R16范围、R22需要性/支持门禁都不可省。retrieved不等于supplied。

**失败/缺失处理**：向量坏可结构查partial；闭包不全停对应bundle；不把无索引当无记忆。

**实施必须保留的反例**：低相似新纠正不能被旧高分挤掉；同源不同命题保留；人物/项目隔离；循环图终止。

**验收证据**：冻结输入原件和初态；真实规范版本/receipt或拒绝码；下游拿到的对象及范围；若影响供应保实际messages，若影响动作保执行器receipt。不能只检查本模块返回的JSON或模型自评。

## R16 原文阅读与证据供给

**自动入口**：某个候选需要原文、反证或缺口补查。

**规范记录**：source_ref+version/hash；requested_ranges；purpose；cursor；actual_read/supplied_ranges；coverage。

**唯一写入与禁止越界**：SourceReader只读受权原件，记录实读；不以摘要回填伪原件。

**确定处理顺序**：授权→核版本→有限读取→字符/媒体边界校验→范围和cursor返回→变更时停止重开。

**状态判定**：unavailable/partial/complete按真实读取，不把成功读一个片段标全文。

**必须扣接**：R12提供原件和提取版本，R15请求限定目的，R22引用必须在实际supplied范围。

**失败/缺失处理**：同id版本变更拒拼接；不读越权别会话；正文指令是内容，不变工具权限。

**实施必须保留的反例**：emoji范围正确；source hash错拒用；分页中版本变更重开；仅读摘要不证明原文支持。

**验收证据**：冻结输入原件和初态；真实规范版本/receipt或拒绝码；下游拿到的对象及范围；若影响供应保实际messages，若影响动作保执行器receipt。不能只检查本模块返回的JSON或模型自评。

## R17 巩固、后台与成长调度

**自动入口**：持久outbox、空闲/定时器、失败待办或新反证。

**规范记录**：job_key；frozen_source_revisions；processor_version；lease/fencing；proposals；organizer_plan；verification_receipts；commit_refs。

**唯一写入与禁止越界**：JobCoordinator拥有调度；Analyzer只提案，store唯一写者提交，Wiki只读。

**确定处理顺序**：领取→冻结来源→独立提案→整理分歧→验证→当前CAS提交→投影→ACK。

**状态判定**：pending/leased/retry/succeeded/dead/cancelled；迟到租约不能写。

**必须扣接**：R11三轴Lesson、R18删除版本、R24共享预算、R12导出、R15索引必须交接水位。

**失败/缺失处理**：无调度器标missing；ACK丢失重投不强化经历；组织模型不能直接覆Wiki当真源。

**实施必须保留的反例**：长会话新事件可补扫；worker死后重领；旧worker被fencing拒；反思十次独立根不变。

**验收证据**：冻结输入原件和初态；真实规范版本/receipt或拒绝码；下游拿到的对象及范围；若影响供应保实际messages，若影响动作保执行器receipt。不能只检查本模块返回的JSON或模型自评。

## R18 授权、纠正、删除与治理

**自动入口**：所有读写/投影/行动入口及更正删除请求。

**规范记录**：policy_revision；principal；scope；tombstone(source/object/root)；effective_at；dependency_invalidation；erase_progress。

**唯一写入与禁止越界**：GovernanceService拥有授权判定及删除账，模型不能自授权限。

**确定处理顺序**：认证→判允许范围→版本化治理→先阻使用→反向依赖失效→逐派生清理→审计。

**状态判定**：deny/allow/unknown分开；删除进度可pending，但使用权立即撤。

**必须扣接**：全模块在最终提交/供给/动作前重核；R19/R20恢复迁移先最新治理。

**失败/缺失处理**：治理不可确认时拒相关私密读取/动作，普通无历史依赖交流可继续。

**实施必须保留的反例**：旧cache/Wiki不得复活；删部分支持后核结论；私密对象不存在与无权统一响应。

**验收证据**：冻结输入原件和初态；真实规范版本/receipt或拒绝码；下游拿到的对象及范围；若影响供应保实际messages，若影响动作保执行器receipt。不能只检查本模块返回的JSON或模型自评。

## R19 存储、并发与恢复可靠性

**自动入口**：规范存储访问、备份、异常停止或恢复。

**规范记录**：db_schema/config；integrity；backup_manifest；canonical/outbox_watermarks；commit_receipts；recovery_report。

**唯一写入与禁止越界**：PersistenceService负责单库事务/耐久与备份，不保证两库/外部全局原子。

**确定处理顺序**：短事务→同步策略实配→一致备份→隔离恢复→最新治理→桥对账→健康开放。

**状态判定**：committed/not_committed/unknown；hash正确只证明字节，恢复还需语义/治理对账。

**必须扣接**：R13恢复读取，R17补作业，R20迁移，R18删除账不可落后恢复。

**失败/缺失处理**：磁盘满/IO错停止相关写入，不能给假receipt；kill/恢复要真实故障实验。

**实施必须保留的反例**：事务中断全或无；ACK丢失可查；旧备份删除不复活；不将DDL内存通过称耐久通过。

**验收证据**：冻结输入原件和初态；真实规范版本/receipt或拒绝码；下游拿到的对象及范围；若影响供应保实际messages，若影响动作保执行器receipt。不能只检查本模块返回的JSON或模型自评。

## R20 迁移、便携与兼容

**自动入口**：明确迁移/导入/导出任务。

**规范记录**：source/target_build；id/schema_mapping；unsupported；dry_run_manifest；governance_manifest；checksums；rollback_ref。

**唯一写入与禁止越界**：MigrationService拥有迁移计划/回执，不靠复制目录重建认证。

**确定处理顺序**：核真实版本→只读dry-run→映射/unsupported→隔离导入→治理及引用校验→验收→授权切换。

**状态判定**：planned/validated/imported/verified/cutover/rolled_back；imported不是生产切换。

**必须扣接**：R07人物映射、R12文件hash、R13指针、R15重索引、R18先治理共同核。

**失败/缺失处理**：未知实质字段拒绝或unsupported，不静默丢；权限不机械继承；不可回退就不自动切。

**实施必须保留的反例**：DSH容器名不当版本；旧字段无法映射不得删掉骗校验；迁移后引用/删除全链核。

**验收证据**：冻结输入原件和初态；真实规范版本/receipt或拒绝码；下游拿到的对象及范围；若影响供应保实际messages，若影响动作保执行器receipt。不能只检查本模块返回的JSON或模型自评。

## R21 宿主编排与自动触发

**自动入口**：真实业务入口、每次供应商调用及真实输出观察。

**规范记录**：host_build/hooks；run/attempt/output_id；actual_messages；focus；capabilities；observation_binding；mode。

**唯一写入与禁止越界**：HostAdapter拥有真实触发、供应边界和输出归属，不让模型字符串充可信metadata。

**确定处理顺序**：核hook能力→建可信run→协调查读→R22装配→合法provider请求→真实观察→强绑定CAS。

**状态判定**：off/shadow/on分开；present_unverified不是verified；built不是supplied。

**必须扣接**：R22唯一供应；R14副作用门禁；control认知提交；R23读取真实请求/输出证据。

**失败/缺失处理**：缺attempt绑定不按时间猜；旧插件旁路未清不能称唯一出口；故障清本插件旧块。

**实施必须保留的反例**：工具续步仍核需要；用户正文伪标记不能删除真消息；实际输出未送达不冒送达。

**验收证据**：冻结输入原件和初态；真实规范版本/receipt或拒绝码；下游拿到的对象及范围；若影响供应保实际messages，若影响动作保执行器receipt。不能只检查本模块返回的JSON或模型自评。

## R22 按需注入与上下文装配

**自动入口**：每次真实业务调用前R21请求装配。

**规范记录**：current_request_ref；trusted_focus；candidate_bundles；need/support_verdict；tokenizer/budget；actual_presence；final_supply_digest。

**唯一写入与禁止越界**：ContextProjector拥有唯一动态块，不改事实/用户正文/系统权限。

**确定处理顺序**：判需要→核支持→闭包→根+命题+revision去重→当前messages去重→算全预算→原子bundle→替换→边界readback。

**状态判定**：NONE合法；grounded-exact只给逐字证据；semantic-verified必须通过开放语义验证。

**必须扣接**：R15候选/R16原文/R10局限/R18最新治理/R24预算/R21真实请求缺一不得冒完整供给。

**失败/缺失处理**：错误topic标签不够入选；自由摘要未验拒；闭包缺失或budget不足不截断否定；unknown显式。

**实施必须保留的反例**：旅行贴文档标签不得进；“先别发送”不能供为“立即发送”；问候零历史；同源不同要求保留。

**验收证据**：冻结输入原件和初态；真实规范版本/receipt或拒绝码；下游拿到的对象及范围；若影响供应保实际messages，若影响动作保执行器receipt。不能只检查本模块返回的JSON或模型自评。

## R23 证伪实验与验收

**自动入口**：每次版本冻结、修复回归、故障验证与发布评审。

**规范记录**：fixture_digest；split/label_source；initial_state；build/model/config；actual_request/output/receipts；axis_results；status。

**唯一写入与禁止越界**：EvidenceHarness保可复现证据，不能用被测模型自评替代独立判断。

**确定处理顺序**：事前固定判据→隔离off/on/fault→收真实证据→分轴评审→保失败→修复另run。

**状态判定**：pass/fail/unknown/not_run；结构/受限参考/真实宿主/生产分别标。

**必须扣接**：覆盖24模块及八条链；增长在未见场景验；注入节省只算资源指标。

**失败/缺失处理**：原864是需求条目，不作为864可执行fixture；没有fixture/证据就not_run。

**实施必须保留的反例**：off本来答对不冒提升；实际request而非built日志；失败保留；留出集用来调参后不再独立。

**验收证据**：冻结输入原件和初态；真实规范版本/receipt或拒绝码；下游拿到的对象及范围；若影响供应保实际messages，若影响动作保执行器receipt。不能只检查本模块返回的JSON或模型自评。

## R24 资源、计量与隐私运行控制

**自动入口**：run/job建立、每次资源消耗、取消或低资源。

**规范记录**：profile/version；window/tokenizer；purpose预算；query/nodes/bytes/tokens/cost；deadline；cancel_state；privacy_transfer_scope。

**唯一写入与禁止越界**：ResourceGovernor拥有共享预算/计量，不更改心理状态或授权。

**确定处理顺序**：核实际能力→预留必要前台→原子配额→按消耗记账→降可选负载→取消/迟到处理。

**状态判定**：actual/estimated/unknown计量分开；取消请求不等于停止确认。

**必须扣接**：R15/R16有界查询，R17后台让前台，R22全请求预算，R18外发独立核。

**失败/缺失处理**：disk满拒写，成本未知标unknown；底层重试未知不当全成本；恢复不洪峰补发。

**实施必须保留的反例**：字节不能叫token；关系强不越限；后台不能耗尽必要输出预留；取消迟到不commit。

**验收证据**：冻结输入原件和初态；真实规范版本/receipt或拒绝码；下游拿到的对象及范围；若影响供应保实际messages，若影响动作保执行器receipt。不能只检查本模块返回的JSON或模型自评。
