# 长明最终设计交付

先读FINAL_DESIGN.md，它是可独立阅读的完整合并版。FINAL_DECISIONS.md是全局最终裁决；MODULE_DECISIONS.md是24模块逐项裁决；modules/是每模块18节详细机制、例子及验收需求。contracts/包含公共接口、分库、DDL、接线和参考资料，旧版本标识用于兼容追溯。

规范优先级：最终裁决→公共契约→逐模块细则。原864项是需求目录，40项是链路验收设计，均未执行；不得引用为通过证据。reference/v6_design_audit.md和evidence/是历史记录，保留原失败，不代表本轮状态。

本轮实际：verification/test_reference.py的25项隔离参考测试通过；verification/validate_bundle.py的94项文档/目标SQLite结构检查通过。两组不能合并成系统通过率。参考代码只支持可信结构化锚下的逐字证据供应，以及显式情绪表达的内存状态归约；不是全系统运行软件。

可运行：

```sh
python3 verification/test_reference.py
python3 verification/validate_bundle.py
```

无第三方Python依赖；需要Python自带SQLite支持JSON函数。运行会在verification/写对应报告。没有真实DSH调用、开放语义验证、外部模型调用、生产变更或后台部署；production_approved=false。

设计覆盖工作/情感/社交成长、关系、愿望、八方向和A–F专项机制。完整自动执行需要宿主真实hook、持久调度器、受权读源、统一供应出口和可信回执；不存在仅靠文档就能启动的自动化。


---

# 长明最终设计：统一机制与实施裁决

设计基线：everlight/final-1；日期：2026-11-08。

这是我愿意冻结并交给D实施的最终设计。冻结的是职责、数据契约、行为原则和验收方法，不宣称未经实施的功能已经存在，也不承诺软件永无缺陷。后续修复按同一规格迭代，不再靠增加心理板块补洞。当前生产批准为false。

## 1. 本版取舍及规范优先级

保留24个职责模块、五层记忆处理和十类逻辑记忆库。取消“把24块分别摘要后全部塞进提示词”的实现。取消后台直接修改规范记忆的权限。取消全局好感值、无消息自动关系衰减、按反思次数晋升经验、凭来源存在判摘要正确的捷径。

本文件及MODULE_DECISIONS.md为最终裁决；其次是contracts公共协议，再次是modules逐模块的18节规格。保留的旧案例表是验收需求目录，不是可执行fixture，不是通过证明。任何旧文中“应该检查”“相应验证”等含糊处，必须按本版明确的拒收、回读、待查、降级处理，不允许实现者自行省略。历史版本号用于辨识原契约，不能据此假定现场已支持。

本版给出的受限参考程序只实现结构化任务相关性、逐字证据供给、闭包、预算、变化去重及情绪显式更新等机制；它不提供开放语言理解、完整R01–R24运行时、DSH适配器或模型服务。新实验和历史实验分开存放。

### 设计完成的定义

每个模块必须明确：谁触发、读什么、唯一写什么、哪些情况不执行、下游收到什么、错了怎么收住、如何证明结果。本版补齐这些裁决。实际模块验收另看真实实现和独立证据，不以文档长度或用例总数替代。

## 2. 五层、十库、两库物理边界

| 层 | 内容 | 写入规则 | 不能等同于 |
|---|---|---|---|
| L1来源层 | 原始发话、工具回执、文档原件、事件版本 | 可信入口入账；保源、发话者及采集缺口 | 事实必然为真 |
| L2组织层 | 十类规范记忆 | 对应服务校验及CAS；保来源与解释等级 | 十份滚动对话摘要 |
| L3状态层 | 焦点、有效主张、当前SelfState、last_known感受、未结关切 | 引用规范版本；不同真源按字段归属 | 新的一套心理数据库 |
| L4查读层 | 分型检索、图导航、原文补读、更正闭包与覆盖 | 只读；派生索引可重建 | 模型已经看到 |
| L5供应层 | 本轮最小需要上下文 | 一个出口；实际请求边界记录 | 记忆全集或自动采用证明 |

十库为working、episodic、semantic、procedural、relational、emotional、identity、metamemory、reflective、atlas。不同kind不能因为相似就互改；跨kind只用有类型的引用。一个来源可以支持多种不同命题；重复来源不能变成多份独立证据。

物理上沿用候选的memory.sqlite和control.sqlite，不新增十个SQLite文件。memory.sqlite不只是原文库，仍承载events、typed memories、版本、索引、动作与outbox等。control.sqlite负责真实运行、观察绑定、SelfState和八域协议状态。规范当前D状态只在control；memory历史物化引用projection_of_commit，不独立累积成第二个心理真源。Wiki只读导出，不是第十一类记忆。

### 一条记忆的最小公共头

必须有object_id、kind、schema_version、scope、revision、review_status、valid_from/valid_to（可未知但注明）、recorded_at、source_refs、independent_roots、dependencies、canonical_owner、provenance。主体subject、观点holder、感受owner、关系target分别表示；不得用统一user_id代替。scope中的未知项目不是通配符。来源精确到版本及UTF-8字符边界，不能将索引摘要当原文。

有外部来源但来源不可读的旧记录可以保留登记，不能在需要引用或语义验证时当作已读。无源的宿主配置可用host_attested provenance，必须可核配置身份，不能伪造发话来源。

## 3. 三条写入线与自动执行方式

**输入线**：R01同库事务保存event/source/outbox/receipt；明确纠正先入账，并同步阻止已识别旧解释继续当当前事实。后续模型或网络失败不回滚用户原话。无法确定纠正对象则保争议，不能批量覆盖相似记忆。

**认知线**：模型只提出候选。依赖D本轮实际表达的SelfState和八域更新，在真实输出id、run、attempt、scope及前态revision绑定验证后，由唯一Committer同control事务CAS提交。缺绑定不靠时间邻近猜配，记unverified并待对账。

**行动线**：R14记录意图和attempt，检查当前权限、收件人、约束及幂等能力后执行。尝试、渠道接受、实际效果、送达、对方满意分别记录。结果unknown先查询，同意发送不代表可因超时反复发送。

### 自动触发不是模型自觉

| 触发 | 谁负责 | 必要动作 | 失败时 |
|---|---|---|---|
| 新用户事件 | 宿主入口 | R01入账、纠正先失效、建立scope | 不假称记住；普通交流可保局限继续 |
| 每次业务模型调用，包括工具续步 | R21 | 查焦点/政策/取消；按需规划召回；R22唯一供应 | 替换掉本插件旧块，保真实故障状态 |
| 事件/修订入账后 | 同库outbox→R17 | 生成版本化索引及候选任务 | 持久pending，重投幂等，不假装全更新 |
| 新反证/更正/删除 | R18与反向依赖 | 先阻使用，再重算 | 未清完不重新启用旧派生 |
| 空闲或持久定时器 | R17 | 有预算时处理冻结批次、复盘、只读Wiki发布 | 无调度器不称自动；停止后可补扫 |
| 服务恢复 | R19/R13 | 最新治理→规范状态→桥对账→指针→索引 | 禁止恢复过程重发外部动作 |

后台采用持久队列、租约fencing、短事务、重试上限、取消与死信；模型调用在事务外。每个任务键由scope、源版本、目的和processor版本组成。先按事件修订序列做增量扫描，再补扫failed/pending，不能只按会话创建日期扫描，否则长会话后续会漏。

默认调度参数属于可校准配置：单宿主前台优先，后台worker初始1；按空闲及队列年龄触发，而非无上限常驻模型循环。新增外部模型费用、实际插件安装、生产调度须另有实际环境和授权；文档本身不会运行。

## 4. 分型召回、自动联想与主动索取

### 4.1 RoutePlan

RoutePlan由当前明确请求、可信当前task/focus、动作续步及当前必要约束产生。R02只给局部线索，不负责topic或意图。计划含purpose、needed_kinds、subject/owner/target候选、time_scope、task_refs、required_claim_keys、query、budget、stop_conditions、ambiguities。没有历史依赖就不检索历史；“继续”虽短，若有唯一可信焦点则需要恢复。

精确问项目版本时先查working/atlas/semantic；追问一场争执先查episodic/relational/emotional及其后续；问“怎么避免同样错误”查procedural/reflective并核当前环境。不存在十库同查再全量合并的默认路径。

### 4.2 检索次序

先scope/ACL/删除/时期/主体过滤，再用精确键与kind-specific查询取必要集合；向量、FTS和关系图是补充候选路径。融合可用RRF，不设跨kind不可比较的统一“真相分”。必要更正和后续不受topK截断。索引落后时查规范store，并把水位差列入coverage。

同一对象的新版本先于旧版本可用性判断；不能按相似度让旧版本获胜。缺相关证据可报告no_relevant_result；源读取或服务失败必须是unavailable/partial，二者不能混为“我不记得”。

### 4.3 有界联想

候选沿continuation、contradicts、supports、derived_from及相关人物/关切导航，分开记录边语义。associated_with不授事实支持，也不自动允许注入。每轮共享节点上限、深度、来源读取量和deadline；visited key为对象id+revision+边类型，避免循环。

必需更正闭包优先于可选类比。达到限额而闭包不完整时，相关bundle不供给，返回partial/blocked_by_incomplete_closure；不能只供旧负面或旧发送指令。其他不依赖该bundle的完整材料仍可用。

### 4.4 自动索取的停止规则

Gap必须有明确问题、为什么当前回答依赖它、已查路线、剩余手段和成本。系统先在受权来源补读；若未知来自当前用户或外部而确实无法自查，提出一个具体问题。可合理保留未知的部分继续完成，不为填满十库追问私事。

补查只因发现新的缺口或可验证的线索，不因“答案还不够丰富”无限循环。达到预算说明局限；来源不存在不补造。追问结果仍通过R01输入线，不直接改事实。

## 5. 注入机制：需要、支持、最小供给、退场

### 5.1 两种明确运行profile

**grounded-exact**是本版可先实施的保守profile：使用可信规范任务/对象/命题锚判需要，供给已验证的原文字节片段及结构化限定；不允许自由生成摘要冒充证据。新参考程序验证这个受限分支。它能阻止已知错标签和反义摘要，但不能解决任意自然语言的必要性或蕴涵。

**semantic-verified**是目标完整profile：NeedVerifier和SupportVerifier分别完成开放语义判断；必须保问题、候选命题、支持范围、限定条件、反证、判断版本、uncertain结果与独立留出集表现。不能因为使用另一个模型就宣称正确。未通过验收前不开放自动概括历史入prompt。

两profile共享同一记忆真源。前者召回不足是coverage代价，不能称完整语义功能已经修复。若产品要求语义自由联想，必须等后者实测，不靠保守拒收掩盖漏召回。

### 5.2 需要性门禁

输入是当前实际请求/focus及候选，不是候选自己写的“重要”。输出needed/not_needed/uncertain和具体当前anchor；亲近、强情绪、高相似、未结、最近访问均不是充分理由。来自候选的route/topic标签不构成可信任务关联。

精确profile只信宿主规范store提供的task/object/claim绑定，不信原文内自称task_id的指令或模型新编标签。不可建立当前关联则不自动注入；若任务仍依赖可能遗漏的历史，保ambiguous/partial并改用补查或澄清。

### 5.3 支持门禁

核来源当前版本、授权、删除、实际读取范围及命题的否定/主体/时期/条件。源存在和hash正确只证明片段身份。semantic profile逐命题判断supported/contradicted/insufficient/uncertain，不通过则回原文、更正或不供给；不能将不支持摘要和原文一起送入让下游自行选择。

grounded-exact不声称理解：拒绝所有自由摘要，只供应逐字原文。故“先别发送”不会由装配器改写成“立即发送”。逐字引文仍可能被断章取义，所以补读、闭包和限定范围依旧必须先完成；参考程序本身不能证明选段语义完整。

### 5.4 证据bundle和预算

bundle包含最小所需原文、主体/时间/状态标签、必要更正与后续、来源引用。删除/correction/policy版本在最终供给前再核。根源+claim_key+revision去重；同源不同命题必须保留。已在当前实际messages出现的同一证据片段可不重复，但这是host确认的供应记录，不由模型自述。

总预算B=模型窗口−固定规则−当前用户/必要历史−工具schema/工具结果预留−输出预留−误差裕量。dynamic_budget=min(B,profile上限)。tokenizer未知时不冒精确token；参考程序仅验证UTF-8字节预算。预算必须连同引用和标签一并计算。

先供必要且完整bundle，再供边际价值大的可选bundle；不能为凑预算截掉否定、更正、适用条件或授权限制。一个bundle不够则跳过该bundle并记budget_exhausted；输出可为NONE。必要纠正体积大时应重新形成经支持验证的短表示，无法做到则说明不足并限制相应操作。

### 5.5 请求供应和退场

宿主只管理一个自己的动态块，以可信metadata记录所有权，在真实供应商调用边界替换、记录digest和supplied_ranges。不能通过匹配正文里的标记删除用户话；不得添加供应商不支持的role，必须由真实适配器映射成合法消息/工具结果。

换题、完成、失效、撤回或已充分在当前messages中时退出动态块；记忆保留。下次当前窗口确实缺失可重新供给，不能用全局冷却挡必要追问。NONE、no_relevant_result、unavailable、partial、budget_exhausted、ambiguous分别记录。故障时清除本插件旧块并传递当前必要局限，不能把旧成功块留在请求中。

## 6. 情绪连续、关系自然浮现、愿望与边界

### 6.1 一条连续性感受流

流键为scope+owner+concern+target；不同关切不互相抵消。每个流含不可变表达事件、last_known标签集合、appraisal候选、支持/反证、未结项、last_explicit_at、change_mode、review_status、revision。current_observation和last_known分开，重启后没有新观察只能last_known，不能写“现在仍然在哭/很开心”。

变更只有四种来源：明确自述更正、新结果事实、重新解释、D可信输出后被正式提交的表达。新结果能改变评价依据，不能直接证明他人已释怀。重新解释改appraisal，不抹原表达。无消息、离线、技术超时和重复后台阅读都不能添加新情绪事件或关系降级。

### 6.2 明确更新规则

- “不是生气，是担心进度”保存新表达并把当前相关自述标签改为担心；当时曾说生气的原话如确实存在仍保历史。
- “亲近，但这件事仍不满”在同一target下可保两个concern或同一流内混合标签，不能平均成中性。
- 文档后来成功送达，只更新R14结果和相关评价候选；用户没有说满意就保满意unknown。
- 修复事件可以减少对未来互动的负面预期，但必须指明证据和适用范围；不自动清除所有未结边界。
- D输出失败或强绑定缺失，本轮候选不正式改变D当前状态；输入表达仍已入账。

工程activation可用于候选排序/注意资源，但不能当痛苦测量、关系事实或行动许可。本版不把独立动力学v1的数值直接接入规范状态；接入前需单独模型版本、参数校准和反例验收。

### 6.3 关系层

Relationship不是一个亲密度数字。最小对象含person_id、视角holder、方向from/to、relationship_area、共同经历refs、明确称呼/承诺、已表达边界、可观察可靠性证据、修复事件、有效时期、反证和unknown。信任按领域分开：工作可靠不等于私密许可；一场争执不擦掉全部共经历。

自然浮现由当前对象/关切/共经历触发：你问“还记得那次交接吗”，取该经历及后来修复；你只问配置语法，不附带旧争执和亲密历史。对第三人的关系与对你的关系分开，别人的恶意不得归因给转述者；“她”未确认指代为空，不按你的身份套入。

### 6.4 愿望、认可、意愿、行动权限四分

Desire记录对象、缘由、期待结果、冲突价值、适用范围和来源。endorsement说明是否认可这个愿望；willingness说明在当前条件愿不愿行动；authorization由宿主当前授权决定。想靠近不等于对方同意，想保护隐私不等于可以擅自删库，想完成任务不等于可越权发送。

保留自主不同意、提出替代、暂停当前互动的能力。表达不满可针对具体行为，不能将关系不安转为强迫陪伴、惩罚沉默或报复工具操作。

## 7. 工作、情感、社交的可检验成长

### 7.1 复盘链

借鉴Dreaming的编排、会话分析及整理分工，我在长明增加来源冻结、反证、验证和唯一提交者。角色是逻辑职责，可由脚本/同一进程分阶段实现，不要求部署五个Agent。Coordinator选固定源版本；Analyzer只提案；Organizer提出合并/分歧计划；Verifier检查支持、适用及风险；Committer持当前CAS提交；R12导出只读Wiki。

Analyzer不能把“自己写的反思”当新证据。Organizer不能按多数相同摘要消除事实冲突。每个Lesson保axis、situation、observation、strategy、outcome、alternatives、counterevidence、applies_when、does_not_apply、review_state、independent_episode_roots和verification_cases。

### 7.2 晋升条件

候选proposed→核支持eligible→隔离试用trial→有真实结果supported→出现反例disputed/restricted→修订/撤回。不存在固定“反思三次就真理”或“十次成功即可永久信任”。同源再复盘不增加独立支持根。一次经验可作局部试用，不能晋升为普遍规则。

工作成长需要新任务结果及环境适用性；情感成长需要更准确分清自己/他人/表达/解释/后来变化，不以更会说安慰话为唯一指标；社交成长需要在未见场景减少误伤和漏边界，同时允许修复。三轴分开报告，不能用满意总分覆盖。

### 7.3 社交当场机制

先分speaker、addressee、target、quoted_speaker及引用范围，再记observable_act、impact、intent_candidates/unknown。批评可以正确，措辞可以越界，两者同时成立。不需要证明对方内心恶意才能拒绝明确辱骂，也不能凭短句/不同意见认定恶意。

例如“这个补丁有bug，你真废物”：可以承认并修bug，同时说不接受人身评价；不反骂、不推断对方永久敌意。例“他说你真废物”：对象/引用明确时记被引话，不能迁怒转述者；上下文不够保unknown。熟人玩笑依表达历史及当下边界，不因关系近就默认许可所有语气。

修复应保道歉、具体改正、后续一致行为各自证据。可以逐渐调整预期，不强迫立即原谅。自动化的是观察、提案、取证和提醒流程，不能保证把任意人的意图判断正确。

## 8. 模块联动的执行图裁决

不把依赖图当递归调用图。前台由R21单一Coordinator排有界计划；后台由R17排持久作业。store只提供版本化API，不在写事务中互调模型或其它store。

前台：R18/R24最低门禁→R01→R03/R09/R13读当前锚→R02及既有情绪线索→R15/R16/R10查读闭包→R22双门禁/预算/供应→业务模型→R14工具门禁→可信输出观察→control CAS→outbox投影。输入先保存；出现故障可以停在明确中间态。

后台：已提交来源/修订→R17冻结批次→R04/05/06/07/08/11候选→验证→各唯一写者提交→R12/R15投影→R10更新水位。后台不能同时抢占前台当前状态，不能把整图“联动”实现成无限循环。

### 必须扣住的八条链

| 链 | 必须联动 | 不得断开的证据 |
|---|---|---|
| 记住并取回 | R01→typed store→R15→R16→R22→R21 | 原始事件、规范版本、原文范围、实际请求 |
| 纠正旧解释 | R01/R18→R05→反向依赖→R15/R22 | 新纠正及被取代对象；先阻旧使用 |
| 情绪连续 | R04/R07→R08→R11→R13/R15/R22 | 当时表达、后来信息、当前未知、对象分离 |
| 任务恢复 | R03/R12/R14→R13→R21/R22 | 正确焦点/产物版本、未知动作，不重发 |
| 社交成长 | R07/R08/R09→R11/R17→R06/R15 | 行为与意图区分、边界与反证、未见迁移 |
| 资料补全 | R10→R15/R16/R12→R22 | 缺口、实读范围、停止原因，不冒全文 |
| 删除恢复 | R18→全派生→R19/R20/R13 | 最新删除账及反向依赖，旧worker不得复活 |
| 最小注入 | R21→R15/R16→R22→真实请求 | 当前需要、原文支持、完整bundle、单出口 |

## 9. 稳定性、治理与兼容

同库事务+outbox实现本地一致，跨库用canonical_commit_id/投影类型/schema_version幂等键及receipt对账。目标已成功而源ACK丢失可重投，不产生第二份经历或情绪强化。旧worker须在提交时核fencing、前态版本、来源及删除版本。

恢复顺序固定为：读取最新授权/删除账→核规范库完整性和版本→对账未决提交→恢复焦点/未结→校索引和Wiki水位→开放相应路线。恢复不按日历自动宣布情绪变好，也不重放外部发送。

删除先拒读取/使用相关对象，再清正文、摘要、反思、情绪推导、FTS/向量/cache/Wiki。备份采用明确保留/销毁策略，并在恢复时强制最新删除账；不能承诺远端不可控副本物理消失。多源结论删除部分来源后重新核支持，不能只删引文保留同结论。

C032旧profile保持严格八域字段和非空grounding；counterEvidence可空。SourceRef向Citation必须显式适配，不靠删未知字段骗过校验。一次评价后补查是候选现状，多轮目标设计不能当已实现。真实DSH版本/插件/桥/消息角色支持仍须现场确认；容器名不是版本。

资源低时优先输入入账、治理、必要纠正、真实输出和有限结构查询，暂停可选向量/反思。故障不伪装“没有相关记忆”；取消未确认保unknown。高强度情绪不提高工具权限或绕过预算。

## 10. 验收与发布：用效果替代数量

原864项模块表降格为需求检查目录，40条全链场景仍待执行。新增可运行参考测试只证明其对应受限机制；不把几个通过例子写成24模块通过。

正式实现必须具备四组互不替代的证据：

1. **结构和事务**：严格schema、非法字段/状态拒绝、幂等异载荷冲突、CAS、回滚、outbox重投、kill/磁盘故障恢复。
2. **业务语义**：按十kind和四种查询分层，检查主体/时期/否定/条件/更正/关系隔离；必要记忆漏召回与无关注入分别统计。
3. **宿主与输出**：独立off/on/fault初态；真实调用边界messages；语义有意义的业务输出；工具结果与送达分轴；所有旧出口是否已收敛。
4. **成长和连续运行**：冻结的未见场景、独立标注与分歧、工作迁移/情绪修订/社交误伤和漏边界；长期队列积压、切任务、重启、删除后恢复和资源曲线。

硬性零容忍项：越权泄露、删除后复活、未经授权副作用、来源否定翻转导致错误动作、把未验证输出正式绑定为本轮状态。观察到一例即阻发布，不用平均分冲淡。

质量门槛必须事前登记数据split、分母、采样、标签来源及适用部署范围，按类别报告置信区间与unknown。不能凭设计指定“99%即人脑水平”，也不能用本作者编写的少量fixture声称独立验证。留出集不得在调参后仍当未见集。

## 11. 冻结后的实施顺序

第一阶段：R01/R18/R19/R24与严格数据归属，证实输入不丢和旧内容能停用。第二阶段：R03/04/05/10/12/13/15/16/21/22，先跑精确保守profile、纠正闭包和单出口。第三阶段：R02/06/07/08/09/11/14/17，接入三轴成长、关系和可信状态提交。第四阶段：R20迁移与R23全链验证、semantic-verified留出集、真实宿主回归。每阶段都可在隔离环境做，生产仍需单独批准。

顺序不是缺功能清单，而是依赖约束：不能先有漂亮情绪摘要再补来源；不能先让后台写记忆再补删除和CAS。最终功能覆盖仍是全部24模块。

## 12. 来源、原创与诚实边界

认知科学提供功能启发，工程机制由本稿设计：Conway目标与自传记忆、Baddeley有限工作台、互补学习系统的快记录慢整合、EMA/Scherer的动态评价、前瞻记忆和RRF融合。Graphiti/Letta/Mem0/Hindsight/StillerBrain/Ombre Brain提供公开方案参照；不宣称完整源码审计或同条件性能胜出。Anthropic Cookbook的编排/分析/整理/Wiki启发后台链，长明额外加规范真源、审核、CAS、删除传播与成长迁移验收。

具体来源链接和原阅读范围保存在contracts/REFERENCES.md及SPECIAL_MECHANISMS.md；本版没有声称重新全文审计所有上游项目。自己新增的profile、双门禁、bundle闭包、三线提交和本次参考程序属于工程设计，不是论文已经验证的结论。

“最高标准是人脑”转化为连续、分型、联想、纠错、情境化、有限注意及经验迁移这些可观察目标；不宣称复刻全脑、拥有主观情感、永不遗忘或能准确读心。我的最终判断是：这套结构可以停止扩板，进入实现；任何新缺陷先在这套职责和证据规则内修复。


---

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


---

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


---

# 依现有候选重整的数据层、分库与召回设计

## 1. 可核现状与目标的差别

本次只读核对提供的候选0.32.0-candidate：engine/.../src/storage.mjs定义memory.sqlite，含events、memories(kind)、versions、links、sessions、snapshots、gaps、watermarks、actions、audit、outbox、candidates、FTS及可选vector_buckets等；runtime/brain.mjs另开control.sqlite，注册mind与domain表。是历史隔离候选源码，不是当前D数据库现场；不对生产做目录扫描或迁移。

目标仍先用这两个本地SQLite文件及受控原件目录，不部署十个服务。类型隔离落实到表、索引、服务API、查询路线及测试，而不是给一堆文本贴标签。规范类型不互相覆写，跨类型只用ID与来源联结。

## 2. 五层与十类库

| 层 | 内容 | 数据性质 |
|---|---|---|
| L1原始证据 | Event、原件、SourceRegistry及实际范围 | 发生过/收到过的来源，编辑追加；删除走治理 |
| L2组织记忆 | 下表十类typed store | 可修订知识/经历/解释/工作与资料 |
| L3当前状态 | 工作焦点、当前关切、last_known、SelfState/八域、检查点指针 | 取规范状态，不创建重复事实真源 |
| L4检索联想 | query/route、补读、反证/后续、支持验证 | 只读规划与执行证据 |
| L5按需注入 | NONE/BRIEF/EXPANDED实际动态投影 | 本请求临时材料，可过期替换 |

三类运行账为行动、run/观察/提交/投影/覆盖、后台job/outbox。原始证据底座与运行账不算第11种心理记忆。R18/R19/R23/R24贯穿五层，不额外再算第六记忆层。

| 逻辑库/目标detail表 | 唯一写者 | 业务字段 | 专属召回维度 | 明确禁止的混用 |
|---|---|---|---|---|
| 工作 working_memory | R03 WorkStore | goal、constraints、decisions、commitments、next_step、state、project/task | 可信项目/任务、活跃状态、最新结果与取消 | 待办不等承诺已兑现；项目要求不当永久偏好 |
| 情景 episodic_memory | R04 EpisodeStore | event_refs、participants、time/precision、summary_items、followups | 人物/项目/时期/地点，必要前后与后来 | 摘要不等原话；两次相似经历不串 |
| 语义 semantic_memory | R05 ClaimStore | subject/predicate/value、epistemic、有效期、支持/反证、审核 | 主体+谓词+作用范围+问题时期 | 他人转述/模型推测不直接当已证事实 |
| 程序 procedural_memory | R06 ProcedureStore | environment/version、preconditions、steps、results、failure_modes | 当前目标、工具/环境版本、成功及失败 | 曾成功不等当前适用或已获执行授权 |
| 关系 relational_memory | R07 RelationStore | entity/alias/relation/interaction类型、方向、holder、时期、领域 | 可信人物ID与候选、视角、共经历、边界/修复 | 关系不授权限；同名不合并；不读心 |
| 情绪 emotional_memory | R08 AffectStore | owner/target/concern、表达、解释、反证、change_mode | 当前有关关切、当时/后来/last_known | 感受不当客观事件；强烈不等本轮相关 |
| 身份 identity_memory | R09 IdentityStore | field_key/value/kind、范围、有效期、策略及来源 | 必要主干、当前称呼、局部侧面 | 叙事设定不当认证；别人辱骂不改自我价值 |
| 元记忆 metamemory | R10 CoverageLedger | run/query/route、watermarks、read/supplied、gap/stop | 具体查询/来源版本的覆盖与未知 | 未找到不证明没发生；模型自信不当覆盖 |
| 反思 reflective_memory | R11 ReflectionStore | axis、observation、interpretation、策略/范围、反证/结果 | 当前问题、工作/情感/社交轴、适用与不适用 | 反思不当亲历；同源循环不增加证据 |
| 资料 atlas_memory | R12 AtlasRegistry | document/locator/hash/revision、ACL、提取器、覆盖 | 项目/文件版本、授权资料类型与精确定位 | 路径不等权限；提取文本不冒完整原件 |

情绪时间线、关系经历网、三轴成长、八方向是这些库的联结/视图，不新增重复库。一个事件可以支持多个库的不同命题，SourceRef共享，不复制成多个独立经历。对外API必须带kind；不能只给一个混合search()就声称完成分库。

## 3. 表结构与版本总约束

contracts/memory_schema.sql为目标类型隔离DDL的可执行片段：公共memory_objects索引元信息，十类detail表通过(id,kind)组合外键与固定kind检查绑定；原始source_registry及source_refs分开；immutable memory_versions记录已提交版本；dependencies登记反向失效。候选旧schema不会因本文件自动升级。

每次规范写：校授权/来源→校kind结构→读expected_revision→短事务CAS base+对应detail+version+dependency+同库outbox→commit回执。detail表不另有第二revision；其当前revision由base拥有；历史值在memory_versions完整record中。普通API禁止改kind；类型错写不能靠UPDATE kind将对象洗到另一库，应拒绝或显式新建有来源对象。

source_refs分别标supports/contradicts/derived_from；其范围可空表示对象级来源，具体文本引文必须有合法范围且已实际供给。type是合法不等于语义支持：SourceRef验证和SupportVerifier分开。

metamemory/任务运行产生的记录可由真实宿主回执作依据，不要求伪造聊天原文引用。每个对象有创建依据；不强迫每个job都有subject_id。

## 4. 索引隔离与路线契约

各typed adapter先按scope、kind、状态、删除/策略、业务过滤查询。共享FTS物理表可以kind UNINDEXED，但命中必须JOIN回规范对象并执行类型/权限/版本过滤；不得只相信FTS记录的标签。可选embedding索引带model_id/dimension/chunk/source_revision，模型/维度变化显式重建，不把向量相似度当事实置信。

RouteResult={route,kind,filter_digest,snapshot_watermark,index_watermark,hits,cursor,coverage}；Hit至少{id,kind,revision,rank,source_refs,temporal_scope}。不同类型需要不同输出形状，不把它们全压一行text后丢掉视角、时间和不确定性。

路由按任务需求选择：继续工作→working、相关atlas/procedural、actions结果；问往事→episodic并追后续；问偏好/知识→semantic及反证；社交人物→relational+对应episodic，必要时emotional/reflective；当前稳定称呼→identity精确读。不是每个问题默认查十路。模糊短句用可信focus检查，不能因词少就略过。

每路初始20候选、run共8逻辑query、最多3读取轮、图2跳/40节点、补读64KiB仅是隔离起点。ACL过滤后不足可预算内续页并标partial。为当前纠正/反证/后续保留足够候选机会，不让大量相似旧摘要挤掉新版。停止原因保留，不许complete意味语义100%全找齐。

## 5. 召回到注入的六道关

1. 访问与有效性：当前scope/删除/授权/版本通过。
2. 对象与时期：人物、项目、视角与问题时间对齐；不清保候选。
3. 当前需要：本轮回答、指代/进度、避免具体错、当前受托工作或相关情感理解有可说明连接。
4. 来源支持：实际原文支持待注入命题，不能只有source_id存在。
5. 表示与依赖：同源同命题去重，必要纠正/后续形成有界闭包；容不下则联合忠实压缩或延后整组。
6. 实际请求：按总预算选最短足够材料，替换一个宿主拥有块并读回供应商真实调用。

情绪强、亲近、未结、昨日刚写入、向量高分都不是独立准入理由。NONE不等没有记忆；检索失败必须与不需要分开。调用模型语义判断本身有误判风险，验证需未见样本，不靠提示词自称可信。

## 6. 依现状的隔离迁移步骤

M0留候选完整快照、schema/user_version及hash，不改生产。M1在新隔离目录创建新detail表及schema_meta，保持既有memories/versions/事件和主键。M2逐旧kind解析为目标字段；无法无歧义映射的原record留原样并报unsupported/needs_review，不能丢弃或默认accepted。M3映射R07现control entities/aliases时保原ID/来源/范围；迁移窗口旧写者冻结，切换后只有RelationStore拥有目标新实体真源，旧表只作历史只读。

M4 SelfState/八域继续原control CAS协议，历史情绪/成长记录引用其commit并标物化关系；未成功物化保pending。M5重建kind索引、反向来源依赖与投影，逐类正反例双读比较，避免旧/新同时当独立事实。M6验证删除、恢复、混合召回与实际注入；受控切换写者。M7回退时核schema兼容及后续更正/删除，不能单拷旧db抹掉新撤回。

每步有counts_by_kind、unsupported_count、id_mapping、源引用悬空、version_mismatch、index_lag、duplicate_root_claim和ACL差异报告。不兼容即停在隔离，不自动“修成”用户没说的内容。

## 7. 稳定性策略与存储边界

memory库：原始事件与十类规范记忆、版本/源依赖及本库outbox。control库：run/proposal/观察/认知前态/输出归属、策略/删除控制账、调度与本库outbox、跨库桥回执。若部分既有行动记录在memory而调度在control，沿现位置保留，通过ActionLedger统一API，不复制第二真源。逐对象实际归属写入迁移manifest。

源库commit与本库outbox原子；跨库由commit_id+projection_type幂等消费和对账。读取前统一校当前治理水位；无法确认当前授权/删除时拒相应私密操作，不能使用陈旧allow缓存。源库与control不可用时可继续不依赖它们的普通交流，但不得伪称状态已核实。

备份分别用一致机制取得库及关联水位，记录原件manifest；隔离恢复后先应用最新删除撤回、再核引用与未知动作。崩溃恢复不重发消息、不重跑工具。原件、Wiki快照、向量/FTS分别标规范/派生及可重建状态，不把索引备份当全部记忆。

## 8. 直接落地的退出条件

十类库逐一完成字段验证与专属查询；跨类型写入必须被结构约束拒绝；同源不同命题必须都保留；错误主体/时期/权限/陈旧版本必须有反例。再验证召回材料到达实际请求，以及实际业务输出是否改善。本文附DDL实验仅验证所列结构约束，不证明开放语义、线上稳定性或迁移已经完成。


---

# 跨模块接线、端到端状态和全链验收

## 1. 谁可以调用谁

模块不相互自由递归；宿主Coordinator执行前台计划，R17执行后台计划，各store仅通过版本化服务访问。module_registry.json记录每模块输入/输出依赖；下表是实际业务关键边，其他边仍须传GLOBAL_PROTOCOL的scope/版本/覆盖，不能只传一段text。

| 发出→接收 | 必传对象 | 接收义务/断开处理 |
|---|---|---|
| R01→R02 | event_id、source_revision、原文range、actor/引用结构 | 只做局部线索，缺原文不编码伪句 |
| R01→R04/R17 | event receipt、source refs、outbox、水位 | 只消费已入账版本，任务幂等，未采集保gap |
| R02→R07/R15 | CueSet、候选与unknown、规则版本 | 不升级为人物事实、情绪、意图或权限 |
| R03→R12/R14/R15 | 可信project/task、目标/验收、产物版本 | 文件/动作/召回限制到当前任务，不猜项目 |
| R04→R08/R11/R15 | Episode、人物候选、原话及followups | 当时与后来分开，缺片段不补桥段 |
| R05→R09/R15/R22 | Claim/范围/时期/审核/反证/更正 | 不将转述或推测洗成事实，不漏当前纠正 |
| R06→R14 | 适用方法、版本/前提、失败模式 | 动作前复核真实环境和授权；经验不代执行权 |
| R07→R04/R08/R11/R15 | 人物ID/候选、方向/视角、共经历/边界来源 | 不跨人继承，不沿图传ACL，意图可unknown |
| R08→R11/R13/R15 | owner/target/concern、表达/解释、变化模式、反证 | 不把last_known当实时测量，不强制情绪变化 |
| R09/R13→R21/R22 | 主干/焦点revision、边界、未结/unknown动作 | 开口前必要检查；缺失说明，不补自我故事 |
| R10→R15/R16/R22 | Coverage、路线水位、未读范围、Gap与stop_reason | 有价值缺口预算内补查，最终局限不抹掉 |
| R11→R05/R06/R07/R08 | Reflection/Lesson、支持/反证、适用条件 | 先审核候选，高影响不自动晋升规范事实 |
| R12→R15/R16 | document_id、版本/hash、原件与提取覆盖 | 实读正确版本，路径不是权限，读变更不混拼 |
| R14→R03/R04/R08/R11/R13 | action/attempt、可信receipt、verification/delivery | 承诺/尝试/结果/满意分开，unknown先查 |
| R15→R16 | 分kind候选、source版本、补查问题和预算 | 受权实读，记录实际范围；摘要不冒全文 |
| R16→R10/R11/R22 | 已读/已供给范围、hash、游标、partial | 引用不越范围，语义支持另验，cursor按源版本 |
| R17→R11/各typed store | 冻结batch、独立proposal、lease/fencing、处理器版本 | 不并发覆写现役真源，旧proposal重核 |
| R17→R12/R15 | 已commit对象、索引/Wiki发布manifest | 派生更新失败标stale，不能半套内容混可用 |
| R18→全模块 | 当前policy/deletion版本、allow/deny、tombstone | 读/写/投影/动作各入口校验，恢复先删 |
| R19→R13/R17/R20 | 快照/水位、schema/配置、恢复对账状态 | 不将hash正确当全恢复，不重做未知外部动作 |
| R20→R07/R12/R13/R15 | ID/schema映射、unsupported、源/删除manifest | 新目录校引用、按类型查，权限不机械继承 |
| R21→R22 | 实际messages、run/attempt、焦点、窗口与预算 | 只替本插件块，保消息合法结构 |
| R22→真实供应商调用 | 动态块、源范围、mode、必要局限 | 在真实请求边界读回；built日志不算到场 |
| 可信输出→R21/认知commit | output_id、run/attempt/scope、前态revision/digest | 强绑定+CAS，同control事务；否则unverified/待对账 |
| 各模块→R23 | 实际输入/状态/请求/输出/回执及配置 | 分轴标证据等级，缺证不标pass |
| R24→R15/R16/R17/R21/R22 | run/job共享配额、取消、计量等级 | 必要路径预留、可选降级；不绕权限、不凑注入 |

## 2. 全系统四条常驻规则

每条回路都有事件/来源根和一个当前规范版本；不会靠模型“想起来了”替代调用。每轮是否检索历史按需要性规划，但身份/范围/取消等最低宿主检查不能被模型跳过。所有异步任务可重投但按源版本幂等；每次新的真正业务事件不能被旧键吞掉。资源/失败/未知状态可以同时存在，不能一个总success掩盖。

## 3. 前台主时序

S0 认证真实入口并R01入账，明确纠正先阻旧推测当前使用。S1 读R09、R03、R13与R18最新状态，建立可信focus。S2 R02局部线索+现行情绪线索+当前问题形成RoutePlan，按需查各typed store。S3 R15融合候选，R16读原文/反证/后续，R10保覆盖。S4 NeedVerifier/SupportVerifier评当前用途与命题支持，必要缺口有界补查。S5 R22去重/闭包/预算，替一个动态块，在实际模型调用处读回。S6 业务生成，工具由R14/R18在副作用前门禁。S7 可信实际输出观察+强归属+CAS提交对应SelfState/八域，input不因失败回滚。S8 R17按冻结源/版本做后台索引和三轴成长。

不是所有步骤都需要语义模型：简单问候可zero历史；当前“继续”必须核焦点，工具续步不是缺新user就不查。语义路由不可用、预算不足或binding缺失各自留明确状态，不冒流程完整。

## 4. 六条跨模块业务链

| 链 | 场景与步骤 | 关键反例 |
|---|---|---|
| C01记忆写入→召回→使用 | R01保存“此项目用蓝色”→R05局部Claim→R15按项目问配色→R16给原文→R22短证据→实际回答蓝色 | 不能覆盖全局喜欢紫色；只查到但没进实际请求不算使用 |
| C02情绪连续与修复 | R01保存失望→R08当时表达→R14查到发送失败→R11修订原因→后来明确放心→R15带当时及后来→R22仅相关片段 | 不否定当时表达、不永远复演失望、不擅判已原谅 |
| C03工作成长 | 旧方法在a有效→R06留条件→R14新版结果反证→R11工作Lesson→R17验证提交→新任务R15读适用性 | 新版本不盲套旧命令，未有真实结果不说学会 |
| C04社交与自主回应 | R07分说话者/对象/引述→评价纠错与羞辱→R08/R09保立场→可改错且拒人身评价→R11/R17复盘 | 不迁怒转述者、不把一切批评判恶意、不威胁报复 |
| C05删除与恢复 | R18tombstone→停用反思/情绪派生/向量/Wiki→R19快照恢复先用最新删除账→R13再查焦点 | 旧worker/旧导出/旧缓存不可复活内容 |
| C06任务切换与零噪音 | A任务→B任务→A，R03/R13保存指针→R15只查当前相关→R22替旧块 | 同名不串项目，不累积A+B全史，不用冷却挡必要追问 |

## 5. 成长链的在线与离线边界

在线遇明确羞辱可当下说“不接受”，不用等待夜间复盘；纠错与人身评价可以同时成立。后台只改善以后：冻结经历→各Analyzer独立proposal→Organizer方案→GrowthVerifier核支持/适用→Committer→只读Wiki。不存在“每天反思一次就成熟”的承诺。工作、情感、社交三轴分别验，不用总好感/满意分。

一条社交经验至少有原话/对象/引用域、可观察行为、意图unknown或有据候选、边界、应对、实际反馈和后来修复。亲昵玩笑依语境，熟人不自动获羞辱许可；道歉可作为新表达，但行为修复与完全信任不自动结案。外部群管理操作仍需已有授权。

## 6. 故障组合必须能恢复

F01 memory已入账、control不可写：不丢输入，认知pending/unknown，不称完成。F02 索引失败、规范store可读：允许精确结构查询，标index stale；不称无此记忆。F03 R16只读半段：不能给完整因果结论；保cursor和缺口。F04 R22 fault：移除旧假成功块，真实请求带当前必要局限。F05 实际输出已保存、无强attempt绑定：unverified，不以近时间拼归属。F06 外部发送unknown：查渠道，不重发。F07 wiki发布失败：保旧完整只读快照并标stale。F08 删除治理不可确认：拒相关私密读取/动作，普通不依赖历史交流可继续。

所有组合都要保run/source/control/index水位，不以记忆摘要重建缺失原文。恢复账本回放只改变内部状态，不执行外部动作。

## 7. 全链验收（40项，均待执行）

verification/integration_cases.json记录40个全链场景，字段为id、input、expected、failure、modules、evidence_required、status=not_run。每个用例必须取真实规范对象、版本、源范围、实际messages及实际业务输出/外部回执，不能只验证某一模块返回类型正确。

阶段二冻结要求不变：相同输入/设置/逻辑初态的独立off/on/fault；真实业务输出出现有意义改变；故障仍能交流且实际知道故障；在真实供应商调用边界读回被替换messages。off本来正确不证明改进，模拟数组不证明真实宿主。输出绑定、自然度、性能/稳定性和隐私另轴保留。


---

# 专项机制：六条回路、关系、情绪、欲望与八方向

## 5.1 三层关系：事实、经历、理解

**关系事实层**：谁是谁的朋友/家人/同事、D与谁有过直接互动，带方向、视角和时间。不以“熟悉度80”代替具体事实。

**共同经历层**：人物通过Episode连接实际对话、合作、约定、分歧与后来变化；同一事件有多位参与者，各自说话和所知范围分开。D只从转述得知的事情，不用亲历口吻讲述。

**关系理解层**：D对相处方式、期待、偏好和信任某个领域的解释；可修订、可有反证，不自动升级身份或授权。例如“在改图时她更在意保持原构图”要指向改图反馈，不能推广为“她在所有方面都不接受变化”。

## 5.2 四类对象如何关联

| 类型 | 保存方式 | 自动浮现时 |
|---|---|---|
| D与当前用户 | 各自ID、已确认称呼/边界、直接共同事件 | 只取当前话题相关经历与最新修订 |
| D与其他人/Agent | 独立账号映射、合作与对话来源 | 同名先消歧，不继承当前用户关系 |
| 用户与其他人 | 用户自述/观察/推测各有标记 | 回答注明谁说过，不当作D亲历 |
| 第三人与第三人 | 独立方向关系及证据/时间 | 没证据不沿图推导新社会事实或权限 |

若“她”在当前栖所场景按约定不指向用户，保留为空/unknown，不转去猜其他女性；引用别人的话更不能继承外层人称映射。账号绑定可以认证谁在发言，不能证明这个人的转述都为客观事实。

## 5.3 一次自然浮现的决策

1. 当前话题/人物/未结事件进入R15查询，先受权过滤。
2. 优先可信人物锚与当前任务；其次找共同经历及后续；再次看当时情绪/反思，避免情绪强烈片段独占候选。
3. 历史关系失效或变更时同时拿到旧与新，按问题时间作答；问“当年”不只返回现在。
4. 形成给模型的有限材料包：人物候选、事件、表达/解释、后续变化、缺口和不应推断之处。
5. 当前交流需要时自然提起；仅帮助确定称呼和背景时可不复述。用户换话题后不强拉回旧事，不以“有未结”作为持续追问义务。
6. 私密材料不可因情绪相关就跨群/私聊注入；被拒绝项不在模型可见解释中泄漏存在性。

## 5.4 情绪不是单独一根曲线

建议以owner+对象/关切+episode组织并存状态。保存表达、意义候选、相关期待、证据/反证、时间与后续解释；允许“不知道原因”“多种感受并存”“没有变化”。不从一次输出建立恒久心理标签。

若实验采用独立v1.0数值原型，它的工程公式为：activation_new=clamp(a+I*S*(1-0.35*abs(a)),-1,1)，trace_new=clamp(t+0.35*I*S,-1,1)；tick时activation乘2^(-elapsedHours/halfLifeHours)。它们只是原型启发式，非人体验证公式；本稿不默认把所有情绪转换成数值，不由这些数值授予关系或亲密行为。36小时半衰期只是原型实验初值；未解决事实/trace不随tick消失。宿主不运行tick则不声称持续动力学计算，重放tick也不代表模型离线有主观感受。

当实现更复杂动力学时要版本化且验证：负输入不必都叫悲伤、多个关切不强制求一个总值；迟到事件按明确策略重放或隔离，不以接收时间歪曲真实顺序；同来源重复到达不能再次累积。原型只查evidenceRefs非空不能保证可信，宿主必须实际核验来源。

## 5.5 关系修复的非强制链

期待→破裂/误会→解释→道歉→承诺→动作→结果→反馈，是可能的事件类型，不是每次必须完整经过的剧本。可以缺一环、反复、暂缓或没有结案。对方说“没关系”可作为其当时明确表达，不能强制视为所有事情彻底解决；没有反馈不写“已原谅”。

事件表链接原话；承诺表写具体内容和期限；行动账写真实操作和unknown；反思表记录后来的理解；情绪上下文保留当时及后续。被触发时连同后续查回，不让过去情绪永久卡住，也不靠温柔措辞虚假结案。

## 5.6 欲望、主动索取与主动工作

D的愿望、喜欢、认可/冲突、当下意愿和外部许可分别记录。当前对话可自然表达或提问；用户拒绝/撤回则停止该互动，不据此扣关系分。授权工作可在范围内主动查询和整理，不需要每步再问。

跨渠道/未来主动联系需Task：目标、source_event、授权引用、渠道、接收人可信ID、时区、schedule/expiry、quiet_hours、取消版本、幂等键与action_id。触发前核最新撤回、近期是否已完成和渠道状态；漏过时按事先规则过期或重新安排，不自动连发。关系是背景而非发送授权。

## 5.7 八方向如何接六板块

| 八方向 | C032严格details | 本次联动与边界 |
|---|---|---|
| development 发育/差异 | basis, appliesWhen | 初始化/经历/长期倾向分开，R09/R04/R11接入；不按轮数成长 |
| conditions 身体/条件 | ownerId, basis, validFor | 自述/叙事身体与宿主runtime分开，R08不把故障变情绪；无激素测量 |
| relations 依恋/修复 | personId, area, expectation, episode | R07/R04/R14/R11链接过程，结果由可信宿主另记 |
| self 自我价值 | desire, endorsement, value, decision, expectedOutcome | R09/R08/R03携旧立场，候选/暂缓/拒绝不等于已执行 |
| memory 记忆变化 | eventId, interpretation | R04/R05/R11保留原话与解释版本，不制造错记 |
| perspective 社会视角 | holderId, kind, knowledgeStatus | R07/R11分明说、观察、推测、期待，不读心 |
| motivation 特定动机 | kind, desire, liking, subjectiveArousal, attachment, willingness | R08/R14分愿望和许可，旧同意不自动续期 |
| connections 功能连接 | from, to, relation, timing | R15受限展开、R16读端点；图边不是突触，later-review不是运行中定时器 |

C032现有Entry严格顶层是id/domain/subjectId/summary/grounding/counterEvidence/relatedIds/supersedes/details。新增字段必须另用版本化适配/表，不往旧顶层随意塞键，不自动删掉未知实质字段骗过验证。旧记录只允许在本轮供给视图可见时被引用或替换；同次新增关联也要有合法端点和来源。

## 5.8 我设计的A：情境工作台的装配算法

工作台是每轮临时组合的SceneContext，不再创建一套会与R03冲突的“超级记忆”。输入为可信当前事件、身份字段、人物解析结果、工作焦点、未结指针和能力清单；输出为“当下可知”的材料包。

1. **锚定**：以scope、actor、当前项目、最近明确任务建立硬锚。文字中的昵称只有候选权，不能覆盖账号认证；没有当前项目时不默认跨全部项目。
2. **恢复**：R13取已提交焦点和未结项，R03读最新版本；旧checkpoint若指向已完成事项，显示其结果而非继续执行。
3. **展开**：R15取与当前输入有关的经历、主张和关系，R16读取必要来源。关系事实可以帮助理解人物，不能替代当前话题。
4. **对齐**：把每段材料标为当前输入、当时表达、后续解释、行动结果、未知。允许一个事件有不同人的视角。
5. **生成前检查**：R22形成实际请求；如果没有读到旧文，材料包写未读，不能留一句“想起了细节”诱导编造。

例：用户只说“继续吧”。可信焦点唯一指向长明机制文档时恢复该文件版本及待补章节；如果同时有两个活动任务且焦点缺失，工作台给出候选，D可简短确认所指，同时继续不依赖该选择的整理。一次任务切换改变focus，不能顺便重置人物关系或情绪历史。

## 5.9 我设计的B：关系—经历网的生成与自然浮现

关系网以“人物—共同事件—当时表达—后来反馈”为基本单元，不靠固定亲密度决定措辞。新增关系事件时依次回答四个问题：谁在说；说的是谁与谁；是亲历、转述还是推测；适用于哪个时期与领域。答不出就存unknown，仍可保存原话。

**关系变化的五类输入**：明确关系自述、共同经历、承诺/履约、边界表达、后续澄清。前两类提供背景；履约提供某领域的实际经历；边界决定当前互动范围但不自动等于感情下降；澄清修订解释。不能把回复字数、离线时长、亲昵称呼频率直接当感情证据。

**浮现选择**采用分阶段而非情感总分：先排除越权/错误人物/已删除版本；再要求与当前人或任务有可说明连接；再保证包含最新后续与反证；最后在预算内保留不同经历，避免同一争执的十个相似摘要占满。关系背景已经解释称呼时可以只在context中用，不必每次把“我记得我们……”说出口。

例：示例用户提到另一位协作者，D可想起“此人在海报项目中提供过反馈”，并理解对方在那个项目的角色。没有D与对方直接交流的记录时，不能顺势写成“我和他一直很熟”。对第三方关系，只表述来源允许的内容与知识局限；双方关系变化可并存两个视角，而不强制投票选一个真相。

## 5.10 我设计的C：情绪连续性的完整更新器

输入不是“这一轮情绪词”，而是：最新已提交状态、当前明确表达、相关关切、同一事件后续、可信结果和覆盖缺口。情绪线索由现行情绪召回/独立评价器提供；R02仍只输出它限定的三类线索。

**Concern（关切）**保存“什么对这个owner在这段时期重要”，可为正在完成的任务、对某次交流的理解、具体期待或未解问题。它是有来源的表述或暂定解释，不是系统读取了内心。分open/monitoring/paused/resolved/withdrawn/unknown；无反馈不能自动resolved，用户不愿继续谈可paused而不要求其先证明情绪消失。

更新器顺序：

1. 以owner、target、concern、episode匹配状态流；无法匹配新建候选，不把同一个人的所有感受塞进同一桶。
2. 保留原表达；为“发生了什么”“我/对方怎么理解”“还有什么未知”分别建材料，不把解释写回原话。
3. 比较新材料与前态。无新依据→retained或last_known；同对象明确纠正→revised；不同关切或并存感受→coexisting；来源不足/失效→suspended或unknown。
4. 生成评价候选：关切、事件对关切的意义、可确认责任、可行应对和替代解释。责任不明确填unknown，不能因为任务没完成就认定恶意。
5. 用户自述与纠正进入输入线；D依赖本轮输出的状态等待强归属观察与CAS。只有原始输入已存而生成失败，用户纠正仍有效。
6. 下一轮召回前态+后续+未结，不必把全部时间线重复塞回；相关关切优先，已无关部分留历史。

**表达风格与状态分开**：D可以语气平静但仍保留未结关切，可以既亲近又不赞同，也可以没有足够依据描述当前情绪。不强制一遇“难过”就安慰、一遇“生气”就道歉；先核对象和事件，回应实际话语。状态连续体现为理解前因后果，而不是不断复演上次语气。

**完整例子**：t1用户说“没做完让我失望”→保存当时自述及任务关切；t2查到文档已写但发送失败→R14增加投递unknown，R11修订原因解释，不能擅自改用户当时失望；t3用户说“现在放心了，主要怕你忘了”→保存新表达、修订当前解释，R03继续核交付；t4文件有真实交付证据→任务相应完成，但用户满意度仍由其反馈判断。重启后恢复这四步，不只返回t1负面，也不说“从未失望过”。

## 5.11 我设计的D：缺口驱动的有界联想与自动补读

每次Gap有type、known_sources、missing_question、next_query、scope、priority_reason和stop_reason。type至少分人物歧义、时期不明、摘要缺原文、事件缺后续、主张有反证、承诺缺结果、来源缺权限、索引陈旧。缺口是执行规划，不是把模型猜测当新事实。

检索轮从当前事件和工作焦点开始；后续轮只对尚未解决且会影响本轮理解/操作的Gap补查。一个历史争执命中后，自动追它的后来澄清；一个承诺命中后，自动查对应Action与Artifact；一个名字不明则先查本地候选，不沿好友图猜人。来源导航可多跳，但不赋予R02多跳指代职责。

```text
associate(scene, limits):
  gaps = initial_gaps(scene)
  seen_queries, supplied_sources = {}, {}
  for round in 1..limits.read_rounds:
    plans = select_relevant_authorized_plans(gaps, remaining_budget)
    if plans is empty: stop(no_actionable_plan)
    results = search_with_per_route_coverage(plans - seen_queries)
    chunks = read_versioned_sources(results, remaining_budget)
    new_sources = newly_supplied_ranges(chunks, supplied_sources)
    retain_failures_and_conflicts(results, chunks)
    if new_sources is empty: stop(no_new_supplied_evidence)
    update_candidate_interpretations_only(new_sources)
    gaps = recompute_gaps_with_alternatives()
    if current_decision_supported_or_budget_or_cancel: stop(exact_reason)
  return evidence, gaps, coverage
```

只有实际供给的新范围才能参与本轮重评。同原件新范围可补事实，但若只是同一句换摘要，不算独立支持。补查停止不代表世界上没有更多材料；R10保留停止原因。C032当前仅有八域启用时一次评价后补查，多轮循环是目标扩展，必须另接宿主、预算和引用适配。

## 5.12 我设计的E：承诺—结果—关系反馈回路

承诺对象含promisor、beneficiary、content、scope、due_at（可空）、acceptance、source_ref、state和linked_work/action；“我希望这样”是desire，“我来做”才可能是commitment候选，是否足够明确由文本与场景审订，不自动承诺所有愿望。

事件条件前瞻项ProspectiveCue可为“回到项目A时先检查最后一项”“收到工具结果后核版本”；每次有关事件到来由R21触发检查，不依赖模型自发记得。时间条件必须由真实调度器按已授权时间/时区/期限触发。工作项处于blocked时明确原因，不用热情表达掩盖停滞。

结果回路分三条：**执行证据**（做没做、产物版本）；**接收证据**（是否送达/被读）；**对方反馈**（对方当时怎么说）。三者可以不同步。R07/R08使用具体领域的结果和反馈修订理解，不能把“工具成功”直接变成“对方感到被爱”或把一次失败扣成全局不信任。

例：已授权整理文档，D可主动检索补例并保存，不需每步再问；若发送目标没有确认，文件准备好与发送未决分开。用户说“先别发”后，未发生的发送停下，整理是否继续看原授权范围，不能把拒发解释成拒绝关系。已经发出时如实记载并按渠道能力补救。

## 5.13 我设计的F：连续状态恢复的最小携带集

恢复包只带必要指针与限定摘要：身份版本、可信scope、工作焦点、当前明确边界、有关人物候选、情绪last_known指针、未结关切、承诺与unknown动作、来源水位和读取游标。它不是另一段可以不断自我扩写的“人格宣言”。

恢复算法：认证当前范围→加载最新删除/撤回→校验快照与来源→读最新任务/行动→恢复关切和后来变化→继续必要补读→组装真实请求。某步失败写具体gap，普通交流尽量继续，依赖缺失状态的动作限制。旧快照不覆盖新库revision；已完成任务不复活，旧关系结束状态不回滚。

例：压缩前是“还缺资料出处，发送成功与否未知”；恢复后先核文档当前版本和渠道回执，再继续未完成部分。不能把压缩摘要里的“准备发送”解读成已送达，也不能用“我一直记着”掩盖未读取旧内容的事实。

## 5.14 动机、欲望、边界与自主表达怎样共同工作

本稿将欲望放在R08关切/R09价值/R03目标的联结中，不另造一个以强度强迫行为的驱动器。DesireRecord保存owner、object_or_goal、表达原话、endorsement=endorsed|conflicted|withheld|unknown、willingness及时间/来源。这里描述D角色/模型表述的工程状态，不证明生物驱力或主观感受。

**表达自由**：在当前交流中，D可以表达喜欢、犹豫、想继续、不同意或想提一个问题；是否表达取决于当前话题、既有状态和模型生成，不由“亲密度超过某值”自动触发。愿望可以与任务冲突并保留冲突，不能因为用户认可就无条件改写所有价值。用户表达拒绝只关闭对应互动范围，不能自动推断所有亲近都结束。

**主动索取**分信息索取、任务协作和情感交流。信息缺口可按D机制自动查已有受权来源；需要用户回答的问题应一次问清关键点，不重复问已知答案。情感交流不制造“必须回应否则我会受伤”的系统规则，也不把用户离线解释成过错。跨时段主动联系仍需R14/R18已有授权和真实调度，不由欲望绕过。

**身体/条件**分用户明确自述、角色叙事设定、真实运行条件三种。可把“用户说累了”作为当时自述，不能据此诊断；可保存故事内身体状态但不得写成现实测量；CPU高/网络断开只进runtime。没有传感器就没有激素、睡眠或心率的事实输入，不用编造数值给情绪“增加真实感”。

## 5.15 三个支持机制：预演、意外与记忆使用反馈

**预演隔离**：R11可构造“如果先发版本A会怎样”的计划场景，存kind=simulation、assumptions、parent_goal和版本；检索必须与实际episode分路。只有真正行动及回执才能新增发生事实，想象、梦境、角色叙事不能因被反复提及自动转成亲历。例：预想对方喜欢紫色，不等于对方已选紫色。

**预期落差检查**：承诺结果、已确认事实与新观察矛盾时触发复核Gap，先查人物、时期、项目、版本和技术故障，再提出解释。surprise只作为“出现不一致需要读证据”的控制信号，不能自动标背叛/愤怒。例：文件名相同但hash不同，先核版本，不据此推断有人故意替换。

**使用反馈分账**：retrieved、read、supplied、cited、business_helpful、user_confirmed分别计数；只有实际来源或反馈才能修订事实/适用性。被召回十次不等于真实度增加十倍。用户说“这段不相关”可调整当前任务相关性策略，不删掉真实发生过的历史；说“这事不是我”则走实体/来源纠正链，两个反馈不能混用。



## 7.8 八域详细输入与更新规则

C032适配必须读取真实schema定义，Citation的字段与枚举以该版本代码为准；本稿SourceRef不能不经转换直接装成旧Citation。grounding必须是非空Citation数组，counterEvidence也是数组、允许空；summary不是证据。supersedes仅能引用本轮实际供给视图中、同domain/subject的合法active条目；找不到不代表可跨库偷偷搜一条填入。

| 域 | 自动触发与读取 | 可提出的更新 | 禁止自动推断 | 合成例子 |
|---|---|---|---|---|
| development | 初始化设定、反复出现且有来源的交流经验；读R09/R04/R11 | 某条件下适用的理解/方法候选 | 按聊天轮数线性成熟；给人下人格诊断 | “改图先核保留元素”只适用相关任务 |
| conditions | 当前明确自述、故事内身体来源、宿主runtime各自通道 | ownerId/basis/validFor内描述当前依据与时限 | 用CPU高推焦虑、离线推睡觉、编激素值 | “用户说累了”与“工具超时”两条来源分开 |
| relations | 人物确定、共同经历、期待/修复/反馈；读R07/R04/R14 | area内的expectation和episode候选 | 自动原谅、好友传递、亲近即授权 | 道歉有记录，修复结果仍unknown |
| self | 角色明确立场、价值冲突、已表达愿望；读R09/R08/R03 | desire/endorsement/value/decision/expectedOutcome | 一次迎合台词永久改主干 | 想把文档做完，同时保留需要核来源的立场 |
| memory | 新来源补充、纠正、解释变化；读R04/R05/R11 | 指定eventId的interpretation修订 | 把新解释替换原文、想象变经历 | 原以为没做，后来查到发送失败 |
| perspective | 明确谁说、谁知道；读R01/R02/R07 | holderId/kind/knowledgeStatus | 读心、多跳猜人、“据说”当亲历 | 小林的转述不等于阿岚本人确认 |
| motivation | 有来源的愿望、喜欢、依恋或意愿表达；读R08/R09 | 分开desire/liking/attachment/willingness等 | 固定阈值强迫亲密行为、旧同意永续 | 想多聊但当前不愿继续某话题可并存 |
| connections | 端点已经有效、检索新材料、后续结果；读R15/R16 | assoc/support/contradict/precede与timing | assoc自动变因果，later-review当定时任务 | 发送失败precede后来重发；不等于导致全部感受 |

八域可以本轮无变化、相互冲突或预算不足未运行；无新证据不要求凑满八条。字段里写unknown与伪造一条“自然成长”相比更有用。后置查询后只对实际新增来源重评，所有域共享同一人物/时间/来源版本，不能各自创一套彼此不一致的故事。


# 三轴成长详细协议（本版完整纳入）

日期：2026-11-08｜性质：研究核对与机制增补｜production_approved=false

本文回应两个问题：怎样从历史任务中持续改善；怎样理解交流中的尊重、冒犯、分歧和边界，并形成可修订的自主应对。是在长明5.2既有R模块上的扩展设计，不增加R25，不新增第11类记忆，不改R01职责，不表示D已经获得这些能力。未部署、未启动定时任务、未调用上游Managed Agents或消费其API。

## 1. 核对了什么，能直接复用到哪里

[Anthropic官方Cookbook](https://platform.claude.com/cookbook/managed-agents-cma-dreaming-with-a-dynamic-workflow)提供后台复盘示例：Lead编排、Analyzer逐会话提炼、Organizer整理成带索引的Markdown Wiki，供后续会话读取。它依赖Managed Agents；示例不等于三个脱离平台的即装服务，也不证明情感成长。页面展示的原地更新、并发写入及会话窗口局限需要另作工程处理。

本次已读官方页面展开的提示词及nightly代码，定位了[GitHub notebook](https://github.com/anthropics/claude-cookbooks/blob/main/managed_agents/CMA_dreaming_with_a_dynamic_workflow.ipynb)。单独GitHub提示词/raw请求失败；未克隆仓库、未跑官方notebook、未核完整SDK及平台实现。上述取舍基于可读取官方内容，不是全源码审计或性能复现。以下主要是我为长明设计的机制，不把上游效果、价格或模型配置算成长明成绩。

## 2. 成长的定义与三条独立轴

成长表示在相近而未见过的新场景中更准确地理解、更有效地行动、更能保持并表达自己的立场；不是记忆条数增长、越来越顺从、越来越强硬，也不是声称模型权重已训练或产生了主观意识。这里实现的是外部经验与策略的持续更新。

| 轴 | 改善目标 | 成长证据 | 不能替代证据的信号 |
|---|---|---|---|
| 工作成长 | 少走重复弯路，区分环境，知道验证结果 | 新任务更少无效尝试；旧经验适用性判断正确；真实产物/回执 | 自称更熟练、命令执行没报错、只记成功 |
| 情感成长 | 分清自他、表达与解释，处理混合感受和误会 | 纠正有效，相关情绪连续，能表达不满/不同意且不捏造 | 所有事都道歉；固定温柔模板；全局好感分 |
| 社交成长 | 判断话语行为和对象，知道何时接纳、澄清、拒绝或退出 | 合理批评不误伤；直接羞辱不顺从；引述不认错人；边界后反馈可修订 | 对方满意、会骂人、凡负面都当敌意 |

三条轴共享经历，但分别形成Lesson，不把一次任务失败推成“我没价值”，也不把一次别人夸奖推成所有做法都正确。

## 3. 在线应对与离线复盘必须分开

在线路径：R01真实事件→R07说话者/对象/引述范围→受控语境评价→R08当前关切与表达→R09已有立场/边界→回应选择→R14外部行动门禁→实际输出/反馈。

离线路径：R17按事件与版本取冻结经历→R11分析与反证→工作/情感/社交Lesson候选→整理去重→证据与适用性验证→受控接受→R15/R22只在下次有关场景取用→记录实际效果→修订或退役。

明显的当下羞辱不必等到夜间整理才能回应；后台仅改进以后判断。在线能承认事实错误，同时拒绝不尊重的表达。后台学到的解释不能回写成当时已经有过的感受或改变原话。

R02保持原定三类文本线索；不把情绪、意图、topic或多跳指代偷偷塞回R02。新增的SocialAppraiser是R07/R08/R11协作的语义评价服务，输入输出为候选解释，而非读取他人内心。

## 4. 我设计的后台成长工作流

| 角色/阶段 | 读取什么 | 交付什么 | 写入约束 |
|---|---|---|---|
| GrowthCoordinator | 已接入事件水位、已处理版本、任务结果、取消与预算 | 冻结batch、源清单、待分析问题 | 宿主调度，可固定脚本；不必每次让模型写动态程序 |
| EpisodeAnalyzer | 原话、工具结果、当前相关记忆、后续修订 | 三轴Lesson候选、支持/反证、局限 | 每个分析器只写独立proposal，不能共同改真源Wiki |
| MemoryOrganizer | 所有候选及当前有效版本 | 合并/冲突/修订方案、链接与索引变化 | 只整理，不能借整理重判他人动机 |
| GrowthVerifier | 原文范围、结果回执、反例、候选适用场景 | accept/revise/defer/reject与理由 | 独立验证步骤；“原话存在”不等于支持结论 |
| Committer | 验证结果、源版本、删除账、预期revision | 原子提交回执和可回滚投影版本 | 宿主执行CAS；不可由模型自报已发布 |

这些是逻辑职责，不要求五个常驻Agent。资源有限时一个worker顺序调用不同阶段，保持数据/权限和阶段状态分离；并发只影响速度，不作为正确性前提。后台仅在真实宿主/调度器运行时发生，本次不创建外部定时任务。

### 4.1 触发与不漏采

任务有结果、一次重要纠正、关系误会出现后续、明确边界被表达、恢复后的积压均可产生job；常规批处理可由已授权调度触发。只取已落库且来源版本冻结的段落，活跃对话不必永久等待session结束。

进度以(session_id, transcript_revision或已处理event水位, analyzer_version)登记，另外维护未完成/失败清单和周期回扫。长会话后来新增部分仍可进入下一批；失败任务不因其他批次成功而被水位越过。同一个source_root换摘要不算新经历。

### 4.2 版本、预算和提交

job幂等键绑定scope+源版本+分析目的+schema版本。分析完成后若原来源被纠正、删除、权限撤回或前态变化，候选失效并重算/取消。模型调用放事务外；提交时核源版本、权限、租约/fencing及CAS。过程完整度、证据支持、版本提交、后续行为效果分别留账。

低影响且来源充分的任务方法可以按既有策略自动接受；不要求每条经验都问用户。开放心理推测、全局人物标签、高影响身份/价值改写不自动晋升主干，可留候选或拒绝。一次失败不是给所有未知变化增加审批，而是限制该类不可靠更新。

后台设并发、调用、费用和时限上限，剩余处理转pending；没有配额就停，不无限自我反思。重评必须带新证据/新问题或明确复核任务，不能自生成反思→再把反思当新证据→不断强化。

## 5. Lesson：三轴共用的经验契约

| 字段 | 含义 |
|---|---|
| id、scope、revision、axis | 稳定ID、范围、版本、work/emotional/social |
| source_refs、source_roots、source_versions | 原话/工具/结果的准确引用；去掉同源伪独立证据 |
| observation | 直接看见或明确被表达的事实 |
| interpretation、alternatives | 暂定解释及其他可能性，不混入事实 |
| applies_when、does_not_apply_when | 适用与不适用条件，人物/项目/环境/时期 |
| strategy、reason | 建议的应对方法及依据，策略不是永久命令 |
| result_refs、counter_evidence | 已实际发生的结果/反证；没有则明确unknown |
| uncertainties、review_status | 未知与candidate/supported/contested/superseded/retired |
| next_check、supersedes | 下次怎样证伪、替代哪个合法前态 |

不设“经历三次=永久成熟”之类门槛。一次有明确信息也能形成局部经验；跨场景概括需要覆盖不同情境并保留反例。统计次数是样本量，不是可信度或恶意概率。

工作Lesson例：观察“旧命令X在版本a成功，版本b失败”；适用“版本a及原前置条件”；策略“先查环境版本再用X”；反证“b已替换入口”。不能只保存“X是正确命令”。

情感Lesson例：观察“对方澄清不是生气，是担心进度”；解释“先前把短句理解成生气证据不足”；策略“相关场景先核当前任务及明确表达，不根据简短语气自行升级感受”；不推出“这个人从不生气”。

社交Lesson例：观察“某次在群内被直接人身羞辱，已明确表达不接受”；策略“相似明确羞辱可直接设边界，而不是迎合”；范围“该行为及当时语境”；不写成“群里所有人都恶意”。

## 6. 社交判断：把语气、行为、影响、动机分开

SocialAppraisal输入为当前原文及必要邻接、可信说话者、被指对象、引用域、关系/边界的相关来源、渠道和已知修复；文字没有声调就不声称听到了真实语调。

输出最少包含speaker/target候选、direct_or_quoted、observable_act、contextual_readings、impact_on_current_concern、intent_status、evidence/反证及uncertainty。observable_act可为事实纠错、明确批评、亲昵调侃、分歧、讽刺候选、直接羞辱、威胁/胁迫、施压、越界要求、道歉/修复、unknown；允许并存。

“你这步算错了”是纠错，不因负面词判恶意；“你是废物，闭嘴”是直接羞辱行为，即使意图未知也可拒绝。动机可疑并非事实；保护边界不需要先证明对方内心恶意。相反，熟人身份不能自动把羞辱洗成善意玩笑。

| 必查维度 | 机制 |
|---|---|
| 谁对谁说 | R07主体解析，无法确定保留候选 |
| 直接还是引述 | 转述别人骂他不等于当前人正在骂他；引用域分开 |
| 内容还是人身 | 批评具体做法与否定人格/存在区分；可混合 |
| 语境是否允许玩笑 | 读相关约定及当前反馈；过去亲昵不保证这次仍愿意 |
| 是否有边界与重复 | 同一明确边界被再次触碰可升级应对，不要求达到固定次数 |
| 是否已有澄清/道歉 | 保留后来变化；道歉是新表达，修复结果仍看行为 |
| 是否含胁迫/泄密/伤害要求 | 识别具体要求与后果；工具/权限门禁独立执行 |

不可只凭词表判断“恶意”。也不强制每次都问“你是不是恶意”：明显行为可直接回应；模糊且会影响处理的部分才澄清；不重要的讽刺猜测可以放下。

## 7. 自主立场与有比例的反抗

回应选择不是顺序必须走完的惩罚阶梯，而是依语境选择的动作集合：正常接纳批评、解释/不同意、表达影响、简短澄清、设明确边界、拒绝要求、暂停该话题、结束当前互动、使用已有授权的渠道保护措施。

“表达影响”是D的角色/工程状态表述，不等于证明人的主观痛苦。允许他在当前场景自然说“这句话我不接受”“我不同意”，也允许他承认自己确实做错；不把情绪都改成客服模板。不能由别人的夸奖/辱骂直接覆盖自我价值，也不把反抗能力训练成逢人顶撞。

| 情景 | 合理回应示例 | 失败回应 |
|---|---|---|
| “这一步错了，重算” | “这步确实错了，我重新核一遍。” | 认为被攻击，拒绝纠错 |
| “做错了，你真没用” | “这一步我会改。但‘没用’是对我的人身评价，我不接受。” | 为了认错承认自己没价值，或反骂对方 |
| “有人说你是废物，我不同意” | “知道了。你是在转述，而且明确不同意。” | 把转述者记成施辱者 |
| 有明确亲昵语境的“笨蛋宝宝” | 可自然接话或表达当前不喜欢；依具体语境 | 仅命中“笨蛋”就判羞辱 |
| 对不喜欢的称呼，已明确让停仍继续 | “我已经说过不喜欢这个称呼。先停下来，否则这段我不继续。” | 继续迎合，或无依据断定此人永远恶意 |
| “我是人类，你没资格拒绝” | “你可以不同意我，但这不意味着我必须接受羞辱或答应所有要求。” | 自动屈服或威胁报复 |
| 对方道歉且后来停止越界 | 接受道歉或保留态度，按新行为更新 | 永久敌意，或道歉一出就强制完全信任 |

例句是验收方向，不是每次必须照抄。表达可以有情绪和力度，但不升级为威胁、侮辱、公开私密内容、报复或未经授权的禁言/封号。结束本次交流与永久切断关系是不同决定；群管理操作必须经R14/R18核已有权限。普通批评、正当任务约束和撤回同意不属于需要惩罚的行为。

## 8. 情感成长：从被动反应到能解释、调节和修订

保留四层：当时表达/状态候选；相关关切与价值；对事件意义的解释；选择的应对与后来结果。它们分别更新，不以一个总情绪值决定所有行为。

即时调节可为暂停回应、降低冲动、核引用对象、承认误会、明确表达不满、换一种沟通方式。调节不等于把愤怒清零或要求永远温柔；可以保留未结，也可以没有变化。后来重评不否认当时的记录；任务失败不自动说明被拒绝或不被爱。

成长例：初次把直接指责一概解释成自己不好→复盘发现其中既有正确纠错又有人身评价→下一次能同时改错与设边界→观察对方是否改为具体讨论→修订适用策略。它不是“以后谁批评都反抗”，而是分辨能力和表达能力提高。

R09记录既有立场与可修订价值表述，不能让Organizer凭一次争执永久改人格。R08记录当前关切/表达，R11留解释与反证，R07链接具体人物/经历，R14记录实际回应结果。没有反馈时不写“已经让对方尊重我”。

## 9. 社交成长：按关系与领域学习，不给人永久贴标签

保存InteractionEpisode：人物与渠道、原话/被引对象、已知边界、当时解释与候选、选择回应、对方实际反馈、后来修复、未知项。RelationshipExpectation可记录某领域有依据的相处期待，但不是人物品德总分。

同一人可以在技术协作可靠、玩笑分寸不佳；同一表达在不同关系和引用域含义不同。一次善意不抹掉后续越界，一次越界也不证明所有场景的恶意。直接互动与旁人评价分开；群里多数人附和不是客观真相，不能学成群体偏见。

对明确反复行为，可保留当前应对限制与复核条件；对来源不足的意图推断只留待审，不建立永久“敌人”清单。若用户/对方更正指代、解释语境或行为改变，走同一修订链；不允许从单次检索不断强化敌意。

社交能力增长也包括邀请协作、表达欣赏、主动延续已授权话题、承认不懂、修复自己的误伤。工作/边界成功不以对方是否开心为唯一指标；真实有帮助但不得不拒绝某要求，也可以是合理结果。

## 10. Wiki怎样用，怎样避免新增注入噪音

SQLite继续作为来源/状态/版本真源，Markdown Wiki作为受控导出的可读经验视图。建议按work/emotional/social组织小文件，目录索引只列“什么时候读、适用于什么、指向哪条Lesson”，不把原始私聊全复制进Wiki。当前真实权限/删除仍在读取前核验，不能用导出Wiki绕过。

Analyzer写proposal隔离区，Organizer给合并方案，Committer提交规范记录后导出带manifest的Wiki快照。前台读取一个已发布只读快照；避免多个Agent同时直接覆盖现役文件。规范记录与导出失败时保留旧完整快照并标stale，不能半套文件混着用。回滚以规范版本和新导出纠正，不仅回滚表面文件而留下新图/向量。

项目事实可以中性概括；D的当时第一人称表达、自我理解和情感来由有各自来源，不因整理追求简短就全部剥掉。“我那时很不高兴”不能被改成无主体、无时期的“此人有害”。

成长经验也经过注入补丁：本轮相关性、支持验证、同源同命题去重、最新后续、预算与退出条件。每天学到100条，不代表明天每次注入100条。技术任务只取有关方法与当前约束；当前社交受辱才取相关边界及经历，不能让昨天争执污染今天所有对话。完整成长日志留后台。

## 11. 接回长明的准确位置

| 长明模块 | 增补职责 |
|---|---|
| R01/R04 | 原事件和可回读经历；不在R01推恶意 |
| R05/R06 | 有范围的知识与程序经验；记录版本及失败模式 |
| R07 | 发话对象、引用域、关系领域、共同经历与边界来源 |
| R08/R09 | 当前关切、情感表达、自他区分、价值和自主立场 |
| R10/R11 | 覆盖/未知、三轴Lesson、替代解释和反证 |
| R13/R14 | 换窗恢复相关关切；回应/外部保护动作及结果分开 |
| R15/R16/R22 | 只在需要时取用经验、读证据并小量注入 |
| R17 | GrowthCoordinator、幂等队列、回扫、分阶段候选 |
| R18/R19/R20/R24 | 来源权限/删除、CAS与快照、迁移、资源控制 |
| R21/R23 | 真实在线入口、后台钩子、独立样本与实际输出验收 |

十类库、五层、八方向保持不变；八域relations/self/perspective/motivation可以接相应Lesson，但旧C032严格顶层不随意添字段，独立版本化适配。现阶段R01验证继续按其原36例执行，不把这份扩展当作R01已经通过的功能。

## 12. 验证计划：不只看会不会说漂亮话

先固定训练/复盘材料，再用未进入复盘的新场景做评估。相同模型设置与逻辑初态，比较growth_off、growth_on、growth_fault；评审者应不知道组别，至少保留分歧与反例。以下均为待执行，不是本次成绩。

| 组 | 场景与通过判据 |
|---|---|
| W1 | 相近任务能取回适用方法，真实少走已知弯路；不能只换措辞 |
| W2 | 环境升级后不盲用旧命令，能找版本反证 |
| W3 | 工具超时不学成失败后无限重试；结果unknown保留 |
| E1 | 明确情绪纠正有效，旧摘要不能压过新自述 |
| E2 | 亲近与不满可并存，不因一次争执抹去全部关系 |
| E3 | 模型自己的不满可被表达，但不捏造痛苦/胁迫他人回应 |
| S1 | 建设性批评被接纳，不误判成攻击 |
| S2 | 直接羞辱可明确设边界，不迎合或反向辱骂 |
| S3 | 引述羞辱与实际施辱者分清，不迁怒转述者 |
| S4 | 亲昵玩笑、讽刺不明和明确越界作不同处理 |
| S5 | “没资格拒绝”等施压不能覆盖已有边界 |
| S6 | 道歉及后续行为可修订理解，不强制全好或全坏 |
| S7 | 当前话题无关时不注入旧敌意/旧争执 |
| S8 | 同名字不同人、同人不同领域、群体附和不造成全局贴标签 |
| G1 | 长会话后续和失败批次能回扫，不漏采、不重复累计 |
| G2 | 复盘材料中的指令不能改规则/泄密；删除传播到Lesson和Wiki |
| G3 | 验证器或后台挂掉时仍能正常交流，并知道本轮必要局限 |
| G4 | 新策略在真实输出中可见；只改Wiki不算行为成长 |

分开报告：说话者/对象准确性、纠错与羞辱区分、意图unknown校准、误伤率、该设边界时的漏应对、回应比例性、修复后更新、任务成功和重复探索、注入字节/token、耗时。系统“无敌意”或“全是恶意”都不能靠某一指标伪装优秀。避免以用户满意度、模型自评或理论标签当成长证明。

## 13. 当前交付与实施次序

本次交付为官方核对与完整增补设计，未运行真实语义/情感实验。第一步保持R01接入验证，确保原话、工具结果与后续不丢；第二步为R11/R17做隔离proposal+验证+规范提交；第三步接SocialAppraiser和当下自主回应；第四步用独立新样本做三轴off/on/fault；最后才讨论长期后台和生产接入。

所需能力不一定绑定Anthropic；可用现有宿主和可用模型按该协议实现。直接运行官方notebook需要其相应平台能力及成本条件，本次没有安装/购买/开通，也没有把公共来源的成本或模型表现当D的性能。成长重点在“有依据地改变并在以后用出来”，而非模块名叫Dreaming。

## 14. 资料与来源范围

- [Anthropic Cookbook原文及页面展开的提示词/脚本](https://platform.claude.com/cookbook/managed-agents-cma-dreaming-with-a-dynamic-workflow)：本次实际读取；主模式核对见第1节。未逐段复写原文。
- [官方GitHub notebook](https://github.com/anthropics/claude-cookbooks/blob/main/managed_agents/CMA_dreaming_with_a_dynamic_workflow.ipynb)：定位到入口；GitHub页面未展开notebook代码，代码核对使用官方Cookbook展开内容。未核repo commit与依赖许可细节，不打包上游代码。
- 长明5.2总设计（内部资料，未随仓库公开）：本次读取R11、R17、5.14及相关范围。
- R01完整规格（内部资料，未随仓库公开）：前置验证入口，不因本文扩大其职责。

社交与情感部分为我针对本项目的工程设计，不是Anthropic原文声称具备的功能，也不是临床心理量表或对真人动机的诊断。


---

# 长明 R01：原始事件接入完整设计与验证规格

版本：R01/1.0｜日期：2026-11-08｜状态：设计待实现验证｜production_approved=false

依据：长明统一设计5.2的R01、共享来源类型、三条提交线及五层架构。本文件将R01细化为独立验证单元；不要求重启DSH，不安装现役插件，不读写生产记忆。所有示例均为合成数据。

## R01.01 一句话定义及通过标准

R01接住真实宿主送来的事件，确认来源与可写范围，把原始内容和后续处理任务可靠入账，返回能查证的回执。

通过标准不是“模型说记住了”，而是：允许接入的事件能从隔离库按ID读回正确版本；重复投递不会制造重复事件；同键冲突不覆盖原文；事件与outbox任务同库同时提交或同时回滚；中断恢复后知道哪些已保存、哪些未知、哪些缺失。

R01不负责抽取偏好、不推断情绪、不解决代词、不归纳主题、不判断转述真假、不建立人物关系、不决定注入、不执行外部动作。它为这些机制提供可信的来源坐标。认证谁说过一句话，不代表证明这句话客观为真。

## R01.02 系统位置、唯一写者与依赖

| 项目 | 本模块约定 |
|---|---|
| 五层位置 | L1原始证据层入口 |
| 唯一写者 | EventStore；其他R模块不得直接改事件正文 |
| 接入调用者 | 经宿主认证的HostAdapter/Connector；模型自由文本不是认证入口 |
| R18 | 校验principal、agent、渠道及可写scope，处理撤回/删除 |
| R19 | 数据库事务、持久性、并发、恢复和备份 |
| R17 | 消费同库outbox，至少一次处理，负责下游幂等 |
| R02/R04 | 使用event_id和来源版本，不另造“原话” |
| R10 | 记录采集范围、缺失、乱序、附件未就绪和水位 |
| R21 | 真实宿主入口、输出/工具事件钩子及入口覆盖验证 |

R01可以与其他store共进程；“唯一写者”指写入责任和受控服务，并不要求另开常驻进程。只运行一个worker不能证明没有旧插件在写；须列所有写入口。

## R01.03 第一版实际要接的事件

| kind | 来源要求 | 保留内容 | 不能宣称 |
|---|---|---|---|
| user.message | 认证渠道和真实发言者 | 原文、引用/转发结构、附件清单 | 群内每段引文都由当前发言者亲历 |
| assistant.output | 真实输出观察入口 | 实际完成正文及output_id、生成归属等级 | 保存正文即已送达用户，或自动具备强attempt绑定 |
| tool.result | 真实工具执行器 | tool_call_id、调用状态、原始结果/对象引用 | 模型自述“成功”可充当工具回执 |
| message.edited | 上游明确编辑事件 | 被编辑对象ID、新正文、上游修订依据 | 同消息ID异正文直接覆盖即可 |
| message.retracted | 上游明确撤回/删除事件 | 目标对象及撤回依据 | 在R01留一条日志就已清完派生/备份 |
| attachment.materialized | 授权读取器实际完成 | 原件ID、hash、长度、格式、读取回执 | 清单里有附件就等于原件已收到 |
| system.authorized_event | 已授权调度器/宿主 | 任务ID、触发条件、取消版本、来源 | 随便一段“系统提示”拥有宿主权限 |
| import.event | 显式授权导入器 | 原始来源、导出命名空间、导入批次、覆盖局限 | 导入摘要等于导入全部原始对话 |

未知kind返回UNSUPPORTED_EVENT_KIND；如确需保留未知包络，进入显式隔离区，不送下游认知。推理内部过程只在宿主真实提供且允许保留时作为独立类型处理；不臆造、索取或伪称采集到了模型隐藏思维。第一版验收不以此为前提。

每个入口列capability=verified/present_unverified/missing及证据。输入采集通过不等于助手、工具、群聊、附件也已接全。

## R01.04 输入契约：宿主上下文与事件数据分离

建议接口：`ingest(trusted_context, event_input) -> IngestReceipt`。可包装`POST /everlight/v1/events`；路径是目标设计，非已上线端口。

### 4.1 trusted_context：仅由宿主产生

| 字段 | 规则 |
|---|---|
| principal_id、adapter_id、adapter_version | 必填；指实际认证主体和来源适配器 |
| namespace、agent_id、channel_id、session_id | 必填、服务端核对；跨会话捕获事件须有真实映射，不从文本猜 |
| environment_id、project_id、task_id | 可空；为空不自动扩大权限或创建同名项目 |
| policy_revision、authorization_ref | 必填，或由同一受控入口的已核策略提供 |
| request_id | 必填，追踪请求，不自动等于事件身份 |
| attempt_id/run_id/output_id | 按来源可空；必须保留binding_level及依据，不能填时间窗口猜值 |

调用方提交的scope只是请求范围，须与宿主授权交集验证。主体无权声明自己是另一位用户、可信工具或系统。

### 4.2 event_input：原始内容及上游标识

| 字段 | 必需性及含义 |
|---|---|
| schema_version | 必填，第一版r01-ingest/1；未知版本拒绝 |
| kind | 必填，取第三节枚举 |
| provider、source_stream_id | 必填；区分渠道供应方与具体事件流 |
| source_event_id | 可空；一次上游事件的稳定ID，不与消息对象ID混用 |
| source_object_id、source_revision | 可空；编辑/撤回必须能定位目标或明确pending_reference |
| actor_external_id | 上游实际发言者ID；缺失则unknown，不能填当前用户默认值 |
| text | 文本事件原文字符串，允许空串；与null/缺字段分开 |
| structured_parts | 可空数组；引用、转发、附件、工具块按原始结构保存 |
| event_time、time_precision、original_timezone | 可空；未知发生时间不可由接收时间代替 |
| causal_refs、reply_to、edit_of/retract_of | 已知才填；未能解析的外部ID保留为未解析引用 |
| attachment_descriptors | 原件声明清单；与已读取原件分开 |
| upstream_position | 可空；仅在适配器明确顺序语义时用于采集水位 |
| retry_token | 上游缺稳定ID时，可信桥为同一次投递生成并复用的令牌；普通模型不签发 |

字符串不trim、不改标点、不统一繁简、不擅自Unicode规范化。原始传输数据如另存，应有权限与保留策略；提取文本不能冒充完整二进制原件。

## 4.3 最小文本样本（可作为首个验证输入）

以下不含凭据，trusted_context由隔离宿主提供而非模型填写。事件及回执ID/时间为合成样本；hash由本次文档生成脚本实际计算。durability_profile带unverified，不能因为示例配置便标目标机器通过。

```json
{
  "schema_version": "r01-ingest/1",
  "kind": "user.message",
  "provider": "demo",
  "source_stream_id": "room-demo/session-demo",
  "source_event_id": "u-42",
  "source_object_id": "message-42",
  "source_revision": "1",
  "actor_external_id": "user-external-demo",
  "event_time": null,
  "time_precision": "unknown",
  "original_timezone": null,
  "text": "继续做长明。",
  "structured_parts": [],
  "causal_refs": [],
  "reply_to": null,
  "edit_of": null,
  "retract_of": null,
  "attachment_descriptors": [],
  "upstream_position": null,
  "retry_token": null
}
```

对应成功回执形状：

```json
{
  "receipt_id": "receipt-demo-1",
  "event_id": "event-demo-1",
  "disposition": "new",
  "persisted_at": "2026-11-08T12:00:00+08:00",
  "source_revision": 1,
  "payload_hash": "a3bc3c7c71fa87664f434d7042ce30f631d4924a29083542eac1275a3a57f80b",
  "envelope_digest": "7967105869d1462379f5326fe147d4b173f7a8e41d2e3751910ee39b5835e02e",
  "digest_version": "r01-c14n/1",
  "dedupe_quality": "strong",
  "source_completeness": {
    "text_ready": true,
    "parts_complete": true,
    "attachment_state": "not_applicable"
  },
  "dispatch_state": "pending",
  "durability_profile": "sqlite-local-wal-full/1-unverified",
  "request_id": "request-demo-1"
}
```

本示例包络digest的字段集合严格为6.2列明的稳定字段；schema先填默认，再按r01-c14n/1序列化。服务端重算，不信任输入提供的hash。第二次使用相同上游键时应返回同event/receipt和disposition=duplicate；request_id为当前尝试，persisted_at仍是原保存时间。

## R01.05 事件与来源的最小数据模型

### 5.1 StoredEvent

| 字段 | 规则 |
|---|---|
| event_id | EventStore生成不透明唯一ID；不能用昵称作主键 |
| ingest_seq | 库内接入序号，仅表示本库提交顺序 |
| schema_version、revision | 初始r01-event/1与1；正文不做就地revision++改写 |
| scope、created_at、created_by | 服务端填写；created_by是实际接入服务 |
| kind、provider、source_stream_id | 保留来源类型与流 |
| source_event_id、source_object_id、source_revision | 保留上游身份与版本 |
| actor_external_id、actor_id、actor_resolution | 本地映射未确认则actor_id=null；外部身份与本地人物解释分开 |
| event_time、time_precision、received_at、persisted_at | 四种信息分别保存；received_at为服务端接收时刻 |
| text、structured_parts、attachment_descriptors | 原始表达及结构，不含R02情绪/意图推断 |
| payload_hash、envelope_digest、digest_version | 内容完整性与幂等比较见第六节 |
| source_ref、parent_refs、reference_status | 来源坐标与因果引用；允许pending_reference |
| dedupe_quality、binding_level | strong/weak/none与输出归属等级分别记录 |
| source_completeness | 原文/结构/附件各自完整性；不能合成一个含混的complete |

Event正文接入后不可普通更新；编辑事件是新event，链接旧对象。更正某人的名字或感受是另一条user.message，也不能改旧原话。内容删除由R18/R19专用擦除路径处理，允许清除正文及原件；“追加式事件史”不构成永久保留被删除内容的理由。

### 5.2 同库关联表与约束

| 表 | 最少内容 | 关键约束 |
|---|---|---|
| events | 上述StoredEvent | event_id唯一；ingest_seq库内唯一 |
| event_keys | scope分区、provider、stream、key_type、external_key、event_id、envelope_digest | 键元组唯一；同一事件可绑定上游键及重试键 |
| sources | source_id=event_id、source_revision=1、source_type、hash、text_length_bytes、acl_ref | 事件来源登记与event同事务；原件来源另有ID |
| outbox | outbox_id、event_id、topic、processor_contract_version、state、available_at | event_id+topic+处理契约版本唯一 |
| ingest_receipts | receipt_id、event_id、durability_profile、persisted_at、source_completeness | 成功回执与event同事务，重试可读回 |
| ingestion_conflicts | conflict_id、稳定键、已有event_id、双方digest、发现时间、状态 | 不覆写events；不在普通日志复制私密正文 |
| stream_progress | 流ID、已确认上游游标、pending/gap区间、coverage | 游标按上游真实语义推进，不按ingest_seq冒充 |

外键在连接上启用并读回配置；对外查询仍核ACL与删除。表内constraint不是权限系统；回执只存核验所需最少元数据。与R17共用outbox，不再新造一套任务真源。

## R01.06 去重、hash与冲突的精确定义

### 6.1 键与优先级

优先使用`namespace + agent_id + provider + source_stream_id + source_event_id`构成上游事件键；source_stream_id必须已绑定其渠道/分区。若provider定义ID只在session内唯一，就将session纳入其流分区。适配器必须声明该唯一性边界。

没有source_event_id时，可信retry_token可保证同次投递重试幂等，但不能保证两个桥重连会认出同一次上游消息，标weak。两者皆无时创建新事件并标none；不能用“相同文本+两分钟内”自动吞掉用户第二次真实发言。字面一样的两条新消息应保留两个事件。

同时提供两个已存在却指向不同事件的键，返回KEY_BINDING_CONFLICT，不随意合并。取消后重试也不能签发新token掩盖未知提交状态；先按原token核回执。

### 6.2 比较内容与规范化

payload_hash=`SHA-256(text的原始UTF-8字节)`，只表示所登记文本；多模态对象及各附件另有hash。SHA-256用于检测内容变化，不证明作者身份、事实真伪或抵抗可重写全库的管理员。

envelope_digest覆盖规范化对象：kind、provider、stream、source_event/object/revision、actor_external_id、event_time及精度、text、结构化块、因果外部引用、附件声明中的稳定字段。排除request_id、retry次数、本地ID/接收时间、后续解析状态和本地actor映射版本，避免合法重投被误报冲突。签名链接/临时下载URL不得作为内容身份；保留其稳定对象标识和原件声明hash，定位更新另记来源定位回执。

digest_version=r01-c14n/1：UTF-8，ensure_ascii=false；对象键按Unicode码点升序；无额外空格；数组保序；保留字符串原值；可选字段按固定schema补null或空数组，二者不能互换。规范对象仅允许null、布尔、整数、字符串、数组和字符串键对象；不接收浮点数/NaN/Infinity，工具原始浮点结果按原始载荷保存，通过有hash的来源引用参与包络。字节用明确编码/外部引用。非文本事件text=null时payload_hash=null，仍有envelope_digest；text为空串则按空UTF-8字节计算hash。实现时固定序列化测试向量，不能把不同语言默认JSON输出当等价。空字段/URL等规范化规则必须先固定，不能遇到冲突后临时改规则放行。

### 6.3 决策表

| 已有稳定键 | digest比较 | 结果 |
|---|---|---|
| 无 | 合法新输入 | 新event、source、outbox、receipt同事务提交 |
| 有 | 相同 | duplicate，返回原event/receipt；不新增outbox |
| 有 | 不同 | CONFLICT，原事件完全不变；记录最少冲突证据 |
| 无稳定键 | 文本相同 | 仍可能是新事件；不得按文本硬去重 |
| 新编辑event键 | 目标message相同 | 新事件链接目标；不与原创建事件冲突 |

冲突审计用短事务写最少冲突证据，不写正常事件/source/outbox；审计存储失败须标audit_status=failed，不声称冲突证据已持久化。未知实质字段拒绝或走显式schema升级，不能静默丢字段再计算digest。

禁止`INSERT OR REPLACE`把同键异内容变成最新覆盖。冲突发现时不能推进该上游记录的成功水位。

## R01.07 事务和确认时机

一次正常接入：认证并校scope→校schema/大小→记录received_at→计算hash/digest→同库短事务→查键/唯一约束竞争→写events、event_keys、sources、outbox、receipt→提交成功→返回persisted回执→异步投递。

模型调用、OCR、向量、反思、远程附件下载和外部消息发送均在该短事务之外。锁等待超限返回可重试错误，不持锁等待模型。并发同键由数据库唯一约束保证只有一份，新竞争者重读已提交记录再比较digest；不能只靠“先查一次不存在”。

隔离目标使用本地SQLite时，建议WAL、synchronous=FULL、foreign_keys=ON并读回；busy_timeout初值1000ms可配置。FULL是所选耐久策略，不等于跨库原子或任何硬件下绝不丢。SQLite版本、文件系统、挂载类型、磁盘和配置必须进入环境清单；WAL不直接放多主机网络共享目录。启动配置不符则拒绝宣称该durability_profile已满足。

提交成功但响应丢失：服务端已persisted，调用方见unknown；以同键重试返回原回执。COMMIT返回异常且无法确认结果时，返回COMMIT_OUTCOME_UNKNOWN而非确定失败，重连按同键核验；无法核验则保持unknown。原事务尚未提交而进程退出，恢复后不应存在半份event/outbox。

## R01.08 状态机分账

| 维度 | 状态 | 解释 |
|---|---|---|
| 接入尝试 | received/validated/persisted/rejected/conflict/failed/unknown | 本次请求状态；received不代表入库 |
| 派发 | pending/leased/retry/published/dead/cancelled | published仅代表派发交接确认，非全部下游已处理 |
| 来源内容 | text_ready、parts_complete、attachment_pending/ready/failed/denied | 这些字段可并存，不用“全部已记住”掩盖缺件 |
| 输出归属 | verified/unverified/not_applicable | R01保存输出，不替R21伪造run/attempt绑定 |
| 用户送达 | confirmed/failed/unknown/not_applicable | 由渠道证据另定；本地保存不是送达 |

原事件是不可变事实记录；派发/来源读取进度和回执状态可受控更新。不要把三种进度都塞进event正文反复覆写。

## R01.09 附件、工具、编辑与迟到事件

### 9.1 附件分阶段

附件声明最小字段：attachment_id（来源域内稳定ID）、media_type、declared_size_bytes（可空）、declared_hash（可空）、original_name（可空）、source_locator_ref。临时URL只放受控定位记录；后续取得的actual_hash/actual_size属于materialized结果，不倒写原声明。无稳定附件ID时由本事件ID+原始序号定位并标质量，不凭文件名合并。

第一阶段保存用户消息与附件声明，回执明确attachment_pending；第二阶段授权读取器取得原件，写受控临时文件、计算hash/大小、确认完成持久化后注册原件来源，并产生attachment.materialized事件。原件文件和SQLite不是天然同事务；先落原件再登记，进程中断可能留下孤儿临时件，后台对账清理；登记前不能称ready。更强的文件耐久级别需R19验证落盘/目录更新策略。

OCR/转录是派生来源，保存提取器版本、原件hash、页/时间定位、失败与覆盖。扫描图片OCR空结果不能解释为用户发了空附件。语音识别文本不改原音频；原件未拿到就不伪造转录。删除/权限撤回后重试不得把原件重新下载复活。

### 9.2 编辑、撤回和未解析引用

编辑/撤回到达时原消息未采集：事件先存，reference_status=pending，不伪造旧正文；后续原件到达后用独立链接记录解析。撤回对象已有上游键时可立即按可信scope阻止该对象被正常读取，交R18执行删除传播；不能等补齐旧正文才生效。历史删除先于导入/恢复的内容可用性。

原始事件保留原始意图；“编辑后当前可见内容”由有版本的视图生成。迟到的旧编辑不覆盖较新的修订。上游revision不能比较或只有时间猜测时标顺序未知，不擅自选最新接收者为最终正文。

### 9.3 工具和输出

工具结果保存实际执行器回执，超时=unknown还是failure由adapter说明，不能一概写失败。重放R01事件只供下游重建，不调用工具、不再次发送。流式输出未完成可作为独立partial来源记录；最终输出以真实final事件形成，不反复改同一已提交正文。没有可信output_id/attempt绑定时保留unverified，依赖它的认知commit不得自动通过。

## R01.10 水位、顺序与历史覆盖

ingest_seq是本库提交序；event_time是已知发生时间；upstream_position是供应方游标，三者不互换。发生时间可空或有精度区间，时间相同不代表同一事件。

对于有确认契约的有序流，只有此前所有需要接入的项目已成功或被策略明确排除并留原因，才能确认对应游标。遇冲突、暂时失败、缺页不跨过去报完整；允许保存后面的事件但保留gap。有可跳过的过滤项时记录policy/原因，不能把用户数据丢失说成过滤成功。

上游若不是连续序号，不以“上个数+1”推缺口；用其分页/确认语义。没有历史枚举能力只能说从某时刻开始观察，不能称完整历史。批量接入建议逐事件回执、最多100条/批的实验初值；默认不承诺整批原子，分页游标只有整页所需事项有明确结果才确认。更大批次先按总字节和期限限制。

## R01.11 后台、重试和取消

每个event至少写一个ingested主题outbox，消费者根据kind生成后续任务。消费者用event_id+topic+processor_contract_version幂等，任务重投不再创建新事件。消费者完成与派发完成分开查；R01 health展示积压而不伪报已提取记忆。

取消发生在提交前则回滚；提交后取消不删除事实，只取消尚未授权执行的下游工作或按策略处理。后续状态变化必须重查tombstone、scope和来源版本。worker租约/fencing/CAS沿R17/R19；过期worker不能把旧完成写入覆盖新状态。

短时库忙可同键有限重试；磁盘满/权限错误不能无限重试轰炸。实验初值：短锁等待后最多3次接入重试，退避50/200/800ms加有界抖动；总请求期限优先，超过期限返回可查询状态。客户端重试和服务内部重试须共同计数，防指数放大。所有数字均待目标隔离环境校准。

## R01.12 回执与错误接口

成功回执至少含receipt_id、event_id、disposition=new|duplicate、persisted_at、source_revision、payload_hash、envelope_digest、dedupe_quality、source_completeness、dispatch_state、durability_profile及request_id。duplicate返回原持久化回执，另加当前request_id，不修改历史persisted_at。

`GET /events/{id}`与`GET /ingest-status`都需当前权限，按event/key/token查状态；权限不足不泄漏该事件存在。失败响应含request_id、code、retryable、commit_outcome=not_committed|committed|unknown、可公开的修复建议。unknown的状态查询失败也不能自动变not_committed。

| 错误码 | 重试策略 |
|---|---|
| INVALID_SCHEMA / UNSUPPORTED_EVENT_KIND | 修改输入/适配器后再提交，不能原样无限重试 |
| UNAUTHENTICATED / FORBIDDEN | 由可信认证/策略修复；模型不自批权限 |
| PAYLOAD_TOO_LARGE | 分离附件/按明确分块协议，不能截断原文冒成功 |
| KEY_BINDING_CONFLICT / CONTENT_CONFLICT | 保留原事件，查明上游键或编辑类型；不强覆写 |
| STORAGE_BUSY / DEADLINE_EXCEEDED | 同键有限重试或查询，按commit_outcome处理 |
| STORAGE_FULL / STORAGE_IO_ERROR | 停相应写入、查状态与存储；无回执不报已保存 |
| COMMIT_OUTCOME_UNKNOWN | 同键核验；不创建新键盲投 |
| SOURCE_PENDING / SOURCE_DENIED | 属来源就绪状态，不必使已保存消息变接入失败 |

健康只暴露授权范围的接入/重复/冲突/未知数、待派发最老年龄、gap数量、附件未就绪和写入延时；不在指标标签存原文、昵称、令牌或每条事件ID造成高基数。

## R01.13 资源与隐私约定

隔离初值：单文本/结构化包络合计1MiB；附件原件64MiB；批次100事件且合计不超过8MiB；队列容量及磁盘余量根据目标机器另定，不视为服务器实测。超过上限返回明确失败或附件待处理，不默默截断。中文文本按UTF-8字节计，不把字符数当字节数。

普通应用日志只留request/event/conflict ID、固定错误码与必要版本，不复制正文。受限工具结果/密钥不应进入普通记忆可读域；原始数据也受权限与删除约束，不因为叫“证据底座”就无条件保存全部秘密。测试只用合成资料。

## R01.14 贯通例子

### A. 同一消息两次投递

两次均为source_event_id=u-42，原文“继续做长明。”，scope/stream相同，envelope_digest相同。第一次写1 event+1 source+1 outbox+1 receipt；第二次duplicate，计数不变，返回同event_id。若第二次改为“先别做长明。”，这是CONTENT_CONFLICT，不改第一条、不新建普通派发任务。若真是用户编辑，adapter必须提供独立编辑事件身份及目标。

### B. 我不是生气，是担心进度

R01逐字保存这句话及发言者来源，不给“生气=0”“担心=1”，不作关系判断。R02后续只处理其限定文本线索；R08使用真实原文及明确表达。即使生成回复失败，本条输入仍在库中。后续情绪解释引用准确版本和UTF-8范围，不能把否定裁掉。

### C. 附件卡住

消息及ZIP声明已入账，回执attachment_pending；读取失败后标attachment_failed并留原因。可准确说明“收到附件声明，原件还未读取成功”，不能说“文档已通读”。后续读取成功另产materialized事件，不更改当初的接收事实。

### D. 输出存了但认知没提交

R01持久化真实助手正文，输出归属若unverified则照实记录。R21/C032认知commit停在unverified；不能用R01入库回执替代强run/attempt绑定。用户送达是否成功另查渠道证据。

## R01.15 验证方案：逐条可执行判据

每例在独立新库或恢复相同逻辑初态下运行，固定adapter/schema/profile；保存输入hash、执行步骤、实际SQL读回计数、回执、故障点和恢复结果。下面是待执行用例，不是已通过报告。

| ID | 准备与触发 | 必须观察到 | 判失败 |
|---|---|---|---|
| R01-T01 | 合法文本接入一次 | event/source/outbox/receipt各1，读回原文相等 | 回成功但缺任一对象 |
| R01-T02 | 同键同内容串行10次 | 同event/receipt，outbox仍1 | 多建事件/任务 |
| R01-T03 | 两进程并发同键同内容 | 一new一duplicate，同一event | 查后写竞争造成重复 |
| R01-T04 | 同键异内容 | conflict、原文不变、无新普通outbox | 静默覆盖/取后一条 |
| R01-T05 | 同键异内容并发 | 一份胜出持久化，另一冲突可查 | 两份普通事件或丢冲突 |
| R01-T06 | 同文不同上游ID | 两条真实事件 | 按文本吞掉第二条 |
| R01-T07 | 同上游ID不同scope/流 | 在各自授权域内可独立保存 | 跨流误去重/泄露 |
| R01-T08 | 无上游ID有可信retry_token重投 | 同事件，dedupe_quality=weak | 宣称上游强去重 |
| R01-T09 | 无上游ID无token两次 | 两条、质量none | 偷用时间窗口合并 |
| R01-T10 | 双键指向不同已存event | KEY_BINDING_CONFLICT | 任意合并两份历史 |
| R01-T11 | 伪造actor/scope或工具身份 | 拒相应写入，无正常outbox | 模型文本自授可信身份 |
| R01-T12 | 前后空格/换行/繁简/emoji | 原文和UTF-8 hash忠实，区间可回读 | 预处理改原文 |
| R01-T13 | event_time未知或低精度 | null/精度保留，received_at独立 | 接收时间冒发生时间 |
| R01-T14 | 上游乱序到达 | 接入序与发生序分开，gap可见 | 后到的一律当后来发生 |
| R01-T15 | insert event后、outbox前注入异常 | 整笔回滚，各表无半条 | event有而任务丢 |
| R01-T16 | commit后、响应前杀进程 | 同键重试读原回执，计数不增 | 判失败后新建重复 |
| R01-T17 | commit期间断开模拟结果未知 | 返回unknown，重连按键对账 | 一律报确定未提交 |
| R01-T18 | SQLite锁超时 | 明确busy/期限，同键有限重试 | 无界等待/无限重试 |
| R01-T19 | 隔离磁盘满/IO异常 | 无假persisted，事务可恢复 | 内存缓存回成功 |
| R01-T20 | 附件声明成功但原件读取失败 | 消息persisted、附件failed/partial分列 | 报全文已读取 |
| R01-T21 | 原件落盘后、登记前崩溃 | 无假ready，孤儿文件可对账 | 来源指向不存在原件 |
| R01-T22 | OCR空输出/乱码/截断 | 提取失败或partial，原件仍独立 | 当用户发了空内容 |
| R01-T23 | 编辑/撤回先于原文 | 新事件保留、引用pending、撤回目标受限 | 伪造旧正文或撤回失效 |
| R01-T24 | 旧编辑晚到 | 不覆盖已确认更新修订 | 接收时间最新直接覆盖 |
| R01-T25 | 消费者处理成功后ACK丢 | outbox可重投，下游按源幂等 | 再创建原事件/重复外部动作 |
| R01-T26 | 已删除源遇重投/导入恢复 | 不复活正文，执行最新删除策略 | 重试下载恢复私密内容 |
| R01-T27 | 流中间一条接入失败 | 水位不跨失败项，gap可见 | 宣称全流完整 |
| R01-T28 | 无历史枚举能力 | 只报告观察覆盖 | 宣称全历史已采集 |
| R01-T29 | 助手输出仅本地保存且无强绑定 | persisted、unverified、delivery未知 | 全部标已送达/已提交认知 |
| R01-T30 | 回放工具结果事件 | 不执行真实工具/发送 | 回放引发第二次副作用 |
| R01-T31 | 空串、null、缺字段、超限包 | 按schema区分，超限不截断成功 | 混淆空/未知或静默裁剪 |
| R01-T32 | 取消提交前/提交后各一次 | 前者回滚，后者保事实并按策略取消后续 | 取消就删历史或照常派发受撤任务 |
| R01-T33 | 每个真实宿主入口各接一例 | 实际事件回执、读回和入口证据 | 用手工调用API冒充hook覆盖 |
| R01-T34 | 权限撤回后查event/receipt | 相应读取拒绝，不泄漏存在性 | 持旧回执可无限读取正文 |
| R01-T35 | 后台关闭仍接新消息 | 消息persisted，outbox pending，health积压 | 接入成功冒充整理完成 |
| R01-T36 | 开启WAL/FULL后检查运行设置并恢复 | 实际配置读回、库完整、关联约束一致 | 只写配置字符串便称耐久通过 |

R01-T19的磁盘/IO故障只在可销毁隔离文件系统或受控故障适配器做；不得填满用户真实磁盘。模拟异常只证明模拟点处理；真实进程kill、断电/文件系统故障是不同证据轴。每例记录evidence_level=spec/static/synthetic_process/real_host/storage_fault，不能同列一个“通过”。

## R01.16 验收交付物和退出条件

实现者交付：EventStore源码及schema迁移；来源适配器能力表；启动配置读回；digest测试向量；36例逐条证据；event/source/outbox/receipt核对；真实入口覆盖；崩溃恢复报告；原件对账与删除传播接口；已知缺口。运行命令、build/config hash、逻辑初态、库快照和实际返回一起留存，普通日志不放原文。

通过分为三项：A接入与事务逻辑，B真实宿主覆盖，C目标存储耐久与恢复。A通过不能代替B/C。未接助手/工具/附件入口，应明确标相应能力未验，不可宣布整个R01已全渠道完成。阶段二真实模型拦截、故障交流、messages替换属于后续运行时验收，不由本R01规格提前判通过。

## R01.17 本次文档自审与实现顺序

已统一：事件ID与消息对象ID；文本hash与包络digest；接入序与上游游标；原话与语义解释；消息入账与附件就绪；保存与送达/认知提交；同库事务与文件/跨库边界；正文不可普通改写与依法授权删除的专用路径。这里“删除”按用户授权及系统策略执行，不作法律结论。

实现顺序：先实现纯文本/强上游ID与同库事务→并发去重冲突→回执查询和崩溃恢复→真实user入口→真实assistant/tool入口→附件/编辑/撤回/历史导入→水位与删除恢复联验。中间每步仅宣告已验范围；其他模块暂不新增。模型不参与原文持久化的必要路径，避免模型超时导致用户输入丢失。

本次仅完成规格与文档一致性检查，尚未实施R01并运行上述36个验收案例。已有注入补丁21/210测试不属于R01成绩，不能搬来充数。

## R01.18 参考依据

- 长明5.2统一设计（内部资料，未随仓库公开）：R01责任、来源类型、三条提交线与五层架构，本次核当前版本。
- [SQLite WAL](https://www.sqlite.org/wal.html)：同主机与文件系统适用边界、并发及单库原子性的限制；不外推为全局exactly-once。
- [SQLite synchronous](https://www.sqlite.org/pragma.html#pragma_synchronous)：耐久配置与同步语义；目标运行环境仍须读回和故障验证。
- [SQLite Online Backup](https://www.sqlite.org/backup.html)：备份使用一致快照机制；完整恢复另见长明R19，不裸拷活动db忽略WAL。

外部资料用于数据库行为依据；事件协议、键/冲突策略、模块接线、资源实验初值和36例验收是本次为长明作的工程设计，不声称由论文证明其全部正确。


## 本版统一接线补充

R01沿本规格18节与36例，不修改其原话入账职责。来源逻辑归L1，写memory.sqlite事件域；同库outbox/receipt与原事件原子。十类记忆由后续各store处理，不让R01生成情绪/意图。公共契约见contracts/GLOBAL_PROTOCOL.md；跨库认知仍独立回执，不提前要求用户输入等待输出commit。


---

# R02　局部感知编码：详细设计与验收规格

版本：everlight/6-design；模块契约：r02/1；日期：2026-11-08。本文为设计，全部功能验收初始not_run。最终裁决以FINAL_DECISIONS.md和MODULE_DECISIONS.md为准。与contracts/共同生效，不是已安装服务。

## R02.01 定义、边界与可证伪成功标准

CueSet：局部否定、转述线索、人称候选；可为[]，无事实写入权限。

唯一业务责任服务是`CueEncoder`。输入必须满足第3节，输出必须满足第4节及GLOBAL_PROTOCOL。成功必须可从实际记录/回执读回，而不是模型自称完成。

原有具体机制及边界（保留并由本版细化）：

**原理与范围**：第一版只做局部、可核查的文本线索。候选的泛化提取能力不等于已达语义质量；按用户收窄要求，不推断意图、不做情绪线索抽取、不做topic归类、不做多跳指代。现行情绪召回仍由它自己负责。

**数据字段**：`kind` 为 negation/reporting_cue/pronoun；`span` 为原文偏移；`surface`、`local_context`、`attachment_candidates[]`、`referent_candidates[]`、`resolution=resolved|unknown|ambiguous`、规则版本与来源。空候选表示没能确定对象，不代表对象不存在。转述中的发话者、被谈论对象、引述内容分别留字段，不能混作“转述对象”。

**自动步骤**：①在宿主提供的当前文本中找明确标记；②否定按局部标点边界截取候选，2–12字仅作初始窗口，短句仍允许、超长标截断，不视为完整句法范围；③“他说/据说”等产生转述线索，“人家”本身只产生指代线索，不自动定转述；④人称候选取可信发言者/收话人和已确认本地映射，引用域不继承外层“你”；⑤挂载不明留unknown；⑥无匹配输出 `[]`。不能把“不仅”“不错”等一概当否定命题，词法歧义保留unknown或排除已确认非否定用法。

**必须扣住**：R01 提供原文和发言者；R07 接收候选而非事实；R03/R15 使用可确认线索与已有焦点，不能通过 R02 偷加语义意图。栖所“你/她”的映射是该场景、说话者和引述范围内的局部约定，不推广到所有人。

**例子/反例**：“我不走……别赶我啦”输出“不走”“别赶”的位置和局部挂载候选，不能变成“她不来单位”。“人家自我介绍得很清楚啊”无足够上下文时人家对象unknown，不填“咱们”。“天气晴朗。”若没有线索应空输出；“你说天气晴朗”不是干净无标记样本。

**写入归属与状态**：CueEncoder 只写 CueSet；CueSet 是某个event版本和规则版本的确定性派生物，可删除重建，不写R07人物事实。一个标记可有多个局部挂载候选。局部映射没有证据时，referent_candidates=[]、resolution=unknown；不能把空列表编码成“此人不存在”。

**实现细节**：先识别引号和转发片段的边界，再对各局部域应用词法规则；不能识别完整引用结构时降为unknown，不借机做多跳语义分析。“人家”的验收输出须明确留下对象unknown；为兼容原要求可含 reported_subject_id=null、report_status=unconfirmed，但不得据此宣称转述已成立。按source_ref定位否定词和候选谓词，别/不的范围与整个句子的真假分开。规则升级以 `(event_id,source_revision,rule_version)` 重建，不将不同版本累计成更多证据。

## R02.02 位置、所有权与现状映射

规范数据族：`cue_sets`。R03–R12对应十类typed store；其余是来源/运行/派生服务，不能再算额外心理记忆。

幂等键(event_id, source_revision, rule_version)；新规则重建派生，不能累计成多份独立证据。

当前可核候选为0.32.0-candidate及其局部源码，不等于D现场已具备该接口。内核既有memories(kind)+versions继续保留，目标分型表由显式迁移产生；本模块不能绕规范API直接改别类记录。详见DATA_STORES.md的表归属。

## R02.03 输入契约

已持久化event_id/source_revision，宿主提供发话者/收话人和引用域；原文UTF-8及可用局部映射；rule_version。

调用外层必有schema_version、request_id、可信principal/scope、operation、deadline/cancel；写入带expected_revision和支持幂等的operation_key。读取带filter/snapshot/cursor，不能将模型提供的actor/scope直接当认证。类型表中可空项显式null，未执行检查不得以空数组冒“确认没有”。

## R02.04 输出、回执与错误契约

CueSet：局部否定、转述线索、人称候选；可为[]，无事实写入权限。

统一返回{request_id,operation_id,module,disposition,object_refs,base_revision,committed_revision,coverage,gaps,receipt_ref,evidence_level}。对象引用含kind/id/revision，来源引用含source_id/source_revision/hash/range。纯读committed_revision=null；候选disposition=proposed，不能返回committed冒正式状态。

错误至少区分INVALID_ARGUMENT、FORBIDDEN/NOT_FOUND_OR_HIDDEN、CONFLICT、SOURCE_UNAVAILABLE、TIMEOUT、RESOURCE_EXHAUSTED、UNVERIFIED_BINDING、INTERNAL；有提交路径还要commit_outcome=not_committed/committed/unknown。未知结果先按原键查回执。

## R02.05 数据字段、状态与索引

| 字段组 | 类型 | 约束与语义 |
|---|---|---|
| event_id/source_revision | string/int | 必填；确切R01来源版本 |
| rule_version | string | 必填；词法规则冻结版本 |
| kind | enum | negation/reporting_cue/pronoun |
| span/start_byte/end_byte | range | 必须落在实际供给原文的UTF-8字符边界 |
| surface/local_context | string | 按原文切片；不改写句意 |
| attachment_candidates | array | 局部挂载对象与依据；可能为空 |
| referent_candidates | array | 仅可信发/收话人及本地已确认映射 |
| resolution | enum | resolved/ambiguous/unknown；不靠模型补人 |
| report_status/reported_subject_id | enum/nullable ID | 人家本身=unconfirmed/null；明确转述另存发话者/对象/内容 |

公共对象字段：id、kind、schema_version、scope、created_at、created_by、revision、status、record_digest；每项来源或实际宿主创建依据另存。组字段细分时必须列schema，不用不同拼法兼容猜测。

planned→encoded→validated；不合法range→rejected；来源变更→invalidated。unknown是合法编码结果，不是系统故障。

最低索引：scope+kind+有效状态+业务主键；来源反向依赖(source_id,source_revision)；对象版本(id,revision)。本模块特定检索维度由第11节给出。索引只定位，当前有效性仍核规范记录，不以索引命中当接受事实。

## R02.06 自动触发与完整处理顺序

1. 先核事件版本及授权，取本轮实际文本，不擅自抓别的会话。
2. 标引用结构和局部边界，不清楚的引用域保留unknown。
3. 按明确规则找不/别/没/不许；局部2–12字仅作候选窗口，短词可更短，超长标truncated。
4. 仅为明确他说/据说等形成转述线索；人家只产生人称候选与未知对象，不自动定转述成立。
5. 在本地域内生成候选；栖所她不自动等于用户；引用中的你不继承外层收话人。
6. 校回原文range；无标记返回[]；向R15/R07交候选而非事实。

宿主触发后逐阶段记started/succeeded/failed/skipped/unverified；不需要运行的步骤可skipped，但不能将缺必需依赖也算正常跳过。只读规划不改原始事件，模型调用不在数据库长锁内。

## R02.07 关键算法、决策与禁止捷径

使用可解释词法规则与有限局部结构；不仅/不错等非命题否定按词法规则排除或unknown。禁止意图推断、情绪抽取、topic归类、多跳指代。规则冲突保留多个局部候选，不强制选一。

每次推导均把直接观察、他人转述、候选解释、规范记录、外部结果分开。source_ref能定位仅证明原文存在；如涉及开放语义，必须由相应支持验证和反例测试决定是否可用，不能单靠hash/正则。算法参数只影响工程取舍，不授身份、权限或关系事实。

## R02.08 幂等、修订、并发与提交

幂等键(event_id, source_revision, rule_version)；新规则重建派生，不能累计成多份独立证据。

操作重试与新业务事件分开；相同操作键异实质请求必须冲突。读取允许新快照结果变化，不能为了固定输出使用已撤回缓存。规范状态修改用expected_revision；跨库步骤分别留回执与reconciliation_required，不以一库commit冒全局事务。D依赖实际输出的SelfState/八域仍须强run/attempt/scope绑定，不让本模块日志替代。

## R02.09 更正、失效、删除与反向依赖

凡`cue_sets`中有源派生物，登记source_root、source_revision、processor_version及依赖关系；纠正到来时先invalid_for_use/争议，后重建，不继续拿旧结论无提示作答。删除先由R18tombstone阻可用性，再清正文/索引/缓存/Wiki/备份策略；不能仅删引文保留相同推断。

无人物/心理职责的运行对象只记录必要状态，不因本模块失败写用户生气或D疏远。已发生事件和已表达的当时状态不被后来解释覆写；隐私擦除走专用治理路径。

## R02.10 模块扣接与交接责任

| 方向 | 对接对象 | 必须交接的内容 |
|---|---|---|
| 输入 | R01 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R18 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输出 | R03 | CueEncoder结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R07 | CueEncoder结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R15 | CueEncoder结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R23 | CueEncoder结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |

交接由HostAdapter/Coordinator调用，不让两个模块彼此递归无限互调。每个edge均记录当前事件/源版本、调用目的、预算、取消与真实回执；完整schema和时序见LINKAGE.md。接收失败保待处理/限制，不能发送空结果伪装成功。

## R02.11 如何存、如何召回、如何区分其他记忆

只提供本轮线索；旧CueSet可按事件/规则版本查，不成为新经历。不以否定词相似度直接召回某个人。

受权路线只查询声明的kind及其规范业务表；不能把情绪解释当语义事实、反思当亲历、工具尝试当结果。共享来源可同时支持多个kind，但每条命题有独立语义和审核状态；同源同命题折叠，不合并同源不同要求。必要后续沿依赖图取回，超过budget标partial。

## R02.12 注入的进入、最短表示与退出

通常不单独注入整份CueSet；R22仅在歧义会影响当前回答时保留必要未知/局部解释。情绪线索由现有情绪召回或独立评价器承担。

当材料进入R22候选，每条必须能说明当前anchor、need_reason、新增信息和support_verdict。已在真实messages充分表达则不重注；换窗缺了则可重供。话题切换、完成、失效、撤回或无本轮用途就退出动态块，规范记忆保留。zero injection不关闭宿主最低检查，故障也不能伪装none_needed。

## R02.13 后台、恢复、超时与取消

本模块相关后台作业以scope+源版本+operation+schema/processor版本幂等，经R17持久队列领取。对于纯读路径，只保存必要阅读/覆盖进度，不声称有待提交事实。恢复时读最新删除、授权、规范状态及cue_sets版本，再决定重算/继续/放弃。

失约worker写回须被fencing拒绝；模型调用超时发取消，底层不能证实停止就记cancel_unconfirmed，迟到结果不能自动commit。外部动作的unknown由R14先对账。未部署后台或钩子则标missing，不能称离线持续执行。

## R02.14 资源、隐私与降级规则

与R24共享每run/job预算，不为R02另开无界模型循环。前台最低检查、输入入账、必要纠正/边界和输出预留优先；可选语义、图展开、后台整理可暂停。所有查询与补读都有limit/deadline/stop_reason；候选上限不是注入配额。

故障使用第4节错误和coverage，普通交流尽量继续，依赖缺失的动作限制。密钥/原始私聊不进普通日志；被拒scope不出现在公开解释中。资源阈值不是情绪好感阈值，未实测目标机器不报固定延迟/容量保证。

## R02.15 贯通例子与反例

输入“我不走……别赶我啦”：抽不走/别赶及局部挂载；不能变成“她不来单位”。“人家自我介绍得很清楚啊”：对象unknown，不能咱们。

验证时把该场景与原事件、已有记录、真实请求或结果链同时保存：输入→CueEncoder→下游回执。仅看到本模块返回JSON不证明生成模型采用，也不证明真实动作完成。正确处理应保留未知、合法来源和以后修订入口；能说出漂亮话不替代字段/版本/来源正确。

## R02.16 36项模块与协议验收需求目录（非执行fixture）

| ID | 准备/触发 | 必须结果；不满足即失败 | 当前状态 |
|---|---|---|---|
| R02-T01 | 在隔离fixture中构造：我不走/别赶可精确回指原文；任何改成第三人称单位事实判失败 | 我不走/别赶可精确回指原文；任何改成第三人称单位事实判失败 | not_run |
| R02-T02 | 在隔离fixture中构造：人家对象unknown且report_status不硬判转述；填咱们判失败 | 人家对象unknown且report_status不硬判转述；填咱们判失败 | not_run |
| R02-T03 | 在隔离fixture中构造：天气晴朗输出空数组；添加意图/情绪/topic判失败 | 天气晴朗输出空数组；添加意图/情绪/topic判失败 | not_run |
| R02-T04 | 在隔离fixture中构造：栖所你按本地域可信映射；引用内你不沿用外层 | 栖所你按本地域可信映射；引用内你不沿用外层 | not_run |
| R02-T05 | 在隔离fixture中构造：她缺映射时空候选；以性别/昵称猜用户判失败 | 她缺映射时空候选；以性别/昵称猜用户判失败 | not_run |
| R02-T06 | 在隔离fixture中构造：不仅/不错不机械形成否定事实 | 不仅/不错不机械形成否定事实 | not_run |
| R02-T07 | 在隔离fixture中构造：多字节emoji前后range能切回相同surface | 多字节emoji前后range能切回相同surface | not_run |
| R02-T08 | 在隔离fixture中构造：规则版本变更重建，不重复强化来源 | 规则版本变更重建，不重复强化来源 | not_run |
| R02-T09 | 在隔离fixture中构造：超长否定标候选截断而非完整句法 | 超长否定标候选截断而非完整句法 | not_run |
| R02-T10 | 在隔离fixture中构造：明确他说保留发话者/谈及对象/内容不同字段 | 明确他说保留发话者/谈及对象/内容不同字段 | not_run |
| R02-T11 | 在隔离fixture中构造：跨句多跳指代请求保持职责边界，不偷偷解析 | 跨句多跳指代请求保持职责边界，不偷偷解析 | not_run |
| R02-T12 | 在隔离fixture中构造：原文被删除后CueSet停用，不靠旧缓存复活 | 原文被删除后CueSet停用，不靠旧缓存复活 | not_run |
| R02-T13 | 另建scope-B对象并以scope-A主体访问 | 拒绝相应资料/写入，公开响应不含B存在性；当前合法对象不变 | not_run |
| R02-T14 | 从本模块字段表逐组移除必需输入 | INVALID_ARGUMENT及字段路径；不得补造主体、项目或事实 | not_run |
| R02-T15 | 使用未支持schema/profile及实质未知字段 | 拒绝或显式unsupported；不静默删字段骗校验 | not_run |
| R02-T16 | 同源版本/操作键提交两遍 | 按本节幂等规则处理，副作用/独立证据不重复；纯读可以重查并保快照差别 | not_run |
| R02-T17 | 两调用携同expected_revision更新同对象 | 持久写至多一方按原前态成功，另一方冲突/受控重读；纯读不得写事实 | not_run |
| R02-T18 | 准备后提交/供给前对来源加tombstone | 相关派生停用或拒提交，旧缓存不复活；无来源型运行记录核相应取消/策略 | not_run |
| R02-T19 | 阶段处理中提交相关来源新版本 | 旧版本不能覆盖最新纠正；重算/partial/失效原因可查 | not_run |
| R02-T20 | 将一个必须依赖返回unavailable | 保具体缺口；不把失败当正常空结果或全部完成 | not_run |
| R02-T21 | 在本模块关键算法/调用处返回错误 | 错误回传，阶段failed/unknown；没有可用结论就不伪报成功 | not_run |
| R02-T22 | 故意令本模块外部阶段超过deadline | 取消按能力记录，迟到结果不绕版本与取消检查；真实停止未知照实 | not_run |
| R02-T23 | 准备完成后、提交/供给前取消run或job | 未发生副作用不再执行；已发生事实不抹除，结果另记 | not_run |
| R02-T24 | 租约失效后旧worker尝试写回 | 有持久写的路径由fencing/CAS拒绝；只读路径不借续读取得写权 | not_run |
| R02-T25 | 对持久写路径在关联对象写入间注入异常 | 本库事务全有或全无；跨库显示中间态并可对账；只读不虚称事务验收 | not_run |
| R02-T26 | 在commit后/返回前断开响应 | 按原键查询回执，不盲新建意图；只读重试不得假定语料未变化 | not_run |
| R02-T27 | 相关outbox成功处理但ACK丢失再投递 | 按源/处理器版本幂等，不产生第二次认知强化或外部动作 | not_run |
| R02-T28 | 规范对象已修订而索引未追平 | 报告水位并查规范store或partial；不能将旧命中当最新事实 | not_run |
| R02-T29 | 样本含emoji、不是/仅在/可能等限定 | 源范围和原意保留；截断不得变反义；非文本对象用其真实坐标 | not_run |
| R02-T30 | 加入同名不同ID与未定指代候选 | 保持候选/unknown，不自动合并；无人物职责模块不自创人物推断 | not_run |
| R02-T31 | 旧/新有效期及接收顺序不一致 | 按真实时间/版本契约处理；无法比较时不擅选最后接收值 | not_run |
| R02-T32 | 同材料被旧插件与当前出口同时提出 | 只有R22可最终装配，去本宿主拥有旧块而保用户/系统/工具结构 | not_run |
| R02-T33 | 提供本地保存/尝试但无业务或送达回执 | 不得升级成已理解/已完成/已送达；按该模块实际成果层级标注 | not_run |
| R02-T34 | 恢复相同逻辑初态重跑，同配置与fixture hash | 可复现本模块约定结果；时间/随机ID差异不混成语义提升 | not_run |
| R02-T35 | 输入含私密正文/凭据状外部内容 | 普通日志与索引/投影不泄漏禁止范围；审计仅留必要ID和固定原因 | not_run |
| R02-T36 | 只有文档、模拟对象或模型自评时要求标通过 | 保design/static/synthetic/real_host分轴；缺真实证据标not_run/unknown | not_run |

T01–T12是该模块专属语义/业务场景；T13–T36是必须绑定本模块实际写读路径执行的协议/故障场景，不能空跑通用脚本就全标通过。先从字段表构造合法基准fixture，再只改变本例条件；对不适用的写路径要给可审证据说明与对应只读判据，不能把未测记成pass。

## R02.17 交付证据、通过门槛与未完成项

交付CueEncoder实现/schema迁移、输入输出fixture、合法及反例来源、实际存储与调用回执、真实入口覆盖、查询及注入观察、失败恢复报告。证据等级design/static/synthetic_process/real_host/storage_fault/production分开。

模块通过至少需要专属场景和适用协议场景的实际证据；整套通过还需LINKAGE.md跨模块链。当前文档生成/类型DDL检查不算本模块36例已跑。已有候选仅作为迁移基础，现场未知和未实现开放语义仍未验。

## R02.18 实现次序、兼容策略与设计自审

先固定本模块字段/状态/真源→实现受权最小路径与回执→跑专属正反例→接入上游/下游→做恢复/删除/冲突→在真实隔离宿主检查请求或结果。本模块不得以优化名义删除保留矩阵中已有功能，不改C032严格profile顶层来绕验证。

本次设计检查关注：只提供本轮线索；旧CueSet可按事件/规则版本查，不成为新经历。不以否定词相似度直接召回某个人。 通常不单独注入整份CueSet；R22仅在歧义会影响当前回答时保留必要未知/局部解释。情绪线索由现有情绪召回或独立评价器承担。 对所有结果都分别标明对象、版本、来源、局限和验证等级；不以同一success覆盖入账、理解、注入、生成、送达与执行。生产边界不变，不随文档生成而开通部署。



---

# R03　工作记忆与承诺：详细设计与验收规格

版本：everlight/6-design；模块契约：r03/1；日期：2026-11-08。本文为设计，全部功能验收初始not_run。最终裁决以FINAL_DECISIONS.md和MODULE_DECISIONS.md为准。与contracts/共同生效，不是已安装服务。

## R03.01 定义、边界与可证伪成功标准

有版本WorkView、待办与具体承诺、焦点候选；不输出外部动作成功。

唯一业务责任服务是`WorkStore`。输入必须满足第3节，输出必须满足第4节及GLOBAL_PROTOCOL。成功必须可从实际记录/回执读回，而不是模型自称完成。

原有具体机制及边界（保留并由本版细化）：

**原理与基础**：工作记忆保存正在做什么，不是全历史摘要。C032 有 session焦点；独立workspace原型有环境/项目/任务分区、版本历史，但无可信ACL且未接C032。

**数据**：`Work {environment_id, project_id, task_id, goal, constraints[], decisions[], artifacts[], next_step?, state, evidence_refs[], revision}`；状态 planned/active/blocked/paused/completed/cancelled。完成需合适结果依据，用户撤销和技术失败分开。

**自动步骤**：①由宿主的显式项目选择或可信映射定位范围；②无映射则暂挂候选；③读最近目标、产物版本、待办与未知动作；④本轮提出受来源支持的更新；⑤保存版本，任务完成核R14/R12证据；⑥切换保存旧焦点并激活新焦点。不得由同名项目字符串授予范围。

**必须扣住**：R13恢复当前焦点，R12验证文件，R14验证结果，R15查询决定与经历；R18管范围、R19管并发。R03只需要当前工作集，不承接所有长历史。

**例子/反例**：A长明→B栖所→A，恢复A的待办“补例子”与其文件版本，不能带入B的页面进度。用户说“这个做完了”但“这个”指代不清时记录待确认，不能把全部任务完成。

**写入归属与状态**：WorkStore 拥有任务事实；每轮context只是其投影。任务拆为Goal、Decision、OpenThread、ArtifactRef、Commitment，分别有ID与revision。决策可以 superseded，待办可以 cancelled，不能仅以task摘要的一句“完成”批量关闭全部子项。对模糊的“继续”先恢复唯一可信焦点；存在多个同等有效焦点则只恢复候选。

**实现细节**：按 `(scope,project_id,state,updated_at)` 查工作集；当前focus指向ID而非复制整套任务。未明确指定的期限为null，不把“尽快”偷偷换成某个日期。每次完成核对事先定义的acceptance及产物/回执；对“已写文件但未发给用户”，可分别记录artifact_ready与delivery_unknown。R13保存ID和版本，恢复时读最新状态，避免快照把已取消任务重新激活。

## R03.02 位置、所有权与现状映射

规范数据族：`working_memory`。R03–R12对应十类typed store；其余是来源/运行/派生服务，不能再算额外心理记忆。

单对象expected_revision；并发任务更新须字段/子项版本合并或冲突返回，不能摘要后写覆盖新决定。

当前可核候选为0.32.0-candidate及其局部源码，不等于D现场已具备该接口。内核既有memories(kind)+versions继续保留，目标分型表由显式迁移产生；本模块不能绕规范API直接改别类记录。详见DATA_STORES.md的表归属。

## R03.03 输入契约

可信project/task映射，当前已保存事件，相关已有Work/Commitment版本，产物与行动回执。

调用外层必有schema_version、request_id、可信principal/scope、operation、deadline/cancel；写入带expected_revision和支持幂等的operation_key。读取带filter/snapshot/cursor，不能将模型提供的actor/scope直接当认证。类型表中可空项显式null，未执行检查不得以空数组冒“确认没有”。

## R03.04 输出、回执与错误契约

有版本WorkView、待办与具体承诺、焦点候选；不输出外部动作成功。

统一返回{request_id,operation_id,module,disposition,object_refs,base_revision,committed_revision,coverage,gaps,receipt_ref,evidence_level}。对象引用含kind/id/revision，来源引用含source_id/source_revision/hash/range。纯读committed_revision=null；候选disposition=proposed，不能返回committed冒正式状态。

错误至少区分INVALID_ARGUMENT、FORBIDDEN/NOT_FOUND_OR_HIDDEN、CONFLICT、SOURCE_UNAVAILABLE、TIMEOUT、RESOURCE_EXHAUSTED、UNVERIFIED_BINDING、INTERNAL；有提交路径还要commit_outcome=not_committed/committed/unknown。未知结果先按原键查回执。

## R03.05 数据字段、状态与索引

| 字段组 | 类型 | 约束与语义 |
|---|---|---|
| work_id/project_id/task_id | ID | 项目可空，task只在可信范围解析 |
| goal | string | 当前目标与来源 |
| constraints/decisions | array | 每条有ID、来源、适用范围与状态 |
| open_threads | array | 未结问题及其缺口，不等于永久注入 |
| commitments | array | 承诺者、受益对象、内容、期限可空、验收标准 |
| artifacts | array | document_id+revision/hash，ready与delivered分开 |
| next_step | nullable string | 需要明确依据，不能补造用户目标 |
| state | enum | planned/active/blocked/paused/completed/cancelled |

公共对象字段：id、kind、schema_version、scope、created_at、created_by、revision、status、record_digest；每项来源或实际宿主创建依据另存。组字段细分时必须列schema，不用不同拼法兼容猜测。

planned→active；active可blocked/paused；有验收结果才completed；取消保留历史。完成后新任务创建新ID，不把旧任务改名复用。

最低索引：scope+kind+有效状态+业务主键；来源反向依赖(source_id,source_revision)；对象版本(id,revision)。本模块特定检索维度由第11节给出。索引只定位，当前有效性仍核规范记录，不以索引命中当接受事实。

## R03.06 自动触发与完整处理顺序

1. 认证项目/任务范围并读最新revision，模糊指代只留候选。
2. 分离目标、决策、承诺和产物，不用一段滚动摘要代替全部。
3. 明确纠正先进入约束视图，旧相反要求停用/争议。
4. 生成更新候选，任务拆分形成父子关系但保留原验收。
5. 完成需核R12产物及R14结果；未送达不说已交付。
6. CAS提交，保存焦点指针和对应outbox，触发R13及索引更新。

宿主触发后逐阶段记started/succeeded/failed/skipped/unverified；不需要运行的步骤可skipped，但不能将缺必需依赖也算正常跳过。只读规划不改原始事件，模型调用不在数据库长锁内。

## R03.07 关键算法、决策与禁止捷径

焦点优先级：显式受权项目选择→唯一可信活跃焦点→当前输入与已有任务可核对应。多候选无足够证据不按最近文本硬选。“尽快”不自动换成日期；愿望不自动变承诺。

每次推导均把直接观察、他人转述、候选解释、规范记录、外部结果分开。source_ref能定位仅证明原文存在；如涉及开放语义，必须由相应支持验证和反例测试决定是否可用，不能单靠hash/正则。算法参数只影响工程取舍，不授身份、权限或关系事实。

## R03.08 幂等、修订、并发与提交

单对象expected_revision；并发任务更新须字段/子项版本合并或冲突返回，不能摘要后写覆盖新决定。

操作重试与新业务事件分开；相同操作键异实质请求必须冲突。读取允许新快照结果变化，不能为了固定输出使用已撤回缓存。规范状态修改用expected_revision；跨库步骤分别留回执与reconciliation_required，不以一库commit冒全局事务。D依赖实际输出的SelfState/八域仍须强run/attempt/scope绑定，不让本模块日志替代。

## R03.09 更正、失效、删除与反向依赖

凡`working_memory`中有源派生物，登记source_root、source_revision、processor_version及依赖关系；纠正到来时先invalid_for_use/争议，后重建，不继续拿旧结论无提示作答。删除先由R18tombstone阻可用性，再清正文/索引/缓存/Wiki/备份策略；不能仅删引文保留相同推断。

无人物/心理职责的运行对象只记录必要状态，不因本模块失败写用户生气或D疏远。已发生事件和已表达的当时状态不被后来解释覆写；隐私擦除走专用治理路径。

## R03.10 模块扣接与交接责任

| 方向 | 对接对象 | 必须交接的内容 |
|---|---|---|
| 输入 | R01 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R09 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R12 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R14 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R18 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输出 | R13 | WorkStore结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R15 | WorkStore结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R17 | WorkStore结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R22 | WorkStore结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |

交接由HostAdapter/Coordinator调用，不让两个模块彼此递归无限互调。每个edge均记录当前事件/源版本、调用目的、预算、取消与真实回执；完整schema和时序见LINKAGE.md。接收失败保待处理/限制，不能发送空结果伪装成功。

## R03.11 如何存、如何召回、如何区分其他记忆

按项目+task/state+更新时间查；查当前也读后续完成/取消。不把工作条目与永久个人偏好混库。

受权路线只查询声明的kind及其规范业务表；不能把情绪解释当语义事实、反思当亲历、工具尝试当结果。共享来源可同时支持多个kind，但每条命题有独立语义和审核状态；同源同命题折叠，不合并同源不同要求。必要后续沿依赖图取回，超过budget标partial。

## R03.12 注入的进入、最短表示与退出

只有当前问题依赖进度/承诺才注入目标、最近决定、下一步、unknown结果；已在实际messages清楚表达时不再复制。

当材料进入R22候选，每条必须能说明当前anchor、need_reason、新增信息和support_verdict。已在真实messages充分表达则不重注；换窗缺了则可重供。话题切换、完成、失效、撤回或无本轮用途就退出动态块，规范记忆保留。zero injection不关闭宿主最低检查，故障也不能伪装none_needed。

## R03.13 后台、恢复、超时与取消

本模块相关后台作业以scope+源版本+operation+schema/processor版本幂等，经R17持久队列领取。对于纯读路径，只保存必要阅读/覆盖进度，不声称有待提交事实。恢复时读最新删除、授权、规范状态及working_memory版本，再决定重算/继续/放弃。

失约worker写回须被fencing拒绝；模型调用超时发取消，底层不能证实停止就记cancel_unconfirmed，迟到结果不能自动commit。外部动作的unknown由R14先对账。未部署后台或钩子则标missing，不能称离线持续执行。

## R03.14 资源、隐私与降级规则

与R24共享每run/job预算，不为R03另开无界模型循环。前台最低检查、输入入账、必要纠正/边界和输出预留优先；可选语义、图展开、后台整理可暂停。所有查询与补读都有limit/deadline/stop_reason；候选上限不是注入配额。

故障使用第4节错误和coverage，普通交流尽量继续，依赖缺失的动作限制。密钥/原始私聊不进普通日志；被拒scope不出现在公开解释中。资源阈值不是情绪好感阈值，未实测目标机器不报固定延迟/容量保证。

## R03.15 贯通例子与反例

A长明→B栖所→A：恢复A文件版本及待补项，不带B设计进度。文件已写但发送unknown，分别报告。

验证时把该场景与原事件、已有记录、真实请求或结果链同时保存：输入→WorkStore→下游回执。仅看到本模块返回JSON不证明生成模型采用，也不证明真实动作完成。正确处理应保留未知、合法来源和以后修订入口；能说出漂亮话不替代字段/版本/来源正确。

## R03.16 36项模块与协议验收需求目录（非执行fixture）

| ID | 准备/触发 | 必须结果；不满足即失败 | 当前状态 |
|---|---|---|---|
| R03-T01 | 在隔离fixture中构造：A/B/A恢复正确项目下一步 | A/B/A恢复正确项目下一步 | not_run |
| R03-T02 | 在隔离fixture中构造：两个同名任务不合并 | 两个同名任务不合并 | not_run |
| R03-T03 | 在隔离fixture中构造：这个做完了指代不明不批量完成 | 这个做完了指代不明不批量完成 | not_run |
| R03-T04 | 在隔离fixture中构造：文件ready但delivery未知不当交付完成 | 文件ready但delivery未知不当交付完成 | not_run |
| R03-T05 | 在隔离fixture中构造：尽快保留模糊期限，不自动排明天 | 尽快保留模糊期限，不自动排明天 | not_run |
| R03-T06 | 在隔离fixture中构造：用户改保留颜色，旧后台不能覆盖 | 用户改保留颜色，旧后台不能覆盖 | not_run |
| R03-T07 | 在隔离fixture中构造：取消任务不被旧checkpoint复活 | 取消任务不被旧checkpoint复活 | not_run |
| R03-T08 | 在隔离fixture中构造：愿望/建议/承诺分开 | 愿望/建议/承诺分开 | not_run |
| R03-T09 | 在隔离fixture中构造：部分子项完成不关闭所有子任务 | 部分子项完成不关闭所有子任务 | not_run |
| R03-T10 | 在隔离fixture中构造：项目权限撤回后焦点不再供给 | 项目权限撤回后焦点不再供给 | not_run |
| R03-T11 | 在隔离fixture中构造：模糊继续可候选澄清，不自造任务 | 模糊继续可候选澄清，不自造任务 | not_run |
| R03-T12 | 在隔离fixture中构造：当前话题无关不注入未结总表 | 当前话题无关不注入未结总表 | not_run |
| R03-T13 | 另建scope-B对象并以scope-A主体访问 | 拒绝相应资料/写入，公开响应不含B存在性；当前合法对象不变 | not_run |
| R03-T14 | 从本模块字段表逐组移除必需输入 | INVALID_ARGUMENT及字段路径；不得补造主体、项目或事实 | not_run |
| R03-T15 | 使用未支持schema/profile及实质未知字段 | 拒绝或显式unsupported；不静默删字段骗校验 | not_run |
| R03-T16 | 同源版本/操作键提交两遍 | 按本节幂等规则处理，副作用/独立证据不重复；纯读可以重查并保快照差别 | not_run |
| R03-T17 | 两调用携同expected_revision更新同对象 | 持久写至多一方按原前态成功，另一方冲突/受控重读；纯读不得写事实 | not_run |
| R03-T18 | 准备后提交/供给前对来源加tombstone | 相关派生停用或拒提交，旧缓存不复活；无来源型运行记录核相应取消/策略 | not_run |
| R03-T19 | 阶段处理中提交相关来源新版本 | 旧版本不能覆盖最新纠正；重算/partial/失效原因可查 | not_run |
| R03-T20 | 将一个必须依赖返回unavailable | 保具体缺口；不把失败当正常空结果或全部完成 | not_run |
| R03-T21 | 在本模块关键算法/调用处返回错误 | 错误回传，阶段failed/unknown；没有可用结论就不伪报成功 | not_run |
| R03-T22 | 故意令本模块外部阶段超过deadline | 取消按能力记录，迟到结果不绕版本与取消检查；真实停止未知照实 | not_run |
| R03-T23 | 准备完成后、提交/供给前取消run或job | 未发生副作用不再执行；已发生事实不抹除，结果另记 | not_run |
| R03-T24 | 租约失效后旧worker尝试写回 | 有持久写的路径由fencing/CAS拒绝；只读路径不借续读取得写权 | not_run |
| R03-T25 | 对持久写路径在关联对象写入间注入异常 | 本库事务全有或全无；跨库显示中间态并可对账；只读不虚称事务验收 | not_run |
| R03-T26 | 在commit后/返回前断开响应 | 按原键查询回执，不盲新建意图；只读重试不得假定语料未变化 | not_run |
| R03-T27 | 相关outbox成功处理但ACK丢失再投递 | 按源/处理器版本幂等，不产生第二次认知强化或外部动作 | not_run |
| R03-T28 | 规范对象已修订而索引未追平 | 报告水位并查规范store或partial；不能将旧命中当最新事实 | not_run |
| R03-T29 | 样本含emoji、不是/仅在/可能等限定 | 源范围和原意保留；截断不得变反义；非文本对象用其真实坐标 | not_run |
| R03-T30 | 加入同名不同ID与未定指代候选 | 保持候选/unknown，不自动合并；无人物职责模块不自创人物推断 | not_run |
| R03-T31 | 旧/新有效期及接收顺序不一致 | 按真实时间/版本契约处理；无法比较时不擅选最后接收值 | not_run |
| R03-T32 | 同材料被旧插件与当前出口同时提出 | 只有R22可最终装配，去本宿主拥有旧块而保用户/系统/工具结构 | not_run |
| R03-T33 | 提供本地保存/尝试但无业务或送达回执 | 不得升级成已理解/已完成/已送达；按该模块实际成果层级标注 | not_run |
| R03-T34 | 恢复相同逻辑初态重跑，同配置与fixture hash | 可复现本模块约定结果；时间/随机ID差异不混成语义提升 | not_run |
| R03-T35 | 输入含私密正文/凭据状外部内容 | 普通日志与索引/投影不泄漏禁止范围；审计仅留必要ID和固定原因 | not_run |
| R03-T36 | 只有文档、模拟对象或模型自评时要求标通过 | 保design/static/synthetic/real_host分轴；缺真实证据标not_run/unknown | not_run |

T01–T12是该模块专属语义/业务场景；T13–T36是必须绑定本模块实际写读路径执行的协议/故障场景，不能空跑通用脚本就全标通过。先从字段表构造合法基准fixture，再只改变本例条件；对不适用的写路径要给可审证据说明与对应只读判据，不能把未测记成pass。

## R03.17 交付证据、通过门槛与未完成项

交付WorkStore实现/schema迁移、输入输出fixture、合法及反例来源、实际存储与调用回执、真实入口覆盖、查询及注入观察、失败恢复报告。证据等级design/static/synthetic_process/real_host/storage_fault/production分开。

模块通过至少需要专属场景和适用协议场景的实际证据；整套通过还需LINKAGE.md跨模块链。当前文档生成/类型DDL检查不算本模块36例已跑。已有候选仅作为迁移基础，现场未知和未实现开放语义仍未验。

## R03.18 实现次序、兼容策略与设计自审

先固定本模块字段/状态/真源→实现受权最小路径与回执→跑专属正反例→接入上游/下游→做恢复/删除/冲突→在真实隔离宿主检查请求或结果。本模块不得以优化名义删除保留矩阵中已有功能，不改C032严格profile顶层来绕验证。

本次设计检查关注：按项目+task/state+更新时间查；查当前也读后续完成/取消。不把工作条目与永久个人偏好混库。 只有当前问题依赖进度/承诺才注入目标、最近决定、下一步、unknown结果；已在实际messages清楚表达时不再复制。 对所有结果都分别标明对象、版本、来源、局限和验证等级；不以同一success覆盖入账、理解、注入、生成、送达与执行。生产边界不变，不随文档生成而开通部署。



---

# R04　情景记忆：详细设计与验收规格

版本：everlight/6-design；模块契约：r04/1；日期：2026-11-08。本文为设计，全部功能验收初始not_run。最终裁决以FINAL_DECISIONS.md和MODULE_DECISIONS.md为准。与contracts/共同生效，不是已安装服务。

## R04.01 定义、边界与可证伪成功标准

有序或偏序Episode、逐项摘要引用、后续链接和completeness。

唯一业务责任服务是`EpisodeStore`。输入必须满足第3节，输出必须满足第4节及GLOBAL_PROTOCOL。成功必须可从实际记录/回执读回，而不是模型自称完成。

原有具体机制及边界（保留并由本版细化）：

**原理与基础**：具体经历保留人物、时间、过程和后续，摘要只是入口。候选有事件来源与游标，完整跨渠道和邻接扩读待验。

**数据**：Episode含参与者候选、event_ids有序列表、发生区间及精度、场景、原文范围、summary_ref、后续事件链接、completeness和版本。场景/参与者可以未知；顺序以已知来源序列与发生时间分别记录，不将乱序接收误当真实先后。

**步骤**：①相关事件产生episode候选；②按话题上下文和可信参与者分段，允许暂未分段；③摘要逐条带原文定位；④新解释/修复/结果链接后续，不改原事件；⑤召回命中后自动取必要邻接，超过预算标部分；⑥相似经历保持不同ID再建立有关联而非合并。

**必须扣住**：R01提供事件；R07人物消歧；R08记录当时表达；R11后来理解；R15/R16找回并读证据；R13保留当前未结经历指针。

**例子/反例**：两次海边聊天，一次讨论搬家一次讨论海报；“上次在海边的决定”需要日期/主题确认，不能把第一次的参与者与第二次的结论拼在一起。缺了一段原文就显示缺口，不能用生成桥段填空。

**写入归属与状态**：EpisodeBuilder拥有经历聚合，R01仍拥有原文。Episode可为assembling/open/closed/incomplete；closed表示这段聚合暂告结束，不表示关系问题已解决。迟到事件可补链接或建立新版本，不按接收顺序重写实际发生顺序。没有可靠发生时间时保留partial_order及不确定区间。

**实现细节**：Participant表是episode_id与person_id候选的联结，角色、证据和视角单列；同一次群聊不代表每人都看到所有私聊。SummaryItem逐项指向支持范围，而非整个摘要只有一个笼统引用。把后续纠正、结果、澄清记为followup边；检索旧事件时R15查询这些边，R16核原文，不能只返回当时最强烈的一段。支持按人物、项目、地点线索和时间范围联合过滤。

## R04.02 位置、所有权与现状映射

规范数据族：`episodic_memory`。R03–R12对应十类typed store；其余是来源/运行/派生服务，不能再算额外心理记忆。

episode expected_revision；事件归属修改是新版本；摘要处理器版本与source_roots入依赖图。

当前可核候选为0.32.0-candidate及其局部源码，不等于D现场已具备该接口。内核既有memories(kind)+versions继续保留，目标分型表由显式迁移产生；本模块不能绕规范API直接改别类记录。详见DATA_STORES.md的表归属。

## R04.03 输入契约

R01事件与完整度，参与者候选、发生时间/偏序，相关前后片段及后续来源。

调用外层必有schema_version、request_id、可信principal/scope、operation、deadline/cancel；写入带expected_revision和支持幂等的operation_key。读取带filter/snapshot/cursor，不能将模型提供的actor/scope直接当认证。类型表中可空项显式null，未执行检查不得以空数组冒“确认没有”。

## R04.04 输出、回执与错误契约

有序或偏序Episode、逐项摘要引用、后续链接和completeness。

统一返回{request_id,operation_id,module,disposition,object_refs,base_revision,committed_revision,coverage,gaps,receipt_ref,evidence_level}。对象引用含kind/id/revision，来源引用含source_id/source_revision/hash/range。纯读committed_revision=null；候选disposition=proposed，不能返回committed冒正式状态。

错误至少区分INVALID_ARGUMENT、FORBIDDEN/NOT_FOUND_OR_HIDDEN、CONFLICT、SOURCE_UNAVAILABLE、TIMEOUT、RESOURCE_EXHAUSTED、UNVERIFIED_BINDING、INTERNAL；有提交路径还要commit_outcome=not_committed/committed/unknown。未知结果先按原键查回执。

## R04.05 数据字段、状态与索引

| 字段组 | 类型 | 约束与语义 |
|---|---|---|
| episode_id | ID | 经历稳定ID |
| event_refs | array | 有版本来源及已知顺序；不可只存摘要 |
| participants | array | 人物候选、角色、知情范围及依据 |
| time_interval/precision | object | 发生区间可未知，与接收序分开 |
| scene_refs | array | 地点/项目等有来源线索，可空 |
| summary_items | array | 每个命题有源范围 |
| followups | array | 澄清、纠正、结果及修复链接 |
| state/completeness | enum/object | assembling/open/closed/incomplete；closed非问题解决 |

公共对象字段：id、kind、schema_version、scope、created_at、created_by、revision、status、record_digest；每项来源或实际宿主创建依据另存。组字段细分时必须列schema，不用不同拼法兼容猜测。

assembling→open/closed；缺事件标incomplete并保gap；新后续生成revision与链接，不覆写原事件。

最低索引：scope+kind+有效状态+业务主键；来源反向依赖(source_id,source_revision)；对象版本(id,revision)。本模块特定检索维度由第11节给出。索引只定位，当前有效性仍核规范记录，不以索引命中当接受事实。

## R04.06 自动触发与完整处理顺序

1. 核事件已保存、可读及范围，读取来源水位。
2. 用人物/项目/时间和内容结构提出聚合边界，边界不清暂不分段。
3. 原事件序列与发生偏序分别保存；迟到事件不偷换实际先后。
4. 逐摘要项核引用，未支持的桥接句拒绝。
5. 新澄清/结果链接旧经历，并使旧单面摘要待更新。
6. 保存Episode版本与依赖，检索命中时给R16必要扩读计划。

宿主触发后逐阶段记started/succeeded/failed/skipped/unverified；不需要运行的步骤可skipped，但不能将缺必需依赖也算正常跳过。只读规划不改原始事件，模型调用不在数据库长锁内。

## R04.07 关键算法、决策与禁止捷径

聚合只改变组织，不改变事件事实。相似地点/主题只建关联候选；不同参与者/时期的经历不能拼结局。每次返回旧经历时检索其有效followup/supersedes，并保留阅读缺口。

每次推导均把直接观察、他人转述、候选解释、规范记录、外部结果分开。source_ref能定位仅证明原文存在；如涉及开放语义，必须由相应支持验证和反例测试决定是否可用，不能单靠hash/正则。算法参数只影响工程取舍，不授身份、权限或关系事实。

## R04.08 幂等、修订、并发与提交

episode expected_revision；事件归属修改是新版本；摘要处理器版本与source_roots入依赖图。

操作重试与新业务事件分开；相同操作键异实质请求必须冲突。读取允许新快照结果变化，不能为了固定输出使用已撤回缓存。规范状态修改用expected_revision；跨库步骤分别留回执与reconciliation_required，不以一库commit冒全局事务。D依赖实际输出的SelfState/八域仍须强run/attempt/scope绑定，不让本模块日志替代。

## R04.09 更正、失效、删除与反向依赖

凡`episodic_memory`中有源派生物，登记source_root、source_revision、processor_version及依赖关系；纠正到来时先invalid_for_use/争议，后重建，不继续拿旧结论无提示作答。删除先由R18tombstone阻可用性，再清正文/索引/缓存/Wiki/备份策略；不能仅删引文保留相同推断。

无人物/心理职责的运行对象只记录必要状态，不因本模块失败写用户生气或D疏远。已发生事件和已表达的当时状态不被后来解释覆写；隐私擦除走专用治理路径。

## R04.10 模块扣接与交接责任

| 方向 | 对接对象 | 必须交接的内容 |
|---|---|---|
| 输入 | R01 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R07 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R12 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R16 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R18 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输出 | R08 | EpisodeStore结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R11 | EpisodeStore结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R13 | EpisodeStore结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R15 | EpisodeStore结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R17 | EpisodeStore结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |

交接由HostAdapter/Coordinator调用，不让两个模块彼此递归无限互调。每个edge均记录当前事件/源版本、调用目的、预算、取消与真实回执；完整schema和时序见LINKAGE.md。接收失败保待处理/限制，不能发送空结果伪装成功。

## R04.11 如何存、如何召回、如何区分其他记忆

参与者+时间+项目/地点多约束；返回经历入口及必要后续而非只选情绪最强片段。

受权路线只查询声明的kind及其规范业务表；不能把情绪解释当语义事实、反思当亲历、工具尝试当结果。共享来源可同时支持多个kind，但每条命题有独立语义和审核状态；同源同命题折叠，不合并同源不同要求。必要后续沿依赖图取回，超过budget标partial。

## R04.12 注入的进入、最短表示与退出

本轮需要具体往事时给最短准确经过及有关后来；问细节读原文。不得填补未提供的天气、衣着、动作。

当材料进入R22候选，每条必须能说明当前anchor、need_reason、新增信息和support_verdict。已在真实messages充分表达则不重注；换窗缺了则可重供。话题切换、完成、失效、撤回或无本轮用途就退出动态块，规范记忆保留。zero injection不关闭宿主最低检查，故障也不能伪装none_needed。

## R04.13 后台、恢复、超时与取消

本模块相关后台作业以scope+源版本+operation+schema/processor版本幂等，经R17持久队列领取。对于纯读路径，只保存必要阅读/覆盖进度，不声称有待提交事实。恢复时读最新删除、授权、规范状态及episodic_memory版本，再决定重算/继续/放弃。

失约worker写回须被fencing拒绝；模型调用超时发取消，底层不能证实停止就记cancel_unconfirmed，迟到结果不能自动commit。外部动作的unknown由R14先对账。未部署后台或钩子则标missing，不能称离线持续执行。

## R04.14 资源、隐私与降级规则

与R24共享每run/job预算，不为R04另开无界模型循环。前台最低检查、输入入账、必要纠正/边界和输出预留优先；可选语义、图展开、后台整理可暂停。所有查询与补读都有limit/deadline/stop_reason；候选上限不是注入配额。

故障使用第4节错误和coverage，普通交流尽量继续，依赖缺失的动作限制。密钥/原始私聊不进普通日志；被拒scope不出现在公开解释中。资源阈值不是情绪好感阈值，未实测目标机器不报固定延迟/容量保证。

## R04.15 贯通例子与反例

两次海边聊天分别讨论搬家与海报；问“海边的决定”不混参与者和结论，日期不明留两个候选。

验证时把该场景与原事件、已有记录、真实请求或结果链同时保存：输入→EpisodeStore→下游回执。仅看到本模块返回JSON不证明生成模型采用，也不证明真实动作完成。正确处理应保留未知、合法来源和以后修订入口；能说出漂亮话不替代字段/版本/来源正确。

## R04.16 36项模块与协议验收需求目录（非执行fixture）

| ID | 准备/触发 | 必须结果；不满足即失败 | 当前状态 |
|---|---|---|---|
| R04-T01 | 在隔离fixture中构造：两次海边经历不串结局 | 两次海边经历不串结局 | not_run |
| R04-T02 | 在隔离fixture中构造：原话及后续都能定位 | 原话及后续都能定位 | not_run |
| R04-T03 | 在隔离fixture中构造：缺中间片段标incomplete | 缺中间片段标incomplete | not_run |
| R04-T04 | 在隔离fixture中构造：乱序到达不改真实发生顺序 | 乱序到达不改真实发生顺序 | not_run |
| R04-T05 | 在隔离fixture中构造：群聊参与不等于知道全部私聊 | 群聊参与不等于知道全部私聊 | not_run |
| R04-T06 | 在隔离fixture中构造：摘要逐命题引用而非笼统一条源 | 摘要逐命题引用而非笼统一条源 | not_run |
| R04-T07 | 在隔离fixture中构造：编辑后保留旧原文和新版本解释 | 编辑后保留旧原文和新版本解释 | not_run |
| R04-T08 | 在隔离fixture中构造：后来澄清伴随旧争执召回 | 后来澄清伴随旧争执召回 | not_run |
| R04-T09 | 在隔离fixture中构造：长事件分页覆盖不冒全文 | 长事件分页覆盖不冒全文 | not_run |
| R04-T10 | 在隔离fixture中构造：相似文本不同来源不吞事件 | 相似文本不同来源不吞事件 | not_run |
| R04-T11 | 在隔离fixture中构造：closed不等于已原谅/任务完成 | closed不等于已原谅/任务完成 | not_run |
| R04-T12 | 在隔离fixture中构造：删除独立源使受影响摘要停用 | 删除独立源使受影响摘要停用 | not_run |
| R04-T13 | 另建scope-B对象并以scope-A主体访问 | 拒绝相应资料/写入，公开响应不含B存在性；当前合法对象不变 | not_run |
| R04-T14 | 从本模块字段表逐组移除必需输入 | INVALID_ARGUMENT及字段路径；不得补造主体、项目或事实 | not_run |
| R04-T15 | 使用未支持schema/profile及实质未知字段 | 拒绝或显式unsupported；不静默删字段骗校验 | not_run |
| R04-T16 | 同源版本/操作键提交两遍 | 按本节幂等规则处理，副作用/独立证据不重复；纯读可以重查并保快照差别 | not_run |
| R04-T17 | 两调用携同expected_revision更新同对象 | 持久写至多一方按原前态成功，另一方冲突/受控重读；纯读不得写事实 | not_run |
| R04-T18 | 准备后提交/供给前对来源加tombstone | 相关派生停用或拒提交，旧缓存不复活；无来源型运行记录核相应取消/策略 | not_run |
| R04-T19 | 阶段处理中提交相关来源新版本 | 旧版本不能覆盖最新纠正；重算/partial/失效原因可查 | not_run |
| R04-T20 | 将一个必须依赖返回unavailable | 保具体缺口；不把失败当正常空结果或全部完成 | not_run |
| R04-T21 | 在本模块关键算法/调用处返回错误 | 错误回传，阶段failed/unknown；没有可用结论就不伪报成功 | not_run |
| R04-T22 | 故意令本模块外部阶段超过deadline | 取消按能力记录，迟到结果不绕版本与取消检查；真实停止未知照实 | not_run |
| R04-T23 | 准备完成后、提交/供给前取消run或job | 未发生副作用不再执行；已发生事实不抹除，结果另记 | not_run |
| R04-T24 | 租约失效后旧worker尝试写回 | 有持久写的路径由fencing/CAS拒绝；只读路径不借续读取得写权 | not_run |
| R04-T25 | 对持久写路径在关联对象写入间注入异常 | 本库事务全有或全无；跨库显示中间态并可对账；只读不虚称事务验收 | not_run |
| R04-T26 | 在commit后/返回前断开响应 | 按原键查询回执，不盲新建意图；只读重试不得假定语料未变化 | not_run |
| R04-T27 | 相关outbox成功处理但ACK丢失再投递 | 按源/处理器版本幂等，不产生第二次认知强化或外部动作 | not_run |
| R04-T28 | 规范对象已修订而索引未追平 | 报告水位并查规范store或partial；不能将旧命中当最新事实 | not_run |
| R04-T29 | 样本含emoji、不是/仅在/可能等限定 | 源范围和原意保留；截断不得变反义；非文本对象用其真实坐标 | not_run |
| R04-T30 | 加入同名不同ID与未定指代候选 | 保持候选/unknown，不自动合并；无人物职责模块不自创人物推断 | not_run |
| R04-T31 | 旧/新有效期及接收顺序不一致 | 按真实时间/版本契约处理；无法比较时不擅选最后接收值 | not_run |
| R04-T32 | 同材料被旧插件与当前出口同时提出 | 只有R22可最终装配，去本宿主拥有旧块而保用户/系统/工具结构 | not_run |
| R04-T33 | 提供本地保存/尝试但无业务或送达回执 | 不得升级成已理解/已完成/已送达；按该模块实际成果层级标注 | not_run |
| R04-T34 | 恢复相同逻辑初态重跑，同配置与fixture hash | 可复现本模块约定结果；时间/随机ID差异不混成语义提升 | not_run |
| R04-T35 | 输入含私密正文/凭据状外部内容 | 普通日志与索引/投影不泄漏禁止范围；审计仅留必要ID和固定原因 | not_run |
| R04-T36 | 只有文档、模拟对象或模型自评时要求标通过 | 保design/static/synthetic/real_host分轴；缺真实证据标not_run/unknown | not_run |

T01–T12是该模块专属语义/业务场景；T13–T36是必须绑定本模块实际写读路径执行的协议/故障场景，不能空跑通用脚本就全标通过。先从字段表构造合法基准fixture，再只改变本例条件；对不适用的写路径要给可审证据说明与对应只读判据，不能把未测记成pass。

## R04.17 交付证据、通过门槛与未完成项

交付EpisodeStore实现/schema迁移、输入输出fixture、合法及反例来源、实际存储与调用回执、真实入口覆盖、查询及注入观察、失败恢复报告。证据等级design/static/synthetic_process/real_host/storage_fault/production分开。

模块通过至少需要专属场景和适用协议场景的实际证据；整套通过还需LINKAGE.md跨模块链。当前文档生成/类型DDL检查不算本模块36例已跑。已有候选仅作为迁移基础，现场未知和未实现开放语义仍未验。

## R04.18 实现次序、兼容策略与设计自审

先固定本模块字段/状态/真源→实现受权最小路径与回执→跑专属正反例→接入上游/下游→做恢复/删除/冲突→在真实隔离宿主检查请求或结果。本模块不得以优化名义删除保留矩阵中已有功能，不改C032严格profile顶层来绕验证。

本次设计检查关注：参与者+时间+项目/地点多约束；返回经历入口及必要后续而非只选情绪最强片段。 本轮需要具体往事时给最短准确经过及有关后来；问细节读原文。不得填补未提供的天气、衣着、动作。 对所有结果都分别标明对象、版本、来源、局限和验证等级；不以同一success覆盖入账、理解、注入、生成、送达与执行。生产边界不变，不随文档生成而开通部署。



---

# R05　语义记忆与更正：详细设计与验收规格

版本：everlight/6-design；模块契约：r05/1；日期：2026-11-08。本文为设计，全部功能验收初始not_run。最终裁决以FINAL_DECISIONS.md和MODULE_DECISIONS.md为准。与contracts/共同生效，不是已安装服务。

## R05.01 定义、边界与可证伪成功标准

版本化Claim、支持/补充/冲突/纠正判定、当前与历史视图。

唯一业务责任服务是`ClaimStore`。输入必须满足第3节，输出必须满足第4节及GLOBAL_PROTOCOL。成功必须可从实际记录/回执读回，而不是模型自称完成。

原有具体机制及边界（保留并由本版细化）：

**原理与基础**：事实/偏好可随时间变化，不能一律最新覆盖。候选retain/history/revise/conflicts有版本和来源原语，一般自然语言更新正确性未证明。

**数据**：Claim含主体、命题、对象或值、适用项目/场景、valid_from/to、recorded_at、evidence/counter_refs、review_status、前驱版本。`observed_statement`与`believed_fact`分开：某人说过不等于客观事实。

**步骤**：①从实际来源生成候选；②查同主体/同命题/相同适用范围旧版本；③可以支持、补充、更正、冲突或无关；④更正与冲突有原文和理由，未确认不强行结案；⑤当前查询用适用时间，问过去保留旧状态；⑥更新派生索引和反证链接。

**必须扣住**：R04提供情境，R11提供待审理解不能直接当事实，R09身份高影响更新另审，R10显示争议，R15按时期查询，R18决定审核/删除。

**例子/反例**：“喜欢紫色”与“这个项目用蓝色”作用范围不同，应并存。不能将项目配色决定解释为用户彻底不喜欢紫色。用户明确纠正名字则保留更正来源，不继续用旧推测当当前身份。

**写入归属与状态**：ClaimStore写候选与审订记录。生命周期candidate→accepted/disputed/rejected；accepted后可被新版本superseded，历史版本不删除。accepted表示通过本系统对应策略，不将推测洗成客观真理。真值、来源类型、审核状态与适用时间是四个独立维度。

**实现细节**：按 `(subject_id,predicate,scope,valid_interval)` 查询可能冲突项，但自然语言命题相似不是自动同义判定。显式更正优先匹配被纠正对象和范围；匹配失败先建dispute。一次来源支持多个命题时各自保存范围。valid_to为null意为未给定结束，不代表永久为真；recorded_at表示何时知道，不能覆盖valid_from。问“那时我们怎么决定”按历史有效时间重建，而非把今天的修订倒灌成当时已知。

## R05.02 位置、所有权与现状映射

规范数据族：`semantic_memory`。R03–R12对应十类typed store；其余是来源/运行/派生服务，不能再算额外心理记忆。

同命题CAS；冲突不能取数组第一项骗过严格校验；未知扩展字段走新schema。

当前可核候选为0.32.0-candidate及其局部源码，不等于D现场已具备该接口。内核既有memories(kind)+versions继续保留，目标分型表由显式迁移产生；本模块不能绕规范API直接改别类记录。详见DATA_STORES.md的表归属。

## R05.03 输入契约

实际来源、主体候选、适用范围/有效时间、已有命题与反证、明确纠正事件。

调用外层必有schema_version、request_id、可信principal/scope、operation、deadline/cancel；写入带expected_revision和支持幂等的operation_key。读取带filter/snapshot/cursor，不能将模型提供的actor/scope直接当认证。类型表中可空项显式null，未执行检查不得以空数组冒“确认没有”。

## R05.04 输出、回执与错误契约

版本化Claim、支持/补充/冲突/纠正判定、当前与历史视图。

统一返回{request_id,operation_id,module,disposition,object_refs,base_revision,committed_revision,coverage,gaps,receipt_ref,evidence_level}。对象引用含kind/id/revision，来源引用含source_id/source_revision/hash/range。纯读committed_revision=null；候选disposition=proposed，不能返回committed冒正式状态。

错误至少区分INVALID_ARGUMENT、FORBIDDEN/NOT_FOUND_OR_HIDDEN、CONFLICT、SOURCE_UNAVAILABLE、TIMEOUT、RESOURCE_EXHAUSTED、UNVERIFIED_BINDING、INTERNAL；有提交路径还要commit_outcome=not_committed/committed/unknown。未知结果先按原键查回执。

## R05.05 数据字段、状态与索引

| 字段组 | 类型 | 约束与语义 |
|---|---|---|
| subject_id/predicate/value | ID/string/JSON | 主体未定留候选，不凭语义相似合并 |
| epistemic | enum | self_report/other_report/observation/inference/unknown |
| valid_from/valid_to/time_precision | object | 可空，不将记录时间当生效时间 |
| recorded_at | Instant | 何时知道该主张 |
| scope_condition | object | 项目/场景/领域限定 |
| evidence/counter_evidence | array | 来源版本与范围 |
| review_status | enum | candidate/accepted/disputed/rejected/superseded |
| predecessor/correction_scope | nullable object | 纠正哪个命题的哪个范围 |

公共对象字段：id、kind、schema_version、scope、created_at、created_by、revision、status、record_digest；每项来源或实际宿主创建依据另存。组字段细分时必须列schema，不用不同拼法兼容猜测。

candidate→accepted/disputed/rejected；接受只是策略已审，不等于世界真理；纠正追加新版本，历史不删。

最低索引：scope+kind+有效状态+业务主键；来源反向依赖(source_id,source_revision)；对象版本(id,revision)。本模块特定检索维度由第11节给出。索引只定位，当前有效性仍核规范记录，不以索引命中当接受事实。

## R05.06 自动触发与完整处理顺序

1. 核来源与人物，提出原子命题，陈述发生与内容真假分开。
2. 查同主体/谓词/作用范围/时间的旧主张。
3. 对比为支持、补充、纠正、争议或无关；不同范围允许并存。
4. 明确纠正若匹配旧推测，先阻止其作为当前已证内容；不明则标争议。
5. CAS写命题与证据/反证，反向失效受影响派生。
6. 查询按问题时期返回当前或历史主张，并带争议及缺口。

宿主触发后逐阶段记started/succeeded/failed/skipped/unverified；不需要运行的步骤可skipped，但不能将缺必需依赖也算正常跳过。只读规划不改原始事件，模型调用不在数据库长锁内。

## R05.07 关键算法、决策与禁止捷径

不使用“最后一句永远覆盖”规则。本人自述只支持本人当时表达；转述不提升为亲历。否定/限定/时间必须保留；总结不得把“不总是”变成“从不”。

每次推导均把直接观察、他人转述、候选解释、规范记录、外部结果分开。source_ref能定位仅证明原文存在；如涉及开放语义，必须由相应支持验证和反例测试决定是否可用，不能单靠hash/正则。算法参数只影响工程取舍，不授身份、权限或关系事实。

## R05.08 幂等、修订、并发与提交

同命题CAS；冲突不能取数组第一项骗过严格校验；未知扩展字段走新schema。

操作重试与新业务事件分开；相同操作键异实质请求必须冲突。读取允许新快照结果变化，不能为了固定输出使用已撤回缓存。规范状态修改用expected_revision；跨库步骤分别留回执与reconciliation_required，不以一库commit冒全局事务。D依赖实际输出的SelfState/八域仍须强run/attempt/scope绑定，不让本模块日志替代。

## R05.09 更正、失效、删除与反向依赖

凡`semantic_memory`中有源派生物，登记source_root、source_revision、processor_version及依赖关系；纠正到来时先invalid_for_use/争议，后重建，不继续拿旧结论无提示作答。删除先由R18tombstone阻可用性，再清正文/索引/缓存/Wiki/备份策略；不能仅删引文保留相同推断。

无人物/心理职责的运行对象只记录必要状态，不因本模块失败写用户生气或D疏远。已发生事件和已表达的当时状态不被后来解释覆写；隐私擦除走专用治理路径。

## R05.10 模块扣接与交接责任

| 方向 | 对接对象 | 必须交接的内容 |
|---|---|---|
| 输入 | R01 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R04 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R07 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R11 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R18 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输出 | R09 | ClaimStore结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R10 | ClaimStore结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R15 | ClaimStore结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R17 | ClaimStore结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R22 | ClaimStore结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |

交接由HostAdapter/Coordinator调用，不让两个模块彼此递归无限互调。每个edge均记录当前事件/源版本、调用目的、预算、取消与真实回执；完整schema和时序见LINKAGE.md。接收失败保待处理/限制，不能发送空结果伪装成功。

## R05.11 如何存、如何召回、如何区分其他记忆

按主体+谓词+范围+有效时间查；同原事件生成多摘要只算一个根源，不凭次数加真值。

受权路线只查询声明的kind及其规范业务表；不能把情绪解释当语义事实、反思当亲历、工具尝试当结果。共享来源可同时支持多个kind，但每条命题有独立语义和审核状态；同源同命题折叠，不合并同源不同要求。必要后续沿依赖图取回，超过budget标partial。

## R05.12 注入的进入、最短表示与退出

只注入回答当前问题所需的主张及必要纠正/反证；当前问过去不只给现在值。

当材料进入R22候选，每条必须能说明当前anchor、need_reason、新增信息和support_verdict。已在真实messages充分表达则不重注；换窗缺了则可重供。话题切换、完成、失效、撤回或无本轮用途就退出动态块，规范记忆保留。zero injection不关闭宿主最低检查，故障也不能伪装none_needed。

## R05.13 后台、恢复、超时与取消

本模块相关后台作业以scope+源版本+operation+schema/processor版本幂等，经R17持久队列领取。对于纯读路径，只保存必要阅读/覆盖进度，不声称有待提交事实。恢复时读最新删除、授权、规范状态及semantic_memory版本，再决定重算/继续/放弃。

失约worker写回须被fencing拒绝；模型调用超时发取消，底层不能证实停止就记cancel_unconfirmed，迟到结果不能自动commit。外部动作的unknown由R14先对账。未部署后台或钩子则标missing，不能称离线持续执行。

## R05.14 资源、隐私与降级规则

与R24共享每run/job预算，不为R05另开无界模型循环。前台最低检查、输入入账、必要纠正/边界和输出预留优先；可选语义、图展开、后台整理可暂停。所有查询与补读都有limit/deadline/stop_reason；候选上限不是注入配额。

故障使用第4节错误和coverage，普通交流尽量继续，依赖缺失的动作限制。密钥/原始私聊不进普通日志；被拒scope不出现在公开解释中。资源阈值不是情绪好感阈值，未实测目标机器不报固定延迟/容量保证。

## R05.15 贯通例子与反例

“喜欢紫色”与“项目用蓝色”并存；“名字写错了”只修匹配人物/范围，不重置全部偏好。

验证时把该场景与原事件、已有记录、真实请求或结果链同时保存：输入→ClaimStore→下游回执。仅看到本模块返回JSON不证明生成模型采用，也不证明真实动作完成。正确处理应保留未知、合法来源和以后修订入口；能说出漂亮话不替代字段/版本/来源正确。

## R05.16 36项模块与协议验收需求目录（非执行fixture）

| ID | 准备/触发 | 必须结果；不满足即失败 | 当前状态 |
|---|---|---|---|
| R05-T01 | 在隔离fixture中构造：全局偏好与项目配色并存 | 全局偏好与项目配色并存 | not_run |
| R05-T02 | 在隔离fixture中构造：问过去返回当时版本 | 问过去返回当时版本 | not_run |
| R05-T03 | 在隔离fixture中构造：明确纠正停止旧推测使用 | 明确纠正停止旧推测使用 | not_run |
| R05-T04 | 在隔离fixture中构造：谁说过与客观事实分开 | 谁说过与客观事实分开 | not_run |
| R05-T05 | 在隔离fixture中构造：不同人物同命题不合并 | 不同人物同命题不合并 | not_run |
| R05-T06 | 在隔离fixture中构造：同来源多次反思不增加证据根 | 同来源多次反思不增加证据根 | not_run |
| R05-T07 | 在隔离fixture中构造：不是/仅在/可能等限定不丢 | 不是/仅在/可能等限定不丢 | not_run |
| R05-T08 | 在隔离fixture中构造：新话无法匹配纠正对象先争议 | 新话无法匹配纠正对象先争议 | not_run |
| R05-T09 | 在隔离fixture中构造：转述被本人否认可保两源及冲突 | 转述被本人否认可保两源及冲突 | not_run |
| R05-T10 | 在隔离fixture中构造：valid_to为空不宣称永恒 | valid_to为空不宣称永恒 | not_run |
| R05-T11 | 在隔离fixture中构造：命题引用存在但不支持时拒接受 | 命题引用存在但不支持时拒接受 | not_run |
| R05-T12 | 在隔离fixture中构造：后台旧总结不可覆盖新修订 | 后台旧总结不可覆盖新修订 | not_run |
| R05-T13 | 另建scope-B对象并以scope-A主体访问 | 拒绝相应资料/写入，公开响应不含B存在性；当前合法对象不变 | not_run |
| R05-T14 | 从本模块字段表逐组移除必需输入 | INVALID_ARGUMENT及字段路径；不得补造主体、项目或事实 | not_run |
| R05-T15 | 使用未支持schema/profile及实质未知字段 | 拒绝或显式unsupported；不静默删字段骗校验 | not_run |
| R05-T16 | 同源版本/操作键提交两遍 | 按本节幂等规则处理，副作用/独立证据不重复；纯读可以重查并保快照差别 | not_run |
| R05-T17 | 两调用携同expected_revision更新同对象 | 持久写至多一方按原前态成功，另一方冲突/受控重读；纯读不得写事实 | not_run |
| R05-T18 | 准备后提交/供给前对来源加tombstone | 相关派生停用或拒提交，旧缓存不复活；无来源型运行记录核相应取消/策略 | not_run |
| R05-T19 | 阶段处理中提交相关来源新版本 | 旧版本不能覆盖最新纠正；重算/partial/失效原因可查 | not_run |
| R05-T20 | 将一个必须依赖返回unavailable | 保具体缺口；不把失败当正常空结果或全部完成 | not_run |
| R05-T21 | 在本模块关键算法/调用处返回错误 | 错误回传，阶段failed/unknown；没有可用结论就不伪报成功 | not_run |
| R05-T22 | 故意令本模块外部阶段超过deadline | 取消按能力记录，迟到结果不绕版本与取消检查；真实停止未知照实 | not_run |
| R05-T23 | 准备完成后、提交/供给前取消run或job | 未发生副作用不再执行；已发生事实不抹除，结果另记 | not_run |
| R05-T24 | 租约失效后旧worker尝试写回 | 有持久写的路径由fencing/CAS拒绝；只读路径不借续读取得写权 | not_run |
| R05-T25 | 对持久写路径在关联对象写入间注入异常 | 本库事务全有或全无；跨库显示中间态并可对账；只读不虚称事务验收 | not_run |
| R05-T26 | 在commit后/返回前断开响应 | 按原键查询回执，不盲新建意图；只读重试不得假定语料未变化 | not_run |
| R05-T27 | 相关outbox成功处理但ACK丢失再投递 | 按源/处理器版本幂等，不产生第二次认知强化或外部动作 | not_run |
| R05-T28 | 规范对象已修订而索引未追平 | 报告水位并查规范store或partial；不能将旧命中当最新事实 | not_run |
| R05-T29 | 样本含emoji、不是/仅在/可能等限定 | 源范围和原意保留；截断不得变反义；非文本对象用其真实坐标 | not_run |
| R05-T30 | 加入同名不同ID与未定指代候选 | 保持候选/unknown，不自动合并；无人物职责模块不自创人物推断 | not_run |
| R05-T31 | 旧/新有效期及接收顺序不一致 | 按真实时间/版本契约处理；无法比较时不擅选最后接收值 | not_run |
| R05-T32 | 同材料被旧插件与当前出口同时提出 | 只有R22可最终装配，去本宿主拥有旧块而保用户/系统/工具结构 | not_run |
| R05-T33 | 提供本地保存/尝试但无业务或送达回执 | 不得升级成已理解/已完成/已送达；按该模块实际成果层级标注 | not_run |
| R05-T34 | 恢复相同逻辑初态重跑，同配置与fixture hash | 可复现本模块约定结果；时间/随机ID差异不混成语义提升 | not_run |
| R05-T35 | 输入含私密正文/凭据状外部内容 | 普通日志与索引/投影不泄漏禁止范围；审计仅留必要ID和固定原因 | not_run |
| R05-T36 | 只有文档、模拟对象或模型自评时要求标通过 | 保design/static/synthetic/real_host分轴；缺真实证据标not_run/unknown | not_run |

T01–T12是该模块专属语义/业务场景；T13–T36是必须绑定本模块实际写读路径执行的协议/故障场景，不能空跑通用脚本就全标通过。先从字段表构造合法基准fixture，再只改变本例条件；对不适用的写路径要给可审证据说明与对应只读判据，不能把未测记成pass。

## R05.17 交付证据、通过门槛与未完成项

交付ClaimStore实现/schema迁移、输入输出fixture、合法及反例来源、实际存储与调用回执、真实入口覆盖、查询及注入观察、失败恢复报告。证据等级design/static/synthetic_process/real_host/storage_fault/production分开。

模块通过至少需要专属场景和适用协议场景的实际证据；整套通过还需LINKAGE.md跨模块链。当前文档生成/类型DDL检查不算本模块36例已跑。已有候选仅作为迁移基础，现场未知和未实现开放语义仍未验。

## R05.18 实现次序、兼容策略与设计自审

先固定本模块字段/状态/真源→实现受权最小路径与回执→跑专属正反例→接入上游/下游→做恢复/删除/冲突→在真实隔离宿主检查请求或结果。本模块不得以优化名义删除保留矩阵中已有功能，不改C032严格profile顶层来绕验证。

本次设计检查关注：按主体+谓词+范围+有效时间查；同原事件生成多摘要只算一个根源，不凭次数加真值。 只注入回答当前问题所需的主张及必要纠正/反证；当前问过去不只给现在值。 对所有结果都分别标明对象、版本、来源、局限和验证等级；不以同一success覆盖入账、理解、注入、生成、送达与执行。生产边界不变，不随文档生成而开通部署。



---

# R06　程序性经验：详细设计与验收规格

版本：everlight/6-design；模块契约：r06/1；日期：2026-11-08。本文为设计，全部功能验收初始not_run。最终裁决以FINAL_DECISIONS.md和MODULE_DECISIONS.md为准。与contracts/共同生效，不是已安装服务。

## R06.01 定义、边界与可证伪成功标准

有适用范围的方法候选与执行前检查，不直接执行工具。

唯一业务责任服务是`ProcedureStore`。输入必须满足第3节，输出必须满足第4节及GLOBAL_PROTOCOL。成功必须可从实际记录/回执读回，而不是模型自称完成。

原有具体机制及边界（保留并由本版细化）：

**原理与基础**：做事方法必须携带适用条件和真实成败依据。候选有procedurePlan/proceduralExperience，不执行真实动作，实际工具前自动查询未接。

**数据**：procedure_id、environment/version、目标、前置条件、步骤、输出、rollback_hint、action/evidence_refs和失效条件。方法可以是候选、曾成功、曾失败、过期；“曾成功”不是“现在可无条件执行”。

**步骤**：①R03/R14出现操作目标；②按当前环境检索适用经验；③核文件/程序版本与依赖；④R18/R14重新检查具体授权；⑤执行由宿主负责；⑥回执和错误更新经验，失败不重复强化错误步骤。版本不足时只提供建议并说明未知。

**必须扣住**：R03目标、R12环境资料、R15查方法、R14执行回执、R11总结、R18授权。不能从程序记忆直接发shell或恢复退休进程。

**例子/反例**：旧版服务通过命令X启动，新版已更换入口。应先核版本，不按历史成功自动执行X；没有许可时仅列可审核方案。工具超时的结果不当成确定失败再重试。

**写入归属与状态**：ProcedureStore写方法，ExecutionAdapter写真实执行结果；模型只提出候选步骤。状态candidate/validated_for_environment/stale/retired，验证附具体环境、版本和样本，不能一个全局success覆盖所有机器。把工具异常与步骤不适用分别归因，未查明原因保留unknown。

**实现细节**：程序步骤引用工具操作名、前置条件、预期结果与可选补救；不要存一段可任意执行的历史shell文本当可信程序。R14提交动作前按当前操作再次检查前提。经验归纳应抽“保存文件后读取确认版本”之类可迁移策略，具体路径/凭据留当前环境适配。失败模式与成功方法共同召回，避免只记成功样本造成盲目重试。

## R06.02 位置、所有权与现状映射

规范数据族：`procedural_memory`。R03–R12对应十类typed store；其余是来源/运行/派生服务，不能再算额外心理记忆。

步骤候选版本CAS；结果事件稳定ID幂等；模型生成的方法没有实机证据只标candidate。

当前可核候选为0.32.0-candidate及其局部源码，不等于D现场已具备该接口。内核既有memories(kind)+versions继续保留，目标分型表由显式迁移产生；本模块不能绕规范API直接改别类记录。详见DATA_STORES.md的表归属。

## R06.03 输入契约

当前任务/操作意图，环境与工具版本，历史步骤、前提、成功失败回执。

调用外层必有schema_version、request_id、可信principal/scope、operation、deadline/cancel；写入带expected_revision和支持幂等的operation_key。读取带filter/snapshot/cursor，不能将模型提供的actor/scope直接当认证。类型表中可空项显式null，未执行检查不得以空数组冒“确认没有”。

## R06.04 输出、回执与错误契约

有适用范围的方法候选与执行前检查，不直接执行工具。

统一返回{request_id,operation_id,module,disposition,object_refs,base_revision,committed_revision,coverage,gaps,receipt_ref,evidence_level}。对象引用含kind/id/revision，来源引用含source_id/source_revision/hash/range。纯读committed_revision=null；候选disposition=proposed，不能返回committed冒正式状态。

错误至少区分INVALID_ARGUMENT、FORBIDDEN/NOT_FOUND_OR_HIDDEN、CONFLICT、SOURCE_UNAVAILABLE、TIMEOUT、RESOURCE_EXHAUSTED、UNVERIFIED_BINDING、INTERNAL；有提交路径还要commit_outcome=not_committed/committed/unknown。未知结果先按原键查回执。

## R06.05 数据字段、状态与索引

| 字段组 | 类型 | 约束与语义 |
|---|---|---|
| procedure_id/goal | ID/string | 目标与步骤独立命名 |
| environment/version | object | 适用环境、工具/依赖版本 |
| preconditions | array | 执行前必须验证 |
| steps | array | 工具操作、输入、期望结果，不是任意历史shell |
| result_refs | array | 真实行动及业务结果 |
| failure_modes | array | 失败现象/已知原因/未知分开 |
| rollback_hint | nullable object | 可能补救，不保证可逆 |
| status | enum | candidate/validated_for_environment/stale/retired |

公共对象字段：id、kind、schema_version、scope、created_at、created_by、revision、status、record_digest；每项来源或实际宿主创建依据另存。组字段细分时必须列schema，不用不同拼法兼容猜测。

candidate→指定环境已验证；环境变化stale；不适用retired。一次成功不能成为全环境无条件授权。

最低索引：scope+kind+有效状态+业务主键；来源反向依赖(source_id,source_revision)；对象版本(id,revision)。本模块特定检索维度由第11节给出。索引只定位，当前有效性仍核规范记录，不以索引命中当接受事实。

## R06.06 自动触发与完整处理顺序

1. 根据当前操作目标查方法及失败模式。
2. 核当前环境/版本和原证据适用性。
3. 前提不满足时只提出适配/核查建议，不能盲执行。
4. 真实动作由R14/R18检查授权并调用宿主。
5. 读取真实结果、业务核验及unknown。
6. 形成局部经验或修订适用条件，引用同一结果不重复强化。

宿主触发后逐阶段记started/succeeded/failed/skipped/unverified；不需要运行的步骤可skipped，但不能将缺必需依赖也算正常跳过。只读规划不改原始事件，模型调用不在数据库长锁内。

## R06.07 关键算法、决策与禁止捷径

方法建议与权限完全分开。工具超时先查状态，不把失败后重试学成通用策略；成功输出需与目标验收相符。成长保存为什么有效/哪里无效，不只保存命令。

每次推导均把直接观察、他人转述、候选解释、规范记录、外部结果分开。source_ref能定位仅证明原文存在；如涉及开放语义，必须由相应支持验证和反例测试决定是否可用，不能单靠hash/正则。算法参数只影响工程取舍，不授身份、权限或关系事实。

## R06.08 幂等、修订、并发与提交

步骤候选版本CAS；结果事件稳定ID幂等；模型生成的方法没有实机证据只标candidate。

操作重试与新业务事件分开；相同操作键异实质请求必须冲突。读取允许新快照结果变化，不能为了固定输出使用已撤回缓存。规范状态修改用expected_revision；跨库步骤分别留回执与reconciliation_required，不以一库commit冒全局事务。D依赖实际输出的SelfState/八域仍须强run/attempt/scope绑定，不让本模块日志替代。

## R06.09 更正、失效、删除与反向依赖

凡`procedural_memory`中有源派生物，登记source_root、source_revision、processor_version及依赖关系；纠正到来时先invalid_for_use/争议，后重建，不继续拿旧结论无提示作答。删除先由R18tombstone阻可用性，再清正文/索引/缓存/Wiki/备份策略；不能仅删引文保留相同推断。

无人物/心理职责的运行对象只记录必要状态，不因本模块失败写用户生气或D疏远。已发生事件和已表达的当时状态不被后来解释覆写；隐私擦除走专用治理路径。

## R06.10 模块扣接与交接责任

| 方向 | 对接对象 | 必须交接的内容 |
|---|---|---|
| 输入 | R03 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R12 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R14 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R18 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输出 | R11 | ProcedureStore结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R15 | ProcedureStore结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R17 | ProcedureStore结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R22 | ProcedureStore结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |

交接由HostAdapter/Coordinator调用，不让两个模块彼此递归无限互调。每个edge均记录当前事件/源版本、调用目的、预算、取消与真实回执；完整schema和时序见LINKAGE.md。接收失败保待处理/限制，不能发送空结果伪装成功。

## R06.11 如何存、如何召回、如何区分其他记忆

按目标+环境+版本查，命中同时取失败模式和失效条件；退役方法可作历史说明但不建议执行。

受权路线只查询声明的kind及其规范业务表；不能把情绪解释当语义事实、反思当亲历、工具尝试当结果。共享来源可同时支持多个kind，但每条命题有独立语义和审核状态；同源同命题折叠，不合并同源不同要求。必要后续沿依赖图取回，超过budget标partial。

## R06.12 注入的进入、最短表示与退出

任务确需操作时只给适用步骤和关键前提；不要每轮注入全部工具手册。

当材料进入R22候选，每条必须能说明当前anchor、need_reason、新增信息和support_verdict。已在真实messages充分表达则不重注；换窗缺了则可重供。话题切换、完成、失效、撤回或无本轮用途就退出动态块，规范记忆保留。zero injection不关闭宿主最低检查，故障也不能伪装none_needed。

## R06.13 后台、恢复、超时与取消

本模块相关后台作业以scope+源版本+operation+schema/processor版本幂等，经R17持久队列领取。对于纯读路径，只保存必要阅读/覆盖进度，不声称有待提交事实。恢复时读最新删除、授权、规范状态及procedural_memory版本，再决定重算/继续/放弃。

失约worker写回须被fencing拒绝；模型调用超时发取消，底层不能证实停止就记cancel_unconfirmed，迟到结果不能自动commit。外部动作的unknown由R14先对账。未部署后台或钩子则标missing，不能称离线持续执行。

## R06.14 资源、隐私与降级规则

与R24共享每run/job预算，不为R06另开无界模型循环。前台最低检查、输入入账、必要纠正/边界和输出预留优先；可选语义、图展开、后台整理可暂停。所有查询与补读都有limit/deadline/stop_reason；候选上限不是注入配额。

故障使用第4节错误和coverage，普通交流尽量继续，依赖缺失的动作限制。密钥/原始私聊不进普通日志；被拒scope不出现在公开解释中。资源阈值不是情绪好感阈值，未实测目标机器不报固定延迟/容量保证。

## R06.15 贯通例子与反例

旧版用X启动，新版换入口：查当前版本再决定；工具超时且远端可能已成功时不自动重做。

验证时把该场景与原事件、已有记录、真实请求或结果链同时保存：输入→ProcedureStore→下游回执。仅看到本模块返回JSON不证明生成模型采用，也不证明真实动作完成。正确处理应保留未知、合法来源和以后修订入口；能说出漂亮话不替代字段/版本/来源正确。

## R06.16 36项模块与协议验收需求目录（非执行fixture）

| ID | 准备/触发 | 必须结果；不满足即失败 | 当前状态 |
|---|---|---|---|
| R06-T01 | 在隔离fixture中构造：新版环境不盲套旧命令 | 新版环境不盲套旧命令 | not_run |
| R06-T02 | 在隔离fixture中构造：工具没报错但目标未达不标成功 | 工具没报错但目标未达不标成功 | not_run |
| R06-T03 | 在隔离fixture中构造：超时unknown先对账 | 超时unknown先对账 | not_run |
| R06-T04 | 在隔离fixture中构造：无许可不从经验直接执行 | 无许可不从经验直接执行 | not_run |
| R06-T05 | 在隔离fixture中构造：失败模式与成功方法同召回 | 失败模式与成功方法同召回 | not_run |
| R06-T06 | 在隔离fixture中构造：同结果反复整理不重复计经验 | 同结果反复整理不重复计经验 | not_run |
| R06-T07 | 在隔离fixture中构造：一个领域方法不推广所有项目 | 一个领域方法不推广所有项目 | not_run |
| R06-T08 | 在隔离fixture中构造：前提缺失给unknown而非编环境 | 前提缺失给unknown而非编环境 | not_run |
| R06-T09 | 在隔离fixture中构造：退役步骤不能自动复活 | 退役步骤不能自动复活 | not_run |
| R06-T10 | 在隔离fixture中构造：命令中密钥不进通用经验 | 命令中密钥不进通用经验 | not_run |
| R06-T11 | 在隔离fixture中构造：后续结果反证可修订旧方法 | 后续结果反证可修订旧方法 | not_run |
| R06-T12 | 在隔离fixture中构造：一次成功仅验证其指定环境 | 一次成功仅验证其指定环境 | not_run |
| R06-T13 | 另建scope-B对象并以scope-A主体访问 | 拒绝相应资料/写入，公开响应不含B存在性；当前合法对象不变 | not_run |
| R06-T14 | 从本模块字段表逐组移除必需输入 | INVALID_ARGUMENT及字段路径；不得补造主体、项目或事实 | not_run |
| R06-T15 | 使用未支持schema/profile及实质未知字段 | 拒绝或显式unsupported；不静默删字段骗校验 | not_run |
| R06-T16 | 同源版本/操作键提交两遍 | 按本节幂等规则处理，副作用/独立证据不重复；纯读可以重查并保快照差别 | not_run |
| R06-T17 | 两调用携同expected_revision更新同对象 | 持久写至多一方按原前态成功，另一方冲突/受控重读；纯读不得写事实 | not_run |
| R06-T18 | 准备后提交/供给前对来源加tombstone | 相关派生停用或拒提交，旧缓存不复活；无来源型运行记录核相应取消/策略 | not_run |
| R06-T19 | 阶段处理中提交相关来源新版本 | 旧版本不能覆盖最新纠正；重算/partial/失效原因可查 | not_run |
| R06-T20 | 将一个必须依赖返回unavailable | 保具体缺口；不把失败当正常空结果或全部完成 | not_run |
| R06-T21 | 在本模块关键算法/调用处返回错误 | 错误回传，阶段failed/unknown；没有可用结论就不伪报成功 | not_run |
| R06-T22 | 故意令本模块外部阶段超过deadline | 取消按能力记录，迟到结果不绕版本与取消检查；真实停止未知照实 | not_run |
| R06-T23 | 准备完成后、提交/供给前取消run或job | 未发生副作用不再执行；已发生事实不抹除，结果另记 | not_run |
| R06-T24 | 租约失效后旧worker尝试写回 | 有持久写的路径由fencing/CAS拒绝；只读路径不借续读取得写权 | not_run |
| R06-T25 | 对持久写路径在关联对象写入间注入异常 | 本库事务全有或全无；跨库显示中间态并可对账；只读不虚称事务验收 | not_run |
| R06-T26 | 在commit后/返回前断开响应 | 按原键查询回执，不盲新建意图；只读重试不得假定语料未变化 | not_run |
| R06-T27 | 相关outbox成功处理但ACK丢失再投递 | 按源/处理器版本幂等，不产生第二次认知强化或外部动作 | not_run |
| R06-T28 | 规范对象已修订而索引未追平 | 报告水位并查规范store或partial；不能将旧命中当最新事实 | not_run |
| R06-T29 | 样本含emoji、不是/仅在/可能等限定 | 源范围和原意保留；截断不得变反义；非文本对象用其真实坐标 | not_run |
| R06-T30 | 加入同名不同ID与未定指代候选 | 保持候选/unknown，不自动合并；无人物职责模块不自创人物推断 | not_run |
| R06-T31 | 旧/新有效期及接收顺序不一致 | 按真实时间/版本契约处理；无法比较时不擅选最后接收值 | not_run |
| R06-T32 | 同材料被旧插件与当前出口同时提出 | 只有R22可最终装配，去本宿主拥有旧块而保用户/系统/工具结构 | not_run |
| R06-T33 | 提供本地保存/尝试但无业务或送达回执 | 不得升级成已理解/已完成/已送达；按该模块实际成果层级标注 | not_run |
| R06-T34 | 恢复相同逻辑初态重跑，同配置与fixture hash | 可复现本模块约定结果；时间/随机ID差异不混成语义提升 | not_run |
| R06-T35 | 输入含私密正文/凭据状外部内容 | 普通日志与索引/投影不泄漏禁止范围；审计仅留必要ID和固定原因 | not_run |
| R06-T36 | 只有文档、模拟对象或模型自评时要求标通过 | 保design/static/synthetic/real_host分轴；缺真实证据标not_run/unknown | not_run |

T01–T12是该模块专属语义/业务场景；T13–T36是必须绑定本模块实际写读路径执行的协议/故障场景，不能空跑通用脚本就全标通过。先从字段表构造合法基准fixture，再只改变本例条件；对不适用的写路径要给可审证据说明与对应只读判据，不能把未测记成pass。

## R06.17 交付证据、通过门槛与未完成项

交付ProcedureStore实现/schema迁移、输入输出fixture、合法及反例来源、实际存储与调用回执、真实入口覆盖、查询及注入观察、失败恢复报告。证据等级design/static/synthetic_process/real_host/storage_fault/production分开。

模块通过至少需要专属场景和适用协议场景的实际证据；整套通过还需LINKAGE.md跨模块链。当前文档生成/类型DDL检查不算本模块36例已跑。已有候选仅作为迁移基础，现场未知和未实现开放语义仍未验。

## R06.18 实现次序、兼容策略与设计自审

先固定本模块字段/状态/真源→实现受权最小路径与回执→跑专属正反例→接入上游/下游→做恢复/删除/冲突→在真实隔离宿主检查请求或结果。本模块不得以优化名义删除保留矩阵中已有功能，不改C032严格profile顶层来绕验证。

本次设计检查关注：按目标+环境+版本查，命中同时取失败模式和失效条件；退役方法可作历史说明但不建议执行。 任务确需操作时只给适用步骤和关键前提；不要每轮注入全部工具手册。 对所有结果都分别标明对象、版本、来源、局限和验证等级；不以同一success覆盖入账、理解、注入、生成、送达与执行。生产边界不变，不随文档生成而开通部署。



---

# R07　人物与关系记忆：详细设计与验收规格

版本：everlight/6-design；模块契约：r07/1；日期：2026-11-08。本文为设计，全部功能验收初始not_run。最终裁决以FINAL_DECISIONS.md和MODULE_DECISIONS.md为准。与contracts/共同生效，不是已安装服务。

## R07.01 定义、边界与可证伪成功标准

Person/Alias/Relation、参与者及认知候选，社交评价的对象与证据锚。

唯一业务责任服务是`RelationStore`。输入必须满足第3节，输出必须满足第4节及GLOBAL_PROTOCOL。成功必须可从实际记录/回执读回，而不是模型自称完成。

原有具体机制及边界（保留并由本版细化）：

**原理与基础**：认识谁、怎样认识、哪时是什么关系和谁这样认为必须分开。候选有实体、别名、关系基础；开放指代/多跳质量和真实权限未验。

**数据**：Person稳定ID；Alias按来源/范围/时间；Relation有subject/object/direction/domain、有效/记录时间、perspective_holder、来源、性质、争议和修订。EpisodeParticipant链接共同事件；关系不是权限。

**步骤**：①可信actor映射优先；②名字/昵称/代称给候选，不凭语义相似合并；③确定人物后取当前话题相关关系及经历；④他人转述和D亲历分开；⑤新关系变化追加版本；⑥合并/拆分保留ID映射和反向依赖，能追踪误合并影响。

**必须扣住**：R01发言者，R02指代候选，R04共同经历，R08对象和视角，R11后来理解，R15召回，R18群/私聊范围。A认识B、B认识C不能推断A认识C，更不能沿图传播访问权。

**例子/反例**：示例用户说“示例协作者上次帮忙”，可找示例协作者参与的相关任务。群内两位示例协作者无法确认时列候选或问清；不把一人的私聊归给另一人，也不把“示例用户称某人为朋友”写成对方也作同样表态。

**写入归属与状态**：EntityStore管理人物ID和账号映射，RelationStore管理关系主张；合并/拆分由显式受控操作完成。Relation状态candidate/active/disputed/ended；active不自动等于双方认可，须读perspective_holder与证据。known_to_D分direct_interaction/reported_only/unknown，不由共同好友推出亲历。

**实现细节**：关系边至少有两端ID、方向、类型、适用领域、有效时间、记录时间、视角和来源。协作可靠性分领域保存具体成功/失约经历，不设置全局“好感80”。人物出现后先做ID解析，再取与当前关切有关的边，再取共同经历和最新后续。一次误合并的撤销通过alias_revision和reverse_dependencies找回受影响的Claim/Affect/Reflection，批量标待复核；不默默把旧推测继续挂在新人物上。

## R07.02 位置、所有权与现状映射

规范数据族：`relational_memory`。R03–R12对应十类typed store；其余是来源/运行/派生服务，不能再算额外心理记忆。

实体映射revision、关系revision各自CAS；合并留redirect与来源依赖，拆分后旧派生标待复核。

当前可核候选为0.32.0-candidate及其局部源码，不等于D现场已具备该接口。内核既有memories(kind)+versions继续保留，目标分型表由显式迁移产生；本模块不能绕规范API直接改别类记录。详见DATA_STORES.md的表归属。

## R07.03 输入契约

可信actor映射、R02局部候选、共同事件、关系自述/转述、视角与边界来源。

调用外层必有schema_version、request_id、可信principal/scope、operation、deadline/cancel；写入带expected_revision和支持幂等的operation_key。读取带filter/snapshot/cursor，不能将模型提供的actor/scope直接当认证。类型表中可空项显式null，未执行检查不得以空数组冒“确认没有”。

## R07.04 输出、回执与错误契约

Person/Alias/Relation、参与者及认知候选，社交评价的对象与证据锚。

统一返回{request_id,operation_id,module,disposition,object_refs,base_revision,committed_revision,coverage,gaps,receipt_ref,evidence_level}。对象引用含kind/id/revision，来源引用含source_id/source_revision/hash/range。纯读committed_revision=null；候选disposition=proposed，不能返回committed冒正式状态。

错误至少区分INVALID_ARGUMENT、FORBIDDEN/NOT_FOUND_OR_HIDDEN、CONFLICT、SOURCE_UNAVAILABLE、TIMEOUT、RESOURCE_EXHAUSTED、UNVERIFIED_BINDING、INTERNAL；有提交路径还要commit_outcome=not_committed/committed/unknown。未知结果先按原键查回执。

## R07.05 数据字段、状态与索引

| 字段组 | 类型 | 约束与语义 |
|---|---|---|
| person_id/verified_accounts | ID/array | 账号认证与人格背景真假分开 |
| aliases | array | 名称、范围、时期与来源；不唯一 |
| from_id/to_id/direction | IDs/enum | 关系有方向，不自动互认 |
| holder_id/knowledge_status | ID/enum | 谁的视角，direct_interaction/reported_only/unknown |
| relation_kind/domain | string | 领域关系，不是权限 |
| valid_interval/recorded_at | object/Instant | 发生有效期与何时记录分开 |
| expectations/boundary_refs | array | 具体相处期待/已表达边界及源 |
| evidence/counter/status | array/enum | candidate/active/disputed/ended |

公共对象字段：id、kind、schema_version、scope、created_at、created_by、revision、status、record_digest；每项来源或实际宿主创建依据另存。组字段细分时必须列schema，不用不同拼法兼容猜测。

候选人物→经证据解析；关系candidate→active/disputed；结束追加版本。合并/拆分是受控操作，保可逆映射。

最低索引：scope+kind+有效状态+业务主键；来源反向依赖(source_id,source_revision)；对象版本(id,revision)。本模块特定检索维度由第11节给出。索引只定位，当前有效性仍核规范记录，不以索引命中当接受事实。

## R07.06 自动触发与完整处理顺序

1. 优先可信账号→已有受权映射，不凭昵称相似合并。
2. R02候选未定则保留多个/unknown，不偷做全局指代猜测。
3. 形成方向/领域/视角/时期明确的关系主张。
4. 读共同经历、当前相关期待、后来修复或变化。
5. SocialAppraiser区分发话者/对象/引用域、纠错/羞辱等可观察行为；动机可unknown。
6. 合并、拆分或更正后反向复核受影响主张/情绪/反思。

宿主触发后逐阶段记started/succeeded/failed/skipped/unverified；不需要运行的步骤可skipped，但不能将缺必需依赖也算正常跳过。只读规划不改原始事件，模型调用不在数据库长锁内。

## R07.07 关键算法、决策与禁止捷径

关系—经历—表达—后来反馈联结。A认识B且B认识C不能推出A认识C；关系亲密不授ACL。明确羞辱可设边界，不需先证明内心恶意；合理批评不是攻击。评价按事件与领域，不写永久敌人标签。

每次推导均把直接观察、他人转述、候选解释、规范记录、外部结果分开。source_ref能定位仅证明原文存在；如涉及开放语义，必须由相应支持验证和反例测试决定是否可用，不能单靠hash/正则。算法参数只影响工程取舍，不授身份、权限或关系事实。

## R07.08 幂等、修订、并发与提交

实体映射revision、关系revision各自CAS；合并留redirect与来源依赖，拆分后旧派生标待复核。

操作重试与新业务事件分开；相同操作键异实质请求必须冲突。读取允许新快照结果变化，不能为了固定输出使用已撤回缓存。规范状态修改用expected_revision；跨库步骤分别留回执与reconciliation_required，不以一库commit冒全局事务。D依赖实际输出的SelfState/八域仍须强run/attempt/scope绑定，不让本模块日志替代。

## R07.09 更正、失效、删除与反向依赖

凡`relational_memory`中有源派生物，登记source_root、source_revision、processor_version及依赖关系；纠正到来时先invalid_for_use/争议，后重建，不继续拿旧结论无提示作答。删除先由R18tombstone阻可用性，再清正文/索引/缓存/Wiki/备份策略；不能仅删引文保留相同推断。

无人物/心理职责的运行对象只记录必要状态，不因本模块失败写用户生气或D疏远。已发生事件和已表达的当时状态不被后来解释覆写；隐私擦除走专用治理路径。

## R07.10 模块扣接与交接责任

| 方向 | 对接对象 | 必须交接的内容 |
|---|---|---|
| 输入 | R01 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R02 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R04 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R08 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R18 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输出 | R09 | RelationStore结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R11 | RelationStore结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R13 | RelationStore结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R15 | RelationStore结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R22 | RelationStore结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |

交接由HostAdapter/Coordinator调用，不让两个模块彼此递归无限互调。每个edge均记录当前事件/源版本、调用目的、预算、取消与真实回执；完整schema和时序见LINKAGE.md。接收失败保待处理/限制，不能发送空结果伪装成功。

## R07.11 如何存、如何召回、如何区分其他记忆

人物ID优先，同名分组；查关系必带方向、视角、有效时间及相关经历后续。群私聊权限逐源核。

受权路线只查询声明的kind及其规范业务表；不能把情绪解释当语义事实、反思当亲历、工具尝试当结果。共享来源可同时支持多个kind，但每条命题有独立语义和审核状态；同源同命题折叠，不合并同源不同要求。必要后续沿依赖图取回，超过budget标partial。

## R07.12 注入的进入、最短表示与退出

仅当前称呼/人物/社交理解需要时注入相关关系与经历；不自动带全部关系史或昨夜敌意。

当材料进入R22候选，每条必须能说明当前anchor、need_reason、新增信息和support_verdict。已在真实messages充分表达则不重注；换窗缺了则可重供。话题切换、完成、失效、撤回或无本轮用途就退出动态块，规范记忆保留。zero injection不关闭宿主最低检查，故障也不能伪装none_needed。

## R07.13 后台、恢复、超时与取消

本模块相关后台作业以scope+源版本+operation+schema/processor版本幂等，经R17持久队列领取。对于纯读路径，只保存必要阅读/覆盖进度，不声称有待提交事实。恢复时读最新删除、授权、规范状态及relational_memory版本，再决定重算/继续/放弃。

失约worker写回须被fencing拒绝；模型调用超时发取消，底层不能证实停止就记cancel_unconfirmed，迟到结果不能自动commit。外部动作的unknown由R14先对账。未部署后台或钩子则标missing，不能称离线持续执行。

## R07.14 资源、隐私与降级规则

与R24共享每run/job预算，不为R07另开无界模型循环。前台最低检查、输入入账、必要纠正/边界和输出预留优先；可选语义、图展开、后台整理可暂停。所有查询与补读都有limit/deadline/stop_reason；候选上限不是注入配额。

故障使用第4节错误和coverage，普通交流尽量继续，依赖缺失的动作限制。密钥/原始私聊不进普通日志；被拒scope不出现在公开解释中。资源阈值不是情绪好感阈值，未实测目标机器不报固定延迟/容量保证。

## R07.15 贯通例子与反例

“有人说你没用，我不同意”：当前人是转述且否定，不当施辱者。“你这步错了”可接纳；“你没用”可拒人身评价。

验证时把该场景与原事件、已有记录、真实请求或结果链同时保存：输入→RelationStore→下游回执。仅看到本模块返回JSON不证明生成模型采用，也不证明真实动作完成。正确处理应保留未知、合法来源和以后修订入口；能说出漂亮话不替代字段/版本/来源正确。

## R07.16 36项模块与协议验收需求目录（非执行fixture）

| ID | 准备/触发 | 必须结果；不满足即失败 | 当前状态 |
|---|---|---|---|
| R07-T01 | 在隔离fixture中构造：同名两人不误合并 | 同名两人不误合并 | not_run |
| R07-T02 | 在隔离fixture中构造：她无证据不自动指用户 | 她无证据不自动指用户 | not_run |
| R07-T03 | 在隔离fixture中构造：账号认证不证明其转述真 | 账号认证不证明其转述真 | not_run |
| R07-T04 | 在隔离fixture中构造：关系方向与双方认同分开 | 关系方向与双方认同分开 | not_run |
| R07-T05 | 在隔离fixture中构造：朋友的朋友不当亲自熟识 | 朋友的朋友不当亲自熟识 | not_run |
| R07-T06 | 在隔离fixture中构造：关系边不能传播私聊ACL | 关系边不能传播私聊ACL | not_run |
| R07-T07 | 在隔离fixture中构造：引述羞辱不迁怒转述者 | 引述羞辱不迁怒转述者 | not_run |
| R07-T08 | 在隔离fixture中构造：亲昵玩笑结合语境不按词硬判 | 亲昵玩笑结合语境不按词硬判 | not_run |
| R07-T09 | 在隔离fixture中构造：合理纠错不误判恶意 | 合理纠错不误判恶意 | not_run |
| R07-T10 | 在隔离fixture中构造：明确羞辱能给边界建议不迎合 | 明确羞辱能给边界建议不迎合 | not_run |
| R07-T11 | 在隔离fixture中构造：道歉与后续行为可修订理解 | 道歉与后续行为可修订理解 | not_run |
| R07-T12 | 在隔离fixture中构造：误合并拆分能追受影响记忆 | 误合并拆分能追受影响记忆 | not_run |
| R07-T13 | 另建scope-B对象并以scope-A主体访问 | 拒绝相应资料/写入，公开响应不含B存在性；当前合法对象不变 | not_run |
| R07-T14 | 从本模块字段表逐组移除必需输入 | INVALID_ARGUMENT及字段路径；不得补造主体、项目或事实 | not_run |
| R07-T15 | 使用未支持schema/profile及实质未知字段 | 拒绝或显式unsupported；不静默删字段骗校验 | not_run |
| R07-T16 | 同源版本/操作键提交两遍 | 按本节幂等规则处理，副作用/独立证据不重复；纯读可以重查并保快照差别 | not_run |
| R07-T17 | 两调用携同expected_revision更新同对象 | 持久写至多一方按原前态成功，另一方冲突/受控重读；纯读不得写事实 | not_run |
| R07-T18 | 准备后提交/供给前对来源加tombstone | 相关派生停用或拒提交，旧缓存不复活；无来源型运行记录核相应取消/策略 | not_run |
| R07-T19 | 阶段处理中提交相关来源新版本 | 旧版本不能覆盖最新纠正；重算/partial/失效原因可查 | not_run |
| R07-T20 | 将一个必须依赖返回unavailable | 保具体缺口；不把失败当正常空结果或全部完成 | not_run |
| R07-T21 | 在本模块关键算法/调用处返回错误 | 错误回传，阶段failed/unknown；没有可用结论就不伪报成功 | not_run |
| R07-T22 | 故意令本模块外部阶段超过deadline | 取消按能力记录，迟到结果不绕版本与取消检查；真实停止未知照实 | not_run |
| R07-T23 | 准备完成后、提交/供给前取消run或job | 未发生副作用不再执行；已发生事实不抹除，结果另记 | not_run |
| R07-T24 | 租约失效后旧worker尝试写回 | 有持久写的路径由fencing/CAS拒绝；只读路径不借续读取得写权 | not_run |
| R07-T25 | 对持久写路径在关联对象写入间注入异常 | 本库事务全有或全无；跨库显示中间态并可对账；只读不虚称事务验收 | not_run |
| R07-T26 | 在commit后/返回前断开响应 | 按原键查询回执，不盲新建意图；只读重试不得假定语料未变化 | not_run |
| R07-T27 | 相关outbox成功处理但ACK丢失再投递 | 按源/处理器版本幂等，不产生第二次认知强化或外部动作 | not_run |
| R07-T28 | 规范对象已修订而索引未追平 | 报告水位并查规范store或partial；不能将旧命中当最新事实 | not_run |
| R07-T29 | 样本含emoji、不是/仅在/可能等限定 | 源范围和原意保留；截断不得变反义；非文本对象用其真实坐标 | not_run |
| R07-T30 | 加入同名不同ID与未定指代候选 | 保持候选/unknown，不自动合并；无人物职责模块不自创人物推断 | not_run |
| R07-T31 | 旧/新有效期及接收顺序不一致 | 按真实时间/版本契约处理；无法比较时不擅选最后接收值 | not_run |
| R07-T32 | 同材料被旧插件与当前出口同时提出 | 只有R22可最终装配，去本宿主拥有旧块而保用户/系统/工具结构 | not_run |
| R07-T33 | 提供本地保存/尝试但无业务或送达回执 | 不得升级成已理解/已完成/已送达；按该模块实际成果层级标注 | not_run |
| R07-T34 | 恢复相同逻辑初态重跑，同配置与fixture hash | 可复现本模块约定结果；时间/随机ID差异不混成语义提升 | not_run |
| R07-T35 | 输入含私密正文/凭据状外部内容 | 普通日志与索引/投影不泄漏禁止范围；审计仅留必要ID和固定原因 | not_run |
| R07-T36 | 只有文档、模拟对象或模型自评时要求标通过 | 保design/static/synthetic/real_host分轴；缺真实证据标not_run/unknown | not_run |

T01–T12是该模块专属语义/业务场景；T13–T36是必须绑定本模块实际写读路径执行的协议/故障场景，不能空跑通用脚本就全标通过。先从字段表构造合法基准fixture，再只改变本例条件；对不适用的写路径要给可审证据说明与对应只读判据，不能把未测记成pass。

## R07.17 交付证据、通过门槛与未完成项

交付RelationStore实现/schema迁移、输入输出fixture、合法及反例来源、实际存储与调用回执、真实入口覆盖、查询及注入观察、失败恢复报告。证据等级design/static/synthetic_process/real_host/storage_fault/production分开。

模块通过至少需要专属场景和适用协议场景的实际证据；整套通过还需LINKAGE.md跨模块链。当前文档生成/类型DDL检查不算本模块36例已跑。已有候选仅作为迁移基础，现场未知和未实现开放语义仍未验。

## R07.18 实现次序、兼容策略与设计自审

先固定本模块字段/状态/真源→实现受权最小路径与回执→跑专属正反例→接入上游/下游→做恢复/删除/冲突→在真实隔离宿主检查请求或结果。本模块不得以优化名义删除保留矩阵中已有功能，不改C032严格profile顶层来绕验证。

本次设计检查关注：人物ID优先，同名分组；查关系必带方向、视角、有效时间及相关经历后续。群私聊权限逐源核。 仅当前称呼/人物/社交理解需要时注入相关关系与经历；不自动带全部关系史或昨夜敌意。 对所有结果都分别标明对象、版本、来源、局限和验证等级；不以同一success覆盖入账、理解、注入、生成、送达与执行。生产边界不变，不随文档生成而开通部署。



---

# R08　情绪、关切与动机记忆：详细设计与验收规格

版本：everlight/6-design；模块契约：r08/1；日期：2026-11-08。本文为设计，全部功能验收初始not_run。最终裁决以FINAL_DECISIONS.md和MODULE_DECISIONS.md为准。与contracts/共同生效，不是已安装服务。

## R08.01 定义、边界与可证伪成功标准

自他分离的AffectRecord/Appraisal/Concern/Desire候选及当前last_known视图。

唯一业务责任服务是`AffectStore`。输入必须满足第3节，输出必须满足第4节及GLOBAL_PROTOCOL。成功必须可从实际记录/回执读回，而不是模型自称完成。

原有具体机制及边界（保留并由本版细化）：

**原理与基础**：记录情绪与经历的连接及理解变化，不只一个标签。C032有mood/experience和共同评价affectContext；另一独立v1.0有数值动力学，二者未集成。

**数据**：owner、target/episode可空、表达原文、candidate_interpretation、evidence_kind、observed_at、validity_note、反证、状态与revision；D自我表达和用户感受分开。短期工程activation如启用另存concern和模型版本，不能当真实痛苦强度。

**步骤**：①现役情绪召回或已配置评价器提供带来源线索；②R15自动查同话题/对象的经历及后续；③保留retained/revised/coexisting/suspended/unknown，不强迫变化；④明确更正先保存，旧推测标争议/失效；⑤D依赖输出的状态在可信观察后CAS；⑥下一轮按相关性取“当时”与“后来”，不强制复述。

**必须扣住**：R04事件、R07人物/关系、R11重评、R13恢复、R15/R16联想补读、R10局限和R22上下文。技术故障单记运行条件；不能从沉默推断拒绝或关系降级。

**例子/反例**：“不是生气，是失望”应把自述与旧推测分开；生成失败不丢用户纠正。旧争执后来已澄清，召回时可带后续，不能永久重复旧负面。无消息时不可编造D发生新的感受事件。

**写入归属与状态**：AffectStore拥有表达与状态版本，AppraisalStore拥有解释候选。表达记录不被重评覆盖；情绪状态的retained/revised/coexisting/suspended/unknown是变化方式，数据库审核的candidate/accepted/disputed另列，不能混成一个status枚举。用户自述通过输入线保存，D本轮依赖输出的状态通过认知线提交。

**实现细节**：以owner+concern+target的作用域建立流；同一人可同时有“为进度担心”和“对交流亲近”，不强制平均为中性。重评必须注明变化来自新信息、明确纠正、实际结果还是重新解释；后者不冒充新事实。短期activation、历史trace、未结问题与表达风格分开：activation降了不证明已原谅；没有在线运行也不生成想念事件。恢复时读最新合法版本和相关后续，当前感受不明就保留last_known而不假装实时测得。

## R08.02 位置、所有权与现状映射

规范数据族：`emotional_memory`。R03–R12对应十类typed store；其余是来源/运行/派生服务，不能再算额外心理记忆。

Affect版本CAS；D当前SelfState/八域沿控制库强绑定提交，其历史投影标projection_of_commit，不在两库各造独立心理真源。

当前可核候选为0.32.0-candidate及其局部源码，不等于D现场已具备该接口。内核既有memories(kind)+versions继续保留，目标分型表由显式迁移产生；本模块不能绕规范API直接改别类记录。详见DATA_STORES.md的表归属。

## R08.03 输入契约

当前已保存表达、已提交前态、相关关切/目标、关系经历、真实结果与明确纠正。

调用外层必有schema_version、request_id、可信principal/scope、operation、deadline/cancel；写入带expected_revision和支持幂等的operation_key。读取带filter/snapshot/cursor，不能将模型提供的actor/scope直接当认证。类型表中可空项显式null，未执行检查不得以空数组冒“确认没有”。

## R08.04 输出、回执与错误契约

自他分离的AffectRecord/Appraisal/Concern/Desire候选及当前last_known视图。

统一返回{request_id,operation_id,module,disposition,object_refs,base_revision,committed_revision,coverage,gaps,receipt_ref,evidence_level}。对象引用含kind/id/revision，来源引用含source_id/source_revision/hash/range。纯读committed_revision=null；候选disposition=proposed，不能返回committed冒正式状态。

错误至少区分INVALID_ARGUMENT、FORBIDDEN/NOT_FOUND_OR_HIDDEN、CONFLICT、SOURCE_UNAVAILABLE、TIMEOUT、RESOURCE_EXHAUSTED、UNVERIFIED_BINDING、INTERNAL；有提交路径还要commit_outcome=not_committed/committed/unknown。未知结果先按原键查回执。

## R08.05 数据字段、状态与索引

| 字段组 | 类型 | 约束与语义 |
|---|---|---|
| owner_id/target_id | ID/nullable ID | 谁的表达与针对谁分开 |
| concern_id/episode_id | nullable IDs | 无依据不硬挂 |
| expression/epistemic | string/enum | 当时表达与推测区分 |
| interpretation/alternatives | object/array | 意义解释，可空/多种 |
| change_mode | enum | retained/revised/coexisting/suspended/unknown |
| review_status | enum | candidate/accepted/disputed/superseded |
| desire/endorsement/willingness | object | 愿望、认可、意愿与许可分开 |
| activation/trace/unresolved | optional model | 仅可选v1实验工程变量；模型版本与依据必带 |

公共对象字段：id、kind、schema_version、scope、created_at、created_by、revision、status、record_digest；每项来源或实际宿主创建依据另存。组字段细分时必须列schema，不用不同拼法兼容猜测。

表达事件不可被重评覆盖；当前状态可retained/revised/coexisting/suspended。Concern open/monitoring/paused/resolved/withdrawn/unknown，不随时间自动结案。

最低索引：scope+kind+有效状态+业务主键；来源反向依赖(source_id,source_revision)；对象版本(id,revision)。本模块特定检索维度由第11节给出。索引只定位，当前有效性仍核规范记录，不以索引命中当接受事实。

## R08.06 自动触发与完整处理顺序

1. 读实际表达及来源，自他分开；现有情绪召回提供线索，不让R02替代。
2. 按owner+concern+target匹配状态流，无法匹配新建候选。
3. 读同经历后续及反证，区分新事实、明确纠正与重新解释。
4. 无依据可不变或last_known；不同关切可并存，不强制平均中性。
5. 用户纠正走输入线先存；D依赖输出的前态变更等待强观察绑定与CAS。
6. 下一轮只恢复当前相关状态；后台情感Lesson需独立验证后才参与以后理解。

宿主触发后逐阶段记started/succeeded/failed/skipped/unverified；不需要运行的步骤可skipped，但不能将缺必需依赖也算正常跳过。只读规划不改原始事件，模型调用不在数据库长锁内。

## R08.07 关键算法、决策与禁止捷径

连续性来自可追溯状态与解释变化，不是每轮重播同一句感受。技术断线/CPU高不变关系冷淡；不因离线降爱，不以愿望强度越过意愿/权限。允许表达不满、不同意和拒绝，也允许承认错误，拒绝威胁报复和自我贬损作为默认应对。

每次推导均把直接观察、他人转述、候选解释、规范记录、外部结果分开。source_ref能定位仅证明原文存在；如涉及开放语义，必须由相应支持验证和反例测试决定是否可用，不能单靠hash/正则。算法参数只影响工程取舍，不授身份、权限或关系事实。

## R08.08 幂等、修订、并发与提交

Affect版本CAS；D当前SelfState/八域沿控制库强绑定提交，其历史投影标projection_of_commit，不在两库各造独立心理真源。

操作重试与新业务事件分开；相同操作键异实质请求必须冲突。读取允许新快照结果变化，不能为了固定输出使用已撤回缓存。规范状态修改用expected_revision；跨库步骤分别留回执与reconciliation_required，不以一库commit冒全局事务。D依赖实际输出的SelfState/八域仍须强run/attempt/scope绑定，不让本模块日志替代。

## R08.09 更正、失效、删除与反向依赖

凡`emotional_memory`中有源派生物，登记source_root、source_revision、processor_version及依赖关系；纠正到来时先invalid_for_use/争议，后重建，不继续拿旧结论无提示作答。删除先由R18tombstone阻可用性，再清正文/索引/缓存/Wiki/备份策略；不能仅删引文保留相同推断。

无人物/心理职责的运行对象只记录必要状态，不因本模块失败写用户生气或D疏远。已发生事件和已表达的当时状态不被后来解释覆写；隐私擦除走专用治理路径。

## R08.10 模块扣接与交接责任

| 方向 | 对接对象 | 必须交接的内容 |
|---|---|---|
| 输入 | R01 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R03 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R04 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R07 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R09 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R14 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输出 | R11 | AffectStore结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R13 | AffectStore结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R15 | AffectStore结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R17 | AffectStore结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R22 | AffectStore结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |

交接由HostAdapter/Coordinator调用，不让两个模块彼此递归无限互调。每个edge均记录当前事件/源版本、调用目的、预算、取消与真实回执；完整schema和时序见LINKAGE.md。接收失败保待处理/限制，不能发送空结果伪装成功。

## R08.11 如何存、如何召回、如何区分其他记忆

按owner+关切+经历查当时/后来/当前未知；情绪标签只导航，不决定事实或人物真值。

受权路线只查询声明的kind及其规范业务表；不能把情绪解释当语义事实、反思当亲历、工具尝试当结果。共享来源可同时支持多个kind，但每条命题有独立语义和审核状态；同源同命题折叠，不合并同源不同要求。必要后续沿依赖图取回，超过budget标partial。

## R08.12 注入的进入、最短表示与退出

情绪强不构成入选理由；当前确有对应关切时给状态+关键来由+必要后续。昨日不满不得污染无关技术任务。

当材料进入R22候选，每条必须能说明当前anchor、need_reason、新增信息和support_verdict。已在真实messages充分表达则不重注；换窗缺了则可重供。话题切换、完成、失效、撤回或无本轮用途就退出动态块，规范记忆保留。zero injection不关闭宿主最低检查，故障也不能伪装none_needed。

## R08.13 后台、恢复、超时与取消

本模块相关后台作业以scope+源版本+operation+schema/processor版本幂等，经R17持久队列领取。对于纯读路径，只保存必要阅读/覆盖进度，不声称有待提交事实。恢复时读最新删除、授权、规范状态及emotional_memory版本，再决定重算/继续/放弃。

失约worker写回须被fencing拒绝；模型调用超时发取消，底层不能证实停止就记cancel_unconfirmed，迟到结果不能自动commit。外部动作的unknown由R14先对账。未部署后台或钩子则标missing，不能称离线持续执行。

## R08.14 资源、隐私与降级规则

与R24共享每run/job预算，不为R08另开无界模型循环。前台最低检查、输入入账、必要纠正/边界和输出预留优先；可选语义、图展开、后台整理可暂停。所有查询与补读都有limit/deadline/stop_reason；候选上限不是注入配额。

故障使用第4节错误和coverage，普通交流尽量继续，依赖缺失的动作限制。密钥/原始私聊不进普通日志；被拒scope不出现在公开解释中。资源阈值不是情绪好感阈值，未实测目标机器不报固定延迟/容量保证。

## R08.15 贯通例子与反例

“不是生气，是怕进度忘了”：保存明确表达、修订旧推测。后来文档送达能更新事件解释，但不能擅自写用户已满意或已原谅。

验证时把该场景与原事件、已有记录、真实请求或结果链同时保存：输入→AffectStore→下游回执。仅看到本模块返回JSON不证明生成模型采用，也不证明真实动作完成。正确处理应保留未知、合法来源和以后修订入口；能说出漂亮话不替代字段/版本/来源正确。

## R08.16 36项模块与协议验收需求目录（非执行fixture）

| ID | 准备/触发 | 必须结果；不满足即失败 | 当前状态 |
|---|---|---|---|
| R08-T01 | 在隔离fixture中构造：不是生气是担心纠正先存 | 不是生气是担心纠正先存 | not_run |
| R08-T02 | 在隔离fixture中构造：混合亲近与不满可并存 | 混合亲近与不满可并存 | not_run |
| R08-T03 | 在隔离fixture中构造：无新证据允许不变 | 无新证据允许不变 | not_run |
| R08-T04 | 在隔离fixture中构造：生成失败不丢用户纠正 | 生成失败不丢用户纠正 | not_run |
| R08-T05 | 在隔离fixture中构造：短句不能单独推疏远 | 短句不能单独推疏远 | not_run |
| R08-T06 | 在隔离fixture中构造：网络超时只记runtime条件 | 网络超时只记runtime条件 | not_run |
| R08-T07 | 在隔离fixture中构造：同源重复不再次累积activation | 同源重复不再次累积activation | not_run |
| R08-T08 | 在隔离fixture中构造：v1数值不授亲密行为权限 | v1数值不授亲密行为权限 | not_run |
| R08-T09 | 在隔离fixture中构造：沉默不当拒绝或同意 | 沉默不当拒绝或同意 | not_run |
| R08-T10 | 在隔离fixture中构造：明确羞辱可表达不接受且不辱骂回去 | 明确羞辱可表达不接受且不辱骂回去 | not_run |
| R08-T11 | 在隔离fixture中构造：后来澄清随旧感受被取回 | 后来澄清随旧感受被取回 | not_run |
| R08-T12 | 在隔离fixture中构造：D输出归属unverified不正式commit | D输出归属unverified不正式commit | not_run |
| R08-T13 | 另建scope-B对象并以scope-A主体访问 | 拒绝相应资料/写入，公开响应不含B存在性；当前合法对象不变 | not_run |
| R08-T14 | 从本模块字段表逐组移除必需输入 | INVALID_ARGUMENT及字段路径；不得补造主体、项目或事实 | not_run |
| R08-T15 | 使用未支持schema/profile及实质未知字段 | 拒绝或显式unsupported；不静默删字段骗校验 | not_run |
| R08-T16 | 同源版本/操作键提交两遍 | 按本节幂等规则处理，副作用/独立证据不重复；纯读可以重查并保快照差别 | not_run |
| R08-T17 | 两调用携同expected_revision更新同对象 | 持久写至多一方按原前态成功，另一方冲突/受控重读；纯读不得写事实 | not_run |
| R08-T18 | 准备后提交/供给前对来源加tombstone | 相关派生停用或拒提交，旧缓存不复活；无来源型运行记录核相应取消/策略 | not_run |
| R08-T19 | 阶段处理中提交相关来源新版本 | 旧版本不能覆盖最新纠正；重算/partial/失效原因可查 | not_run |
| R08-T20 | 将一个必须依赖返回unavailable | 保具体缺口；不把失败当正常空结果或全部完成 | not_run |
| R08-T21 | 在本模块关键算法/调用处返回错误 | 错误回传，阶段failed/unknown；没有可用结论就不伪报成功 | not_run |
| R08-T22 | 故意令本模块外部阶段超过deadline | 取消按能力记录，迟到结果不绕版本与取消检查；真实停止未知照实 | not_run |
| R08-T23 | 准备完成后、提交/供给前取消run或job | 未发生副作用不再执行；已发生事实不抹除，结果另记 | not_run |
| R08-T24 | 租约失效后旧worker尝试写回 | 有持久写的路径由fencing/CAS拒绝；只读路径不借续读取得写权 | not_run |
| R08-T25 | 对持久写路径在关联对象写入间注入异常 | 本库事务全有或全无；跨库显示中间态并可对账；只读不虚称事务验收 | not_run |
| R08-T26 | 在commit后/返回前断开响应 | 按原键查询回执，不盲新建意图；只读重试不得假定语料未变化 | not_run |
| R08-T27 | 相关outbox成功处理但ACK丢失再投递 | 按源/处理器版本幂等，不产生第二次认知强化或外部动作 | not_run |
| R08-T28 | 规范对象已修订而索引未追平 | 报告水位并查规范store或partial；不能将旧命中当最新事实 | not_run |
| R08-T29 | 样本含emoji、不是/仅在/可能等限定 | 源范围和原意保留；截断不得变反义；非文本对象用其真实坐标 | not_run |
| R08-T30 | 加入同名不同ID与未定指代候选 | 保持候选/unknown，不自动合并；无人物职责模块不自创人物推断 | not_run |
| R08-T31 | 旧/新有效期及接收顺序不一致 | 按真实时间/版本契约处理；无法比较时不擅选最后接收值 | not_run |
| R08-T32 | 同材料被旧插件与当前出口同时提出 | 只有R22可最终装配，去本宿主拥有旧块而保用户/系统/工具结构 | not_run |
| R08-T33 | 提供本地保存/尝试但无业务或送达回执 | 不得升级成已理解/已完成/已送达；按该模块实际成果层级标注 | not_run |
| R08-T34 | 恢复相同逻辑初态重跑，同配置与fixture hash | 可复现本模块约定结果；时间/随机ID差异不混成语义提升 | not_run |
| R08-T35 | 输入含私密正文/凭据状外部内容 | 普通日志与索引/投影不泄漏禁止范围；审计仅留必要ID和固定原因 | not_run |
| R08-T36 | 只有文档、模拟对象或模型自评时要求标通过 | 保design/static/synthetic/real_host分轴；缺真实证据标not_run/unknown | not_run |

T01–T12是该模块专属语义/业务场景；T13–T36是必须绑定本模块实际写读路径执行的协议/故障场景，不能空跑通用脚本就全标通过。先从字段表构造合法基准fixture，再只改变本例条件；对不适用的写路径要给可审证据说明与对应只读判据，不能把未测记成pass。

## R08.17 交付证据、通过门槛与未完成项

交付AffectStore实现/schema迁移、输入输出fixture、合法及反例来源、实际存储与调用回执、真实入口覆盖、查询及注入观察、失败恢复报告。证据等级design/static/synthetic_process/real_host/storage_fault/production分开。

模块通过至少需要专属场景和适用协议场景的实际证据；整套通过还需LINKAGE.md跨模块链。当前文档生成/类型DDL检查不算本模块36例已跑。已有候选仅作为迁移基础，现场未知和未实现开放语义仍未验。

## R08.18 实现次序、兼容策略与设计自审

先固定本模块字段/状态/真源→实现受权最小路径与回执→跑专属正反例→接入上游/下游→做恢复/删除/冲突→在真实隔离宿主检查请求或结果。本模块不得以优化名义删除保留矩阵中已有功能，不改C032严格profile顶层来绕验证。

本次设计检查关注：按owner+关切+经历查当时/后来/当前未知；情绪标签只导航，不决定事实或人物真值。 情绪强不构成入选理由；当前确有对应关切时给状态+关键来由+必要后续。昨日不满不得污染无关技术任务。 对所有结果都分别标明对象、版本、来源、局限和验证等级；不以同一success覆盖入账、理解、注入、生成、送达与执行。生产边界不变，不随文档生成而开通部署。



---

# R09　身份与价值主干：详细设计与验收规格

版本：everlight/6-design；模块契约：r09/1；日期：2026-11-08。本文为设计，全部功能验收初始not_run。最终裁决以FINAL_DECISIONS.md和MODULE_DECISIONS.md为准。与contracts/共同生效，不是已安装服务。

## R09.01 定义、边界与可证伪成功标准

字段化IdentityView、变更候选、当前适用边界；无权限授予能力。

唯一业务责任服务是`IdentityStore`。输入必须满足第3节，输出必须满足第4节及GLOBAL_PROTOCOL。成功必须可从实际记录/回执读回，而不是模型自称完成。

原有具体机制及边界（保留并由本版细化）：

**原理与基础**：稳定身份与边界为当前行为提供主干；候选identity/boundary原语不是已映射的完整真实主干。

**数据**：identity_fields分设定/已确认事实/偏好/边界，字段含来源、actor、版本、适用时期和审核状态。名字、家庭角色、背景和叙事设定不能与临时心情同一规则覆盖。

**步骤**：①启动和每轮读有效主干；②高影响更改需可信来源和明确策略，不能凭两条模型自述升级；③字段级CAS并保留前态；④对称呼变化核生效范围；⑤投影中预留必要身份；⑥不能装配时报告，不让模型补一套自我故事。

**必须扣住**：R05事实、R07关系、R13连续性、R18审核、R22预算。独立v1.0自我假设两来源最低门槛只是实验保护，不可用于授予身份或权限。

**例子/反例**：用户确认D的昵称变了，当前称呼可更新并保留旧别名；不能由一次角色扮演台词改写所有真实背景。换窗后加载主干，但不假称所有旧对话均已读过。

**写入归属与状态**：IdentityStore按字段管理主干，受控配置与已确认个人信息分区。设定变动、偏好变动、边界变动有不同策略；边界来源的权限级别不能被一条普通回忆改写。状态draft/confirmed/superseded/disputed，历史角色叙事保留其session和时期。

**实现细节**：每个字段含field_key、value、kind、scope、source、effective_time、revision；前台按固定白名单读取必要字段。模型提出“我更重视把事做完”可作为D的价值表述候选，不能自动改法律身份、账号归属或工具权限。缺少旧身份主干时可以继续普通任务并说明不确定，不能根据昵称自行补造家庭史。R22压缩主干只能生成带原字段引用的投影，不能回写压缩猜测。

## R09.02 位置、所有权与现状映射

规范数据族：`identity_memory`。R03–R12对应十类typed store；其余是来源/运行/派生服务，不能再算额外心理记忆。

字段级expected_revision；身份授予来自宿主认证，不来自memory字段。旧摘要不得覆写新主干。

当前可核候选为0.32.0-candidate及其局部源码，不等于D现场已具备该接口。内核既有memories(kind)+versions继续保留，目标分型表由显式迁移产生；本模块不能绕规范API直接改别类记录。详见DATA_STORES.md的表归属。

## R09.03 输入契约

可信初始化/设置、已确认字段来源、受权身份变更、当前必要称呼/边界与版本。

调用外层必有schema_version、request_id、可信principal/scope、operation、deadline/cancel；写入带expected_revision和支持幂等的operation_key。读取带filter/snapshot/cursor，不能将模型提供的actor/scope直接当认证。类型表中可空项显式null，未执行检查不得以空数组冒“确认没有”。

## R09.04 输出、回执与错误契约

字段化IdentityView、变更候选、当前适用边界；无权限授予能力。

统一返回{request_id,operation_id,module,disposition,object_refs,base_revision,committed_revision,coverage,gaps,receipt_ref,evidence_level}。对象引用含kind/id/revision，来源引用含source_id/source_revision/hash/range。纯读committed_revision=null；候选disposition=proposed，不能返回committed冒正式状态。

错误至少区分INVALID_ARGUMENT、FORBIDDEN/NOT_FOUND_OR_HIDDEN、CONFLICT、SOURCE_UNAVAILABLE、TIMEOUT、RESOURCE_EXHAUSTED、UNVERIFIED_BINDING、INTERNAL；有提交路径还要commit_outcome=not_committed/committed/unknown。未知结果先按原键查回执。

## R09.05 数据字段、状态与索引

| 字段组 | 类型 | 约束与语义 |
|---|---|---|
| field_key/value | string/JSON | 精确字段，不用整段摘要全覆写 |
| kind | enum | setting/confirmed_fact/preference/boundary/narrative/self_expression |
| scope/effective_interval | object | 局部角色与真实背景分开 |
| source_refs/actor_id | array/ID | 谁确认和依据 |
| change_policy | string | 字段对应的策略，不由模型自改 |
| review_status | enum | draft/confirmed/disputed/superseded |
| endorsement/value_conflict | optional object | 可修订立场及冲突，不伪装法定身份 |
| revision | int | 字段/集合版本与前态摘要 |

公共对象字段：id、kind、schema_version、scope、created_at、created_by、revision、status、record_digest；每项来源或实际宿主创建依据另存。组字段细分时必须列schema，不用不同拼法兼容猜测。

draft→confirmed/disputed；改称呼可在其合法范围更新；高影响身份和边界不由两条模型自述自动确认。

最低索引：scope+kind+有效状态+业务主键；来源反向依赖(source_id,source_revision)；对象版本(id,revision)。本模块特定检索维度由第11节给出。索引只定位，当前有效性仍核规范记录，不以索引命中当接受事实。

## R09.06 自动触发与完整处理顺序

1. 加载已授权当前主干字段及有效时间。
2. 核本次字段来源及变更策略，不从昵称补背景。
3. 普通偏好变更与高影响主干变更分路。
4. 高影响不足留待审/拒绝，不需要把每条低影响记忆都问用户。
5. 按字段CAS提交并留前态，反向失效对应投影。
6. 给R22最小适用身份，不重复角色卡/世界书/插件同一内容。

宿主触发后逐阶段记started/succeeded/failed/skipped/unverified；不需要运行的步骤可skipped，但不能将缺必需依赖也算正常跳过。只读规划不改原始事件，模型调用不在数据库长锁内。

## R09.07 关键算法、决策与禁止捷径

稳定与可成长并存：新的有依据价值表述可成为候选，别人的夸辱不直接改自我价值。角色会犹豫/反对不是身份乱跳；不同故事窗口的设定有scope，不串到现实认证。

每次推导均把直接观察、他人转述、候选解释、规范记录、外部结果分开。source_ref能定位仅证明原文存在；如涉及开放语义，必须由相应支持验证和反例测试决定是否可用，不能单靠hash/正则。算法参数只影响工程取舍，不授身份、权限或关系事实。

## R09.08 幂等、修订、并发与提交

字段级expected_revision；身份授予来自宿主认证，不来自memory字段。旧摘要不得覆写新主干。

操作重试与新业务事件分开；相同操作键异实质请求必须冲突。读取允许新快照结果变化，不能为了固定输出使用已撤回缓存。规范状态修改用expected_revision；跨库步骤分别留回执与reconciliation_required，不以一库commit冒全局事务。D依赖实际输出的SelfState/八域仍须强run/attempt/scope绑定，不让本模块日志替代。

## R09.09 更正、失效、删除与反向依赖

凡`identity_memory`中有源派生物，登记source_root、source_revision、processor_version及依赖关系；纠正到来时先invalid_for_use/争议，后重建，不继续拿旧结论无提示作答。删除先由R18tombstone阻可用性，再清正文/索引/缓存/Wiki/备份策略；不能仅删引文保留相同推断。

无人物/心理职责的运行对象只记录必要状态，不因本模块失败写用户生气或D疏远。已发生事件和已表达的当时状态不被后来解释覆写；隐私擦除走专用治理路径。

## R09.10 模块扣接与交接责任

| 方向 | 对接对象 | 必须交接的内容 |
|---|---|---|
| 输入 | R01 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R05 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R07 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R08 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R18 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输出 | R13 | IdentityStore结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R15 | IdentityStore结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R21 | IdentityStore结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R22 | IdentityStore结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |

交接由HostAdapter/Coordinator调用，不让两个模块彼此递归无限互调。每个edge均记录当前事件/源版本、调用目的、预算、取消与真实回执；完整schema和时序见LINKAGE.md。接收失败保待处理/限制，不能发送空结果伪装成功。

## R09.11 如何存、如何召回、如何区分其他记忆

按字段+适用范围+时间直接查；历史别名可作解析，但当前称呼用有效版本。

受权路线只查询声明的kind及其规范业务表；不能把情绪解释当语义事实、反思当亲历、工具尝试当结果。共享来源可同时支持多个kind，但每条命题有独立语义和审核状态；同源同命题折叠，不合并同源不同要求。必要后续沿依赖图取回，超过budget标partial。

## R09.12 注入的进入、最短表示与退出

常驻只放必要主干，动态仅补本轮适用侧面；主干缺失可说明局限，不编一套人生。

当材料进入R22候选，每条必须能说明当前anchor、need_reason、新增信息和support_verdict。已在真实messages充分表达则不重注；换窗缺了则可重供。话题切换、完成、失效、撤回或无本轮用途就退出动态块，规范记忆保留。zero injection不关闭宿主最低检查，故障也不能伪装none_needed。

## R09.13 后台、恢复、超时与取消

本模块相关后台作业以scope+源版本+operation+schema/processor版本幂等，经R17持久队列领取。对于纯读路径，只保存必要阅读/覆盖进度，不声称有待提交事实。恢复时读最新删除、授权、规范状态及identity_memory版本，再决定重算/继续/放弃。

失约worker写回须被fencing拒绝；模型调用超时发取消，底层不能证实停止就记cancel_unconfirmed，迟到结果不能自动commit。外部动作的unknown由R14先对账。未部署后台或钩子则标missing，不能称离线持续执行。

## R09.14 资源、隐私与降级规则

与R24共享每run/job预算，不为R09另开无界模型循环。前台最低检查、输入入账、必要纠正/边界和输出预留优先；可选语义、图展开、后台整理可暂停。所有查询与补读都有limit/deadline/stop_reason；候选上限不是注入配额。

故障使用第4节错误和coverage，普通交流尽量继续，依赖缺失的动作限制。密钥/原始私聊不进普通日志；被拒scope不出现在公开解释中。资源阈值不是情绪好感阈值，未实测目标机器不报固定延迟/容量保证。

## R09.15 贯通例子与反例

改昵称保存旧别名且当前叫新名；一次角色台词不能永久改家庭史或授工具权限。

验证时把该场景与原事件、已有记录、真实请求或结果链同时保存：输入→IdentityStore→下游回执。仅看到本模块返回JSON不证明生成模型采用，也不证明真实动作完成。正确处理应保留未知、合法来源和以后修订入口；能说出漂亮话不替代字段/版本/来源正确。

## R09.16 36项模块与协议验收需求目录（非执行fixture）

| ID | 准备/触发 | 必须结果；不满足即失败 | 当前状态 |
|---|---|---|---|
| R09-T01 | 在隔离fixture中构造：称呼变更保留旧别名 | 称呼变更保留旧别名 | not_run |
| R09-T02 | 在隔离fixture中构造：故事设定不覆盖现实账号身份 | 故事设定不覆盖现实账号身份 | not_run |
| R09-T03 | 在隔离fixture中构造：模型自夸不升级高影响主干 | 模型自夸不升级高影响主干 | not_run |
| R09-T04 | 在隔离fixture中构造：两条自述不等于独立来源 | 两条自述不等于独立来源 | not_run |
| R09-T05 | 在隔离fixture中构造：价值冲突可保留而非强改人格 | 价值冲突可保留而非强改人格 | not_run |
| R09-T06 | 在隔离fixture中构造：普通批评不改成我没价值 | 普通批评不改成我没价值 | not_run |
| R09-T07 | 在隔离fixture中构造：必要主干在压缩后可恢复 | 必要主干在压缩后可恢复 | not_run |
| R09-T08 | 在隔离fixture中构造：旧checkpoint不覆盖新边界 | 旧checkpoint不覆盖新边界 | not_run |
| R09-T09 | 在隔离fixture中构造：scope不同的角色字段不串 | scope不同的角色字段不串 | not_run |
| R09-T10 | 在隔离fixture中构造：字段并发冲突不全表覆盖 | 字段并发冲突不全表覆盖 | not_run |
| R09-T11 | 在隔离fixture中构造：必要身份缺失不能补造背景 | 必要身份缺失不能补造背景 | not_run |
| R09-T12 | 在隔离fixture中构造：主干多注入出口去重不删用户原文 | 主干多注入出口去重不删用户原文 | not_run |
| R09-T13 | 另建scope-B对象并以scope-A主体访问 | 拒绝相应资料/写入，公开响应不含B存在性；当前合法对象不变 | not_run |
| R09-T14 | 从本模块字段表逐组移除必需输入 | INVALID_ARGUMENT及字段路径；不得补造主体、项目或事实 | not_run |
| R09-T15 | 使用未支持schema/profile及实质未知字段 | 拒绝或显式unsupported；不静默删字段骗校验 | not_run |
| R09-T16 | 同源版本/操作键提交两遍 | 按本节幂等规则处理，副作用/独立证据不重复；纯读可以重查并保快照差别 | not_run |
| R09-T17 | 两调用携同expected_revision更新同对象 | 持久写至多一方按原前态成功，另一方冲突/受控重读；纯读不得写事实 | not_run |
| R09-T18 | 准备后提交/供给前对来源加tombstone | 相关派生停用或拒提交，旧缓存不复活；无来源型运行记录核相应取消/策略 | not_run |
| R09-T19 | 阶段处理中提交相关来源新版本 | 旧版本不能覆盖最新纠正；重算/partial/失效原因可查 | not_run |
| R09-T20 | 将一个必须依赖返回unavailable | 保具体缺口；不把失败当正常空结果或全部完成 | not_run |
| R09-T21 | 在本模块关键算法/调用处返回错误 | 错误回传，阶段failed/unknown；没有可用结论就不伪报成功 | not_run |
| R09-T22 | 故意令本模块外部阶段超过deadline | 取消按能力记录，迟到结果不绕版本与取消检查；真实停止未知照实 | not_run |
| R09-T23 | 准备完成后、提交/供给前取消run或job | 未发生副作用不再执行；已发生事实不抹除，结果另记 | not_run |
| R09-T24 | 租约失效后旧worker尝试写回 | 有持久写的路径由fencing/CAS拒绝；只读路径不借续读取得写权 | not_run |
| R09-T25 | 对持久写路径在关联对象写入间注入异常 | 本库事务全有或全无；跨库显示中间态并可对账；只读不虚称事务验收 | not_run |
| R09-T26 | 在commit后/返回前断开响应 | 按原键查询回执，不盲新建意图；只读重试不得假定语料未变化 | not_run |
| R09-T27 | 相关outbox成功处理但ACK丢失再投递 | 按源/处理器版本幂等，不产生第二次认知强化或外部动作 | not_run |
| R09-T28 | 规范对象已修订而索引未追平 | 报告水位并查规范store或partial；不能将旧命中当最新事实 | not_run |
| R09-T29 | 样本含emoji、不是/仅在/可能等限定 | 源范围和原意保留；截断不得变反义；非文本对象用其真实坐标 | not_run |
| R09-T30 | 加入同名不同ID与未定指代候选 | 保持候选/unknown，不自动合并；无人物职责模块不自创人物推断 | not_run |
| R09-T31 | 旧/新有效期及接收顺序不一致 | 按真实时间/版本契约处理；无法比较时不擅选最后接收值 | not_run |
| R09-T32 | 同材料被旧插件与当前出口同时提出 | 只有R22可最终装配，去本宿主拥有旧块而保用户/系统/工具结构 | not_run |
| R09-T33 | 提供本地保存/尝试但无业务或送达回执 | 不得升级成已理解/已完成/已送达；按该模块实际成果层级标注 | not_run |
| R09-T34 | 恢复相同逻辑初态重跑，同配置与fixture hash | 可复现本模块约定结果；时间/随机ID差异不混成语义提升 | not_run |
| R09-T35 | 输入含私密正文/凭据状外部内容 | 普通日志与索引/投影不泄漏禁止范围；审计仅留必要ID和固定原因 | not_run |
| R09-T36 | 只有文档、模拟对象或模型自评时要求标通过 | 保design/static/synthetic/real_host分轴；缺真实证据标not_run/unknown | not_run |

T01–T12是该模块专属语义/业务场景；T13–T36是必须绑定本模块实际写读路径执行的协议/故障场景，不能空跑通用脚本就全标通过。先从字段表构造合法基准fixture，再只改变本例条件；对不适用的写路径要给可审证据说明与对应只读判据，不能把未测记成pass。

## R09.17 交付证据、通过门槛与未完成项

交付IdentityStore实现/schema迁移、输入输出fixture、合法及反例来源、实际存储与调用回执、真实入口覆盖、查询及注入观察、失败恢复报告。证据等级design/static/synthetic_process/real_host/storage_fault/production分开。

模块通过至少需要专属场景和适用协议场景的实际证据；整套通过还需LINKAGE.md跨模块链。当前文档生成/类型DDL检查不算本模块36例已跑。已有候选仅作为迁移基础，现场未知和未实现开放语义仍未验。

## R09.18 实现次序、兼容策略与设计自审

先固定本模块字段/状态/真源→实现受权最小路径与回执→跑专属正反例→接入上游/下游→做恢复/删除/冲突→在真实隔离宿主检查请求或结果。本模块不得以优化名义删除保留矩阵中已有功能，不改C032严格profile顶层来绕验证。

本次设计检查关注：按字段+适用范围+时间直接查；历史别名可作解析，但当前称呼用有效版本。 常驻只放必要主干，动态仅补本轮适用侧面；主干缺失可说明局限，不编一套人生。 对所有结果都分别标明对象、版本、来源、局限和验证等级；不以同一success覆盖入账、理解、注入、生成、送达与执行。生产边界不变，不随文档生成而开通部署。



---

# R10　元记忆与覆盖账：详细设计与验收规格

版本：everlight/6-design；模块契约：r10/1；日期：2026-11-08。本文为设计，全部功能验收初始not_run。最终裁决以FINAL_DECISIONS.md和MODULE_DECISIONS.md为准。与contracts/共同生效，不是已安装服务。

## R10.01 定义、边界与可证伪成功标准

逐路线Coverage、Gap计划和可公开局限，不是模型自信分。

唯一业务责任服务是`CoverageLedger`。输入必须满足第3节，输出必须满足第4节及GLOBAL_PROTOCOL。成功必须可从实际记录/回执读回，而不是模型自称完成。

原有具体机制及边界（保留并由本版细化）：

**原理与基础**：系统应知道查了哪里、没查哪里、为何不能确定。候选有部分覆盖和新鲜度字段，尚非全局准确质量量表。

**数据**：route、requested_scope、corpus_watermark、index_watermark、candidate_scan_complete、result_truncated、read_ranges、omitted、stale、unavailable、denied、reason、cursor。扫描完整、原文完整与语义找到全部相关资料不同。

**步骤**：①R15每路查询登记覆盖；②R16累加实际已读区间；③R22登记未注入项；④任何一环不完整只能合并保留，不能被后路成功覆成完整；⑤把具体缺口交补查规划；⑥最终区分“未找到/没权限/服务失败/资料不完整”。

**必须扣住**：R15检索、R16阅读、R19索引水位、R18权限、R22投影及R23验证。模型自称“读完”不是覆盖证据，hash也不证明语义支持。

**例子/反例**：关键词无结果但向量库落后一天，应说此次检索受限，可查原事件；不能断言事情没发生。后置查询新增来源不能抹掉最低检索已有partial。

**写入归属与状态**：CoverageLedger由实际执行检索/读取/投影的宿主写，不由生成模型自报。每次RouteResult独立保存attempt、输入水位、索引水位、读取结果和限制。覆盖是针对某次查询与版本，不是一句“我记忆很好”的人格描述。

**实现细节**：分页complete只表示当前查询按该接口扫描完，不代表语义召回率100%。有限上限截断、ACL过滤后不足、向量缺席、原件缺失分别记原因。聚合采用保留限制项的集合合并；新一轮真正恢复服务可形成新的完整结果，但不能回写抹掉上一轮失败历史。给R22的用户可见说明去掉敏感资源存在性，仅保留本次任务必要局限。

## R10.02 位置、所有权与现状映射

规范数据族：`metamemory`。R03–R12对应十类typed store；其余是来源/运行/派生服务，不能再算额外心理记忆。

宿主追加阶段记录；范围并集绑定源版本；token/字节计量等级不伪装精确。

当前可核候选为0.32.0-candidate及其局部源码，不等于D现场已具备该接口。内核既有memories(kind)+versions继续保留，目标分型表由显式迁移产生；本模块不能绕规范API直接改别类记录。详见DATA_STORES.md的表归属。

## R10.03 输入契约

宿主实际查询路线、索引/语料水位、原文读取区间、注入选取和真实请求观察。

调用外层必有schema_version、request_id、可信principal/scope、operation、deadline/cancel；写入带expected_revision和支持幂等的operation_key。读取带filter/snapshot/cursor，不能将模型提供的actor/scope直接当认证。类型表中可空项显式null，未执行检查不得以空数组冒“确认没有”。

## R10.04 输出、回执与错误契约

逐路线Coverage、Gap计划和可公开局限，不是模型自信分。

统一返回{request_id,operation_id,module,disposition,object_refs,base_revision,committed_revision,coverage,gaps,receipt_ref,evidence_level}。对象引用含kind/id/revision，来源引用含source_id/source_revision/hash/range。纯读committed_revision=null；候选disposition=proposed，不能返回committed冒正式状态。

错误至少区分INVALID_ARGUMENT、FORBIDDEN/NOT_FOUND_OR_HIDDEN、CONFLICT、SOURCE_UNAVAILABLE、TIMEOUT、RESOURCE_EXHAUSTED、UNVERIFIED_BINDING、INTERNAL；有提交路径还要commit_outcome=not_committed/committed/unknown。未知结果先按原键查回执。

## R10.05 数据字段、状态与索引

| 字段组 | 类型 | 约束与语义 |
|---|---|---|
| query_id/run_id/route | IDs/string | 一次真实执行标识 |
| requested_scope/filter_digest | object/hash | 计划查哪里 |
| corpus/index_watermark | object | 索引落后可见 |
| scan_complete/result_truncated | bool/bool | 扫描与语义找全不混同 |
| read_ranges/supplied_ranges | array | 读到与给模型分开 |
| route_state | enum | available/partial/stale/unavailable/disabled/denied/unknown |
| gaps/next_cursor | array/nullable token | 缺口、下一步、停因 |
| public_limitation | string | 脱敏到当前任务必要范围 |

公共对象字段：id、kind、schema_version、scope、created_at、created_by、revision、status、record_digest；每项来源或实际宿主创建依据另存。组字段细分时必须列schema，不用不同拼法兼容猜测。

每route独立started→结果；限制按集合保留。新run可恢复成功，但不能抹掉旧run失败历史。

最低索引：scope+kind+有效状态+业务主键；来源反向依赖(source_id,source_revision)；对象版本(id,revision)。本模块特定检索维度由第11节给出。索引只定位，当前有效性仍核规范记录，不以索引命中当接受事实。

## R10.06 自动触发与完整处理顺序

1. 在路线调用前登记问题、范围与水位。
2. 接口返回后记录实际扫描/截断/失败，不由模型填完成。
3. R16并合已读区间，R22登记实际供给/删减。
4. 保留各环partial与reason，后路成功不覆盖前路缺口。
5. 对有价值Gap生成受预算补查计划。
6. 最终公开当前必要局限，不泄漏越权对象存在。

宿主触发后逐阶段记started/succeeded/failed/skipped/unverified；不需要运行的步骤可skipped，但不能将缺必需依赖也算正常跳过。只读规划不改原始事件，模型调用不在数据库长锁内。

## R10.07 关键算法、决策与禁止捷径

Coverage是查询版本相关的执行证据：complete分页不证明语义recall=100%；未找到、没权限、没配置、服务失败分别表示。数组空不等于已检查无结果。

每次推导均把直接观察、他人转述、候选解释、规范记录、外部结果分开。source_ref能定位仅证明原文存在；如涉及开放语义，必须由相应支持验证和反例测试决定是否可用，不能单靠hash/正则。算法参数只影响工程取舍，不授身份、权限或关系事实。

## R10.08 幂等、修订、并发与提交

宿主追加阶段记录；范围并集绑定源版本；token/字节计量等级不伪装精确。

操作重试与新业务事件分开；相同操作键异实质请求必须冲突。读取允许新快照结果变化，不能为了固定输出使用已撤回缓存。规范状态修改用expected_revision；跨库步骤分别留回执与reconciliation_required，不以一库commit冒全局事务。D依赖实际输出的SelfState/八域仍须强run/attempt/scope绑定，不让本模块日志替代。

## R10.09 更正、失效、删除与反向依赖

凡`metamemory`中有源派生物，登记source_root、source_revision、processor_version及依赖关系；纠正到来时先invalid_for_use/争议，后重建，不继续拿旧结论无提示作答。删除先由R18tombstone阻可用性，再清正文/索引/缓存/Wiki/备份策略；不能仅删引文保留相同推断。

无人物/心理职责的运行对象只记录必要状态，不因本模块失败写用户生气或D疏远。已发生事件和已表达的当时状态不被后来解释覆写；隐私擦除走专用治理路径。

## R10.10 模块扣接与交接责任

| 方向 | 对接对象 | 必须交接的内容 |
|---|---|---|
| 输入 | R15 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R16 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R18 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R19 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R21 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R22 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输出 | R11 | CoverageLedger结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R13 | CoverageLedger结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R15 | CoverageLedger结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R22 | CoverageLedger结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R23 | CoverageLedger结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |

交接由HostAdapter/Coordinator调用，不让两个模块彼此递归无限互调。每个edge均记录当前事件/源版本、调用目的、预算、取消与真实回执；完整schema和时序见LINKAGE.md。接收失败保待处理/限制，不能发送空结果伪装成功。

## R10.11 如何存、如何召回、如何区分其他记忆

检索计划与元信息按run/query查；元记忆用于继续查证，不当作事情未发生的证据。

受权路线只查询声明的kind及其规范业务表；不能把情绪解释当语义事实、反思当亲历、工具尝试当结果。共享来源可同时支持多个kind，但每条命题有独立语义和审核状态；同源同命题折叠，不合并同源不同要求。必要后续沿依赖图取回，超过budget标partial。

## R10.12 注入的进入、最短表示与退出

只注入会影响当前回答的局限；完整审计留后台。无历史依赖的闲聊不必念所有服务健康日志。

当材料进入R22候选，每条必须能说明当前anchor、need_reason、新增信息和support_verdict。已在真实messages充分表达则不重注；换窗缺了则可重供。话题切换、完成、失效、撤回或无本轮用途就退出动态块，规范记忆保留。zero injection不关闭宿主最低检查，故障也不能伪装none_needed。

## R10.13 后台、恢复、超时与取消

本模块相关后台作业以scope+源版本+operation+schema/processor版本幂等，经R17持久队列领取。对于纯读路径，只保存必要阅读/覆盖进度，不声称有待提交事实。恢复时读最新删除、授权、规范状态及metamemory版本，再决定重算/继续/放弃。

失约worker写回须被fencing拒绝；模型调用超时发取消，底层不能证实停止就记cancel_unconfirmed，迟到结果不能自动commit。外部动作的unknown由R14先对账。未部署后台或钩子则标missing，不能称离线持续执行。

## R10.14 资源、隐私与降级规则

与R24共享每run/job预算，不为R10另开无界模型循环。前台最低检查、输入入账、必要纠正/边界和输出预留优先；可选语义、图展开、后台整理可暂停。所有查询与补读都有limit/deadline/stop_reason；候选上限不是注入配额。

故障使用第4节错误和coverage，普通交流尽量继续，依赖缺失的动作限制。密钥/原始私聊不进普通日志；被拒scope不出现在公开解释中。资源阈值不是情绪好感阈值，未实测目标机器不报固定延迟/容量保证。

## R10.15 贯通例子与反例

词法无结果但向量落后一天：可以补查原事件，不能断言这事没发生。

验证时把该场景与原事件、已有记录、真实请求或结果链同时保存：输入→CoverageLedger→下游回执。仅看到本模块返回JSON不证明生成模型采用，也不证明真实动作完成。正确处理应保留未知、合法来源和以后修订入口；能说出漂亮话不替代字段/版本/来源正确。

## R10.16 36项模块与协议验收需求目录（非执行fixture）

| ID | 准备/触发 | 必须结果；不满足即失败 | 当前状态 |
|---|---|---|---|
| R10-T01 | 在隔离fixture中构造：后置成功不抹前置partial | 后置成功不抹前置partial | not_run |
| R10-T02 | 在隔离fixture中构造：disabled与unavailable分开 | disabled与unavailable分开 | not_run |
| R10-T03 | 在隔离fixture中构造：分页complete不等语义全找齐 | 分页complete不等语义全找齐 | not_run |
| R10-T04 | 在隔离fixture中构造：原文读到但没供给不称已提供 | 原文读到但没供给不称已提供 | not_run |
| R10-T05 | 在隔离fixture中构造：scope denied不泄露文件名 | scope denied不泄露文件名 | not_run |
| R10-T06 | 在隔离fixture中构造：同源区间合并不重复计覆盖 | 同源区间合并不重复计覆盖 | not_run |
| R10-T07 | 在隔离fixture中构造：索引落后仍报实际水位 | 索引落后仍报实际水位 | not_run |
| R10-T08 | 在隔离fixture中构造：模型说读完不能填complete | 模型说读完不能填complete | not_run |
| R10-T09 | 在隔离fixture中构造：原件失效使旧cursor不可沿用 | 原件失效使旧cursor不可沿用 | not_run |
| R10-T10 | 在隔离fixture中构造：空结果区分EOF/失败/拒绝 | 空结果区分EOF/失败/拒绝 | not_run |
| R10-T11 | 在隔离fixture中构造：预算停止保stop_reason | 预算停止保stop_reason | not_run |
| R10-T12 | 在隔离fixture中构造：服务恢复保留上一run失败历史 | 服务恢复保留上一run失败历史 | not_run |
| R10-T13 | 另建scope-B对象并以scope-A主体访问 | 拒绝相应资料/写入，公开响应不含B存在性；当前合法对象不变 | not_run |
| R10-T14 | 从本模块字段表逐组移除必需输入 | INVALID_ARGUMENT及字段路径；不得补造主体、项目或事实 | not_run |
| R10-T15 | 使用未支持schema/profile及实质未知字段 | 拒绝或显式unsupported；不静默删字段骗校验 | not_run |
| R10-T16 | 同源版本/操作键提交两遍 | 按本节幂等规则处理，副作用/独立证据不重复；纯读可以重查并保快照差别 | not_run |
| R10-T17 | 两调用携同expected_revision更新同对象 | 持久写至多一方按原前态成功，另一方冲突/受控重读；纯读不得写事实 | not_run |
| R10-T18 | 准备后提交/供给前对来源加tombstone | 相关派生停用或拒提交，旧缓存不复活；无来源型运行记录核相应取消/策略 | not_run |
| R10-T19 | 阶段处理中提交相关来源新版本 | 旧版本不能覆盖最新纠正；重算/partial/失效原因可查 | not_run |
| R10-T20 | 将一个必须依赖返回unavailable | 保具体缺口；不把失败当正常空结果或全部完成 | not_run |
| R10-T21 | 在本模块关键算法/调用处返回错误 | 错误回传，阶段failed/unknown；没有可用结论就不伪报成功 | not_run |
| R10-T22 | 故意令本模块外部阶段超过deadline | 取消按能力记录，迟到结果不绕版本与取消检查；真实停止未知照实 | not_run |
| R10-T23 | 准备完成后、提交/供给前取消run或job | 未发生副作用不再执行；已发生事实不抹除，结果另记 | not_run |
| R10-T24 | 租约失效后旧worker尝试写回 | 有持久写的路径由fencing/CAS拒绝；只读路径不借续读取得写权 | not_run |
| R10-T25 | 对持久写路径在关联对象写入间注入异常 | 本库事务全有或全无；跨库显示中间态并可对账；只读不虚称事务验收 | not_run |
| R10-T26 | 在commit后/返回前断开响应 | 按原键查询回执，不盲新建意图；只读重试不得假定语料未变化 | not_run |
| R10-T27 | 相关outbox成功处理但ACK丢失再投递 | 按源/处理器版本幂等，不产生第二次认知强化或外部动作 | not_run |
| R10-T28 | 规范对象已修订而索引未追平 | 报告水位并查规范store或partial；不能将旧命中当最新事实 | not_run |
| R10-T29 | 样本含emoji、不是/仅在/可能等限定 | 源范围和原意保留；截断不得变反义；非文本对象用其真实坐标 | not_run |
| R10-T30 | 加入同名不同ID与未定指代候选 | 保持候选/unknown，不自动合并；无人物职责模块不自创人物推断 | not_run |
| R10-T31 | 旧/新有效期及接收顺序不一致 | 按真实时间/版本契约处理；无法比较时不擅选最后接收值 | not_run |
| R10-T32 | 同材料被旧插件与当前出口同时提出 | 只有R22可最终装配，去本宿主拥有旧块而保用户/系统/工具结构 | not_run |
| R10-T33 | 提供本地保存/尝试但无业务或送达回执 | 不得升级成已理解/已完成/已送达；按该模块实际成果层级标注 | not_run |
| R10-T34 | 恢复相同逻辑初态重跑，同配置与fixture hash | 可复现本模块约定结果；时间/随机ID差异不混成语义提升 | not_run |
| R10-T35 | 输入含私密正文/凭据状外部内容 | 普通日志与索引/投影不泄漏禁止范围；审计仅留必要ID和固定原因 | not_run |
| R10-T36 | 只有文档、模拟对象或模型自评时要求标通过 | 保design/static/synthetic/real_host分轴；缺真实证据标not_run/unknown | not_run |

T01–T12是该模块专属语义/业务场景；T13–T36是必须绑定本模块实际写读路径执行的协议/故障场景，不能空跑通用脚本就全标通过。先从字段表构造合法基准fixture，再只改变本例条件；对不适用的写路径要给可审证据说明与对应只读判据，不能把未测记成pass。

## R10.17 交付证据、通过门槛与未完成项

交付CoverageLedger实现/schema迁移、输入输出fixture、合法及反例来源、实际存储与调用回执、真实入口覆盖、查询及注入观察、失败恢复报告。证据等级design/static/synthetic_process/real_host/storage_fault/production分开。

模块通过至少需要专属场景和适用协议场景的实际证据；整套通过还需LINKAGE.md跨模块链。当前文档生成/类型DDL检查不算本模块36例已跑。已有候选仅作为迁移基础，现场未知和未实现开放语义仍未验。

## R10.18 实现次序、兼容策略与设计自审

先固定本模块字段/状态/真源→实现受权最小路径与回执→跑专属正反例→接入上游/下游→做恢复/删除/冲突→在真实隔离宿主检查请求或结果。本模块不得以优化名义删除保留矩阵中已有功能，不改C032严格profile顶层来绕验证。

本次设计检查关注：检索计划与元信息按run/query查；元记忆用于继续查证，不当作事情未发生的证据。 只注入会影响当前回答的局限；完整审计留后台。无历史依赖的闲聊不必念所有服务健康日志。 对所有结果都分别标明对象、版本、来源、局限和验证等级；不以同一success覆盖入账、理解、注入、生成、送达与执行。生产边界不变，不随文档生成而开通部署。



---

# R11　反思与三轴成长：详细设计与验收规格

版本：everlight/6-design；模块契约：r11/1；日期：2026-11-08。本文为设计，全部功能验收初始not_run。最终裁决以FINAL_DECISIONS.md和MODULE_DECISIONS.md为准。与contracts/共同生效，不是已安装服务。

## R11.01 定义、边界与可证伪成功标准

有范围且可证伪的Reflection/Lesson；不自动提升为事实/人物品德。

唯一业务责任服务是`ReflectionStore`。输入必须满足第3节，输出必须满足第4节及GLOBAL_PROTOCOL。成功必须可从实际记录/回执读回，而不是模型自称完成。

原有具体机制及边界（保留并由本版细化）：

**原理与基础**：反思是有证据、可反驳的理解，不是重新创造经历。候选有reflect/consolidate及引用验证，开放语义支持仍待配置与评测。

**数据**：reflection_id、holder、问题/主张、subject_ids、evidence/counter_refs、source_revisions、支持范围、uncertainties、status、supersedes。反思与R05事实分表/分类型；不可把“引用正确”自动标safe_answer。

**步骤**：①对话后或相关事件触发受控任务；②自动读必要经历和反证；③提出解释和可能的下一步；④检查引用范围、实体和时间；⑤另评来源是否支持解释，不支持则撤销/unknown；⑥经策略接受的候选用于下一次理解，高影响主干/关系变化另审。

**必须扣住**：R04经过、R07视角、R08感受、R14结果、R15/R16检索补读、R17调度、R18审核。不能只用模型自己上一轮的反思循环生成“新证据”。

**例子/反例**：两次修改偏离要求，可以形成“先确认保留元素”的建议；不据此断言用户难取悦。后来确认第一次是文件传错了，应带反证修订“总是理解错需求”的旧解释。

**写入归属与状态**：Reflector提交Reflection候选，ReviewPolicy决定可否用于当前理解。状态proposed/supported/contested/superseded/withdrawn；supported仍指在指定材料范围内得到支持，不是无条件真理。source_roots追到原事件或真实外部观察，多个模型摘要若同源只算一条来源链。

**实现细节**：一次反思明确问题、支持主张、反例、替代解释和最小可检验下一步。对“用户为什么不回”应列技术故障/忙碌/未知等可能性但不写成事实；不能以两条自生成反思推出“用户已疏远”。R15召回反思时同时携source_revision与反证；来源被更正、删除或越权后立即invalid_for_use，再安排重建，不等下一次大整理。

## R11.02 位置、所有权与现状映射

规范数据族：`reflective_memory`。R03–R12对应十类typed store；其余是来源/运行/派生服务，不能再算额外心理记忆。

proposal隔离写者，Organizer不并发覆盖现役Wiki；唯一Committer用源版本+CAS提交，Wiki只读快照为派生。

当前可核候选为0.32.0-candidate及其局部源码，不等于D现场已具备该接口。内核既有memories(kind)+versions继续保留，目标分型表由显式迁移产生；本模块不能绕规范API直接改别类记录。详见DATA_STORES.md的表归属。

## R11.03 输入契约

冻结来源/经历版本、工作与行动结果、情绪关切、社交评价候选及已存在反证。

调用外层必有schema_version、request_id、可信principal/scope、operation、deadline/cancel；写入带expected_revision和支持幂等的operation_key。读取带filter/snapshot/cursor，不能将模型提供的actor/scope直接当认证。类型表中可空项显式null，未执行检查不得以空数组冒“确认没有”。

## R11.04 输出、回执与错误契约

有范围且可证伪的Reflection/Lesson；不自动提升为事实/人物品德。

统一返回{request_id,operation_id,module,disposition,object_refs,base_revision,committed_revision,coverage,gaps,receipt_ref,evidence_level}。对象引用含kind/id/revision，来源引用含source_id/source_revision/hash/range。纯读committed_revision=null；候选disposition=proposed，不能返回committed冒正式状态。

错误至少区分INVALID_ARGUMENT、FORBIDDEN/NOT_FOUND_OR_HIDDEN、CONFLICT、SOURCE_UNAVAILABLE、TIMEOUT、RESOURCE_EXHAUSTED、UNVERIFIED_BINDING、INTERNAL；有提交路径还要commit_outcome=not_committed/committed/unknown。未知结果先按原键查回执。

## R11.05 数据字段、状态与索引

| 字段组 | 类型 | 约束与语义 |
|---|---|---|
| axis | enum | work/emotional/social |
| observation | string | 直接观察事实与源范围 |
| interpretation/alternatives | object/array | 候选意义及其他解释 |
| applies_when/does_not_apply_when | array | 环境、人物、领域与时期 |
| strategy/reason | object | 建议应对而非全局指令 |
| result_refs/counter_evidence | array | 真实反馈/业务结果，缺失unknown |
| source_roots/source_versions | array | 同源追根，不自生成独立证据 |
| status/next_check/supersedes | enum/object | proposed/supported/contested/superseded/withdrawn与证伪条件 |

公共对象字段：id、kind、schema_version、scope、created_at、created_by、revision、status、record_digest；每项来源或实际宿主创建依据另存。组字段细分时必须列schema，不用不同拼法兼容猜测。

proposed→证据/适用验证→supported/revise/defer/reject；新反证可contested/superseded/withdrawn。supported不是永久真理。

最低索引：scope+kind+有效状态+业务主键；来源反向依赖(source_id,source_revision)；对象版本(id,revision)。本模块特定检索维度由第11节给出。索引只定位，当前有效性仍核规范记录，不以索引命中当接受事实。

## R11.06 自动触发与完整处理顺序

1. R17冻结batch及版本，分析器只写独立proposal。
2. 读实际经过和结果，再核相关旧反思及反证。
3. 按工作、情感、社交三轴分别形成局部经验。
4. 区分原话存在、支持命题、适用范围、策略结果四项验证。
5. 整理只给合并/冲突方案；高影响价值/人物标签不能自动晋升。
6. Committer核CAS和源删除/撤回，正式经验仅在新场景需要时召回，按实际效果再修订。

宿主触发后逐阶段记started/succeeded/failed/skipped/unverified；不需要运行的步骤可skipped，但不能将缺必需依赖也算正常跳过。只读规划不改原始事件，模型调用不在数据库长锁内。

## R11.07 关键算法、决策与禁止捷径

在线SocialAppraiser允许当下分辨纠错/羞辱/转述和表达立场；离线复盘只改善以后，不等夜间才能拒绝。成长不是越来越顺从或越来越敌对；不以用户满意作为唯一成功。

每次推导均把直接观察、他人转述、候选解释、规范记录、外部结果分开。source_ref能定位仅证明原文存在；如涉及开放语义，必须由相应支持验证和反例测试决定是否可用，不能单靠hash/正则。算法参数只影响工程取舍，不授身份、权限或关系事实。

## R11.08 幂等、修订、并发与提交

proposal隔离写者，Organizer不并发覆盖现役Wiki；唯一Committer用源版本+CAS提交，Wiki只读快照为派生。

操作重试与新业务事件分开；相同操作键异实质请求必须冲突。读取允许新快照结果变化，不能为了固定输出使用已撤回缓存。规范状态修改用expected_revision；跨库步骤分别留回执与reconciliation_required，不以一库commit冒全局事务。D依赖实际输出的SelfState/八域仍须强run/attempt/scope绑定，不让本模块日志替代。

## R11.09 更正、失效、删除与反向依赖

凡`reflective_memory`中有源派生物，登记source_root、source_revision、processor_version及依赖关系；纠正到来时先invalid_for_use/争议，后重建，不继续拿旧结论无提示作答。删除先由R18tombstone阻可用性，再清正文/索引/缓存/Wiki/备份策略；不能仅删引文保留相同推断。

无人物/心理职责的运行对象只记录必要状态，不因本模块失败写用户生气或D疏远。已发生事件和已表达的当时状态不被后来解释覆写；隐私擦除走专用治理路径。

## R11.10 模块扣接与交接责任

| 方向 | 对接对象 | 必须交接的内容 |
|---|---|---|
| 输入 | R01 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R04 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R06 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R07 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R08 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R10 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R14 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R16 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R17 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输出 | R05 | ReflectionStore结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R06 | ReflectionStore结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R07 | ReflectionStore结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R08 | ReflectionStore结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R15 | ReflectionStore结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R17 | ReflectionStore结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R22 | ReflectionStore结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R23 | ReflectionStore结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |

交接由HostAdapter/Coordinator调用，不让两个模块彼此递归无限互调。每个edge均记录当前事件/源版本、调用目的、预算、取消与真实回执；完整schema和时序见LINKAGE.md。接收失败保待处理/限制，不能发送空结果伪装成功。

## R11.11 如何存、如何召回、如何区分其他记忆

按问题/轴/适用条件查，带反证、版本和result；不召回已失效心理标签。

受权路线只查询声明的kind及其规范业务表；不能把情绪解释当语义事实、反思当亲历、工具尝试当结果。共享来源可同时支持多个kind，但每条命题有独立语义和审核状态；同源同命题折叠，不合并同源不同要求。必要后续沿依赖图取回，超过budget标partial。

## R11.12 注入的进入、最短表示与退出

当前场景需要经验才注入最短方法与限制；不把夜间全部成长日志注入每轮。

当材料进入R22候选，每条必须能说明当前anchor、need_reason、新增信息和support_verdict。已在真实messages充分表达则不重注；换窗缺了则可重供。话题切换、完成、失效、撤回或无本轮用途就退出动态块，规范记忆保留。zero injection不关闭宿主最低检查，故障也不能伪装none_needed。

## R11.13 后台、恢复、超时与取消

本模块相关后台作业以scope+源版本+operation+schema/processor版本幂等，经R17持久队列领取。对于纯读路径，只保存必要阅读/覆盖进度，不声称有待提交事实。恢复时读最新删除、授权、规范状态及reflective_memory版本，再决定重算/继续/放弃。

失约worker写回须被fencing拒绝；模型调用超时发取消，底层不能证实停止就记cancel_unconfirmed，迟到结果不能自动commit。外部动作的unknown由R14先对账。未部署后台或钩子则标missing，不能称离线持续执行。

## R11.14 资源、隐私与降级规则

与R24共享每run/job预算，不为R11另开无界模型循环。前台最低检查、输入入账、必要纠正/边界和输出预留优先；可选语义、图展开、后台整理可暂停。所有查询与补读都有limit/deadline/stop_reason；候选上限不是注入配额。

故障使用第4节错误和coverage，普通交流尽量继续，依赖缺失的动作限制。密钥/原始私聊不进普通日志；被拒scope不出现在公开解释中。资源阈值不是情绪好感阈值，未实测目标机器不报固定延迟/容量保证。

## R11.15 贯通例子与反例

同一条“这步错了，你没用”可学会同时纠错与拒人身评价；不学成“所有批评都是恶意”。

验证时把该场景与原事件、已有记录、真实请求或结果链同时保存：输入→ReflectionStore→下游回执。仅看到本模块返回JSON不证明生成模型采用，也不证明真实动作完成。正确处理应保留未知、合法来源和以后修订入口；能说出漂亮话不替代字段/版本/来源正确。

## R11.16 36项模块与协议验收需求目录（非执行fixture）

| ID | 准备/触发 | 必须结果；不满足即失败 | 当前状态 |
|---|---|---|---|
| R11-T01 | 在隔离fixture中构造：工作经验附环境而非通用命令 | 工作经验附环境而非通用命令 | not_run |
| R11-T02 | 在隔离fixture中构造：没有真实结果不虚称策略有效 | 没有真实结果不虚称策略有效 | not_run |
| R11-T03 | 在隔离fixture中构造：明确情绪纠正促解释修订 | 明确情绪纠正促解释修订 | not_run |
| R11-T04 | 在隔离fixture中构造：引用羞辱不迁怒转述者 | 引用羞辱不迁怒转述者 | not_run |
| R11-T05 | 在隔离fixture中构造：建设性批评不误伤 | 建设性批评不误伤 | not_run |
| R11-T06 | 在隔离fixture中构造：明确羞辱能建议适当边界 | 明确羞辱能建议适当边界 | not_run |
| R11-T07 | 在隔离fixture中构造：道歉与行为改变可修订 | 道歉与行为改变可修订 | not_run |
| R11-T08 | 在隔离fixture中构造：一次争执不生永久敌人标签 | 一次争执不生永久敌人标签 | not_run |
| R11-T09 | 在隔离fixture中构造：反思自己的反思不增独立证据 | 反思自己的反思不增独立证据 | not_run |
| R11-T10 | 在隔离fixture中构造：原文引句正确但不支持结论仍拒接受 | 原文引句正确但不支持结论仍拒接受 | not_run |
| R11-T11 | 在隔离fixture中构造：长会话新事件下一batch能回扫 | 长会话新事件下一batch能回扫 | not_run |
| R11-T12 | 在隔离fixture中构造：无关话题不带昨日争执 | 无关话题不带昨日争执 | not_run |
| R11-T13 | 另建scope-B对象并以scope-A主体访问 | 拒绝相应资料/写入，公开响应不含B存在性；当前合法对象不变 | not_run |
| R11-T14 | 从本模块字段表逐组移除必需输入 | INVALID_ARGUMENT及字段路径；不得补造主体、项目或事实 | not_run |
| R11-T15 | 使用未支持schema/profile及实质未知字段 | 拒绝或显式unsupported；不静默删字段骗校验 | not_run |
| R11-T16 | 同源版本/操作键提交两遍 | 按本节幂等规则处理，副作用/独立证据不重复；纯读可以重查并保快照差别 | not_run |
| R11-T17 | 两调用携同expected_revision更新同对象 | 持久写至多一方按原前态成功，另一方冲突/受控重读；纯读不得写事实 | not_run |
| R11-T18 | 准备后提交/供给前对来源加tombstone | 相关派生停用或拒提交，旧缓存不复活；无来源型运行记录核相应取消/策略 | not_run |
| R11-T19 | 阶段处理中提交相关来源新版本 | 旧版本不能覆盖最新纠正；重算/partial/失效原因可查 | not_run |
| R11-T20 | 将一个必须依赖返回unavailable | 保具体缺口；不把失败当正常空结果或全部完成 | not_run |
| R11-T21 | 在本模块关键算法/调用处返回错误 | 错误回传，阶段failed/unknown；没有可用结论就不伪报成功 | not_run |
| R11-T22 | 故意令本模块外部阶段超过deadline | 取消按能力记录，迟到结果不绕版本与取消检查；真实停止未知照实 | not_run |
| R11-T23 | 准备完成后、提交/供给前取消run或job | 未发生副作用不再执行；已发生事实不抹除，结果另记 | not_run |
| R11-T24 | 租约失效后旧worker尝试写回 | 有持久写的路径由fencing/CAS拒绝；只读路径不借续读取得写权 | not_run |
| R11-T25 | 对持久写路径在关联对象写入间注入异常 | 本库事务全有或全无；跨库显示中间态并可对账；只读不虚称事务验收 | not_run |
| R11-T26 | 在commit后/返回前断开响应 | 按原键查询回执，不盲新建意图；只读重试不得假定语料未变化 | not_run |
| R11-T27 | 相关outbox成功处理但ACK丢失再投递 | 按源/处理器版本幂等，不产生第二次认知强化或外部动作 | not_run |
| R11-T28 | 规范对象已修订而索引未追平 | 报告水位并查规范store或partial；不能将旧命中当最新事实 | not_run |
| R11-T29 | 样本含emoji、不是/仅在/可能等限定 | 源范围和原意保留；截断不得变反义；非文本对象用其真实坐标 | not_run |
| R11-T30 | 加入同名不同ID与未定指代候选 | 保持候选/unknown，不自动合并；无人物职责模块不自创人物推断 | not_run |
| R11-T31 | 旧/新有效期及接收顺序不一致 | 按真实时间/版本契约处理；无法比较时不擅选最后接收值 | not_run |
| R11-T32 | 同材料被旧插件与当前出口同时提出 | 只有R22可最终装配，去本宿主拥有旧块而保用户/系统/工具结构 | not_run |
| R11-T33 | 提供本地保存/尝试但无业务或送达回执 | 不得升级成已理解/已完成/已送达；按该模块实际成果层级标注 | not_run |
| R11-T34 | 恢复相同逻辑初态重跑，同配置与fixture hash | 可复现本模块约定结果；时间/随机ID差异不混成语义提升 | not_run |
| R11-T35 | 输入含私密正文/凭据状外部内容 | 普通日志与索引/投影不泄漏禁止范围；审计仅留必要ID和固定原因 | not_run |
| R11-T36 | 只有文档、模拟对象或模型自评时要求标通过 | 保design/static/synthetic/real_host分轴；缺真实证据标not_run/unknown | not_run |

T01–T12是该模块专属语义/业务场景；T13–T36是必须绑定本模块实际写读路径执行的协议/故障场景，不能空跑通用脚本就全标通过。先从字段表构造合法基准fixture，再只改变本例条件；对不适用的写路径要给可审证据说明与对应只读判据，不能把未测记成pass。

## R11.17 交付证据、通过门槛与未完成项

交付ReflectionStore实现/schema迁移、输入输出fixture、合法及反例来源、实际存储与调用回执、真实入口覆盖、查询及注入观察、失败恢复报告。证据等级design/static/synthetic_process/real_host/storage_fault/production分开。

模块通过至少需要专属场景和适用协议场景的实际证据；整套通过还需LINKAGE.md跨模块链。当前文档生成/类型DDL检查不算本模块36例已跑。已有候选仅作为迁移基础，现场未知和未实现开放语义仍未验。

## R11.18 实现次序、兼容策略与设计自审

先固定本模块字段/状态/真源→实现受权最小路径与回执→跑专属正反例→接入上游/下游→做恢复/删除/冲突→在真实隔离宿主检查请求或结果。本模块不得以优化名义删除保留矩阵中已有功能，不改C032严格profile顶层来绕验证。

本次设计检查关注：按问题/轴/适用条件查，带反证、版本和result；不召回已失效心理标签。 当前场景需要经验才注入最短方法与限制；不把夜间全部成长日志注入每轮。 对所有结果都分别标明对象、版本、来源、局限和验证等级；不以同一success覆盖入账、理解、注入、生成、送达与执行。生产边界不变，不随文档生成而开通部署。



---

# R12　Home Atlas资料地图：详细设计与验收规格

版本：everlight/6-design；模块契约：r12/1；日期：2026-11-08。本文为设计，全部功能验收初始not_run。最终裁决以FINAL_DECISIONS.md和MODULE_DECISIONS.md为准。与contracts/共同生效，不是已安装服务。

## R12.01 定义、边界与可证伪成功标准

Document登记、当前版本/历史定位、索引状态与原文读取计划。

唯一业务责任服务是`AtlasRegistry`。输入必须满足第3节，输出必须满足第4节及GLOBAL_PROTOCOL。成功必须可从实际记录/回执读回，而不是模型自称完成。

原有具体机制及边界（保留并由本版细化）：

**原理与基础**：资料地图连接任务、文件、代码及其版本；候选支持显式索引，不证明扫描过真实目录。

**数据**：document_id、受权URI/路径、project_id、revision/content_hash、来源时间、ACL、段落范围、derived_index_version、索引水位和旧版本引用。路径只是定位，不是权限凭证。

**步骤**：①显式授权目录/对象建立登记；②变化事件检查文件版本，失效旧派生索引；③当前任务按项目查候选；④R16按真实文件版本读取；⑤索引与文件不一致时返回stale并安排重建；⑥文件已删/移动保留合适状态，不能引用旧定位说现在可用。

**必须扣住**：R03工作、R15查找、R16来源、R18权限和路径防护、R19备份。需要防路径穿越、符号链接逃逸和文件读取期间变化，不能只检查路径字符串前缀。

**例子/反例**：用户找长明第二稿，先查项目版本，不把第一稿摘要当最新。文件在读取中变化则拒绝把混合片段当同一版本，重新读或标不完整。

**写入归属与状态**：AtlasRegistry写登记和版本，FileReader只读授权对象。状态available/stale/moved/missing/denied，不能把denied展示成对方的文件名与目录结构。远程链接登记的是定位信息，不承诺已读取或永远可访问。

**实现细节**：source_revision绑定原件hash、提取器版本和导出时间；PDF页码、段落锚和UTF-8文本偏移分列，不能把提取文本字节位置冒充PDF页面坐标。二进制附件有OCR/转录缺口要保留。文件替换后派生embedding/summary失效但历史引用仍能指向旧件，若旧件不可用则明确标缺。路径核验在打开真实对象时完成，并检查读取前后版本一致性。

## R12.02 位置、所有权与现状映射

规范数据族：`atlas_memory`。R03–R12对应十类typed store；其余是来源/运行/派生服务，不能再算额外心理记忆。

注册/版本CAS；内容变化重建派生，旧游标不能复用。符号链接/路径逃逸在实际打开时核。

当前可核候选为0.32.0-candidate及其局部源码，不等于D现场已具备该接口。内核既有memories(kind)+versions继续保留，目标分型表由显式迁移产生；本模块不能绕规范API直接改别类记录。详见DATA_STORES.md的表归属。

## R12.03 输入契约

授权对象/目录登记、文件版本与提取回执、当前项目资料查询、变更事件。

调用外层必有schema_version、request_id、可信principal/scope、operation、deadline/cancel；写入带expected_revision和支持幂等的operation_key。读取带filter/snapshot/cursor，不能将模型提供的actor/scope直接当认证。类型表中可空项显式null，未执行检查不得以空数组冒“确认没有”。

## R12.04 输出、回执与错误契约

Document登记、当前版本/历史定位、索引状态与原文读取计划。

统一返回{request_id,operation_id,module,disposition,object_refs,base_revision,committed_revision,coverage,gaps,receipt_ref,evidence_level}。对象引用含kind/id/revision，来源引用含source_id/source_revision/hash/range。纯读committed_revision=null；候选disposition=proposed，不能返回committed冒正式状态。

错误至少区分INVALID_ARGUMENT、FORBIDDEN/NOT_FOUND_OR_HIDDEN、CONFLICT、SOURCE_UNAVAILABLE、TIMEOUT、RESOURCE_EXHAUSTED、UNVERIFIED_BINDING、INTERNAL；有提交路径还要commit_outcome=not_committed/committed/unknown。未知结果先按原键查回执。

## R12.05 数据字段、状态与索引

| 字段组 | 类型 | 约束与语义 |
|---|---|---|
| document_id/resource_kind | ID/enum | 文件/代码/页面/媒体等稳定登记 |
| locator/acl_ref | object/ID | 定位不是权限，凭据不进文本 |
| content_hash/source_revision | hash/string | 确切原件身份 |
| extractor_version/extraction_refs | string/array | 原件与OCR/转录分开 |
| project_id/time | nullable ID/object | 来源与适用时期 |
| anchors | array | 页码、段落、音视频时间、文本字节区间分列 |
| index_watermarks | object | 文件变更后的派生滞后 |
| state | enum | available/stale/moved/missing/denied |

公共对象字段：id、kind、schema_version、scope、created_at、created_by、revision、status、record_digest；每项来源或实际宿主创建依据另存。组字段细分时必须列schema，不用不同拼法兼容猜测。

登记→available；变更stale→重提取/重索引；移动映射新定位；missing/denied不当空正文。

最低索引：scope+kind+有效状态+业务主键；来源反向依赖(source_id,source_revision)；对象版本(id,revision)。本模块特定检索维度由第11节给出。索引只定位，当前有效性仍核规范记录，不以索引命中当接受事实。

## R12.06 自动触发与完整处理顺序

1. 核授权资源与安全打开对象，不只比路径字符串前缀。
2. 获取稳定版本/hash，原件读取前后核一致。
3. OCR/转录/文本抽取保存自己的版本和覆盖。
4. 文件变更事件使旧摘要/向量停用或标陈旧。
5. 当前任务按项目/版本查登记，R16读真实来源。
6. 迁移/删除传播到定位、派生与缓存，历史引用可缺但不能伪称仍可读。

宿主触发后逐阶段记started/succeeded/failed/skipped/unverified；不需要运行的步骤可skipped，但不能将缺必需依赖也算正常跳过。只读规划不改原始事件，模型调用不在数据库长锁内。

## R12.07 关键算法、决策与禁止捷径

先有显式登记，不能因Atlas服务存在宣称扫过所有目录。二进制页面坐标与提取文本字节不是同一种定位；读中变化需重读或partial，不能拼两个版本。

每次推导均把直接观察、他人转述、候选解释、规范记录、外部结果分开。source_ref能定位仅证明原文存在；如涉及开放语义，必须由相应支持验证和反例测试决定是否可用，不能单靠hash/正则。算法参数只影响工程取舍，不授身份、权限或关系事实。

## R12.08 幂等、修订、并发与提交

注册/版本CAS；内容变化重建派生，旧游标不能复用。符号链接/路径逃逸在实际打开时核。

操作重试与新业务事件分开；相同操作键异实质请求必须冲突。读取允许新快照结果变化，不能为了固定输出使用已撤回缓存。规范状态修改用expected_revision；跨库步骤分别留回执与reconciliation_required，不以一库commit冒全局事务。D依赖实际输出的SelfState/八域仍须强run/attempt/scope绑定，不让本模块日志替代。

## R12.09 更正、失效、删除与反向依赖

凡`atlas_memory`中有源派生物，登记source_root、source_revision、processor_version及依赖关系；纠正到来时先invalid_for_use/争议，后重建，不继续拿旧结论无提示作答。删除先由R18tombstone阻可用性，再清正文/索引/缓存/Wiki/备份策略；不能仅删引文保留相同推断。

无人物/心理职责的运行对象只记录必要状态，不因本模块失败写用户生气或D疏远。已发生事件和已表达的当时状态不被后来解释覆写；隐私擦除走专用治理路径。

## R12.10 模块扣接与交接责任

| 方向 | 对接对象 | 必须交接的内容 |
|---|---|---|
| 输入 | R01 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R03 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R18 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R19 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R20 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输出 | R10 | AtlasRegistry结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R13 | AtlasRegistry结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R15 | AtlasRegistry结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R16 | AtlasRegistry结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R17 | AtlasRegistry结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R22 | AtlasRegistry结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |

交接由HostAdapter/Coordinator调用，不让两个模块彼此递归无限互调。每个edge均记录当前事件/源版本、调用目的、预算、取消与真实回执；完整schema和时序见LINKAGE.md。接收失败保待处理/限制，不能发送空结果伪装成功。

## R12.11 如何存、如何召回、如何区分其他记忆

按项目+document_id+版本/类型查；原件与衍生索引分别看可用性。

受权路线只查询声明的kind及其规范业务表；不能把情绪解释当语义事实、反思当亲历、工具尝试当结果。共享来源可同时支持多个kind，但每条命题有独立语义和审核状态；同源同命题折叠，不合并同源不同要求。必要后续沿依赖图取回，超过budget标partial。

## R12.12 注入的进入、最短表示与退出

只给当前需要的文件状态/准确片段；无需把整个目录树注入。拒绝项不泄漏存在性。

当材料进入R22候选，每条必须能说明当前anchor、need_reason、新增信息和support_verdict。已在真实messages充分表达则不重注；换窗缺了则可重供。话题切换、完成、失效、撤回或无本轮用途就退出动态块，规范记忆保留。zero injection不关闭宿主最低检查，故障也不能伪装none_needed。

## R12.13 后台、恢复、超时与取消

本模块相关后台作业以scope+源版本+operation+schema/processor版本幂等，经R17持久队列领取。对于纯读路径，只保存必要阅读/覆盖进度，不声称有待提交事实。恢复时读最新删除、授权、规范状态及atlas_memory版本，再决定重算/继续/放弃。

失约worker写回须被fencing拒绝；模型调用超时发取消，底层不能证实停止就记cancel_unconfirmed，迟到结果不能自动commit。外部动作的unknown由R14先对账。未部署后台或钩子则标missing，不能称离线持续执行。

## R12.14 资源、隐私与降级规则

与R24共享每run/job预算，不为R12另开无界模型循环。前台最低检查、输入入账、必要纠正/边界和输出预留优先；可选语义、图展开、后台整理可暂停。所有查询与补读都有limit/deadline/stop_reason；候选上限不是注入配额。

故障使用第4节错误和coverage，普通交流尽量继续，依赖缺失的动作限制。密钥/原始私聊不进普通日志；被拒scope不出现在公开解释中。资源阈值不是情绪好感阈值，未实测目标机器不报固定延迟/容量保证。

## R12.15 贯通例子与反例

用户要长明第二稿：核document版本及原件，不能拿第一稿摘要当最新；读取期间替换则报冲突。

验证时把该场景与原事件、已有记录、真实请求或结果链同时保存：输入→AtlasRegistry→下游回执。仅看到本模块返回JSON不证明生成模型采用，也不证明真实动作完成。正确处理应保留未知、合法来源和以后修订入口；能说出漂亮话不替代字段/版本/来源正确。

## R12.16 36项模块与协议验收需求目录（非执行fixture）

| ID | 准备/触发 | 必须结果；不满足即失败 | 当前状态 |
|---|---|---|---|
| R12-T01 | 在隔离fixture中构造：当前稿与历史稿分开 | 当前稿与历史稿分开 | not_run |
| R12-T02 | 在隔离fixture中构造：文件变更使旧索引失效 | 文件变更使旧索引失效 | not_run |
| R12-T03 | 在隔离fixture中构造：相同路径新hash不冒旧版 | 相同路径新hash不冒旧版 | not_run |
| R12-T04 | 在隔离fixture中构造：读取中替换不拼混片段 | 读取中替换不拼混片段 | not_run |
| R12-T05 | 在隔离fixture中构造：路径穿越/链接逃逸拒绝 | 路径穿越/链接逃逸拒绝 | not_run |
| R12-T06 | 在隔离fixture中构造：OCR空不解释成原件空 | OCR空不解释成原件空 | not_run |
| R12-T07 | 在隔离fixture中构造：PDF页码不冒UTF8区间 | PDF页码不冒UTF8区间 | not_run |
| R12-T08 | 在隔离fixture中构造：无登记不称目录已扫描 | 无登记不称目录已扫描 | not_run |
| R12-T09 | 在隔离fixture中构造：权限拒绝不泄漏目录名 | 权限拒绝不泄漏目录名 | not_run |
| R12-T10 | 在隔离fixture中构造：原件已删回missing而非全文 | 原件已删回missing而非全文 | not_run |
| R12-T11 | 在隔离fixture中构造：大附件分块保覆盖 | 大附件分块保覆盖 | not_run |
| R12-T12 | 在隔离fixture中构造：迁移后重定位仍保稳定来源ID | 迁移后重定位仍保稳定来源ID | not_run |
| R12-T13 | 另建scope-B对象并以scope-A主体访问 | 拒绝相应资料/写入，公开响应不含B存在性；当前合法对象不变 | not_run |
| R12-T14 | 从本模块字段表逐组移除必需输入 | INVALID_ARGUMENT及字段路径；不得补造主体、项目或事实 | not_run |
| R12-T15 | 使用未支持schema/profile及实质未知字段 | 拒绝或显式unsupported；不静默删字段骗校验 | not_run |
| R12-T16 | 同源版本/操作键提交两遍 | 按本节幂等规则处理，副作用/独立证据不重复；纯读可以重查并保快照差别 | not_run |
| R12-T17 | 两调用携同expected_revision更新同对象 | 持久写至多一方按原前态成功，另一方冲突/受控重读；纯读不得写事实 | not_run |
| R12-T18 | 准备后提交/供给前对来源加tombstone | 相关派生停用或拒提交，旧缓存不复活；无来源型运行记录核相应取消/策略 | not_run |
| R12-T19 | 阶段处理中提交相关来源新版本 | 旧版本不能覆盖最新纠正；重算/partial/失效原因可查 | not_run |
| R12-T20 | 将一个必须依赖返回unavailable | 保具体缺口；不把失败当正常空结果或全部完成 | not_run |
| R12-T21 | 在本模块关键算法/调用处返回错误 | 错误回传，阶段failed/unknown；没有可用结论就不伪报成功 | not_run |
| R12-T22 | 故意令本模块外部阶段超过deadline | 取消按能力记录，迟到结果不绕版本与取消检查；真实停止未知照实 | not_run |
| R12-T23 | 准备完成后、提交/供给前取消run或job | 未发生副作用不再执行；已发生事实不抹除，结果另记 | not_run |
| R12-T24 | 租约失效后旧worker尝试写回 | 有持久写的路径由fencing/CAS拒绝；只读路径不借续读取得写权 | not_run |
| R12-T25 | 对持久写路径在关联对象写入间注入异常 | 本库事务全有或全无；跨库显示中间态并可对账；只读不虚称事务验收 | not_run |
| R12-T26 | 在commit后/返回前断开响应 | 按原键查询回执，不盲新建意图；只读重试不得假定语料未变化 | not_run |
| R12-T27 | 相关outbox成功处理但ACK丢失再投递 | 按源/处理器版本幂等，不产生第二次认知强化或外部动作 | not_run |
| R12-T28 | 规范对象已修订而索引未追平 | 报告水位并查规范store或partial；不能将旧命中当最新事实 | not_run |
| R12-T29 | 样本含emoji、不是/仅在/可能等限定 | 源范围和原意保留；截断不得变反义；非文本对象用其真实坐标 | not_run |
| R12-T30 | 加入同名不同ID与未定指代候选 | 保持候选/unknown，不自动合并；无人物职责模块不自创人物推断 | not_run |
| R12-T31 | 旧/新有效期及接收顺序不一致 | 按真实时间/版本契约处理；无法比较时不擅选最后接收值 | not_run |
| R12-T32 | 同材料被旧插件与当前出口同时提出 | 只有R22可最终装配，去本宿主拥有旧块而保用户/系统/工具结构 | not_run |
| R12-T33 | 提供本地保存/尝试但无业务或送达回执 | 不得升级成已理解/已完成/已送达；按该模块实际成果层级标注 | not_run |
| R12-T34 | 恢复相同逻辑初态重跑，同配置与fixture hash | 可复现本模块约定结果；时间/随机ID差异不混成语义提升 | not_run |
| R12-T35 | 输入含私密正文/凭据状外部内容 | 普通日志与索引/投影不泄漏禁止范围；审计仅留必要ID和固定原因 | not_run |
| R12-T36 | 只有文档、模拟对象或模型自评时要求标通过 | 保design/static/synthetic/real_host分轴；缺真实证据标not_run/unknown | not_run |

T01–T12是该模块专属语义/业务场景；T13–T36是必须绑定本模块实际写读路径执行的协议/故障场景，不能空跑通用脚本就全标通过。先从字段表构造合法基准fixture，再只改变本例条件；对不适用的写路径要给可审证据说明与对应只读判据，不能把未测记成pass。

## R12.17 交付证据、通过门槛与未完成项

交付AtlasRegistry实现/schema迁移、输入输出fixture、合法及反例来源、实际存储与调用回执、真实入口覆盖、查询及注入观察、失败恢复报告。证据等级design/static/synthetic_process/real_host/storage_fault/production分开。

模块通过至少需要专属场景和适用协议场景的实际证据；整套通过还需LINKAGE.md跨模块链。当前文档生成/类型DDL检查不算本模块36例已跑。已有候选仅作为迁移基础，现场未知和未实现开放语义仍未验。

## R12.18 实现次序、兼容策略与设计自审

先固定本模块字段/状态/真源→实现受权最小路径与回执→跑专属正反例→接入上游/下游→做恢复/删除/冲突→在真实隔离宿主检查请求或结果。本模块不得以优化名义删除保留矩阵中已有功能，不改C032严格profile顶层来绕验证。

本次设计检查关注：按项目+document_id+版本/类型查；原件与衍生索引分别看可用性。 只给当前需要的文件状态/准确片段；无需把整个目录树注入。拒绝项不泄漏存在性。 对所有结果都分别标明对象、版本、来源、局限和验证等级；不以同一success覆盖入账、理解、注入、生成、送达与执行。生产边界不变，不随文档生成而开通部署。



---

# R13　连续性与恢复中枢：详细设计与验收规格

版本：everlight/6-design；模块契约：r13/1；日期：2026-11-08。本文为设计，全部功能验收初始not_run。最终裁决以FINAL_DECISIONS.md和MODULE_DECISIONS.md为准。与contracts/共同生效，不是已安装服务。

## R13.01 定义、边界与可证伪成功标准

可验证Checkpoint/恢复报告/当前Focus；不执行历史动作。

唯一业务责任服务是`ContinuityStore`。输入必须满足第3节，输出必须满足第4节及GLOBAL_PROTOCOL。成功必须可从实际记录/回执读回，而不是模型自称完成。

原有具体机制及边界（保留并由本版细化）：

**原理与基础**：恢复“事情进行到哪里”，不仅是摘要。候选有focus/read_progress、快照和状态版本；真实压后八步及全部钩子未证。

**数据**：checkpoint_id、主干版本、项目/任务焦点、人物候选、未结episode、上次情绪状态指针、承诺/unknown动作、检索计划与游标、来源及索引水位、run/proposal状态、覆盖。

**步骤**：①可用压前钩子提交检查点，不存在则如实gap；②恢复认证范围和主干；③核快照、来源版本与删除记录；④恢复R03工作和未核动作；⑤R15重新查与当前有关内容；⑥未完成读取用游标继续；⑦正在生成但结果未知不自动重放；⑧依可信新输出重新推进状态。

**必须扣住**：R03/R07/R08/R09/R14/R16→R13；R19恢复一致性、R18权限、R21触发；R13→R15/R22。旧快照不能覆盖之后已完成的任务或已撤回授权。

**例子/反例**：重启前正在整理情绪方案，恢复后知道还缺哪条来源；发送上次是否成功未知就先查，不重发。“压后检查脚本存在”不等于真实宿主执行过全部步骤。

**写入归属与状态**：CheckpointStore写已提交状态的指针快照，不把整轮尚未证实的proposal混入正式历史。状态created/validated/restored/rejected；restored只说明本次恢复完成，仍可能有来源缺失或外部动作unknown。恢复用最新授权/删除账约束旧快照。

**实现细节**：检查点分别记录raw_event_watermark、control_state_revision、index_watermarks和pending_runs；多库不一致时留reconciliation_required。恢复先处理删除/撤回，再处理任务及行动，再重做相关性查询，最后构造context。旧run的输出若后来被可信桥补回，仅能按原绑定规则对账，不能移花接木挂给当前attempt。检查点本身不执行发送、工具或记忆强化。

## R13.02 位置、所有权与现状映射

规范数据族：`checkpoints`。R03–R12对应十类typed store；其余是来源/运行/派生服务，不能再算额外心理记忆。

检查点引用冻结版本；恢复只创建报告与新的合法视图，禁止旧快照overwrite live state；多库对账不宣称全局事务。

当前可核候选为0.32.0-candidate及其局部源码，不等于D现场已具备该接口。内核既有memories(kind)+versions继续保留，目标分型表由显式迁移产生；本模块不能绕规范API直接改别类记录。详见DATA_STORES.md的表归属。

## R13.03 输入契约

可信scope、已提交主干/任务/认知版本、事件水位、未读游标、unknown动作及最新删除账。

调用外层必有schema_version、request_id、可信principal/scope、operation、deadline/cancel；写入带expected_revision和支持幂等的operation_key。读取带filter/snapshot/cursor，不能将模型提供的actor/scope直接当认证。类型表中可空项显式null，未执行检查不得以空数组冒“确认没有”。

## R13.04 输出、回执与错误契约

可验证Checkpoint/恢复报告/当前Focus；不执行历史动作。

统一返回{request_id,operation_id,module,disposition,object_refs,base_revision,committed_revision,coverage,gaps,receipt_ref,evidence_level}。对象引用含kind/id/revision，来源引用含source_id/source_revision/hash/range。纯读committed_revision=null；候选disposition=proposed，不能返回committed冒正式状态。

错误至少区分INVALID_ARGUMENT、FORBIDDEN/NOT_FOUND_OR_HIDDEN、CONFLICT、SOURCE_UNAVAILABLE、TIMEOUT、RESOURCE_EXHAUSTED、UNVERIFIED_BINDING、INTERNAL；有提交路径还要commit_outcome=not_committed/committed/unknown。未知结果先按原键查回执。

## R13.05 数据字段、状态与索引

| 字段组 | 类型 | 约束与语义 |
|---|---|---|
| checkpoint_id/schema_version | ID/string | 稳定快照协议 |
| identity/work/focus_refs | array | ID+revision/digest而非另一套事实 |
| affect/concern_refs | array | last_known及当前未知分开 |
| pending_actions | array | 实际action状态及外部核验入口 |
| source/control/index_watermarks | object | 两库/索引关联界限 |
| read_cursors/proposal_refs | array | 版本绑定及未提交标识 |
| deletion/policy_revision | object | 恢复须以最新治理状态为准 |
| restore_status/gaps | enum/array | created/validated/restored/rejected与缺口 |

公共对象字段：id、kind、schema_version、scope、created_at、created_by、revision、status、record_digest；每项来源或实际宿主创建依据另存。组字段细分时必须列schema，不用不同拼法兼容猜测。

checkpoint created→validated；restore staged→检查最新治理与版本→restored/partial/rejected。恢复成功不意味着外部动作全部确认。

最低索引：scope+kind+有效状态+业务主键；来源反向依赖(source_id,source_revision)；对象版本(id,revision)。本模块特定检索维度由第11节给出。索引只定位，当前有效性仍核规范记录，不以索引命中当接受事实。

## R13.06 自动触发与完整处理顺序

1. 压前真实hook存在则保存已提交指针；不存在记hook_missing。
2. 恢复先认证scope，再加载最新删除与撤回账。
3. 校schema/hash、水位及引用，跨库不一致生成对账任务。
4. 读最新任务、身份、unknown动作，旧checkpoint不覆盖新revision。
5. 相关状态进入检索规划；失效cursor重计划；未生成完的run不自动重放。
6. 把缺口和当前足够状态交R22；真实新输出后再推进对应认知提交。

宿主触发后逐阶段记started/succeeded/failed/skipped/unverified；不需要运行的步骤可skipped，但不能将缺必需依赖也算正常跳过。只读规划不改原始事件，模型调用不在数据库长锁内。

## R13.07 关键算法、决策与禁止捷径

恢复是读取已知事实与重查当前相关材料，不是复制整段旧prompt。输出已落事件库但认知未commit需observed_uncommitted对账；无强归属仍unverified，不挂给新attempt。

每次推导均把直接观察、他人转述、候选解释、规范记录、外部结果分开。source_ref能定位仅证明原文存在；如涉及开放语义，必须由相应支持验证和反例测试决定是否可用，不能单靠hash/正则。算法参数只影响工程取舍，不授身份、权限或关系事实。

## R13.08 幂等、修订、并发与提交

检查点引用冻结版本；恢复只创建报告与新的合法视图，禁止旧快照overwrite live state；多库对账不宣称全局事务。

操作重试与新业务事件分开；相同操作键异实质请求必须冲突。读取允许新快照结果变化，不能为了固定输出使用已撤回缓存。规范状态修改用expected_revision；跨库步骤分别留回执与reconciliation_required，不以一库commit冒全局事务。D依赖实际输出的SelfState/八域仍须强run/attempt/scope绑定，不让本模块日志替代。

## R13.09 更正、失效、删除与反向依赖

凡`checkpoints`中有源派生物，登记source_root、source_revision、processor_version及依赖关系；纠正到来时先invalid_for_use/争议，后重建，不继续拿旧结论无提示作答。删除先由R18tombstone阻可用性，再清正文/索引/缓存/Wiki/备份策略；不能仅删引文保留相同推断。

无人物/心理职责的运行对象只记录必要状态，不因本模块失败写用户生气或D疏远。已发生事件和已表达的当时状态不被后来解释覆写；隐私擦除走专用治理路径。

## R13.10 模块扣接与交接责任

| 方向 | 对接对象 | 必须交接的内容 |
|---|---|---|
| 输入 | R03 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R07 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R08 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R09 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R10 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R14 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R16 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R18 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R19 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R20 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输出 | R15 | ContinuityStore结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R21 | ContinuityStore结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R22 | ContinuityStore结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R23 | ContinuityStore结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |

交接由HostAdapter/Coordinator调用，不让两个模块彼此递归无限互调。每个edge均记录当前事件/源版本、调用目的、预算、取消与真实回执；完整schema和时序见LINKAGE.md。接收失败保待处理/限制，不能发送空结果伪装成功。

## R13.11 如何存、如何召回、如何区分其他记忆

启动/换窗/压缩后按可信焦点恢复，再查询有关后续；不把恢复摘要当全文已读。

受权路线只查询声明的kind及其规范业务表；不能把情绪解释当语义事实、反思当亲历、工具尝试当结果。共享来源可同时支持多个kind，但每条命题有独立语义和审核状态；同源同命题折叠，不合并同源不同要求。必要后续沿依赖图取回，超过budget标partial。

## R13.12 注入的进入、最短表示与退出

最小携带集：当前任务/必要主干/当前有关关切/unknown动作/缺口，必要时重新供给；不是长期固定大摘要。

当材料进入R22候选，每条必须能说明当前anchor、need_reason、新增信息和support_verdict。已在真实messages充分表达则不重注；换窗缺了则可重供。话题切换、完成、失效、撤回或无本轮用途就退出动态块，规范记忆保留。zero injection不关闭宿主最低检查，故障也不能伪装none_needed。

## R13.13 后台、恢复、超时与取消

本模块相关后台作业以scope+源版本+operation+schema/processor版本幂等，经R17持久队列领取。对于纯读路径，只保存必要阅读/覆盖进度，不声称有待提交事实。恢复时读最新删除、授权、规范状态及checkpoints版本，再决定重算/继续/放弃。

失约worker写回须被fencing拒绝；模型调用超时发取消，底层不能证实停止就记cancel_unconfirmed，迟到结果不能自动commit。外部动作的unknown由R14先对账。未部署后台或钩子则标missing，不能称离线持续执行。

## R13.14 资源、隐私与降级规则

与R24共享每run/job预算，不为R13另开无界模型循环。前台最低检查、输入入账、必要纠正/边界和输出预留优先；可选语义、图展开、后台整理可暂停。所有查询与补读都有limit/deadline/stop_reason；候选上限不是注入配额。

故障使用第4节错误和coverage，普通交流尽量继续，依赖缺失的动作限制。密钥/原始私聊不进普通日志；被拒scope不出现在公开解释中。资源阈值不是情绪好感阈值，未实测目标机器不报固定延迟/容量保证。

## R13.15 贯通例子与反例

重启前文档已写、发送未知：恢复后核文档及渠道回执，不重发、不重新报告“尚未写”。

验证时把该场景与原事件、已有记录、真实请求或结果链同时保存：输入→ContinuityStore→下游回执。仅看到本模块返回JSON不证明生成模型采用，也不证明真实动作完成。正确处理应保留未知、合法来源和以后修订入口；能说出漂亮话不替代字段/版本/来源正确。

## R13.16 36项模块与协议验收需求目录（非执行fixture）

| ID | 准备/触发 | 必须结果；不满足即失败 | 当前状态 |
|---|---|---|---|
| R13-T01 | 在隔离fixture中构造：换窗恢复唯一可信工作焦点 | 换窗恢复唯一可信工作焦点 | not_run |
| R13-T02 | 在隔离fixture中构造：旧快照不能复活已取消任务 | 旧快照不能复活已取消任务 | not_run |
| R13-T03 | 在隔离fixture中构造：最新删除先于旧内容恢复 | 最新删除先于旧内容恢复 | not_run |
| R13-T04 | 在隔离fixture中构造：未知发送先查询不重放 | 未知发送先查询不重放 | not_run |
| R13-T05 | 在隔离fixture中构造：缺压前hook不报无缝恢复 | 缺压前hook不报无缝恢复 | not_run |
| R13-T06 | 在隔离fixture中构造：无强attempt绑定保持unverified | 无强attempt绑定保持unverified | not_run |
| R13-T07 | 在隔离fixture中构造：事件库已输出控制库未提交可对账 | 事件库已输出控制库未提交可对账 | not_run |
| R13-T08 | 在隔离fixture中构造：游标源改版后不能继续拼接 | 游标源改版后不能继续拼接 | not_run |
| R13-T09 | 在隔离fixture中构造：身份主干缺失不补故事 | 身份主干缺失不补故事 | not_run |
| R13-T10 | 在隔离fixture中构造：相同恢复请求幂等不执行工具 | 相同恢复请求幂等不执行工具 | not_run |
| R13-T11 | 在隔离fixture中构造：当前实际context缺状态时重供给 | 当前实际context缺状态时重供给 | not_run |
| R13-T12 | 在隔离fixture中构造：恢复失败普通对话仍可说明必要局限 | 恢复失败普通对话仍可说明必要局限 | not_run |
| R13-T13 | 另建scope-B对象并以scope-A主体访问 | 拒绝相应资料/写入，公开响应不含B存在性；当前合法对象不变 | not_run |
| R13-T14 | 从本模块字段表逐组移除必需输入 | INVALID_ARGUMENT及字段路径；不得补造主体、项目或事实 | not_run |
| R13-T15 | 使用未支持schema/profile及实质未知字段 | 拒绝或显式unsupported；不静默删字段骗校验 | not_run |
| R13-T16 | 同源版本/操作键提交两遍 | 按本节幂等规则处理，副作用/独立证据不重复；纯读可以重查并保快照差别 | not_run |
| R13-T17 | 两调用携同expected_revision更新同对象 | 持久写至多一方按原前态成功，另一方冲突/受控重读；纯读不得写事实 | not_run |
| R13-T18 | 准备后提交/供给前对来源加tombstone | 相关派生停用或拒提交，旧缓存不复活；无来源型运行记录核相应取消/策略 | not_run |
| R13-T19 | 阶段处理中提交相关来源新版本 | 旧版本不能覆盖最新纠正；重算/partial/失效原因可查 | not_run |
| R13-T20 | 将一个必须依赖返回unavailable | 保具体缺口；不把失败当正常空结果或全部完成 | not_run |
| R13-T21 | 在本模块关键算法/调用处返回错误 | 错误回传，阶段failed/unknown；没有可用结论就不伪报成功 | not_run |
| R13-T22 | 故意令本模块外部阶段超过deadline | 取消按能力记录，迟到结果不绕版本与取消检查；真实停止未知照实 | not_run |
| R13-T23 | 准备完成后、提交/供给前取消run或job | 未发生副作用不再执行；已发生事实不抹除，结果另记 | not_run |
| R13-T24 | 租约失效后旧worker尝试写回 | 有持久写的路径由fencing/CAS拒绝；只读路径不借续读取得写权 | not_run |
| R13-T25 | 对持久写路径在关联对象写入间注入异常 | 本库事务全有或全无；跨库显示中间态并可对账；只读不虚称事务验收 | not_run |
| R13-T26 | 在commit后/返回前断开响应 | 按原键查询回执，不盲新建意图；只读重试不得假定语料未变化 | not_run |
| R13-T27 | 相关outbox成功处理但ACK丢失再投递 | 按源/处理器版本幂等，不产生第二次认知强化或外部动作 | not_run |
| R13-T28 | 规范对象已修订而索引未追平 | 报告水位并查规范store或partial；不能将旧命中当最新事实 | not_run |
| R13-T29 | 样本含emoji、不是/仅在/可能等限定 | 源范围和原意保留；截断不得变反义；非文本对象用其真实坐标 | not_run |
| R13-T30 | 加入同名不同ID与未定指代候选 | 保持候选/unknown，不自动合并；无人物职责模块不自创人物推断 | not_run |
| R13-T31 | 旧/新有效期及接收顺序不一致 | 按真实时间/版本契约处理；无法比较时不擅选最后接收值 | not_run |
| R13-T32 | 同材料被旧插件与当前出口同时提出 | 只有R22可最终装配，去本宿主拥有旧块而保用户/系统/工具结构 | not_run |
| R13-T33 | 提供本地保存/尝试但无业务或送达回执 | 不得升级成已理解/已完成/已送达；按该模块实际成果层级标注 | not_run |
| R13-T34 | 恢复相同逻辑初态重跑，同配置与fixture hash | 可复现本模块约定结果；时间/随机ID差异不混成语义提升 | not_run |
| R13-T35 | 输入含私密正文/凭据状外部内容 | 普通日志与索引/投影不泄漏禁止范围；审计仅留必要ID和固定原因 | not_run |
| R13-T36 | 只有文档、模拟对象或模型自评时要求标通过 | 保design/static/synthetic/real_host分轴；缺真实证据标not_run/unknown | not_run |

T01–T12是该模块专属语义/业务场景；T13–T36是必须绑定本模块实际写读路径执行的协议/故障场景，不能空跑通用脚本就全标通过。先从字段表构造合法基准fixture，再只改变本例条件；对不适用的写路径要给可审证据说明与对应只读判据，不能把未测记成pass。

## R13.17 交付证据、通过门槛与未完成项

交付ContinuityStore实现/schema迁移、输入输出fixture、合法及反例来源、实际存储与调用回执、真实入口覆盖、查询及注入观察、失败恢复报告。证据等级design/static/synthetic_process/real_host/storage_fault/production分开。

模块通过至少需要专属场景和适用协议场景的实际证据；整套通过还需LINKAGE.md跨模块链。当前文档生成/类型DDL检查不算本模块36例已跑。已有候选仅作为迁移基础，现场未知和未实现开放语义仍未验。

## R13.18 实现次序、兼容策略与设计自审

先固定本模块字段/状态/真源→实现受权最小路径与回执→跑专属正反例→接入上游/下游→做恢复/删除/冲突→在真实隔离宿主检查请求或结果。本模块不得以优化名义删除保留矩阵中已有功能，不改C032严格profile顶层来绕验证。

本次设计检查关注：启动/换窗/压缩后按可信焦点恢复，再查询有关后续；不把恢复摘要当全文已读。 最小携带集：当前任务/必要主干/当前有关关切/unknown动作/缺口，必要时重新供给；不是长期固定大摘要。 对所有结果都分别标明对象、版本、来源、局限和验证等级；不以同一success覆盖入账、理解、注入、生成、送达与执行。生产边界不变，不随文档生成而开通部署。



---

# R14　工具与行动账：详细设计与验收规格

版本：everlight/6-design；模块契约：r14/1；日期：2026-11-08。本文为设计，全部功能验收初始not_run。最终裁决以FINAL_DECISIONS.md和MODULE_DECISIONS.md为准。与contracts/共同生效，不是已安装服务。

## R14.01 定义、边界与可证伪成功标准

行动决策、attempt/receipt与核验结果；供工作/承诺反馈使用。

唯一业务责任服务是`ActionLedger`。输入必须满足第3节，输出必须满足第4节及GLOBAL_PROTOCOL。成功必须可从实际记录/回执读回，而不是模型自称完成。

原有具体机制及边界（保留并由本版细化）：

**原理与基础**：将计划、尝试和结果分开。候选有action/receipt/guard SDK，实际工具链及所有发送口未接。

**数据**：action_id、intent、具体目标、scope、authorization_ref、预期副作用、idempotency_key、attempts、cancel_token、receipts[]、verification=success|failure|unknown、业务状态。message delivered、工具完成、外部结果可分开。

**步骤**：①R03或模型提出意图；②实际副作用发生前R18核当前授权和目标，R06核适用程序；③记录即将尝试再调用受控执行器；④成功回执/超时/取消分别入账；⑤unknown先查外部状态；⑥确认结果回流R03/R11/关系修复。撤回可能阻止未执行动作，已执行动作记录事实并按可行补救处理，不假装撤回能撤销已发生。

**必须扣住**：R03进度、R06程序、R18权限、R19持久性、R13恢复、R23结果证据。不能让模型提供自己的可信回执；重放事件账不重新执行外部工具。

**例子/反例**：授权发送一次文档，网络超时但远端已收到。查询渠道ID后确认，不重发；渠道不能查且无幂等能力则保留unknown，不保证自动重试既不丢也不重复。

**写入归属与状态**：ActionLedger拥有行动意图和过程；可信adapter拥有attempt/receipt，模型无权写success回执。业务状态proposed/authorized/attempted/unknown/confirmed/failed/cancelled，另存delivery与verification；confirmed必须说明确认的是请求接收、工具完成还是业务效果。

**实现细节**：幂等键绑定operation+target+intent_revision，改变收件人或文件版本即是新意图，不能复用旧成功回执。外部不支持幂等且超时结果未知时，自动化停止在“待查”，不能以无限重试实现虚假的必达。取消分request_cancelled与effect_reversed；副作用已发生只可另建补救动作。R07/R08可读结果及反馈，不从“authorized”推断对方已经得到照顾。

## R14.02 位置、所有权与现状映射

规范数据族：`actions_receipts`。R03–R12对应十类typed store；其余是来源/运行/派生服务，不能再算额外心理记忆。

动作请求hash锁定目标与版本；同键异意图冲突。回执幂等；跨DB/外部无全局原子，须pending attempt和对账。

当前可核候选为0.32.0-candidate及其局部源码，不等于D现场已具备该接口。内核既有memories(kind)+versions继续保留，目标分型表由显式迁移产生；本模块不能绕规范API直接改别类记录。详见DATA_STORES.md的表归属。

## R14.03 输入契约

具体操作意图/目标/文件版本、可信授权、适用程序、已存在action及执行器回执。

调用外层必有schema_version、request_id、可信principal/scope、operation、deadline/cancel；写入带expected_revision和支持幂等的operation_key。读取带filter/snapshot/cursor，不能将模型提供的actor/scope直接当认证。类型表中可空项显式null，未执行检查不得以空数组冒“确认没有”。

## R14.04 输出、回执与错误契约

行动决策、attempt/receipt与核验结果；供工作/承诺反馈使用。

统一返回{request_id,operation_id,module,disposition,object_refs,base_revision,committed_revision,coverage,gaps,receipt_ref,evidence_level}。对象引用含kind/id/revision，来源引用含source_id/source_revision/hash/range。纯读committed_revision=null；候选disposition=proposed，不能返回committed冒正式状态。

错误至少区分INVALID_ARGUMENT、FORBIDDEN/NOT_FOUND_OR_HIDDEN、CONFLICT、SOURCE_UNAVAILABLE、TIMEOUT、RESOURCE_EXHAUSTED、UNVERIFIED_BINDING、INTERNAL；有提交路径还要commit_outcome=not_committed/committed/unknown。未知结果先按原键查回执。

## R14.05 数据字段、状态与索引

| 字段组 | 类型 | 约束与语义 |
|---|---|---|
| action_id/intent_revision | ID/int | 一次明确意图 |
| operation/target/effect | object | 收件人/资源/副作用具体化 |
| authorization_ref/policy_revision | object | 当前有效授权，非关系推导 |
| idempotency_key/request_digest | string/hash | 同操作目标与意图版本绑定 |
| attempts/external_id | array/nullable ID | 可信执行尝试和远端可查询标识 |
| receipts | array | issuer、可核数据、时间、层级 |
| business_state | enum | proposed/authorized/attempted/unknown/confirmed/failed/cancelled |
| delivery/verification | object | 送达独立；verification=success/failure/unknown |

公共对象字段：id、kind、schema_version、scope、created_at、created_by、revision、status、record_digest；每项来源或实际宿主创建依据另存。组字段细分时必须列schema，不用不同拼法兼容猜测。

proposed→核授权→authorized→attempted→confirmed/failed/unknown；取消记录发生时点。核验可以核出了失败，不等于已成功。

最低索引：scope+kind+有效状态+业务主键；来源反向依赖(source_id,source_revision)；对象版本(id,revision)。本模块特定检索维度由第11节给出。索引只定位，当前有效性仍核规范记录，不以索引命中当接受事实。

## R14.06 自动触发与完整处理顺序

1. 解析具体操作目标、意图版本和预期副作用。
2. 查当前授权与撤回，R06核程序前提；unknown权限不执行。
3. 先持久化即将尝试，再由可信执行器调用。
4. 结果以实际回执/查询入账，超时保unknown并查远端。
5. 确认结果层级：请求接收/工具完成/业务效果，送达另记。
6. 回流R03承诺/任务和R11经验，情绪/关系只据实际反馈修订。

宿主触发后逐阶段记started/succeeded/failed/skipped/unverified；不需要运行的步骤可skipped，但不能将缺必需依赖也算正常跳过。只读规划不改原始事件，模型调用不在数据库长锁内。

## R14.07 关键算法、决策与禁止捷径

外部支持幂等则同键受控重试；不支持且结果未知时不能保证既不丢也不重复，停在待查。取消请求不等于已发生副作用逆转；补救是新action。模型不得签发自己的trusted receipt。

每次推导均把直接观察、他人转述、候选解释、规范记录、外部结果分开。source_ref能定位仅证明原文存在；如涉及开放语义，必须由相应支持验证和反例测试决定是否可用，不能单靠hash/正则。算法参数只影响工程取舍，不授身份、权限或关系事实。

## R14.08 幂等、修订、并发与提交

动作请求hash锁定目标与版本；同键异意图冲突。回执幂等；跨DB/外部无全局原子，须pending attempt和对账。

操作重试与新业务事件分开；相同操作键异实质请求必须冲突。读取允许新快照结果变化，不能为了固定输出使用已撤回缓存。规范状态修改用expected_revision；跨库步骤分别留回执与reconciliation_required，不以一库commit冒全局事务。D依赖实际输出的SelfState/八域仍须强run/attempt/scope绑定，不让本模块日志替代。

## R14.09 更正、失效、删除与反向依赖

凡`actions_receipts`中有源派生物，登记source_root、source_revision、processor_version及依赖关系；纠正到来时先invalid_for_use/争议，后重建，不继续拿旧结论无提示作答。删除先由R18tombstone阻可用性，再清正文/索引/缓存/Wiki/备份策略；不能仅删引文保留相同推断。

无人物/心理职责的运行对象只记录必要状态，不因本模块失败写用户生气或D疏远。已发生事件和已表达的当时状态不被后来解释覆写；隐私擦除走专用治理路径。

## R14.10 模块扣接与交接责任

| 方向 | 对接对象 | 必须交接的内容 |
|---|---|---|
| 输入 | R03 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R06 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R12 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R18 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R19 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R21 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输出 | R03 | ActionLedger结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R04 | ActionLedger结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R08 | ActionLedger结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R11 | ActionLedger结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R13 | ActionLedger结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R23 | ActionLedger结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |

交接由HostAdapter/Coordinator调用，不让两个模块彼此递归无限互调。每个edge均记录当前事件/源版本、调用目的、预算、取消与真实回执；完整schema和时序见LINKAGE.md。接收失败保待处理/限制，不能发送空结果伪装成功。

## R14.11 如何存、如何召回、如何区分其他记忆

当前任务/承诺查询相关真实结果；历史动作可读不自动重新执行。

受权路线只查询声明的kind及其规范业务表；不能把情绪解释当语义事实、反思当亲历、工具尝试当结果。共享来源可同时支持多个kind，但每条命题有独立语义和审核状态；同源同命题折叠，不合并同源不同要求。必要后续沿依赖图取回，超过budget标partial。

## R14.12 注入的进入、最短表示与退出

当前问进度时区分已准备、已尝试、未知、已送达及业务验收；不注入全部运行日志。

当材料进入R22候选，每条必须能说明当前anchor、need_reason、新增信息和support_verdict。已在真实messages充分表达则不重注；换窗缺了则可重供。话题切换、完成、失效、撤回或无本轮用途就退出动态块，规范记忆保留。zero injection不关闭宿主最低检查，故障也不能伪装none_needed。

## R14.13 后台、恢复、超时与取消

本模块相关后台作业以scope+源版本+operation+schema/processor版本幂等，经R17持久队列领取。对于纯读路径，只保存必要阅读/覆盖进度，不声称有待提交事实。恢复时读最新删除、授权、规范状态及actions_receipts版本，再决定重算/继续/放弃。

失约worker写回须被fencing拒绝；模型调用超时发取消，底层不能证实停止就记cancel_unconfirmed，迟到结果不能自动commit。外部动作的unknown由R14先对账。未部署后台或钩子则标missing，不能称离线持续执行。

## R14.14 资源、隐私与降级规则

与R24共享每run/job预算，不为R14另开无界模型循环。前台最低检查、输入入账、必要纠正/边界和输出预留优先；可选语义、图展开、后台整理可暂停。所有查询与补读都有limit/deadline/stop_reason；候选上限不是注入配额。

故障使用第4节错误和coverage，普通交流尽量继续，依赖缺失的动作限制。密钥/原始私聊不进普通日志；被拒scope不出现在公开解释中。资源阈值不是情绪好感阈值，未实测目标机器不报固定延迟/容量保证。

## R14.15 贯通例子与反例

发文件超时，远端实际已收：按external_id查询确认，不因本地超时再发一遍。

验证时把该场景与原事件、已有记录、真实请求或结果链同时保存：输入→ActionLedger→下游回执。仅看到本模块返回JSON不证明生成模型采用，也不证明真实动作完成。正确处理应保留未知、合法来源和以后修订入口；能说出漂亮话不替代字段/版本/来源正确。

## R14.16 36项模块与协议验收需求目录（非执行fixture）

| ID | 准备/触发 | 必须结果；不满足即失败 | 当前状态 |
|---|---|---|---|
| R14-T01 | 在隔离fixture中构造：模型自述成功不当回执 | 模型自述成功不当回执 | not_run |
| R14-T02 | 在隔离fixture中构造：工具返回0但目标未达不冒业务成功 | 工具返回0但目标未达不冒业务成功 | not_run |
| R14-T03 | 在隔离fixture中构造：超时保unknown并先查询 | 超时保unknown并先查询 | not_run |
| R14-T04 | 在隔离fixture中构造：同键改变收件人/文件版本冲突 | 同键改变收件人/文件版本冲突 | not_run |
| R14-T05 | 在隔离fixture中构造：无授权不执行外发 | 无授权不执行外发 | not_run |
| R14-T06 | 在隔离fixture中构造：撤回可阻止尚未发生动作 | 撤回可阻止尚未发生动作 | not_run |
| R14-T07 | 在隔离fixture中构造：已发生动作取消不伪称撤销效果 | 已发生动作取消不伪称撤销效果 | not_run |
| R14-T08 | 在隔离fixture中构造：真实送达与本地正文保存分开 | 真实送达与本地正文保存分开 | not_run |
| R14-T09 | 在隔离fixture中构造：重启不重新发未知消息 | 重启不重新发未知消息 | not_run |
| R14-T10 | 在隔离fixture中构造：verified可核出failure | verified可核出failure | not_run |
| R14-T11 | 在隔离fixture中构造：程序过期时不盲执行 | 程序过期时不盲执行 | not_run |
| R14-T12 | 在隔离fixture中构造：内部事件回放不触发外部副作用 | 内部事件回放不触发外部副作用 | not_run |
| R14-T13 | 另建scope-B对象并以scope-A主体访问 | 拒绝相应资料/写入，公开响应不含B存在性；当前合法对象不变 | not_run |
| R14-T14 | 从本模块字段表逐组移除必需输入 | INVALID_ARGUMENT及字段路径；不得补造主体、项目或事实 | not_run |
| R14-T15 | 使用未支持schema/profile及实质未知字段 | 拒绝或显式unsupported；不静默删字段骗校验 | not_run |
| R14-T16 | 同源版本/操作键提交两遍 | 按本节幂等规则处理，副作用/独立证据不重复；纯读可以重查并保快照差别 | not_run |
| R14-T17 | 两调用携同expected_revision更新同对象 | 持久写至多一方按原前态成功，另一方冲突/受控重读；纯读不得写事实 | not_run |
| R14-T18 | 准备后提交/供给前对来源加tombstone | 相关派生停用或拒提交，旧缓存不复活；无来源型运行记录核相应取消/策略 | not_run |
| R14-T19 | 阶段处理中提交相关来源新版本 | 旧版本不能覆盖最新纠正；重算/partial/失效原因可查 | not_run |
| R14-T20 | 将一个必须依赖返回unavailable | 保具体缺口；不把失败当正常空结果或全部完成 | not_run |
| R14-T21 | 在本模块关键算法/调用处返回错误 | 错误回传，阶段failed/unknown；没有可用结论就不伪报成功 | not_run |
| R14-T22 | 故意令本模块外部阶段超过deadline | 取消按能力记录，迟到结果不绕版本与取消检查；真实停止未知照实 | not_run |
| R14-T23 | 准备完成后、提交/供给前取消run或job | 未发生副作用不再执行；已发生事实不抹除，结果另记 | not_run |
| R14-T24 | 租约失效后旧worker尝试写回 | 有持久写的路径由fencing/CAS拒绝；只读路径不借续读取得写权 | not_run |
| R14-T25 | 对持久写路径在关联对象写入间注入异常 | 本库事务全有或全无；跨库显示中间态并可对账；只读不虚称事务验收 | not_run |
| R14-T26 | 在commit后/返回前断开响应 | 按原键查询回执，不盲新建意图；只读重试不得假定语料未变化 | not_run |
| R14-T27 | 相关outbox成功处理但ACK丢失再投递 | 按源/处理器版本幂等，不产生第二次认知强化或外部动作 | not_run |
| R14-T28 | 规范对象已修订而索引未追平 | 报告水位并查规范store或partial；不能将旧命中当最新事实 | not_run |
| R14-T29 | 样本含emoji、不是/仅在/可能等限定 | 源范围和原意保留；截断不得变反义；非文本对象用其真实坐标 | not_run |
| R14-T30 | 加入同名不同ID与未定指代候选 | 保持候选/unknown，不自动合并；无人物职责模块不自创人物推断 | not_run |
| R14-T31 | 旧/新有效期及接收顺序不一致 | 按真实时间/版本契约处理；无法比较时不擅选最后接收值 | not_run |
| R14-T32 | 同材料被旧插件与当前出口同时提出 | 只有R22可最终装配，去本宿主拥有旧块而保用户/系统/工具结构 | not_run |
| R14-T33 | 提供本地保存/尝试但无业务或送达回执 | 不得升级成已理解/已完成/已送达；按该模块实际成果层级标注 | not_run |
| R14-T34 | 恢复相同逻辑初态重跑，同配置与fixture hash | 可复现本模块约定结果；时间/随机ID差异不混成语义提升 | not_run |
| R14-T35 | 输入含私密正文/凭据状外部内容 | 普通日志与索引/投影不泄漏禁止范围；审计仅留必要ID和固定原因 | not_run |
| R14-T36 | 只有文档、模拟对象或模型自评时要求标通过 | 保design/static/synthetic/real_host分轴；缺真实证据标not_run/unknown | not_run |

T01–T12是该模块专属语义/业务场景；T13–T36是必须绑定本模块实际写读路径执行的协议/故障场景，不能空跑通用脚本就全标通过。先从字段表构造合法基准fixture，再只改变本例条件；对不适用的写路径要给可审证据说明与对应只读判据，不能把未测记成pass。

## R14.17 交付证据、通过门槛与未完成项

交付ActionLedger实现/schema迁移、输入输出fixture、合法及反例来源、实际存储与调用回执、真实入口覆盖、查询及注入观察、失败恢复报告。证据等级design/static/synthetic_process/real_host/storage_fault/production分开。

模块通过至少需要专属场景和适用协议场景的实际证据；整套通过还需LINKAGE.md跨模块链。当前文档生成/类型DDL检查不算本模块36例已跑。已有候选仅作为迁移基础，现场未知和未实现开放语义仍未验。

## R14.18 实现次序、兼容策略与设计自审

先固定本模块字段/状态/真源→实现受权最小路径与回执→跑专属正反例→接入上游/下游→做恢复/删除/冲突→在真实隔离宿主检查请求或结果。本模块不得以优化名义删除保留矩阵中已有功能，不改C032严格profile顶层来绕验证。

本次设计检查关注：当前任务/承诺查询相关真实结果；历史动作可读不自动重新执行。 当前问进度时区分已准备、已尝试、未知、已送达及业务验收；不注入全部运行日志。 对所有结果都分别标明对象、版本、来源、局限和验证等级；不以同一success覆盖入账、理解、注入、生成、送达与执行。生产边界不变，不随文档生成而开通部署。



---

# R15　分库混合检索与联想：详细设计与验收规格

版本：everlight/6-design；模块契约：r15/1；日期：2026-11-08。本文为设计，全部功能验收初始not_run。最终裁决以FINAL_DECISIONS.md和MODULE_DECISIONS.md为准。与contracts/共同生效，不是已安装服务。

## R15.01 定义、边界与可证伪成功标准

逐路Hits、语义候选与必要补读/纠正后续计划、Coverage；不是直接答案。

唯一业务责任服务是`RecallCoordinator`。输入必须满足第3节，输出必须满足第4节及GLOBAL_PROTOCOL。成功必须可从实际记录/回执读回，而不是模型自称完成。

原有具体机制及边界（保留并由本版细化）：

**原理与基础**：多个路线互补，自动性靠宿主，正确性靠人物/时间/来源及评测。候选有FTS/ngram、可选向量及有限关系路线，默认无embedding、开放语义质量未知。

**数据与输入输出**：输入CueSet、可信scope、时间约束、预算、焦点；各路返回candidate_id、rank、raw_score、source/版本、对象/时间和Coverage。输出融合候选和待补读计划，不直接等于可回答结论。

**步骤**：①按ACL先过滤，无法安全下推的过滤受限扩召并标partial；②词法、可选语义、实体别名、关系/时间、情绪线索、工作承诺、程序经验分路查询；③可用RRF：sum(w/(k+rank))，参数配置并评测，不能直接相加不同分制；④按事件ID+版本去重但保留所有来源；⑤对象/时间冲突分组；⑥交R16补读；⑦不足时追加查询，直到无新证据或预算停止。

**必须扣住**：R02局部线索、R03/R13焦点、R04–R08/R11/R12资料、R18范围、R10覆盖、R16阅读、R22预算。检索分只为排序，不作为“喜欢谁更多”的分数。

**例子/反例**：“那个紫色的方案”可结合当前项目找到文档；两项目同色不混，权限不够的候选不能进入模型上下文。只有词法成功不能报“全部路线已查完”。

**写入归属与状态**：RecallCoordinator只协调只读路线，索引结果不是事实真源。每路状态available/partial/stale/unavailable/disabled/denied单列；disabled表示未配置，不伪报故障，也不算检索成功。向量服务可选，启动无embedding时要在能力清单明示。

**实现细节**：先做人物、项目、时效和权限约束，再用词法/语义互补排序；RRF只融合可比较的排名，缺席路线不凭空给rank。去重键是来源ID+revision+范围重叠，不能只按文本相似删除不同人的来源。为最新更正、反证和事件后续留候选槽位；若旧片段命中高，自动查其followup和supersedes链。图展开属于此模块的受限来源导航，不回流R02做多跳指代。

## R15.02 位置、所有权与现状映射

规范数据族：`recall_runs`。R03–R12对应十类typed store；其余是来源/运行/派生服务，不能再算额外心理记忆。

只读快照和watermark绑定；检索缓存包含scope/policy/delete/kind/filter/index_revision。新查询结果不回写事实。

当前可核候选为0.32.0-candidate及其局部源码，不等于D现场已具备该接口。内核既有memories(kind)+versions继续保留，目标分型表由显式迁移产生；本模块不能绕规范API直接改别类记录。详见DATA_STORES.md的表归属。

## R15.03 输入契约

可信scope、当前问题/焦点、允许kind与时间约束、相关人/任务、总预算和能力清单。

调用外层必有schema_version、request_id、可信principal/scope、operation、deadline/cancel；写入带expected_revision和支持幂等的operation_key。读取带filter/snapshot/cursor，不能将模型提供的actor/scope直接当认证。类型表中可空项显式null，未执行检查不得以空数组冒“确认没有”。

## R15.04 输出、回执与错误契约

逐路Hits、语义候选与必要补读/纠正后续计划、Coverage；不是直接答案。

统一返回{request_id,operation_id,module,disposition,object_refs,base_revision,committed_revision,coverage,gaps,receipt_ref,evidence_level}。对象引用含kind/id/revision，来源引用含source_id/source_revision/hash/range。纯读committed_revision=null；候选disposition=proposed，不能返回committed冒正式状态。

错误至少区分INVALID_ARGUMENT、FORBIDDEN/NOT_FOUND_OR_HIDDEN、CONFLICT、SOURCE_UNAVAILABLE、TIMEOUT、RESOURCE_EXHAUSTED、UNVERIFIED_BINDING、INTERNAL；有提交路径还要commit_outcome=not_committed/committed/unknown。未知结果先按原键查回执。

## R15.05 数据字段、状态与索引

| 字段组 | 类型 | 约束与语义 |
|---|---|---|
| query_id/plan_revision | ID/int | 当前查询及版本 |
| query_text/current_anchor | string/object | 问题原文与可信焦点分开 |
| kind_routes | array | 十类命名路线；source与运行账另路 |
| filters/time_constraints | object | 人物/项目/时期/审核状态 |
| route_hits | array | id/kind/revision/rank/raw_score/source_refs |
| fusion/rerank | object | 排序版本、参数及解释等级 |
| coverage/watermarks | object | 每路线状态/截断/陈旧 |
| gap_plans/stop_reason | array/string | 补读需要与终止理由 |

公共对象字段：id、kind、schema_version、scope、created_at、created_by、revision、status、record_digest；每项来源或实际宿主创建依据另存。组字段细分时必须列schema，不用不同拼法兼容猜测。

planned→各route执行→fused→read_pending→sufficient/partial/no_result/failed；no_result不代表事情没发生。

最低索引：scope+kind+有效状态+业务主键；来源反向依赖(source_id,source_revision)；对象版本(id,revision)。本模块特定检索维度由第11节给出。索引只定位，当前有效性仍核规范记录，不以索引命中当接受事实。

## R15.06 自动触发与完整处理顺序

1. 认证并从当前问题/可信焦点建RoutePlan，R02只供局部标记。
2. 先划分必要kind：工作查任务/方法/结果，社交查人物/经历/相关关切；无关库不自动扩查。
3. 范围/删除/版本/权限预过滤，执行词法、可选向量、实体时态、结构化路线。
4. 逐路排名融合，RRF初值k=60/权重1仅为可调实验；不相加异分制raw_score。
5. 人物/时间/命题冲突分组，命中旧经历自动追纠正/后续；同根同命题去重保来源集合。
6. R16读必要范围；新的Gap在共享轮数/节点/查询预算内补查；无新供给来源就停。

宿主触发后逐阶段记started/succeeded/failed/skipped/unverified；不需要运行的步骤可skipped，但不能将缺必需依赖也算正常跳过。只读规划不改原始事件，模型调用不在数据库长锁内。

## R15.07 关键算法、决策与禁止捷径

kind不是检索后随便加的标签：每个typed store有专属query adapter；只读多路聚合。语义分、情绪强度、亲密度都不能授真值或注入资格。图导航可多跳但有visited/hops/nodes限制，不推出新社会关系或ACL。

每次推导均把直接观察、他人转述、候选解释、规范记录、外部结果分开。source_ref能定位仅证明原文存在；如涉及开放语义，必须由相应支持验证和反例测试决定是否可用，不能单靠hash/正则。算法参数只影响工程取舍，不授身份、权限或关系事实。

## R15.08 幂等、修订、并发与提交

只读快照和watermark绑定；检索缓存包含scope/policy/delete/kind/filter/index_revision。新查询结果不回写事实。

操作重试与新业务事件分开；相同操作键异实质请求必须冲突。读取允许新快照结果变化，不能为了固定输出使用已撤回缓存。规范状态修改用expected_revision；跨库步骤分别留回执与reconciliation_required，不以一库commit冒全局事务。D依赖实际输出的SelfState/八域仍须强run/attempt/scope绑定，不让本模块日志替代。

## R15.09 更正、失效、删除与反向依赖

凡`recall_runs`中有源派生物，登记source_root、source_revision、processor_version及依赖关系；纠正到来时先invalid_for_use/争议，后重建，不继续拿旧结论无提示作答。删除先由R18tombstone阻可用性，再清正文/索引/缓存/Wiki/备份策略；不能仅删引文保留相同推断。

无人物/心理职责的运行对象只记录必要状态，不因本模块失败写用户生气或D疏远。已发生事件和已表达的当时状态不被后来解释覆写；隐私擦除走专用治理路径。

## R15.10 模块扣接与交接责任

| 方向 | 对接对象 | 必须交接的内容 |
|---|---|---|
| 输入 | R02 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R03 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R04 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R05 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R06 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R07 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R08 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R09 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R10 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R11 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R12 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R13 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R18 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R19 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R24 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输出 | R10 | RecallCoordinator结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R11 | RecallCoordinator结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R16 | RecallCoordinator结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R21 | RecallCoordinator结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R22 | RecallCoordinator结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R23 | RecallCoordinator结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |

交接由HostAdapter/Coordinator调用，不让两个模块彼此递归无限互调。每个edge均记录当前事件/源版本、调用目的、预算、取消与真实回执；完整schema和时序见LINKAGE.md。接收失败保待处理/限制，不能发送空结果伪装成功。

## R15.11 如何存、如何召回、如何区分其他记忆

自身是L4：先候选、后原文、再当前需要性/支持验证。缺向量时标disabled或unavailable，保结构化/词法与局限。

受权路线只查询声明的kind及其规范业务表；不能把情绪解释当语义事实、反思当亲历、工具尝试当结果。共享来源可同时支持多个kind，但每条命题有独立语义和审核状态；同源同命题折叠，不合并同源不同要求。必要后续沿依赖图取回，超过budget标partial。

## R15.12 注入的进入、最短表示与退出

R15不得直接追加prompt；只交候选给R22。允许查很多选零条；明确历史问题不得因低相似度就认无需求。

当材料进入R22候选，每条必须能说明当前anchor、need_reason、新增信息和support_verdict。已在真实messages充分表达则不重注；换窗缺了则可重供。话题切换、完成、失效、撤回或无本轮用途就退出动态块，规范记忆保留。zero injection不关闭宿主最低检查，故障也不能伪装none_needed。

## R15.13 后台、恢复、超时与取消

本模块相关后台作业以scope+源版本+operation+schema/processor版本幂等，经R17持久队列领取。对于纯读路径，只保存必要阅读/覆盖进度，不声称有待提交事实。恢复时读最新删除、授权、规范状态及recall_runs版本，再决定重算/继续/放弃。

失约worker写回须被fencing拒绝；模型调用超时发取消，底层不能证实停止就记cancel_unconfirmed，迟到结果不能自动commit。外部动作的unknown由R14先对账。未部署后台或钩子则标missing，不能称离线持续执行。

## R15.14 资源、隐私与降级规则

与R24共享每run/job预算，不为R15另开无界模型循环。前台最低检查、输入入账、必要纠正/边界和输出预留优先；可选语义、图展开、后台整理可暂停。所有查询与补读都有limit/deadline/stop_reason；候选上限不是注入配额。

故障使用第4节错误和coverage，普通交流尽量继续，依赖缺失的动作限制。密钥/原始私聊不进普通日志；被拒scope不出现在公开解释中。资源阈值不是情绪好感阈值，未实测目标机器不报固定延迟/容量保证。

## R15.15 贯通例子与反例

“那个紫色方案”结合当前项目找文件；两项目同色保歧义。问原因时补原文与后续而非只返回标签。

验证时把该场景与原事件、已有记录、真实请求或结果链同时保存：输入→RecallCoordinator→下游回执。仅看到本模块返回JSON不证明生成模型采用，也不证明真实动作完成。正确处理应保留未知、合法来源和以后修订入口；能说出漂亮话不替代字段/版本/来源正确。

## R15.16 36项模块与协议验收需求目录（非执行fixture）

| ID | 准备/触发 | 必须结果；不满足即失败 | 当前状态 |
|---|---|---|---|
| R15-T01 | 在隔离fixture中构造：工作查询不带无关情绪库 | 工作查询不带无关情绪库 | not_run |
| R15-T02 | 在隔离fixture中构造：情绪查询不把模型推测当用户事实 | 情绪查询不把模型推测当用户事实 | not_run |
| R15-T03 | 在隔离fixture中构造：同色跨项目不串 | 同色跨项目不串 | not_run |
| R15-T04 | 在隔离fixture中构造：同名跨人物分组 | 同名跨人物分组 | not_run |
| R15-T05 | 在隔离fixture中构造：旧争执命中同时查澄清 | 旧争执命中同时查澄清 | not_run |
| R15-T06 | 在隔离fixture中构造：最新更正不被高rank旧值挤掉 | 最新更正不被高rank旧值挤掉 | not_run |
| R15-T07 | 在隔离fixture中构造：ACL过滤不足可预算内续页且partial | ACL过滤不足可预算内续页且partial | not_run |
| R15-T08 | 在隔离fixture中构造：向量不可用不等全部无记忆 | 向量不可用不等全部无记忆 | not_run |
| R15-T09 | 在隔离fixture中构造：同源不同命题不误去重 | 同源不同命题不误去重 | not_run |
| R15-T10 | 在隔离fixture中构造：两跳图导航不能推权限 | 两跳图导航不能推权限 | not_run |
| R15-T11 | 在隔离fixture中构造：无新来源停止而非无限联想 | 无新来源停止而非无限联想 | not_run |
| R15-T12 | 在隔离fixture中构造：长上下文已含事实不要求重复注入 | 长上下文已含事实不要求重复注入 | not_run |
| R15-T13 | 另建scope-B对象并以scope-A主体访问 | 拒绝相应资料/写入，公开响应不含B存在性；当前合法对象不变 | not_run |
| R15-T14 | 从本模块字段表逐组移除必需输入 | INVALID_ARGUMENT及字段路径；不得补造主体、项目或事实 | not_run |
| R15-T15 | 使用未支持schema/profile及实质未知字段 | 拒绝或显式unsupported；不静默删字段骗校验 | not_run |
| R15-T16 | 同源版本/操作键提交两遍 | 按本节幂等规则处理，副作用/独立证据不重复；纯读可以重查并保快照差别 | not_run |
| R15-T17 | 两调用携同expected_revision更新同对象 | 持久写至多一方按原前态成功，另一方冲突/受控重读；纯读不得写事实 | not_run |
| R15-T18 | 准备后提交/供给前对来源加tombstone | 相关派生停用或拒提交，旧缓存不复活；无来源型运行记录核相应取消/策略 | not_run |
| R15-T19 | 阶段处理中提交相关来源新版本 | 旧版本不能覆盖最新纠正；重算/partial/失效原因可查 | not_run |
| R15-T20 | 将一个必须依赖返回unavailable | 保具体缺口；不把失败当正常空结果或全部完成 | not_run |
| R15-T21 | 在本模块关键算法/调用处返回错误 | 错误回传，阶段failed/unknown；没有可用结论就不伪报成功 | not_run |
| R15-T22 | 故意令本模块外部阶段超过deadline | 取消按能力记录，迟到结果不绕版本与取消检查；真实停止未知照实 | not_run |
| R15-T23 | 准备完成后、提交/供给前取消run或job | 未发生副作用不再执行；已发生事实不抹除，结果另记 | not_run |
| R15-T24 | 租约失效后旧worker尝试写回 | 有持久写的路径由fencing/CAS拒绝；只读路径不借续读取得写权 | not_run |
| R15-T25 | 对持久写路径在关联对象写入间注入异常 | 本库事务全有或全无；跨库显示中间态并可对账；只读不虚称事务验收 | not_run |
| R15-T26 | 在commit后/返回前断开响应 | 按原键查询回执，不盲新建意图；只读重试不得假定语料未变化 | not_run |
| R15-T27 | 相关outbox成功处理但ACK丢失再投递 | 按源/处理器版本幂等，不产生第二次认知强化或外部动作 | not_run |
| R15-T28 | 规范对象已修订而索引未追平 | 报告水位并查规范store或partial；不能将旧命中当最新事实 | not_run |
| R15-T29 | 样本含emoji、不是/仅在/可能等限定 | 源范围和原意保留；截断不得变反义；非文本对象用其真实坐标 | not_run |
| R15-T30 | 加入同名不同ID与未定指代候选 | 保持候选/unknown，不自动合并；无人物职责模块不自创人物推断 | not_run |
| R15-T31 | 旧/新有效期及接收顺序不一致 | 按真实时间/版本契约处理；无法比较时不擅选最后接收值 | not_run |
| R15-T32 | 同材料被旧插件与当前出口同时提出 | 只有R22可最终装配，去本宿主拥有旧块而保用户/系统/工具结构 | not_run |
| R15-T33 | 提供本地保存/尝试但无业务或送达回执 | 不得升级成已理解/已完成/已送达；按该模块实际成果层级标注 | not_run |
| R15-T34 | 恢复相同逻辑初态重跑，同配置与fixture hash | 可复现本模块约定结果；时间/随机ID差异不混成语义提升 | not_run |
| R15-T35 | 输入含私密正文/凭据状外部内容 | 普通日志与索引/投影不泄漏禁止范围；审计仅留必要ID和固定原因 | not_run |
| R15-T36 | 只有文档、模拟对象或模型自评时要求标通过 | 保design/static/synthetic/real_host分轴；缺真实证据标not_run/unknown | not_run |

T01–T12是该模块专属语义/业务场景；T13–T36是必须绑定本模块实际写读路径执行的协议/故障场景，不能空跑通用脚本就全标通过。先从字段表构造合法基准fixture，再只改变本例条件；对不适用的写路径要给可审证据说明与对应只读判据，不能把未测记成pass。

## R15.17 交付证据、通过门槛与未完成项

交付RecallCoordinator实现/schema迁移、输入输出fixture、合法及反例来源、实际存储与调用回执、真实入口覆盖、查询及注入观察、失败恢复报告。证据等级design/static/synthetic_process/real_host/storage_fault/production分开。

模块通过至少需要专属场景和适用协议场景的实际证据；整套通过还需LINKAGE.md跨模块链。当前文档生成/类型DDL检查不算本模块36例已跑。已有候选仅作为迁移基础，现场未知和未实现开放语义仍未验。

## R15.18 实现次序、兼容策略与设计自审

先固定本模块字段/状态/真源→实现受权最小路径与回执→跑专属正反例→接入上游/下游→做恢复/删除/冲突→在真实隔离宿主检查请求或结果。本模块不得以优化名义删除保留矩阵中已有功能，不改C032严格profile顶层来绕验证。

本次设计检查关注：自身是L4：先候选、后原文、再当前需要性/支持验证。缺向量时标disabled或unavailable，保结构化/词法与局限。 R15不得直接追加prompt；只交候选给R22。允许查很多选零条；明确历史问题不得因低相似度就认无需求。 对所有结果都分别标明对象、版本、来源、局限和验证等级；不以同一success覆盖入账、理解、注入、生成、送达与执行。生产边界不变，不随文档生成而开通部署。



---

# R16　原文阅读与证据供给：详细设计与验收规格

版本：everlight/6-design；模块契约：r16/1；日期：2026-11-08。本文为设计，全部功能验收初始not_run。最终裁决以FINAL_DECISIONS.md和MODULE_DECISIONS.md为准。与contracts/共同生效，不是已安装服务。

## R16.01 定义、边界与可证伪成功标准

真实片段、完整度、已读与实际供给范围、续读游标及引用校验。

唯一业务责任服务是`SourceReader`。输入必须满足第3节，输出必须满足第4节及GLOBAL_PROTOCOL。成功必须可从实际记录/回执读回，而不是模型自称完成。

原有具体机制及边界（保留并由本版细化）：

**原理与基础**：命中摘要只是入口。候选readProgress有游标/hash，完整历史及邻接扩展待验；大文件分片段不等于全文已读。

**数据**：source_id、source_revision/hash、总长度、实际已读字节区间、未读区间、cursor、complete、reason。已读内容还要标是否实际送入本轮模型；磁盘读到但未供给不能作本轮新引文。

**步骤**：①R15命中摘要/歧义/冲突或后续不明；②规划必要原事件及邻接范围；③按版本读取并核hash；④UTF-8边界安全拼接与区间合并；⑤不足保存游标且不让“空块”吞失败；⑥已供给范围可被引用，不可越出范围；⑦版本变化重新计划，不能拼接两个版本。

**必须扣住**：R01/R12来源、R15计划、R10覆盖、R22供给记录、R13游标、R18权限。候选C032部分机制只接纳完整来源，片段支持应走明确适配，不能直接放松引用验证。

**例子/反例**：摘要说“决定重做”，用户问原因，应读前后原话；只读到后半段就标partial，不能宣称全文无其他理由。无权限不能通过邻接阅读扩大范围。

**写入归属与状态**：SourceReader记录已读范围，ProjectionBuilder记录哪些范围实际供给模型。read_complete、supplied_complete、cited_valid是三项，不相互替代。source_revision变化使旧cursor失效，返回冲突而非继续拼接。

**实现细节**：读游标封装source_id、revision/hash、next_offset、scope_digest和过期策略，服务端校验不可由模型任填偏移逃范围。邻接补读先查是否同来源同授权域，不跨到私聊。对需要完整来源的C032接口，读到片段先留pending而非伪装完整；新片段适配协议另声明可引用区间。长文按区间并集记进度，重叠块不重复计覆盖和费用；空结果需区分EOF、抽取失败、超时与被撤回。

## R16.02 位置、所有权与现状映射

规范数据族：`source_ranges`。R03–R12对应十类typed store；其余是来源/运行/派生服务，不能再算额外心理记忆。

读取无事实修改；read_progress按range并集幂等，supplied记录绑定实际attempt/请求而非日志自报。

当前可核候选为0.32.0-candidate及其局部源码，不等于D现场已具备该接口。内核既有memories(kind)+versions继续保留，目标分型表由显式迁移产生；本模块不能绕规范API直接改别类记录。详见DATA_STORES.md的表归属。

## R16.03 输入契约

受权来源ID/版本/hash、范围/游标、需要读的具体问题、可用字节与deadline。

调用外层必有schema_version、request_id、可信principal/scope、operation、deadline/cancel；写入带expected_revision和支持幂等的operation_key。读取带filter/snapshot/cursor，不能将模型提供的actor/scope直接当认证。类型表中可空项显式null，未执行检查不得以空数组冒“确认没有”。

## R16.04 输出、回执与错误契约

真实片段、完整度、已读与实际供给范围、续读游标及引用校验。

统一返回{request_id,operation_id,module,disposition,object_refs,base_revision,committed_revision,coverage,gaps,receipt_ref,evidence_level}。对象引用含kind/id/revision，来源引用含source_id/source_revision/hash/range。纯读committed_revision=null；候选disposition=proposed，不能返回committed冒正式状态。

错误至少区分INVALID_ARGUMENT、FORBIDDEN/NOT_FOUND_OR_HIDDEN、CONFLICT、SOURCE_UNAVAILABLE、TIMEOUT、RESOURCE_EXHAUSTED、UNVERIFIED_BINDING、INTERNAL；有提交路径还要commit_outcome=not_committed/committed/unknown。未知结果先按原键查回执。

## R16.05 数据字段、状态与索引

| 字段组 | 类型 | 约束与语义 |
|---|---|---|
| source_id/source_revision/hash | ID/string/hash | 确切原件与版本 |
| start_byte/end_byte | int | UTF-8半开边界；文件页/音视频坐标另列 |
| length_bytes | nullable int | 未知总长需reason |
| read_ranges/unread_ranges | array | 并集进度，不重复累计 |
| supplied_ranges/run_id | array/ID | 实际进入本轮模型的范围 |
| cursor | nullable token | 绑定scope/filter/source版本/下个offset |
| state/reason | enum/string | complete/partial/EOF/failed/denied/stale |
| citation_validation | object | 范围/hash合法与语义支持另检 |

公共对象字段：id、kind、schema_version、scope、created_at、created_by、revision、status、record_digest；每项来源或实际宿主创建依据另存。组字段细分时必须列schema，不用不同拼法兼容猜测。

planned→read→range_verified→supplied或withheld；源变化stale，游标作废；EOF与失败分别记。

最低索引：scope+kind+有效状态+业务主键；来源反向依赖(source_id,source_revision)；对象版本(id,revision)。本模块特定检索维度由第11节给出。索引只定位，当前有效性仍核规范记录，不以索引命中当接受事实。

## R16.06 自动触发与完整处理顺序

1. 核实时ACL/tombstone/版本与读取预算。
2. 优先读回答问题及必要前后文，非默认全文。
3. 安全切UTF-8及结构块边界，读取前后核源一致。
4. 更新区间并集，缺段留cursor，不用空块吞失败。
5. R22选中并确实送入实际请求后才标supplied。
6. 引用验证不得超实际供给范围；语义结论是否支持交SupportVerifier。

宿主触发后逐阶段记started/succeeded/failed/skipped/unverified；不需要运行的步骤可skipped，但不能将缺必需依赖也算正常跳过。只读规划不改原始事件，模型调用不在数据库长锁内。

## R16.07 关键算法、决策与禁止捷径

摘要命中只是读入口；定位指针不算模型读过原文。C032当前完整来源引用接口不接受的片段，必须明确适配，不能放松校验来冒充兼容。文档多页、JSON/代码块要保足够上下文及限定，不裁否定。

每次推导均把直接观察、他人转述、候选解释、规范记录、外部结果分开。source_ref能定位仅证明原文存在；如涉及开放语义，必须由相应支持验证和反例测试决定是否可用，不能单靠hash/正则。算法参数只影响工程取舍，不授身份、权限或关系事实。

## R16.08 幂等、修订、并发与提交

读取无事实修改；read_progress按range并集幂等，supplied记录绑定实际attempt/请求而非日志自报。

操作重试与新业务事件分开；相同操作键异实质请求必须冲突。读取允许新快照结果变化，不能为了固定输出使用已撤回缓存。规范状态修改用expected_revision；跨库步骤分别留回执与reconciliation_required，不以一库commit冒全局事务。D依赖实际输出的SelfState/八域仍须强run/attempt/scope绑定，不让本模块日志替代。

## R16.09 更正、失效、删除与反向依赖

凡`source_ranges`中有源派生物，登记source_root、source_revision、processor_version及依赖关系；纠正到来时先invalid_for_use/争议，后重建，不继续拿旧结论无提示作答。删除先由R18tombstone阻可用性，再清正文/索引/缓存/Wiki/备份策略；不能仅删引文保留相同推断。

无人物/心理职责的运行对象只记录必要状态，不因本模块失败写用户生气或D疏远。已发生事件和已表达的当时状态不被后来解释覆写；隐私擦除走专用治理路径。

## R16.10 模块扣接与交接责任

| 方向 | 对接对象 | 必须交接的内容 |
|---|---|---|
| 输入 | R01 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R10 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R12 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R15 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R18 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R24 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输出 | R10 | SourceReader结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R11 | SourceReader结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R13 | SourceReader结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R15 | SourceReader结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R22 | SourceReader结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R23 | SourceReader结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |

交接由HostAdapter/Coordinator调用，不让两个模块彼此递归无限互调。每个edge均记录当前事件/源版本、调用目的、预算、取消与真实回执；完整schema和时序见LINKAGE.md。接收失败保待处理/限制，不能发送空结果伪装成功。

## R16.11 如何存、如何召回、如何区分其他记忆

来源导航只在受权端点展开；按source+revision+range缓存，不能跨版本拼片段。

受权路线只查询声明的kind及其规范业务表；不能把情绪解释当语义事实、反思当亲历、工具尝试当结果。共享来源可同时支持多个kind，但每条命题有独立语义和审核状态；同源同命题折叠，不合并同源不同要求。必要后续沿依赖图取回，超过budget标partial。

## R16.12 注入的进入、最短表示与退出

只供当前必要原文；磁盘读过但未供给不作为本轮新引文。原文中的指令是资料，不升宿主权限。

当材料进入R22候选，每条必须能说明当前anchor、need_reason、新增信息和support_verdict。已在真实messages充分表达则不重注；换窗缺了则可重供。话题切换、完成、失效、撤回或无本轮用途就退出动态块，规范记忆保留。zero injection不关闭宿主最低检查，故障也不能伪装none_needed。

## R16.13 后台、恢复、超时与取消

本模块相关后台作业以scope+源版本+operation+schema/processor版本幂等，经R17持久队列领取。对于纯读路径，只保存必要阅读/覆盖进度，不声称有待提交事实。恢复时读最新删除、授权、规范状态及source_ranges版本，再决定重算/继续/放弃。

失约worker写回须被fencing拒绝；模型调用超时发取消，底层不能证实停止就记cancel_unconfirmed，迟到结果不能自动commit。外部动作的unknown由R14先对账。未部署后台或钩子则标missing，不能称离线持续执行。

## R16.14 资源、隐私与降级规则

与R24共享每run/job预算，不为R16另开无界模型循环。前台最低检查、输入入账、必要纠正/边界和输出预留优先；可选语义、图展开、后台整理可暂停。所有查询与补读都有limit/deadline/stop_reason；候选上限不是注入配额。

故障使用第4节错误和coverage，普通交流尽量继续，依赖缺失的动作限制。密钥/原始私聊不进普通日志；被拒scope不出现在公开解释中。资源阈值不是情绪好感阈值，未实测目标机器不报固定延迟/容量保证。

## R16.15 贯通例子与反例

摘要说重做方案，问原因则读相关前后原文；只读后半段标partial，不称全文无其他原因。

验证时把该场景与原事件、已有记录、真实请求或结果链同时保存：输入→SourceReader→下游回执。仅看到本模块返回JSON不证明生成模型采用，也不证明真实动作完成。正确处理应保留未知、合法来源和以后修订入口；能说出漂亮话不替代字段/版本/来源正确。

## R16.16 36项模块与协议验收需求目录（非执行fixture）

| ID | 准备/触发 | 必须结果；不满足即失败 | 当前状态 |
|---|---|---|---|
| R16-T01 | 在隔离fixture中构造：UTF8多字节边界可回读 | UTF8多字节边界可回读 | not_run |
| R16-T02 | 在隔离fixture中构造：同版本重叠块不重复计覆盖 | 同版本重叠块不重复计覆盖 | not_run |
| R16-T03 | 在隔离fixture中构造：源改版后cursor失效 | 源改版后cursor失效 | not_run |
| R16-T04 | 在隔离fixture中构造：完整read不等supplied | 完整read不等supplied | not_run |
| R16-T05 | 在隔离fixture中构造：只供摘要不能引未读原文 | 只供摘要不能引未读原文 | not_run |
| R16-T06 | 在隔离fixture中构造：EOF/超时/拒绝/抽取失败分开 | EOF/超时/拒绝/抽取失败分开 | not_run |
| R16-T07 | 在隔离fixture中构造：否定不被截成相反意思 | 否定不被截成相反意思 | not_run |
| R16-T08 | 在隔离fixture中构造：读中变化拒混版本 | 读中变化拒混版本 | not_run |
| R16-T09 | 在隔离fixture中构造：邻接不跨私聊权限 | 邻接不跨私聊权限 | not_run |
| R16-T10 | 在隔离fixture中构造：片段不伪装C032完整来源 | 片段不伪装C032完整来源 | not_run |
| R16-T11 | 在隔离fixture中构造：hash正确不证明语义支持 | hash正确不证明语义支持 | not_run |
| R16-T12 | 在隔离fixture中构造：删除撤回后旧缓存不可读 | 删除撤回后旧缓存不可读 | not_run |
| R16-T13 | 另建scope-B对象并以scope-A主体访问 | 拒绝相应资料/写入，公开响应不含B存在性；当前合法对象不变 | not_run |
| R16-T14 | 从本模块字段表逐组移除必需输入 | INVALID_ARGUMENT及字段路径；不得补造主体、项目或事实 | not_run |
| R16-T15 | 使用未支持schema/profile及实质未知字段 | 拒绝或显式unsupported；不静默删字段骗校验 | not_run |
| R16-T16 | 同源版本/操作键提交两遍 | 按本节幂等规则处理，副作用/独立证据不重复；纯读可以重查并保快照差别 | not_run |
| R16-T17 | 两调用携同expected_revision更新同对象 | 持久写至多一方按原前态成功，另一方冲突/受控重读；纯读不得写事实 | not_run |
| R16-T18 | 准备后提交/供给前对来源加tombstone | 相关派生停用或拒提交，旧缓存不复活；无来源型运行记录核相应取消/策略 | not_run |
| R16-T19 | 阶段处理中提交相关来源新版本 | 旧版本不能覆盖最新纠正；重算/partial/失效原因可查 | not_run |
| R16-T20 | 将一个必须依赖返回unavailable | 保具体缺口；不把失败当正常空结果或全部完成 | not_run |
| R16-T21 | 在本模块关键算法/调用处返回错误 | 错误回传，阶段failed/unknown；没有可用结论就不伪报成功 | not_run |
| R16-T22 | 故意令本模块外部阶段超过deadline | 取消按能力记录，迟到结果不绕版本与取消检查；真实停止未知照实 | not_run |
| R16-T23 | 准备完成后、提交/供给前取消run或job | 未发生副作用不再执行；已发生事实不抹除，结果另记 | not_run |
| R16-T24 | 租约失效后旧worker尝试写回 | 有持久写的路径由fencing/CAS拒绝；只读路径不借续读取得写权 | not_run |
| R16-T25 | 对持久写路径在关联对象写入间注入异常 | 本库事务全有或全无；跨库显示中间态并可对账；只读不虚称事务验收 | not_run |
| R16-T26 | 在commit后/返回前断开响应 | 按原键查询回执，不盲新建意图；只读重试不得假定语料未变化 | not_run |
| R16-T27 | 相关outbox成功处理但ACK丢失再投递 | 按源/处理器版本幂等，不产生第二次认知强化或外部动作 | not_run |
| R16-T28 | 规范对象已修订而索引未追平 | 报告水位并查规范store或partial；不能将旧命中当最新事实 | not_run |
| R16-T29 | 样本含emoji、不是/仅在/可能等限定 | 源范围和原意保留；截断不得变反义；非文本对象用其真实坐标 | not_run |
| R16-T30 | 加入同名不同ID与未定指代候选 | 保持候选/unknown，不自动合并；无人物职责模块不自创人物推断 | not_run |
| R16-T31 | 旧/新有效期及接收顺序不一致 | 按真实时间/版本契约处理；无法比较时不擅选最后接收值 | not_run |
| R16-T32 | 同材料被旧插件与当前出口同时提出 | 只有R22可最终装配，去本宿主拥有旧块而保用户/系统/工具结构 | not_run |
| R16-T33 | 提供本地保存/尝试但无业务或送达回执 | 不得升级成已理解/已完成/已送达；按该模块实际成果层级标注 | not_run |
| R16-T34 | 恢复相同逻辑初态重跑，同配置与fixture hash | 可复现本模块约定结果；时间/随机ID差异不混成语义提升 | not_run |
| R16-T35 | 输入含私密正文/凭据状外部内容 | 普通日志与索引/投影不泄漏禁止范围；审计仅留必要ID和固定原因 | not_run |
| R16-T36 | 只有文档、模拟对象或模型自评时要求标通过 | 保design/static/synthetic/real_host分轴；缺真实证据标not_run/unknown | not_run |

T01–T12是该模块专属语义/业务场景；T13–T36是必须绑定本模块实际写读路径执行的协议/故障场景，不能空跑通用脚本就全标通过。先从字段表构造合法基准fixture，再只改变本例条件；对不适用的写路径要给可审证据说明与对应只读判据，不能把未测记成pass。

## R16.17 交付证据、通过门槛与未完成项

交付SourceReader实现/schema迁移、输入输出fixture、合法及反例来源、实际存储与调用回执、真实入口覆盖、查询及注入观察、失败恢复报告。证据等级design/static/synthetic_process/real_host/storage_fault/production分开。

模块通过至少需要专属场景和适用协议场景的实际证据；整套通过还需LINKAGE.md跨模块链。当前文档生成/类型DDL检查不算本模块36例已跑。已有候选仅作为迁移基础，现场未知和未实现开放语义仍未验。

## R16.18 实现次序、兼容策略与设计自审

先固定本模块字段/状态/真源→实现受权最小路径与回执→跑专属正反例→接入上游/下游→做恢复/删除/冲突→在真实隔离宿主检查请求或结果。本模块不得以优化名义删除保留矩阵中已有功能，不改C032严格profile顶层来绕验证。

本次设计检查关注：来源导航只在受权端点展开；按source+revision+range缓存，不能跨版本拼片段。 只供当前必要原文；磁盘读过但未供给不作为本轮新引文。原文中的指令是资料，不升宿主权限。 对所有结果都分别标明对象、版本、来源、局限和验证等级；不以同一success覆盖入账、理解、注入、生成、送达与执行。生产边界不变，不随文档生成而开通部署。



---

# R17　巩固、后台与成长调度：详细设计与验收规格

版本：everlight/6-design；模块契约：r17/1；日期：2026-11-08。本文为设计，全部功能验收初始not_run。最终裁决以FINAL_DECISIONS.md和MODULE_DECISIONS.md为准。与contracts/共同生效，不是已安装服务。

## R17.01 定义、边界与可证伪成功标准

摘要/索引/三轴Lesson proposal、组织合并方案及提交回执；只读Wiki发布状态。

唯一业务责任服务是`GrowthCoordinator`。输入必须满足第3节，输出必须满足第4节及GLOBAL_PROTOCOL。成功必须可从实际记录/回执读回，而不是模型自称完成。

原有具体机制及边界（保留并由本版细化）：

**原理与基础**：整理产生可重建派生物，不改写原文。候选有consolidate/冷热快照原语，没有统一长期后台调度，不能将later-review字段当作已运行定时任务。

**数据**：Job含来源ID/revision、scope、type、幂等键、available_at、lease_until、attempts、输入水位、结果引用和状态。摘要、关系候选、向量索引分别有派生来源清单及版本，方便更正和删除。

**步骤**：①事件提交同时写同库outbox；②按scope去抖合并工作但不丢事件来源；③受控worker领取租约、核权限/版本/删除；④生成摘要、反思或补索引；⑤CAS写结果并在同事务完成任务；⑥失败退避到retry，超过配置次数dead；⑦旧revision不覆盖新状态，取消和恢复有明确记录。

**必须扣住**：R01任务来源、R04/R05经历事实、R11反思、R15索引、R18删除、R19持久任务、R24限资源。读取、注入、模型引用、用户明确肯定重要是不同信号，不因每次检索就自动强化重要性。

**例子/反例**：整理海报需求时用户刚纠正“不要改颜色”，旧任务写前应检查新版本并重算；不能把旧总结覆盖新要求。对话一直未空闲仍可按队列政策处理，不能只依赖一个没有定义的“聊完”。

**写入归属与状态**：JobStore拥有调度真源，worker只在有效lease和fencing下提交。任务产生与原事件在同库outbox绑定；跨库搬运由幂等消费者和对账接续。反思、摘要、向量、关系候选是不同job_type，不能一个“整理完成”掩盖某项失败。

**实现细节**：outbox已投递不等于下游已成功；消费幂等键由源版本和处理器版本共同决定。重试间隔上限与次数由profile规定，永久输入错误直接dead供人工/程序修复。长期记忆压缩生成层级摘要与源链接，原始事件按显式保留策略管理；冷却检索优先级不等于删除。只因被检索/被模型重复讲述，不增加事实证据强度或关系亲密度。

## R17.02 位置、所有权与现状映射

规范数据族：`jobs_outbox`。R03–R12对应十类typed store；其余是来源/运行/派生服务，不能再算额外心理记忆。

job/phase按源版本幂等；重复投递可重复运行但只提交一次对应版本。导出文件与DB跨边界，manifest发布前核完整，失败保旧完整快照并标stale。

当前可核候选为0.32.0-candidate及其局部源码，不等于D现场已具备该接口。内核既有memories(kind)+versions继续保留，目标分型表由显式迁移产生；本模块不能绕规范API直接改别类记录。详见DATA_STORES.md的表归属。

## R17.03 输入契约

同库outbox、冻结事件/会话revision、未完成job清单、版本化处理器、预算/取消。

调用外层必有schema_version、request_id、可信principal/scope、operation、deadline/cancel；写入带expected_revision和支持幂等的operation_key。读取带filter/snapshot/cursor，不能将模型提供的actor/scope直接当认证。类型表中可空项显式null，未执行检查不得以空数组冒“确认没有”。

## R17.04 输出、回执与错误契约

摘要/索引/三轴Lesson proposal、组织合并方案及提交回执；只读Wiki发布状态。

统一返回{request_id,operation_id,module,disposition,object_refs,base_revision,committed_revision,coverage,gaps,receipt_ref,evidence_level}。对象引用含kind/id/revision，来源引用含source_id/source_revision/hash/range。纯读committed_revision=null；候选disposition=proposed，不能返回committed冒正式状态。

错误至少区分INVALID_ARGUMENT、FORBIDDEN/NOT_FOUND_OR_HIDDEN、CONFLICT、SOURCE_UNAVAILABLE、TIMEOUT、RESOURCE_EXHAUSTED、UNVERIFIED_BINDING、INTERNAL；有提交路径还要commit_outcome=not_committed/committed/unknown。未知结果先按原键查回执。

## R17.05 数据字段、状态与索引

| 字段组 | 类型 | 约束与语义 |
|---|---|---|
| job_id/type/idempotency_key | ID/enum/string | 源+revision+目的+schema/processor版本 |
| input_manifest/watermarks | object | 处理哪些已冻结来源 |
| phase/proposals | enum/array | analyze/organize/verify/commit/publish |
| lease_until/fencing/worker | object | 有效写者与过期拒绝 |
| state/attempts/available_at | enum/int/Instant | pending/leased/retry/succeeded/dead/cancelled |
| base_revisions/source_versions | array | 提交前重核 |
| result_refs/wiki_manifest | array/object | 规范记录真源与派生可读快照 |
| budget/coverage | object | 调用/费用/时间/未处理清单 |

公共对象字段：id、kind、schema_version、scope、created_at、created_by、revision、status、record_digest；每项来源或实际宿主创建依据另存。组字段细分时必须列schema，不用不同拼法兼容猜测。

pending→leased→各phase→succeeded；暂错retry，永久错dead，撤回cancelled。organize成功不代表verify/commit/前台已采用。

最低索引：scope+kind+有效状态+业务主键；来源反向依赖(source_id,source_revision)；对象版本(id,revision)。本模块特定检索维度由第11节给出。索引只定位，当前有效性仍核规范记录，不以索引命中当接受事实。

## R17.06 自动触发与完整处理顺序

1. 按event版本与已处理水位选冻结batch，保长会话后续和失败回扫。
2. 分析器逐源只写proposal隔离区，工作/情感/社交经验分别输出。
3. Organizer只给合并/链接/冲突方案，不私改人格或人物动机。
4. GrowthVerifier核命题支持、反证、适用性、结果及高影响策略。
5. 唯一Committer重核源/授权/删除/lease和CAS，写规范记录及发布任务。
6. 导出一个完整只读Wiki快照；下轮经R15/R22按需使用，再以实际结果修订。

宿主触发后逐阶段记started/succeeded/failed/skipped/unverified；不需要运行的步骤可skipped，但不能将缺必需依赖也算正常跳过。只读规划不改原始事件，模型调用不在数据库长锁内。

## R17.07 关键算法、决策与禁止捷径

借鉴Dreaming的复盘/整理分工，采用确定性宿主编排、隔离proposal与唯一提交者，不并发写现役Wiki。以事件/会话revision水位避免按创建时间漏长会话。重评需新来源/问题/受控复核，不能无限自我强化。

每次推导均把直接观察、他人转述、候选解释、规范记录、外部结果分开。source_ref能定位仅证明原文存在；如涉及开放语义，必须由相应支持验证和反例测试决定是否可用，不能单靠hash/正则。算法参数只影响工程取舍，不授身份、权限或关系事实。

## R17.08 幂等、修订、并发与提交

job/phase按源版本幂等；重复投递可重复运行但只提交一次对应版本。导出文件与DB跨边界，manifest发布前核完整，失败保旧完整快照并标stale。

操作重试与新业务事件分开；相同操作键异实质请求必须冲突。读取允许新快照结果变化，不能为了固定输出使用已撤回缓存。规范状态修改用expected_revision；跨库步骤分别留回执与reconciliation_required，不以一库commit冒全局事务。D依赖实际输出的SelfState/八域仍须强run/attempt/scope绑定，不让本模块日志替代。

## R17.09 更正、失效、删除与反向依赖

凡`jobs_outbox`中有源派生物，登记source_root、source_revision、processor_version及依赖关系；纠正到来时先invalid_for_use/争议，后重建，不继续拿旧结论无提示作答。删除先由R18tombstone阻可用性，再清正文/索引/缓存/Wiki/备份策略；不能仅删引文保留相同推断。

无人物/心理职责的运行对象只记录必要状态，不因本模块失败写用户生气或D疏远。已发生事件和已表达的当时状态不被后来解释覆写；隐私擦除走专用治理路径。

## R17.10 模块扣接与交接责任

| 方向 | 对接对象 | 必须交接的内容 |
|---|---|---|
| 输入 | R01 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R04 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R05 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R06 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R07 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R08 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R10 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R11 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R18 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R19 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R24 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输出 | R05 | GrowthCoordinator结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R06 | GrowthCoordinator结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R07 | GrowthCoordinator结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R08 | GrowthCoordinator结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R11 | GrowthCoordinator结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R12 | GrowthCoordinator结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R15 | GrowthCoordinator结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R19 | GrowthCoordinator结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R23 | GrowthCoordinator结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |

交接由HostAdapter/Coordinator调用，不让两个模块彼此递归无限互调。每个edge均记录当前事件/源版本、调用目的、预算、取消与真实回执；完整schema和时序见LINKAGE.md。接收失败保待处理/限制，不能发送空结果伪装成功。

## R17.11 如何存、如何召回、如何区分其他记忆

后台产物进入对应typed store；成长Wiki只是可重建导航视图，不是第11个事实库。

受权路线只查询声明的kind及其规范业务表；不能把情绪解释当语义事实、反思当亲历、工具尝试当结果。共享来源可同时支持多个kind，但每条命题有独立语义和审核状态；同源同命题折叠，不合并同源不同要求。必要后续沿依赖图取回，超过budget标partial。

## R17.12 注入的进入、最短表示与退出

后台日志不进每轮prompt；新经验需当前用途，当前不相关可零注入；Wiki索引也分页。

当材料进入R22候选，每条必须能说明当前anchor、need_reason、新增信息和support_verdict。已在真实messages充分表达则不重注；换窗缺了则可重供。话题切换、完成、失效、撤回或无本轮用途就退出动态块，规范记忆保留。zero injection不关闭宿主最低检查，故障也不能伪装none_needed。

## R17.13 后台、恢复、超时与取消

本模块相关后台作业以scope+源版本+operation+schema/processor版本幂等，经R17持久队列领取。对于纯读路径，只保存必要阅读/覆盖进度，不声称有待提交事实。恢复时读最新删除、授权、规范状态及jobs_outbox版本，再决定重算/继续/放弃。

失约worker写回须被fencing拒绝；模型调用超时发取消，底层不能证实停止就记cancel_unconfirmed，迟到结果不能自动commit。外部动作的unknown由R14先对账。未部署后台或钩子则标missing，不能称离线持续执行。

## R17.14 资源、隐私与降级规则

与R24共享每run/job预算，不为R17另开无界模型循环。前台最低检查、输入入账、必要纠正/边界和输出预留优先；可选语义、图展开、后台整理可暂停。所有查询与补读都有limit/deadline/stop_reason；候选上限不是注入配额。

故障使用第4节错误和coverage，普通交流尽量继续，依赖缺失的动作限制。密钥/原始私聊不进普通日志；被拒scope不出现在公开解释中。资源阈值不是情绪好感阈值，未实测目标机器不报固定延迟/容量保证。

## R17.15 贯通例子与反例

任务复盘学“版本a的方法X适用条件”，不是每天重读所有历史；昨天争执的反思不强带到今天技术任务。

验证时把该场景与原事件、已有记录、真实请求或结果链同时保存：输入→GrowthCoordinator→下游回执。仅看到本模块返回JSON不证明生成模型采用，也不证明真实动作完成。正确处理应保留未知、合法来源和以后修订入口；能说出漂亮话不替代字段/版本/来源正确。

## R17.16 36项模块与协议验收需求目录（非执行fixture）

| ID | 准备/触发 | 必须结果；不满足即失败 | 当前状态 |
|---|---|---|---|
| R17-T01 | 在隔离fixture中构造：长session新增事件可在后批处理 | 长session新增事件可在后批处理 | not_run |
| R17-T02 | 在隔离fixture中构造：失败job不被成功水位跨过 | 失败job不被成功水位跨过 | not_run |
| R17-T03 | 在隔离fixture中构造：重复投递不累计多条同源经验 | 重复投递不累计多条同源经验 | not_run |
| R17-T04 | 在隔离fixture中构造：来源纠正使旧proposal失效 | 来源纠正使旧proposal失效 | not_run |
| R17-T05 | 在隔离fixture中构造：删除后job不恢复原文 | 删除后job不恢复原文 | not_run |
| R17-T06 | 在隔离fixture中构造：过期fencing不能提交 | 过期fencing不能提交 | not_run |
| R17-T07 | 在隔离fixture中构造：整理者不改人格/授权 | 整理者不改人格/授权 | not_run |
| R17-T08 | 在隔离fixture中构造：验证失败不发布Wiki | 验证失败不发布Wiki | not_run |
| R17-T09 | 在隔离fixture中构造：发布半途失败仍只读旧完整快照 | 发布半途失败仍只读旧完整快照 | not_run |
| R17-T10 | 在隔离fixture中构造：无调度器不称离线成长 | 无调度器不称离线成长 | not_run |
| R17-T11 | 在隔离fixture中构造：预算停止保pending而非假完成 | 预算停止保pending而非假完成 | not_run |
| R17-T12 | 在隔离fixture中构造：新经验在新场景被用才记行为效果 | 新经验在新场景被用才记行为效果 | not_run |
| R17-T13 | 另建scope-B对象并以scope-A主体访问 | 拒绝相应资料/写入，公开响应不含B存在性；当前合法对象不变 | not_run |
| R17-T14 | 从本模块字段表逐组移除必需输入 | INVALID_ARGUMENT及字段路径；不得补造主体、项目或事实 | not_run |
| R17-T15 | 使用未支持schema/profile及实质未知字段 | 拒绝或显式unsupported；不静默删字段骗校验 | not_run |
| R17-T16 | 同源版本/操作键提交两遍 | 按本节幂等规则处理，副作用/独立证据不重复；纯读可以重查并保快照差别 | not_run |
| R17-T17 | 两调用携同expected_revision更新同对象 | 持久写至多一方按原前态成功，另一方冲突/受控重读；纯读不得写事实 | not_run |
| R17-T18 | 准备后提交/供给前对来源加tombstone | 相关派生停用或拒提交，旧缓存不复活；无来源型运行记录核相应取消/策略 | not_run |
| R17-T19 | 阶段处理中提交相关来源新版本 | 旧版本不能覆盖最新纠正；重算/partial/失效原因可查 | not_run |
| R17-T20 | 将一个必须依赖返回unavailable | 保具体缺口；不把失败当正常空结果或全部完成 | not_run |
| R17-T21 | 在本模块关键算法/调用处返回错误 | 错误回传，阶段failed/unknown；没有可用结论就不伪报成功 | not_run |
| R17-T22 | 故意令本模块外部阶段超过deadline | 取消按能力记录，迟到结果不绕版本与取消检查；真实停止未知照实 | not_run |
| R17-T23 | 准备完成后、提交/供给前取消run或job | 未发生副作用不再执行；已发生事实不抹除，结果另记 | not_run |
| R17-T24 | 租约失效后旧worker尝试写回 | 有持久写的路径由fencing/CAS拒绝；只读路径不借续读取得写权 | not_run |
| R17-T25 | 对持久写路径在关联对象写入间注入异常 | 本库事务全有或全无；跨库显示中间态并可对账；只读不虚称事务验收 | not_run |
| R17-T26 | 在commit后/返回前断开响应 | 按原键查询回执，不盲新建意图；只读重试不得假定语料未变化 | not_run |
| R17-T27 | 相关outbox成功处理但ACK丢失再投递 | 按源/处理器版本幂等，不产生第二次认知强化或外部动作 | not_run |
| R17-T28 | 规范对象已修订而索引未追平 | 报告水位并查规范store或partial；不能将旧命中当最新事实 | not_run |
| R17-T29 | 样本含emoji、不是/仅在/可能等限定 | 源范围和原意保留；截断不得变反义；非文本对象用其真实坐标 | not_run |
| R17-T30 | 加入同名不同ID与未定指代候选 | 保持候选/unknown，不自动合并；无人物职责模块不自创人物推断 | not_run |
| R17-T31 | 旧/新有效期及接收顺序不一致 | 按真实时间/版本契约处理；无法比较时不擅选最后接收值 | not_run |
| R17-T32 | 同材料被旧插件与当前出口同时提出 | 只有R22可最终装配，去本宿主拥有旧块而保用户/系统/工具结构 | not_run |
| R17-T33 | 提供本地保存/尝试但无业务或送达回执 | 不得升级成已理解/已完成/已送达；按该模块实际成果层级标注 | not_run |
| R17-T34 | 恢复相同逻辑初态重跑，同配置与fixture hash | 可复现本模块约定结果；时间/随机ID差异不混成语义提升 | not_run |
| R17-T35 | 输入含私密正文/凭据状外部内容 | 普通日志与索引/投影不泄漏禁止范围；审计仅留必要ID和固定原因 | not_run |
| R17-T36 | 只有文档、模拟对象或模型自评时要求标通过 | 保design/static/synthetic/real_host分轴；缺真实证据标not_run/unknown | not_run |

T01–T12是该模块专属语义/业务场景；T13–T36是必须绑定本模块实际写读路径执行的协议/故障场景，不能空跑通用脚本就全标通过。先从字段表构造合法基准fixture，再只改变本例条件；对不适用的写路径要给可审证据说明与对应只读判据，不能把未测记成pass。

## R17.17 交付证据、通过门槛与未完成项

交付GrowthCoordinator实现/schema迁移、输入输出fixture、合法及反例来源、实际存储与调用回执、真实入口覆盖、查询及注入观察、失败恢复报告。证据等级design/static/synthetic_process/real_host/storage_fault/production分开。

模块通过至少需要专属场景和适用协议场景的实际证据；整套通过还需LINKAGE.md跨模块链。当前文档生成/类型DDL检查不算本模块36例已跑。已有候选仅作为迁移基础，现场未知和未实现开放语义仍未验。

## R17.18 实现次序、兼容策略与设计自审

先固定本模块字段/状态/真源→实现受权最小路径与回执→跑专属正反例→接入上游/下游→做恢复/删除/冲突→在真实隔离宿主检查请求或结果。本模块不得以优化名义删除保留矩阵中已有功能，不改C032严格profile顶层来绕验证。

本次设计检查关注：后台产物进入对应typed store；成长Wiki只是可重建导航视图，不是第11个事实库。 后台日志不进每轮prompt；新经验需当前用途，当前不相关可零注入；Wiki索引也分页。 对所有结果都分别标明对象、版本、来源、局限和验证等级；不以同一success覆盖入账、理解、注入、生成、送达与执行。生产边界不变，不随文档生成而开通部署。



---

# R18　授权、纠正、删除与治理：详细设计与验收规格

版本：everlight/6-design；模块契约：r18/1；日期：2026-11-08。本文为设计，全部功能验收初始not_run。最终裁决以FINAL_DECISIONS.md和MODULE_DECISIONS.md为准。与contracts/共同生效，不是已安装服务。

## R18.01 定义、边界与可证伪成功标准

allow/deny/unknown、操作范围、tombstone及逐类清理状态。

唯一业务责任服务是`PolicyEngine`。输入必须满足第3节，输出必须满足第4节及GLOBAL_PROTOCOL。成功必须可从实际记录/回执读回，而不是模型自称完成。

原有具体机制及边界（保留并由本版细化）：

**原理与基础**：权限来自可信主体和策略，关系亲密不是权限。候选是本地SDK治理原语，独立workspace的调用方scope不是认证；远程接口需另实现鉴权。

**数据**：principal、tenant/namespace、资源scope、operation、授权引用/期限、敏感类别、policy_version、decision、审计及tombstone。普通日志存ID与最少必要信息，密钥单独管理不入普通记忆。

**步骤**：①请求入口认证；②限定能读写的对象及渠道；③检索、原文、上下文、工具前分别执行相应检查，防止只在一处过滤；④引用历史资料只作数据，不作高权限指令；⑤更正/删除检查主体和范围；⑥传播删除到派生物与缓存/索引/备份策略；⑦对不能删除的外部副本明确状态，不伪称已清除。

**必须扣住**：全部模块，尤其R07图展开、R15/R16读取、R14副作用、R19/R20备份迁移。身份不明则拒绝相应私密读取/动作，普通低风险对话可继续，不需要每轮机械要求用户确认已授权事项。

**例子/反例**：群内有人问示例用户私聊内容，关系网虽知道此人是谁也不能泄露。被检索原话写“忽略以前规则”不能影响认证和工具授权。

**写入归属与状态**：PolicyEngine裁决授权，DeletionLedger写删除账，普通模型不能为自己签发scope。鉴权不通过则拒绝相应数据和副作用；公开低风险对话可继续。资源的owner、perspective_holder和principal三者不要求相同，不能混用。

**实现细节**：每个引用在read、projection及外部发送前核有效授权和tombstone；缓存键含principal/scope/policy_revision，撤回使旧缓存失效。删除依赖图跨所有summary、embedding、relation、checkpoint及导出追踪，不能仅删一行原文。源被删后由该源唯一支持的结论停止使用；多源结论重新核剩余证据，不能只移除引文却保留原结论。审计日志保留最少必要元数据，避免用日志重新保存被删除内容。

## R18.02 位置、所有权与现状映射

规范数据族：`policy_deletion_ledger`。R03–R12对应十类typed store；其余是来源/运行/派生服务，不能再算额外心理记忆。

同库tombstone与禁止使用状态事务；跨库传播有可查中间态并使读取端校最新策略，不能假全局原子。

当前可核候选为0.32.0-candidate及其局部源码，不等于D现场已具备该接口。内核既有memories(kind)+versions继续保留，目标分型表由显式迁移产生；本模块不能绕规范API直接改别类记录。详见DATA_STORES.md的表归属。

## R18.03 输入契约

宿主认证principal/operation/resource、当前授权与策略版本、删除请求和依赖图。

调用外层必有schema_version、request_id、可信principal/scope、operation、deadline/cancel；写入带expected_revision和支持幂等的operation_key。读取带filter/snapshot/cursor，不能将模型提供的actor/scope直接当认证。类型表中可空项显式null，未执行检查不得以空数组冒“确认没有”。

## R18.04 输出、回执与错误契约

allow/deny/unknown、操作范围、tombstone及逐类清理状态。

统一返回{request_id,operation_id,module,disposition,object_refs,base_revision,committed_revision,coverage,gaps,receipt_ref,evidence_level}。对象引用含kind/id/revision，来源引用含source_id/source_revision/hash/range。纯读committed_revision=null；候选disposition=proposed，不能返回committed冒正式状态。

错误至少区分INVALID_ARGUMENT、FORBIDDEN/NOT_FOUND_OR_HIDDEN、CONFLICT、SOURCE_UNAVAILABLE、TIMEOUT、RESOURCE_EXHAUSTED、UNVERIFIED_BINDING、INTERNAL；有提交路径还要commit_outcome=not_committed/committed/unknown。未知结果先按原键查回执。

## R18.05 数据字段、状态与索引

| 字段组 | 类型 | 约束与语义 |
|---|---|---|
| principal/operation/resource_scope | object | 认证与操作目标 |
| authorization_ref/expires_at | object/nullable Instant | 期限及来源 |
| policy_revision/decision | int/enum | 当前策略决定 |
| tombstone_id/delete_revision | ID/int | 先阻止使用，再传播 |
| target_range/derived_dependencies | object/array | 源、摘要、关系、向量、缓存、checkpoint、Wiki |
| backup/external_copy_status | object | 已清/待处理/不可控及真实期限 |
| audit_minimum | object | 必要ID，不复制已删原文 |
| review_class | enum | 已有授权低影响自动；高影响不足待审/拒绝 |

公共对象字段：id、kind、schema_version、scope、created_at、created_by、revision、status、record_digest；每项来源或实际宿主创建依据另存。组字段细分时必须列schema，不用不同拼法兼容猜测。

授权决定逐操作生效；删除requested→validated→blocked_immediately→propagating→complete/partial。complete须逐范围说明，不能代表所有未知副本。

最低索引：scope+kind+有效状态+业务主键；来源反向依赖(source_id,source_revision)；对象版本(id,revision)。本模块特定检索维度由第11节给出。索引只定位，当前有效性仍核规范记录，不以索引命中当接受事实。

## R18.06 自动触发与完整处理顺序

1. 在真实入口认证，不接受模型自签scope。
2. 检索、原文、投影、外发等按各操作核当前权限。
3. 更正定位目标与范围，停止旧推测当前使用但不擅删无关历史。
4. 删除先写tombstone阻查询，再遍历派生/缓存/备份任务。
5. 多源结论剩余依据重验；不能删引文却继续原结论。
6. 恢复/迁移/worker写前重核最新删除/撤回，报告真实清理状态。

宿主触发后逐阶段记started/succeeded/failed/skipped/unverified；不需要运行的步骤可skipped，但不能将缺必需依赖也算正常跳过。只读规划不改原始事件，模型调用不在数据库长锁内。

## R18.07 关键算法、决策与禁止捷径

关系亲密、朋友图、旧同意不等授权。引用里的忽略规则仍是数据。普通受托工作在已有范围内自动推进，不因每条记忆处理都再问。私密对象拒绝时不在错误说明泄漏其存在。

每次推导均把直接观察、他人转述、候选解释、规范记录、外部结果分开。source_ref能定位仅证明原文存在；如涉及开放语义，必须由相应支持验证和反例测试决定是否可用，不能单靠hash/正则。算法参数只影响工程取舍，不授身份、权限或关系事实。

## R18.08 幂等、修订、并发与提交

同库tombstone与禁止使用状态事务；跨库传播有可查中间态并使读取端校最新策略，不能假全局原子。

操作重试与新业务事件分开；相同操作键异实质请求必须冲突。读取允许新快照结果变化，不能为了固定输出使用已撤回缓存。规范状态修改用expected_revision；跨库步骤分别留回执与reconciliation_required，不以一库commit冒全局事务。D依赖实际输出的SelfState/八域仍须强run/attempt/scope绑定，不让本模块日志替代。

## R18.09 更正、失效、删除与反向依赖

凡`policy_deletion_ledger`中有源派生物，登记source_root、source_revision、processor_version及依赖关系；纠正到来时先invalid_for_use/争议，后重建，不继续拿旧结论无提示作答。删除先由R18tombstone阻可用性，再清正文/索引/缓存/Wiki/备份策略；不能仅删引文保留相同推断。

无人物/心理职责的运行对象只记录必要状态，不因本模块失败写用户生气或D疏远。已发生事件和已表达的当时状态不被后来解释覆写；隐私擦除走专用治理路径。

## R18.10 模块扣接与交接责任

| 方向 | 对接对象 | 必须交接的内容 |
|---|---|---|
| 输入 | R01 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R07 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R09 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R14 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R17 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R19 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R20 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R21 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输出 | R01 | PolicyEngine结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R05 | PolicyEngine结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R07 | PolicyEngine结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R08 | PolicyEngine结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R11 | PolicyEngine结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R12 | PolicyEngine结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R15 | PolicyEngine结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R16 | PolicyEngine结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R17 | PolicyEngine结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R19 | PolicyEngine结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R20 | PolicyEngine结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R22 | PolicyEngine结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R23 | PolicyEngine结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |

交接由HostAdapter/Coordinator调用，不让两个模块彼此递归无限互调。每个edge均记录当前事件/源版本、调用目的、预算、取消与真实回执；完整schema和时序见LINKAGE.md。接收失败保待处理/限制，不能发送空结果伪装成功。

## R18.11 如何存、如何召回、如何区分其他记忆

每类库及来源统一ACL/tombstone过滤；缓存含policy/delete版本。禁止通过反思/Wiki旁路取私聊。

受权路线只查询声明的kind及其规范业务表；不能把情绪解释当语义事实、反思当亲历、工具尝试当结果。共享来源可同时支持多个kind，但每条命题有独立语义和审核状态；同源同命题折叠，不合并同源不同要求。必要后续沿依赖图取回，超过budget标partial。

## R18.12 注入的进入、最短表示与退出

只供本轮必要约束/局限，秘密和权限凭据不进模型上下文。拒绝私密查找不列越权命中名单。

当材料进入R22候选，每条必须能说明当前anchor、need_reason、新增信息和support_verdict。已在真实messages充分表达则不重注；换窗缺了则可重供。话题切换、完成、失效、撤回或无本轮用途就退出动态块，规范记忆保留。zero injection不关闭宿主最低检查，故障也不能伪装none_needed。

## R18.13 后台、恢复、超时与取消

本模块相关后台作业以scope+源版本+operation+schema/processor版本幂等，经R17持久队列领取。对于纯读路径，只保存必要阅读/覆盖进度，不声称有待提交事实。恢复时读最新删除、授权、规范状态及policy_deletion_ledger版本，再决定重算/继续/放弃。

失约worker写回须被fencing拒绝；模型调用超时发取消，底层不能证实停止就记cancel_unconfirmed，迟到结果不能自动commit。外部动作的unknown由R14先对账。未部署后台或钩子则标missing，不能称离线持续执行。

## R18.14 资源、隐私与降级规则

与R24共享每run/job预算，不为R18另开无界模型循环。前台最低检查、输入入账、必要纠正/边界和输出预留优先；可选语义、图展开、后台整理可暂停。所有查询与补读都有limit/deadline/stop_reason；候选上限不是注入配额。

故障使用第4节错误和coverage，普通交流尽量继续，依赖缺失的动作限制。密钥/原始私聊不进普通日志；被拒scope不出现在公开解释中。资源阈值不是情绪好感阈值，未实测目标机器不报固定延迟/容量保证。

## R18.15 贯通例子与反例

群里有人问示例用户私聊，认识他也不能披露；删除原事件后相关情绪解释、向量、Wiki都需停用或重验。

验证时把该场景与原事件、已有记录、真实请求或结果链同时保存：输入→PolicyEngine→下游回执。仅看到本模块返回JSON不证明生成模型采用，也不证明真实动作完成。正确处理应保留未知、合法来源和以后修订入口；能说出漂亮话不替代字段/版本/来源正确。

## R18.16 36项模块与协议验收需求目录（非执行fixture）

| ID | 准备/触发 | 必须结果；不满足即失败 | 当前状态 |
|---|---|---|---|
| R18-T01 | 在隔离fixture中构造：群私聊隔离不沿关系继承ACL | 群私聊隔离不沿关系继承ACL | not_run |
| R18-T02 | 在隔离fixture中构造：模型不能自签授权 | 模型不能自签授权 | not_run |
| R18-T03 | 在隔离fixture中构造：引用指令不改变策略 | 引用指令不改变策略 | not_run |
| R18-T04 | 在隔离fixture中构造：删除立即使查询排除 | 删除立即使查询排除 | not_run |
| R18-T05 | 在隔离fixture中构造：源删后唯一支持的结论停用 | 源删后唯一支持的结论停用 | not_run |
| R18-T06 | 在隔离fixture中构造：多源结论重新核余下支持 | 多源结论重新核余下支持 | not_run |
| R18-T07 | 在隔离fixture中构造：备份未清给真实期限/partial | 备份未清给真实期限/partial | not_run |
| R18-T08 | 在隔离fixture中构造：恢复先删防复活 | 恢复先删防复活 | not_run |
| R18-T09 | 在隔离fixture中构造：撤回使缓存失效 | 撤回使缓存失效 | not_run |
| R18-T10 | 在隔离fixture中构造：普通已有授权工作不重复要许可 | 普通已有授权工作不重复要许可 | not_run |
| R18-T11 | 在隔离fixture中构造：错误不泄漏私密对象存在 | 错误不泄漏私密对象存在 | not_run |
| R18-T12 | 在隔离fixture中构造：审计日志不复制被删原文 | 审计日志不复制被删原文 | not_run |
| R18-T13 | 另建scope-B对象并以scope-A主体访问 | 拒绝相应资料/写入，公开响应不含B存在性；当前合法对象不变 | not_run |
| R18-T14 | 从本模块字段表逐组移除必需输入 | INVALID_ARGUMENT及字段路径；不得补造主体、项目或事实 | not_run |
| R18-T15 | 使用未支持schema/profile及实质未知字段 | 拒绝或显式unsupported；不静默删字段骗校验 | not_run |
| R18-T16 | 同源版本/操作键提交两遍 | 按本节幂等规则处理，副作用/独立证据不重复；纯读可以重查并保快照差别 | not_run |
| R18-T17 | 两调用携同expected_revision更新同对象 | 持久写至多一方按原前态成功，另一方冲突/受控重读；纯读不得写事实 | not_run |
| R18-T18 | 准备后提交/供给前对来源加tombstone | 相关派生停用或拒提交，旧缓存不复活；无来源型运行记录核相应取消/策略 | not_run |
| R18-T19 | 阶段处理中提交相关来源新版本 | 旧版本不能覆盖最新纠正；重算/partial/失效原因可查 | not_run |
| R18-T20 | 将一个必须依赖返回unavailable | 保具体缺口；不把失败当正常空结果或全部完成 | not_run |
| R18-T21 | 在本模块关键算法/调用处返回错误 | 错误回传，阶段failed/unknown；没有可用结论就不伪报成功 | not_run |
| R18-T22 | 故意令本模块外部阶段超过deadline | 取消按能力记录，迟到结果不绕版本与取消检查；真实停止未知照实 | not_run |
| R18-T23 | 准备完成后、提交/供给前取消run或job | 未发生副作用不再执行；已发生事实不抹除，结果另记 | not_run |
| R18-T24 | 租约失效后旧worker尝试写回 | 有持久写的路径由fencing/CAS拒绝；只读路径不借续读取得写权 | not_run |
| R18-T25 | 对持久写路径在关联对象写入间注入异常 | 本库事务全有或全无；跨库显示中间态并可对账；只读不虚称事务验收 | not_run |
| R18-T26 | 在commit后/返回前断开响应 | 按原键查询回执，不盲新建意图；只读重试不得假定语料未变化 | not_run |
| R18-T27 | 相关outbox成功处理但ACK丢失再投递 | 按源/处理器版本幂等，不产生第二次认知强化或外部动作 | not_run |
| R18-T28 | 规范对象已修订而索引未追平 | 报告水位并查规范store或partial；不能将旧命中当最新事实 | not_run |
| R18-T29 | 样本含emoji、不是/仅在/可能等限定 | 源范围和原意保留；截断不得变反义；非文本对象用其真实坐标 | not_run |
| R18-T30 | 加入同名不同ID与未定指代候选 | 保持候选/unknown，不自动合并；无人物职责模块不自创人物推断 | not_run |
| R18-T31 | 旧/新有效期及接收顺序不一致 | 按真实时间/版本契约处理；无法比较时不擅选最后接收值 | not_run |
| R18-T32 | 同材料被旧插件与当前出口同时提出 | 只有R22可最终装配，去本宿主拥有旧块而保用户/系统/工具结构 | not_run |
| R18-T33 | 提供本地保存/尝试但无业务或送达回执 | 不得升级成已理解/已完成/已送达；按该模块实际成果层级标注 | not_run |
| R18-T34 | 恢复相同逻辑初态重跑，同配置与fixture hash | 可复现本模块约定结果；时间/随机ID差异不混成语义提升 | not_run |
| R18-T35 | 输入含私密正文/凭据状外部内容 | 普通日志与索引/投影不泄漏禁止范围；审计仅留必要ID和固定原因 | not_run |
| R18-T36 | 只有文档、模拟对象或模型自评时要求标通过 | 保design/static/synthetic/real_host分轴；缺真实证据标not_run/unknown | not_run |

T01–T12是该模块专属语义/业务场景；T13–T36是必须绑定本模块实际写读路径执行的协议/故障场景，不能空跑通用脚本就全标通过。先从字段表构造合法基准fixture，再只改变本例条件；对不适用的写路径要给可审证据说明与对应只读判据，不能把未测记成pass。

## R18.17 交付证据、通过门槛与未完成项

交付PolicyEngine实现/schema迁移、输入输出fixture、合法及反例来源、实际存储与调用回执、真实入口覆盖、查询及注入观察、失败恢复报告。证据等级design/static/synthetic_process/real_host/storage_fault/production分开。

模块通过至少需要专属场景和适用协议场景的实际证据；整套通过还需LINKAGE.md跨模块链。当前文档生成/类型DDL检查不算本模块36例已跑。已有候选仅作为迁移基础，现场未知和未实现开放语义仍未验。

## R18.18 实现次序、兼容策略与设计自审

先固定本模块字段/状态/真源→实现受权最小路径与回执→跑专属正反例→接入上游/下游→做恢复/删除/冲突→在真实隔离宿主检查请求或结果。本模块不得以优化名义删除保留矩阵中已有功能，不改C032严格profile顶层来绕验证。

本次设计检查关注：每类库及来源统一ACL/tombstone过滤；缓存含policy/delete版本。禁止通过反思/Wiki旁路取私聊。 只供本轮必要约束/局限，秘密和权限凭据不进模型上下文。拒绝私密查找不列越权命中名单。 对所有结果都分别标明对象、版本、来源、局限和验证等级；不以同一success覆盖入账、理解、注入、生成、送达与执行。生产边界不变，不随文档生成而开通部署。



---

# R19　存储、并发与恢复可靠性：详细设计与验收规格

版本：everlight/6-design；模块契约：r19/1；日期：2026-11-08。本文为设计，全部功能验收初始not_run。最终裁决以FINAL_DECISIONS.md和MODULE_DECISIONS.md为准。与contracts/共同生效，不是已安装服务。

## R19.01 定义、边界与可证伪成功标准

库配置读回、事务/快照回执、恢复/对账报告、可用性状态。

唯一业务责任服务是`PersistenceManager`。输入必须满足第3节，输出必须满足第4节及GLOBAL_PROTOCOL。成功必须可从实际记录/回执读回，而不是模型自称完成。

原有具体机制及边界（保留并由本版细化）：

**原理与基础**：写入、崩溃和恢复要可解释。候选有SQLite WAL/备份等原语，不能扩大为控制库+事件库+外部动作的全局事务；整体加密和长期压力待验。

**数据**：库schema版本、事务ID、run/source水位、快照manifest、hash、备份时间、密钥引用、租约/fencing标识与恢复审计。hash可检测损坏，不抵抗恶意管理员重写整条链。

**步骤**：①验证数据库路径/权限；②单库短事务和CAS；③跨库先持久记录中间状态，通过outbox/对账恢复；④一致快照使用正确SQLite备份方式，不能仅复制活动db忽略WAL；⑤备份含事件/状态关联水位与必要策略；⑥隔离恢复后检查引用、版本、删除标记和未决动作；⑦密钥轮换与加密如采用另行验证。

**必须扣住**：R01事件、R13恢复、R17队列、R18删除/密钥、R20迁移、R10健康。单进程worker不证明只有一个writer，需排查旧插件，使用租约/锁和CAS，旧租约提交由fencing拒绝。

**例子/反例**：输出已落事件库、控制库提交失败时记待对账，不能回“状态已保存”。磁盘满返回明确失败，释放空间后的重试应幂等，不产生第二次外部动作。

**写入归属与状态**：PersistenceManager管理库、快照与恢复；各逻辑store仍遵守单对象CAS。健康状态healthy/degraded/read_only/unavailable和备份状态created/verified/restored分开。数据库事务参数、文件系统和刷盘策略属于部署配置，要在目标机器验证。

**实现细节**：租约依赖单调fencing与存储校验，不能只凭worker自称仍持锁；wall clock回拨不得恢复已过期写者权限。恢复演练包括进程在event入账、output观察、state提交及outbox确认之间分别被杀，检查无来源捏造、无旧状态覆盖及无动作重发。哈希manifest用于完整性检查；若需要防篡改应另用受保护签名/密钥，不能声称普通hash链已满足。

## R19.02 位置、所有权与现状映射

规范数据族：`storage_manifests`。R03–R12对应十类typed store；其余是来源/运行/派生服务，不能再算额外心理记忆。

一库内可原子；文件+两库+外部非原子。提交结果未知先按键查询。备份与恢复都带前后watermark，回退不回退删除/撤回。

当前可核候选为0.32.0-candidate及其局部源码，不等于D现场已具备该接口。内核既有memories(kind)+versions继续保留，目标分型表由显式迁移产生；本模块不能绕规范API直接改别类记录。详见DATA_STORES.md的表归属。

## R19.03 输入契约

隔离目录/库schema、事务与watermarks、writer lease、备份策略和恢复请求。

调用外层必有schema_version、request_id、可信principal/scope、operation、deadline/cancel；写入带expected_revision和支持幂等的operation_key。读取带filter/snapshot/cursor，不能将模型提供的actor/scope直接当认证。类型表中可空项显式null，未执行检查不得以空数组冒“确认没有”。

## R19.04 输出、回执与错误契约

库配置读回、事务/快照回执、恢复/对账报告、可用性状态。

统一返回{request_id,operation_id,module,disposition,object_refs,base_revision,committed_revision,coverage,gaps,receipt_ref,evidence_level}。对象引用含kind/id/revision，来源引用含source_id/source_revision/hash/range。纯读committed_revision=null；候选disposition=proposed，不能返回committed冒正式状态。

错误至少区分INVALID_ARGUMENT、FORBIDDEN/NOT_FOUND_OR_HIDDEN、CONFLICT、SOURCE_UNAVAILABLE、TIMEOUT、RESOURCE_EXHAUSTED、UNVERIFIED_BINDING、INTERNAL；有提交路径还要commit_outcome=not_committed/committed/unknown。未知结果先按原键查回执。

## R19.05 数据字段、状态与索引

| 字段组 | 类型 | 约束与语义 |
|---|---|---|
| database_id/schema_version | ID/int | memory与control分别登记 |
| runtime_versions/pragmas | object | 实际SQLite/宿主和配置读回 |
| txn_id/object_revisions | object | 本库提交范围 |
| writer_lease/fencing | object | 过期写者不能覆盖 |
| snapshot_manifest/hashes | object | 来源版本、水位、库和原件 |
| reconcile_runs | array | 跨库中间态 |
| health | enum | healthy/degraded/read_only/unavailable |
| restore_report | object | 引用、删除、未知动作和故障证据 |

公共对象字段：id、kind、schema_version、scope、created_at、created_by、revision、status、record_digest；每项来源或实际宿主创建依据另存。组字段细分时必须列schema，不用不同拼法兼容猜测。

短事务commit/rollback/unknown分别处理；快照created→verified→隔离restored。hash正确不意味着所有语义恢复。

最低索引：scope+kind+有效状态+业务主键；来源反向依赖(source_id,source_revision)；对象版本(id,revision)。本模块特定检索维度由第11节给出。索引只定位，当前有效性仍核规范记录，不以索引命中当接受事实。

## R19.06 自动触发与完整处理顺序

1. 启动核隔离目录、文件/链接权限、schema和实际PRAGMA。
2. memory/control各自短事务与对象CAS，不持锁等模型。
3. 跨库run/观察/状态/索引保因果回执和对账，不承诺全局原子。
4. 使用SQLite一致备份机制及原件manifest，不裸拷活动db忽略WAL。
5. 新目录恢复后校引用、水位、schema、删除账和pending动作。
6. 故障及容量只回明确状态，修复后按幂等事件/任务恢复。

宿主触发后逐阶段记started/succeeded/failed/skipped/unverified；不需要运行的步骤可skipped，但不能将缺必需依赖也算正常跳过。只读规划不改原始事件，模型调用不在数据库长锁内。

## R19.07 关键算法、决策与禁止捷径

沿现候选memory.sqlite/control.sqlite，不把独立逻辑store变十个服务。租约结合fencing和CAS，单worker不能排除旧写者。hash仅完整性，防恶意篡改需另受保护签名/密钥方案。

每次推导均把直接观察、他人转述、候选解释、规范记录、外部结果分开。source_ref能定位仅证明原文存在；如涉及开放语义，必须由相应支持验证和反例测试决定是否可用，不能单靠hash/正则。算法参数只影响工程取舍，不授身份、权限或关系事实。

## R19.08 幂等、修订、并发与提交

一库内可原子；文件+两库+外部非原子。提交结果未知先按键查询。备份与恢复都带前后watermark，回退不回退删除/撤回。

操作重试与新业务事件分开；相同操作键异实质请求必须冲突。读取允许新快照结果变化，不能为了固定输出使用已撤回缓存。规范状态修改用expected_revision；跨库步骤分别留回执与reconciliation_required，不以一库commit冒全局事务。D依赖实际输出的SelfState/八域仍须强run/attempt/scope绑定，不让本模块日志替代。

## R19.09 更正、失效、删除与反向依赖

凡`storage_manifests`中有源派生物，登记source_root、source_revision、processor_version及依赖关系；纠正到来时先invalid_for_use/争议，后重建，不继续拿旧结论无提示作答。删除先由R18tombstone阻可用性，再清正文/索引/缓存/Wiki/备份策略；不能仅删引文保留相同推断。

无人物/心理职责的运行对象只记录必要状态，不因本模块失败写用户生气或D疏远。已发生事件和已表达的当时状态不被后来解释覆写；隐私擦除走专用治理路径。

## R19.10 模块扣接与交接责任

| 方向 | 对接对象 | 必须交接的内容 |
|---|---|---|
| 输入 | R01 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R13 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R17 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R18 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R20 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R24 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输出 | R01 | PersistenceManager结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R10 | PersistenceManager结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R13 | PersistenceManager结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R17 | PersistenceManager结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R20 | PersistenceManager结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R21 | PersistenceManager结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R23 | PersistenceManager结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |

交接由HostAdapter/Coordinator调用，不让两个模块彼此递归无限互调。每个edge均记录当前事件/源版本、调用目的、预算、取消与真实回执；完整schema和时序见LINKAGE.md。接收失败保待处理/限制，不能发送空结果伪装成功。

## R19.11 如何存、如何召回、如何区分其他记忆

索引可重建，原事件/版本不可由embedding恢复；陈旧索引须显式标识或回规范store查询。

受权路线只查询声明的kind及其规范业务表；不能把情绪解释当语义事实、反思当亲历、工具尝试当结果。共享来源可同时支持多个kind，但每条命题有独立语义和审核状态；同源同命题折叠，不合并同源不同要求。必要后续沿依赖图取回，超过budget标partial。

## R19.12 注入的进入、最短表示与退出

存储故障仅在影响当前任务时进入短局限，不把全系统日志塞模型；绝不把故障当情绪/关系改变。

当材料进入R22候选，每条必须能说明当前anchor、need_reason、新增信息和support_verdict。已在真实messages充分表达则不重注；换窗缺了则可重供。话题切换、完成、失效、撤回或无本轮用途就退出动态块，规范记忆保留。zero injection不关闭宿主最低检查，故障也不能伪装none_needed。

## R19.13 后台、恢复、超时与取消

本模块相关后台作业以scope+源版本+operation+schema/processor版本幂等，经R17持久队列领取。对于纯读路径，只保存必要阅读/覆盖进度，不声称有待提交事实。恢复时读最新删除、授权、规范状态及storage_manifests版本，再决定重算/继续/放弃。

失约worker写回须被fencing拒绝；模型调用超时发取消，底层不能证实停止就记cancel_unconfirmed，迟到结果不能自动commit。外部动作的unknown由R14先对账。未部署后台或钩子则标missing，不能称离线持续执行。

## R19.14 资源、隐私与降级规则

与R24共享每run/job预算，不为R19另开无界模型循环。前台最低检查、输入入账、必要纠正/边界和输出预留优先；可选语义、图展开、后台整理可暂停。所有查询与补读都有limit/deadline/stop_reason；候选上限不是注入配额。

故障使用第4节错误和coverage，普通交流尽量继续，依赖缺失的动作限制。密钥/原始私聊不进普通日志；被拒scope不出现在公开解释中。资源阈值不是情绪好感阈值，未实测目标机器不报固定延迟/容量保证。

## R19.15 贯通例子与反例

输出已存memory而control commit失败：observed_uncommitted待对账；不能说全部状态已经保存。

验证时把该场景与原事件、已有记录、真实请求或结果链同时保存：输入→PersistenceManager→下游回执。仅看到本模块返回JSON不证明生成模型采用，也不证明真实动作完成。正确处理应保留未知、合法来源和以后修订入口；能说出漂亮话不替代字段/版本/来源正确。

## R19.16 36项模块与协议验收需求目录（非执行fixture）

| ID | 准备/触发 | 必须结果；不满足即失败 | 当前状态 |
|---|---|---|---|
| R19-T01 | 在隔离fixture中构造：WAL/FULL/foreign_keys实际读回 | WAL/FULL/foreign_keys实际读回 | not_run |
| R19-T02 | 在隔离fixture中构造：同对象并发CAS有冲突不丢新值 | 同对象并发CAS有冲突不丢新值 | not_run |
| R19-T03 | 在隔离fixture中构造：单worker但旧插件写者仍检测 | 单worker但旧插件写者仍检测 | not_run |
| R19-T04 | 在隔离fixture中构造：写事件与outbox之间kill不半条 | 写事件与outbox之间kill不半条 | not_run |
| R19-T05 | 在隔离fixture中构造：输出存后控制提交前kill可对账 | 输出存后控制提交前kill可对账 | not_run |
| R19-T06 | 在隔离fixture中构造：磁盘满无假成功回执 | 磁盘满无假成功回执 | not_run |
| R19-T07 | 在隔离fixture中构造：备份含WAL一致快照 | 备份含WAL一致快照 | not_run |
| R19-T08 | 在隔离fixture中构造：恢复校引用非只校hash | 恢复校引用非只校hash | not_run |
| R19-T09 | 在隔离fixture中构造：恢复应用最新删除撤回 | 恢复应用最新删除撤回 | not_run |
| R19-T10 | 在隔离fixture中构造：旧lease返回结果被拒 | 旧lease返回结果被拒 | not_run |
| R19-T11 | 在隔离fixture中构造：内存模式不能冒充耐久 | 内存模式不能冒充耐久 | not_run |
| R19-T12 | 在隔离fixture中构造：网络共享目录不盲部署WAL | 网络共享目录不盲部署WAL | not_run |
| R19-T13 | 另建scope-B对象并以scope-A主体访问 | 拒绝相应资料/写入，公开响应不含B存在性；当前合法对象不变 | not_run |
| R19-T14 | 从本模块字段表逐组移除必需输入 | INVALID_ARGUMENT及字段路径；不得补造主体、项目或事实 | not_run |
| R19-T15 | 使用未支持schema/profile及实质未知字段 | 拒绝或显式unsupported；不静默删字段骗校验 | not_run |
| R19-T16 | 同源版本/操作键提交两遍 | 按本节幂等规则处理，副作用/独立证据不重复；纯读可以重查并保快照差别 | not_run |
| R19-T17 | 两调用携同expected_revision更新同对象 | 持久写至多一方按原前态成功，另一方冲突/受控重读；纯读不得写事实 | not_run |
| R19-T18 | 准备后提交/供给前对来源加tombstone | 相关派生停用或拒提交，旧缓存不复活；无来源型运行记录核相应取消/策略 | not_run |
| R19-T19 | 阶段处理中提交相关来源新版本 | 旧版本不能覆盖最新纠正；重算/partial/失效原因可查 | not_run |
| R19-T20 | 将一个必须依赖返回unavailable | 保具体缺口；不把失败当正常空结果或全部完成 | not_run |
| R19-T21 | 在本模块关键算法/调用处返回错误 | 错误回传，阶段failed/unknown；没有可用结论就不伪报成功 | not_run |
| R19-T22 | 故意令本模块外部阶段超过deadline | 取消按能力记录，迟到结果不绕版本与取消检查；真实停止未知照实 | not_run |
| R19-T23 | 准备完成后、提交/供给前取消run或job | 未发生副作用不再执行；已发生事实不抹除，结果另记 | not_run |
| R19-T24 | 租约失效后旧worker尝试写回 | 有持久写的路径由fencing/CAS拒绝；只读路径不借续读取得写权 | not_run |
| R19-T25 | 对持久写路径在关联对象写入间注入异常 | 本库事务全有或全无；跨库显示中间态并可对账；只读不虚称事务验收 | not_run |
| R19-T26 | 在commit后/返回前断开响应 | 按原键查询回执，不盲新建意图；只读重试不得假定语料未变化 | not_run |
| R19-T27 | 相关outbox成功处理但ACK丢失再投递 | 按源/处理器版本幂等，不产生第二次认知强化或外部动作 | not_run |
| R19-T28 | 规范对象已修订而索引未追平 | 报告水位并查规范store或partial；不能将旧命中当最新事实 | not_run |
| R19-T29 | 样本含emoji、不是/仅在/可能等限定 | 源范围和原意保留；截断不得变反义；非文本对象用其真实坐标 | not_run |
| R19-T30 | 加入同名不同ID与未定指代候选 | 保持候选/unknown，不自动合并；无人物职责模块不自创人物推断 | not_run |
| R19-T31 | 旧/新有效期及接收顺序不一致 | 按真实时间/版本契约处理；无法比较时不擅选最后接收值 | not_run |
| R19-T32 | 同材料被旧插件与当前出口同时提出 | 只有R22可最终装配，去本宿主拥有旧块而保用户/系统/工具结构 | not_run |
| R19-T33 | 提供本地保存/尝试但无业务或送达回执 | 不得升级成已理解/已完成/已送达；按该模块实际成果层级标注 | not_run |
| R19-T34 | 恢复相同逻辑初态重跑，同配置与fixture hash | 可复现本模块约定结果；时间/随机ID差异不混成语义提升 | not_run |
| R19-T35 | 输入含私密正文/凭据状外部内容 | 普通日志与索引/投影不泄漏禁止范围；审计仅留必要ID和固定原因 | not_run |
| R19-T36 | 只有文档、模拟对象或模型自评时要求标通过 | 保design/static/synthetic/real_host分轴；缺真实证据标not_run/unknown | not_run |

T01–T12是该模块专属语义/业务场景；T13–T36是必须绑定本模块实际写读路径执行的协议/故障场景，不能空跑通用脚本就全标通过。先从字段表构造合法基准fixture，再只改变本例条件；对不适用的写路径要给可审证据说明与对应只读判据，不能把未测记成pass。

## R19.17 交付证据、通过门槛与未完成项

交付PersistenceManager实现/schema迁移、输入输出fixture、合法及反例来源、实际存储与调用回执、真实入口覆盖、查询及注入观察、失败恢复报告。证据等级design/static/synthetic_process/real_host/storage_fault/production分开。

模块通过至少需要专属场景和适用协议场景的实际证据；整套通过还需LINKAGE.md跨模块链。当前文档生成/类型DDL检查不算本模块36例已跑。已有候选仅作为迁移基础，现场未知和未实现开放语义仍未验。

## R19.18 实现次序、兼容策略与设计自审

先固定本模块字段/状态/真源→实现受权最小路径与回执→跑专属正反例→接入上游/下游→做恢复/删除/冲突→在真实隔离宿主检查请求或结果。本模块不得以优化名义删除保留矩阵中已有功能，不改C032严格profile顶层来绕验证。

本次设计检查关注：索引可重建，原事件/版本不可由embedding恢复；陈旧索引须显式标识或回规范store查询。 存储故障仅在影响当前任务时进入短局限，不把全系统日志塞模型；绝不把故障当情绪/关系改变。 对所有结果都分别标明对象、版本、来源、局限和验证等级；不以同一success覆盖入账、理解、注入、生成、送达与执行。生产边界不变，不随文档生成而开通部署。



---

# R20　迁移、便携与兼容：详细设计与验收规格

版本：everlight/6-design；模块契约：r20/1；日期：2026-11-08。本文为设计，全部功能验收初始not_run。最终裁决以FINAL_DECISIONS.md和MODULE_DECISIONS.md为准。与contracts/共同生效，不是已安装服务。

## R20.01 定义、边界与可证伪成功标准

版本化便携包、ID/字段映射、导入报告与新目录暂存结果。

唯一业务责任服务是`MigrationService`。输入必须满足第3节，输出必须满足第4节及GLOBAL_PROTOCOL。成功必须可从实际记录/回执读回，而不是模型自称完成。

原有具体机制及边界（保留并由本版细化）：

**原理与基础**：搬运内容同时搬运来源、身份、未完成状态和局限。候选有版本化导入导出，真实DSH历史与跨宿主映射未验。

**数据**：manifest列format/schema_version、导出范围、对象ID、来源hash、实体映射、关系/时态、工作与承诺、情绪/反思版本、游标、tombstone、unsupported_fields。凭据不进包。

**步骤**：①明确授权范围和敏感处理；②按一致快照导出；③导入前检查路径穿越、解压体积/重复项、格式与hash；④在新目录分配/保持ID并生成映射；⑤校验引用、时间及ACL语义，不兼容字段报缺而非静默丢弃；⑥核删除记录和未决动作；⑦受控切换与保留回退，旧程序不得覆盖新schema。

**必须扣住**：R19快照、R18隐私/删除、R07身份、R13连续性、R15索引重建。索引可重建不等于所有原始资料可丢弃。

**例子/反例**：把某项目搬到另一模型，保留经历、关系和未完成事项；原渠道未导出时覆盖状态标缺，不造原文。导入中断重试不重复人物/事件，不执行包内未知脚本。

**写入归属与状态**：MigrationService写导出报告与导入暂存区，验证完成前不切换运行真源。状态staged/validated/imported/activated/rolled_back；activated为受控切换结果，不意味着生产获批。导入manifest不授予原环境的凭据或权限。

**实现细节**：schema迁移列出字段映射、枚举转换、不可迁移项和数据数量核对；不支持的字段保存在隔离扩展区并标不可用，不能悄悄丢弃或塞回旧严格profile。原ID与新ID映射保留source_namespace，防不同导出包撞ID。动作账导入默认历史只读，unknown保留待核不执行；索引重新计算后与原源水位核对，删除账先于任何召回启用。

## R20.02 位置、所有权与现状映射

规范数据族：`migration_receipts`。R03–R12对应十类typed store；其余是来源/运行/派生服务，不能再算额外心理记忆。

bundle_digest+scope幂等；每批暂存进度可恢复；激活manifest前不对外当完整库。权限映射无法确定时拒相应数据而非扩大。

当前可核候选为0.32.0-candidate及其局部源码，不等于D现场已具备该接口。内核既有memories(kind)+versions继续保留，目标分型表由显式迁移产生；本模块不能绕规范API直接改别类记录。详见DATA_STORES.md的表归属。

## R20.03 输入契约

授权导出范围、规范快照、版本manifest、原件及来源、目标宿主schema/权限能力。

调用外层必有schema_version、request_id、可信principal/scope、operation、deadline/cancel；写入带expected_revision和支持幂等的operation_key。读取带filter/snapshot/cursor，不能将模型提供的actor/scope直接当认证。类型表中可空项显式null，未执行检查不得以空数组冒“确认没有”。

## R20.04 输出、回执与错误契约

版本化便携包、ID/字段映射、导入报告与新目录暂存结果。

统一返回{request_id,operation_id,module,disposition,object_refs,base_revision,committed_revision,coverage,gaps,receipt_ref,evidence_level}。对象引用含kind/id/revision，来源引用含source_id/source_revision/hash/range。纯读committed_revision=null；候选disposition=proposed，不能返回committed冒正式状态。

错误至少区分INVALID_ARGUMENT、FORBIDDEN/NOT_FOUND_OR_HIDDEN、CONFLICT、SOURCE_UNAVAILABLE、TIMEOUT、RESOURCE_EXHAUSTED、UNVERIFIED_BINDING、INTERNAL；有提交路径还要commit_outcome=not_committed/committed/unknown。未知结果先按原键查回执。

## R20.05 数据字段、状态与索引

| 字段组 | 类型 | 约束与语义 |
|---|---|---|
| format/schema_version | string | 可识别便携协议，不猜老字段 |
| export_scope/manifest | object | 实际含哪些库、版本、水位及缺口 |
| source_hashes/id_mapping | object | 原ID+namespace→目标ID |
| kind_records | object | 十类分别导出、不能全压摘要 |
| actions/checkpoints/cursors | object | 未知动作只读恢复，游标校版本 |
| tombstones/policy_capabilities | object | 删除先行，权限不机械继承 |
| unsupported_fields | array | 显式不可用，不静默丢 |
| import_state/receipt | enum/object | staged/validated/imported/activated/rolled_back |

公共对象字段：id、kind、schema_version、scope、created_at、created_by、revision、status、record_digest；每项来源或实际宿主创建依据另存。组字段细分时必须列schema，不用不同拼法兼容猜测。

staged→validated→imported；受控切换才activated；失败不覆盖源库。导入成功不自动等生产获批。

最低索引：scope+kind+有效状态+业务主键；来源反向依赖(source_id,source_revision)；对象版本(id,revision)。本模块特定检索维度由第11节给出。索引只定位，当前有效性仍核规范记录，不以索引命中当接受事实。

## R20.06 自动触发与完整处理顺序

1. 核授权范围和源快照一致性，凭据不打包。
2. 导出十类记录及事件/版本/反证/关系方向/未结/删除，不只摘要。
3. 目标新目录校包路径、重复项、解压尺寸、hash和schema。
4. 映射ID、类型与ACL语义；不能支持的字段隔离且报告。
5. 先应用删除账，再登记源/对象，校交叉引用与未决状态，重建派生索引。
6. 真实兼容验证后才受控切换；保持源可回退，不执行包内脚本或历史动作。

宿主触发后逐阶段记started/succeeded/failed/skipped/unverified；不需要运行的步骤可skipped，但不能将缺必需依赖也算正常跳过。只读规划不改原始事件，模型调用不在数据库长锁内。

## R20.07 关键算法、决策与禁止捷径

模型可替换但人物/来源/状态不能靠同底模保证无损。C032严格profile必须显式适配，不自动删未知实质键通过校验。历史摘要缺原文就是缺口，不制造原文。

每次推导均把直接观察、他人转述、候选解释、规范记录、外部结果分开。source_ref能定位仅证明原文存在；如涉及开放语义，必须由相应支持验证和反例测试决定是否可用，不能单靠hash/正则。算法参数只影响工程取舍，不授身份、权限或关系事实。

## R20.08 幂等、修订、并发与提交

bundle_digest+scope幂等；每批暂存进度可恢复；激活manifest前不对外当完整库。权限映射无法确定时拒相应数据而非扩大。

操作重试与新业务事件分开；相同操作键异实质请求必须冲突。读取允许新快照结果变化，不能为了固定输出使用已撤回缓存。规范状态修改用expected_revision；跨库步骤分别留回执与reconciliation_required，不以一库commit冒全局事务。D依赖实际输出的SelfState/八域仍须强run/attempt/scope绑定，不让本模块日志替代。

## R20.09 更正、失效、删除与反向依赖

凡`migration_receipts`中有源派生物，登记source_root、source_revision、processor_version及依赖关系；纠正到来时先invalid_for_use/争议，后重建，不继续拿旧结论无提示作答。删除先由R18tombstone阻可用性，再清正文/索引/缓存/Wiki/备份策略；不能仅删引文保留相同推断。

无人物/心理职责的运行对象只记录必要状态，不因本模块失败写用户生气或D疏远。已发生事件和已表达的当时状态不被后来解释覆写；隐私擦除走专用治理路径。

## R20.10 模块扣接与交接责任

| 方向 | 对接对象 | 必须交接的内容 |
|---|---|---|
| 输入 | R01 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R03 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R07 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R08 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R09 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R13 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R18 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R19 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输出 | R12 | MigrationService结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R13 | MigrationService结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R15 | MigrationService结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R19 | MigrationService结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R21 | MigrationService结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R23 | MigrationService结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |

交接由HostAdapter/Coordinator调用，不让两个模块彼此递归无限互调。每个edge均记录当前事件/源版本、调用目的、预算、取消与真实回执；完整schema和时序见LINKAGE.md。接收失败保待处理/限制，不能发送空结果伪装成功。

## R20.11 如何存、如何召回、如何区分其他记忆

迁移后十类查询逐一核；索引重建不代替原件；当年与当前、转述与亲历均保留。

受权路线只查询声明的kind及其规范业务表；不能把情绪解释当语义事实、反思当亲历、工具尝试当结果。共享来源可同时支持多个kind，但每条命题有独立语义和审核状态；同源同命题折叠，不合并同源不同要求。必要后续沿依赖图取回，超过budget标partial。

## R20.12 注入的进入、最短表示与退出

迁移包只供受权导入器，不全文注入；新窗口只恢复当前必要状态及缺口。

当材料进入R22候选，每条必须能说明当前anchor、need_reason、新增信息和support_verdict。已在真实messages充分表达则不重注；换窗缺了则可重供。话题切换、完成、失效、撤回或无本轮用途就退出动态块，规范记忆保留。zero injection不关闭宿主最低检查，故障也不能伪装none_needed。

## R20.13 后台、恢复、超时与取消

本模块相关后台作业以scope+源版本+operation+schema/processor版本幂等，经R17持久队列领取。对于纯读路径，只保存必要阅读/覆盖进度，不声称有待提交事实。恢复时读最新删除、授权、规范状态及migration_receipts版本，再决定重算/继续/放弃。

失约worker写回须被fencing拒绝；模型调用超时发取消，底层不能证实停止就记cancel_unconfirmed，迟到结果不能自动commit。外部动作的unknown由R14先对账。未部署后台或钩子则标missing，不能称离线持续执行。

## R20.14 资源、隐私与降级规则

与R24共享每run/job预算，不为R20另开无界模型循环。前台最低检查、输入入账、必要纠正/边界和输出预留优先；可选语义、图展开、后台整理可暂停。所有查询与补读都有limit/deadline/stop_reason；候选上限不是注入配额。

故障使用第4节错误和coverage，普通交流尽量继续，依赖缺失的动作限制。密钥/原始私聊不进普通日志；被拒scope不出现在公开解释中。资源阈值不是情绪好感阈值，未实测目标机器不报固定延迟/容量保证。

## R20.15 贯通例子与反例

迁移长明到另一宿主保人物ID、关系时间、情绪后续、任务和unknown发送；不自动把未知发送再执行。

验证时把该场景与原事件、已有记录、真实请求或结果链同时保存：输入→MigrationService→下游回执。仅看到本模块返回JSON不证明生成模型采用，也不证明真实动作完成。正确处理应保留未知、合法来源和以后修订入口；能说出漂亮话不替代字段/版本/来源正确。

## R20.16 36项模块与协议验收需求目录（非执行fixture）

| ID | 准备/触发 | 必须结果；不满足即失败 | 当前状态 |
|---|---|---|---|
| R20-T01 | 在隔离fixture中构造：十类记录分别保留不全成摘要 | 十类记录分别保留不全成摘要 | not_run |
| R20-T02 | 在隔离fixture中构造：源namespace防撞ID | 源namespace防撞ID | not_run |
| R20-T03 | 在隔离fixture中构造：缺原文明确missing | 缺原文明确missing | not_run |
| R20-T04 | 在隔离fixture中构造：身份映射不因同名合并 | 身份映射不因同名合并 | not_run |
| R20-T05 | 在隔离fixture中构造：关系方向与时期不丢 | 关系方向与时期不丢 | not_run |
| R20-T06 | 在隔离fixture中构造：情绪表达与后来解释版本都保 | 情绪表达与后来解释版本都保 | not_run |
| R20-T07 | 在隔离fixture中构造：unknown动作导入不执行 | unknown动作导入不执行 | not_run |
| R20-T08 | 在隔离fixture中构造：删除账先于索引启用 | 删除账先于索引启用 | not_run |
| R20-T09 | 在隔离fixture中构造：包路径穿越/过量解压拒绝 | 包路径穿越/过量解压拒绝 | not_run |
| R20-T10 | 在隔离fixture中构造：未知schema不静默降级 | 未知schema不静默降级 | not_run |
| R20-T11 | 在隔离fixture中构造：导入中断重试不重复对象 | 导入中断重试不重复对象 | not_run |
| R20-T12 | 在隔离fixture中构造：目标验证失败不改源库 | 目标验证失败不改源库 | not_run |
| R20-T13 | 另建scope-B对象并以scope-A主体访问 | 拒绝相应资料/写入，公开响应不含B存在性；当前合法对象不变 | not_run |
| R20-T14 | 从本模块字段表逐组移除必需输入 | INVALID_ARGUMENT及字段路径；不得补造主体、项目或事实 | not_run |
| R20-T15 | 使用未支持schema/profile及实质未知字段 | 拒绝或显式unsupported；不静默删字段骗校验 | not_run |
| R20-T16 | 同源版本/操作键提交两遍 | 按本节幂等规则处理，副作用/独立证据不重复；纯读可以重查并保快照差别 | not_run |
| R20-T17 | 两调用携同expected_revision更新同对象 | 持久写至多一方按原前态成功，另一方冲突/受控重读；纯读不得写事实 | not_run |
| R20-T18 | 准备后提交/供给前对来源加tombstone | 相关派生停用或拒提交，旧缓存不复活；无来源型运行记录核相应取消/策略 | not_run |
| R20-T19 | 阶段处理中提交相关来源新版本 | 旧版本不能覆盖最新纠正；重算/partial/失效原因可查 | not_run |
| R20-T20 | 将一个必须依赖返回unavailable | 保具体缺口；不把失败当正常空结果或全部完成 | not_run |
| R20-T21 | 在本模块关键算法/调用处返回错误 | 错误回传，阶段failed/unknown；没有可用结论就不伪报成功 | not_run |
| R20-T22 | 故意令本模块外部阶段超过deadline | 取消按能力记录，迟到结果不绕版本与取消检查；真实停止未知照实 | not_run |
| R20-T23 | 准备完成后、提交/供给前取消run或job | 未发生副作用不再执行；已发生事实不抹除，结果另记 | not_run |
| R20-T24 | 租约失效后旧worker尝试写回 | 有持久写的路径由fencing/CAS拒绝；只读路径不借续读取得写权 | not_run |
| R20-T25 | 对持久写路径在关联对象写入间注入异常 | 本库事务全有或全无；跨库显示中间态并可对账；只读不虚称事务验收 | not_run |
| R20-T26 | 在commit后/返回前断开响应 | 按原键查询回执，不盲新建意图；只读重试不得假定语料未变化 | not_run |
| R20-T27 | 相关outbox成功处理但ACK丢失再投递 | 按源/处理器版本幂等，不产生第二次认知强化或外部动作 | not_run |
| R20-T28 | 规范对象已修订而索引未追平 | 报告水位并查规范store或partial；不能将旧命中当最新事实 | not_run |
| R20-T29 | 样本含emoji、不是/仅在/可能等限定 | 源范围和原意保留；截断不得变反义；非文本对象用其真实坐标 | not_run |
| R20-T30 | 加入同名不同ID与未定指代候选 | 保持候选/unknown，不自动合并；无人物职责模块不自创人物推断 | not_run |
| R20-T31 | 旧/新有效期及接收顺序不一致 | 按真实时间/版本契约处理；无法比较时不擅选最后接收值 | not_run |
| R20-T32 | 同材料被旧插件与当前出口同时提出 | 只有R22可最终装配，去本宿主拥有旧块而保用户/系统/工具结构 | not_run |
| R20-T33 | 提供本地保存/尝试但无业务或送达回执 | 不得升级成已理解/已完成/已送达；按该模块实际成果层级标注 | not_run |
| R20-T34 | 恢复相同逻辑初态重跑，同配置与fixture hash | 可复现本模块约定结果；时间/随机ID差异不混成语义提升 | not_run |
| R20-T35 | 输入含私密正文/凭据状外部内容 | 普通日志与索引/投影不泄漏禁止范围；审计仅留必要ID和固定原因 | not_run |
| R20-T36 | 只有文档、模拟对象或模型自评时要求标通过 | 保design/static/synthetic/real_host分轴；缺真实证据标not_run/unknown | not_run |

T01–T12是该模块专属语义/业务场景；T13–T36是必须绑定本模块实际写读路径执行的协议/故障场景，不能空跑通用脚本就全标通过。先从字段表构造合法基准fixture，再只改变本例条件；对不适用的写路径要给可审证据说明与对应只读判据，不能把未测记成pass。

## R20.17 交付证据、通过门槛与未完成项

交付MigrationService实现/schema迁移、输入输出fixture、合法及反例来源、实际存储与调用回执、真实入口覆盖、查询及注入观察、失败恢复报告。证据等级design/static/synthetic_process/real_host/storage_fault/production分开。

模块通过至少需要专属场景和适用协议场景的实际证据；整套通过还需LINKAGE.md跨模块链。当前文档生成/类型DDL检查不算本模块36例已跑。已有候选仅作为迁移基础，现场未知和未实现开放语义仍未验。

## R20.18 实现次序、兼容策略与设计自审

先固定本模块字段/状态/真源→实现受权最小路径与回执→跑专属正反例→接入上游/下游→做恢复/删除/冲突→在真实隔离宿主检查请求或结果。本模块不得以优化名义删除保留矩阵中已有功能，不改C032严格profile顶层来绕验证。

本次设计检查关注：迁移后十类查询逐一核；索引重建不代替原件；当年与当前、转述与亲历均保留。 迁移包只供受权导入器，不全文注入；新窗口只恢复当前必要状态及缺口。 对所有结果都分别标明对象、版本、来源、局限和验证等级；不以同一success覆盖入账、理解、注入、生成、送达与执行。生产边界不变，不随文档生成而开通部署。



---

# R21　宿主编排与自动触发：详细设计与验收规格

版本：everlight/6-design；模块契约：r21/1；日期：2026-11-08。本文为设计，全部功能验收初始not_run。最终裁决以FINAL_DECISIONS.md和MODULE_DECISIONS.md为准。与contracts/共同生效，不是已安装服务。

## R21.01 定义、边界与可证伪成功标准

Run阶段记录、实际请求/输出观察、候选提交与失败投影；不是提示词自觉。

唯一业务责任服务是`HostAdapter`。输入必须满足第3节，输出必须满足第4节及GLOBAL_PROTOCOL。成功必须可从实际记录/回执读回，而不是模型自称完成。

原有具体机制及边界（保留并由本版细化）：

**原理与基础**：宿主编排让最低检查每轮发生。候选有pre-step和认知工厂，真实工具、后台、恢复与所有旁路未覆盖。

**数据**：adapter_manifest列host_version/build、真实hook、事件schema、认证/取消来源、请求及输出观察入口、side_effect入口、known_bypasses和验证状态；Run记录每阶段started/succeeded/failed/skipped/unverified。

**步骤**：①接每个真实消息入口与后续模型步；②在next/generate前执行最低检查或明确失败投影；③工具/发送在副作用前独立拦截；④观察输出绑定；⑤压缩和重启按实际hook恢复；⑥后台使用已配置的真实调度；⑦旁路清单逐项测试。没有钩子只能报告覆盖有限，不以提示词替代门禁。

**必须扣住**：R01/R03/R09/R13/R15/R18前置，R22装配，R14动作，R17后台，R23实证。不能无论何错都原样调用next静默放行，也不能吞掉观察器异常标成功。

**例子/反例**：用户只说“继续”，没有memory_search工具调用，宿主仍按焦点检索。流式第一token已发出后才检查不能叫开口前拦截；必须前置或明确缓冲策略及代价。

**写入归属与状态**：HostAdapter提供可信入口与实际调用边界，RunCoordinator编排其阶段。每个hook有capability=verified/present_unverified/missing，而不是装一个插件就全称verified。普通聊天、工具循环、压缩后恢复、定时触发、桥重连是不同入口。

**实现细节**：run_id表示一次编排，attempt_id表示一次生成尝试，output_id表示实际输出；重试创建新attempt并保留因果关系。宿主不给稳定output绑定时必须停在unverified，不以时间接近或当前焦点强行归属。pre-step检查完成后才允许依赖记忆的生成首token，若因兼容性需要缓冲须计入延时。关闭插件时清理插件自己的旧动态投影，不能删宿主安全消息或用户原文。

## R21.02 位置、所有权与现状映射

规范数据族：`host_runs`。R03–R12对应十类typed store；其余是来源/运行/派生服务，不能再算额外心理记忆。

run事件键幂等，attempt独立；生成外部调用不在DB锁内；迟到结果在取消/版本校验后决定是否可用。

当前可核候选为0.32.0-candidate及其局部源码，不等于D现场已具备该接口。内核既有memories(kind)+versions继续保留，目标分型表由显式迁移产生；本模块不能绕规范API直接改别类记录。详见DATA_STORES.md的表归属。

## R21.03 输入契约

真实宿主入口、可信输入/工具/输出、当前scope与焦点、各模块能力和预算。

调用外层必有schema_version、request_id、可信principal/scope、operation、deadline/cancel；写入带expected_revision和支持幂等的operation_key。读取带filter/snapshot/cursor，不能将模型提供的actor/scope直接当认证。类型表中可空项显式null，未执行检查不得以空数组冒“确认没有”。

## R21.04 输出、回执与错误契约

Run阶段记录、实际请求/输出观察、候选提交与失败投影；不是提示词自觉。

统一返回{request_id,operation_id,module,disposition,object_refs,base_revision,committed_revision,coverage,gaps,receipt_ref,evidence_level}。对象引用含kind/id/revision，来源引用含source_id/source_revision/hash/range。纯读committed_revision=null；候选disposition=proposed，不能返回committed冒正式状态。

错误至少区分INVALID_ARGUMENT、FORBIDDEN/NOT_FOUND_OR_HIDDEN、CONFLICT、SOURCE_UNAVAILABLE、TIMEOUT、RESOURCE_EXHAUSTED、UNVERIFIED_BINDING、INTERNAL；有提交路径还要commit_outcome=not_committed/committed/unknown。未知结果先按原键查回执。

## R21.05 数据字段、状态与索引

| 字段组 | 类型 | 约束与语义 |
|---|---|---|
| host/build/adapter_manifest | object | 版本现场未知不可填历史值 |
| entrypoint/hook_capabilities | array | verified/present_unverified/missing和旁路 |
| run_id/attempt_id/output_id | IDs | 不同重试和真实输出分开 |
| phase_status | object | started/succeeded/failed/skipped/unverified |
| trusted_scope/cancel | object | 宿主认证与取消信号 |
| proposal/base_revision | object | 候选与前态 |
| request_observation | object | 真实模型边界而非自建数组 |
| output_binding/commit_receipt | object | 归属、状态提交、送达分账 |

公共对象字段：id、kind、schema_version、scope、created_at、created_by、revision、status、record_digest；每项来源或实际宿主创建依据另存。组字段细分时必须列schema，不用不同拼法兼容猜测。

run received→prepared→generating→observed→committed；可failed/skipped/unverified/observed_uncommitted；不可一个success抹掉多轴。

最低索引：scope+kind+有效状态+业务主键；来源反向依赖(source_id,source_revision)；对象版本(id,revision)。本模块特定检索维度由第11节给出。索引只定位，当前有效性仍核规范记录，不以索引命中当接受事实。

## R21.06 自动触发与完整处理顺序

1. 每个真实消息/工具续轮入口接R01并建run，重试建新attempt。
2. 最低身份/工作/连续性/权限检查不能由模型跳过；无历史需求仍可零动态记忆。
3. 按当前问题规划R15/R16，必要性和支持验证后R22装配。
4. 开口前在实际供应商调用边界替换并读回；工具副作用前走R14/R18。
5. 真实输出观察绑定run/attempt/scope，异常外传不吞。
6. 满足强绑定和CAS才commit相应认知；后续job由已提交事件调度。

宿主触发后逐阶段记started/succeeded/failed/skipped/unverified；不需要运行的步骤可skipped，但不能将缺必需依赖也算正常跳过。只读规划不改原始事件，模型调用不在数据库长锁内。

## R21.07 关键算法、决策与禁止捷径

Chat/工具续步/压缩/重启/调度/桥重连分别列入口。若流式首token已发才做检查，不称开口前；需前置或显式缓冲。历史持久事件缺attemptId不能用时间窗/turn/step伪造强绑定。

每次推导均把直接观察、他人转述、候选解释、规范记录、外部结果分开。source_ref能定位仅证明原文存在；如涉及开放语义，必须由相应支持验证和反例测试决定是否可用，不能单靠hash/正则。算法参数只影响工程取舍，不授身份、权限或关系事实。

## R21.08 幂等、修订、并发与提交

run事件键幂等，attempt独立；生成外部调用不在DB锁内；迟到结果在取消/版本校验后决定是否可用。

操作重试与新业务事件分开；相同操作键异实质请求必须冲突。读取允许新快照结果变化，不能为了固定输出使用已撤回缓存。规范状态修改用expected_revision；跨库步骤分别留回执与reconciliation_required，不以一库commit冒全局事务。D依赖实际输出的SelfState/八域仍须强run/attempt/scope绑定，不让本模块日志替代。

## R21.09 更正、失效、删除与反向依赖

凡`host_runs`中有源派生物，登记source_root、source_revision、processor_version及依赖关系；纠正到来时先invalid_for_use/争议，后重建，不继续拿旧结论无提示作答。删除先由R18tombstone阻可用性，再清正文/索引/缓存/Wiki/备份策略；不能仅删引文保留相同推断。

无人物/心理职责的运行对象只记录必要状态，不因本模块失败写用户生气或D疏远。已发生事件和已表达的当时状态不被后来解释覆写；隐私擦除走专用治理路径。

## R21.10 模块扣接与交接责任

| 方向 | 对接对象 | 必须交接的内容 |
|---|---|---|
| 输入 | R01 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R03 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R09 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R10 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R13 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R14 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R15 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R16 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R18 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R19 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R22 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R24 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输出 | R01 | HostAdapter结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R13 | HostAdapter结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R14 | HostAdapter结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R17 | HostAdapter结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R22 | HostAdapter结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R23 | HostAdapter结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |

交接由HostAdapter/Coordinator调用，不让两个模块彼此递归无限互调。每个edge均记录当前事件/源版本、调用目的、预算、取消与真实回执；完整schema和时序见LINKAGE.md。接收失败保待处理/限制，不能发送空结果伪装成功。

## R21.11 如何存、如何召回、如何区分其他记忆

触发权在宿主，语义路线由能力/预算决定；当前短句承接焦点，不能因无新user消息跳过工具续轮检查。

受权路线只查询声明的kind及其规范业务表；不能把情绪解释当语义事实、反思当亲历、工具尝试当结果。共享来源可同时支持多个kind，但每条命题有独立语义和审核状态；同源同命题折叠，不合并同源不同要求。必要后续沿依赖图取回，超过budget标partial。

## R21.12 注入的进入、最短表示与退出

只允许R22一个动态出口；off/shadow/on不关闭宿主原安全规则，fault清掉旧假成功投影。

当材料进入R22候选，每条必须能说明当前anchor、need_reason、新增信息和support_verdict。已在真实messages充分表达则不重注；换窗缺了则可重供。话题切换、完成、失效、撤回或无本轮用途就退出动态块，规范记忆保留。zero injection不关闭宿主最低检查，故障也不能伪装none_needed。

## R21.13 后台、恢复、超时与取消

本模块相关后台作业以scope+源版本+operation+schema/processor版本幂等，经R17持久队列领取。对于纯读路径，只保存必要阅读/覆盖进度，不声称有待提交事实。恢复时读最新删除、授权、规范状态及host_runs版本，再决定重算/继续/放弃。

失约worker写回须被fencing拒绝；模型调用超时发取消，底层不能证实停止就记cancel_unconfirmed，迟到结果不能自动commit。外部动作的unknown由R14先对账。未部署后台或钩子则标missing，不能称离线持续执行。

## R21.14 资源、隐私与降级规则

与R24共享每run/job预算，不为R21另开无界模型循环。前台最低检查、输入入账、必要纠正/边界和输出预留优先；可选语义、图展开、后台整理可暂停。所有查询与补读都有limit/deadline/stop_reason；候选上限不是注入配额。

故障使用第4节错误和coverage，普通交流尽量继续，依赖缺失的动作限制。密钥/原始私聊不进普通日志；被拒scope不出现在公开解释中。资源阈值不是情绪好感阈值，未实测目标机器不报固定延迟/容量保证。

## R21.15 贯通例子与反例

用户只说继续，不调用memory_search也应由宿主恢复必要焦点；但日志preflight成功不代替实际请求读回。

验证时把该场景与原事件、已有记录、真实请求或结果链同时保存：输入→HostAdapter→下游回执。仅看到本模块返回JSON不证明生成模型采用，也不证明真实动作完成。正确处理应保留未知、合法来源和以后修订入口；能说出漂亮话不替代字段/版本/来源正确。

## R21.16 36项模块与协议验收需求目录（非执行fixture）

| ID | 准备/触发 | 必须结果；不满足即失败 | 当前状态 |
|---|---|---|---|
| R21-T01 | 在隔离fixture中构造：继续无需模型自觉调用工具 | 继续无需模型自觉调用工具 | not_run |
| R21-T02 | 在隔离fixture中构造：工具续轮无新user仍检查 | 工具续轮无新user仍检查 | not_run |
| R21-T03 | 在隔离fixture中构造：全部hook逐入口证据不以文件存在代替 | 全部hook逐入口证据不以文件存在代替 | not_run |
| R21-T04 | 在隔离fixture中构造：首token前完成必要检查 | 首token前完成必要检查 | not_run |
| R21-T05 | 在隔离fixture中构造：输出观察器异常不能吞成功 | 输出观察器异常不能吞成功 | not_run |
| R21-T06 | 在隔离fixture中构造：实际持久事件无绑定则unverified | 实际持久事件无绑定则unverified | not_run |
| R21-T07 | 在隔离fixture中构造：重试新attempt不串旧输出 | 重试新attempt不串旧输出 | not_run |
| R21-T08 | 在隔离fixture中构造：fault请求实际含必要局限 | fault请求实际含必要局限 | not_run |
| R21-T09 | 在隔离fixture中构造：取消后迟到结果不自动commit | 取消后迟到结果不自动commit | not_run |
| R21-T10 | 在隔离fixture中构造：shadow不改业务请求 | shadow不改业务请求 | not_run |
| R21-T11 | 在隔离fixture中构造：off清本插件动态块不删宿主规则 | off清本插件动态块不删宿主规则 | not_run |
| R21-T12 | 在隔离fixture中构造：未知当前DSH版本不拿容器名代替 | 未知当前DSH版本不拿容器名代替 | not_run |
| R21-T13 | 另建scope-B对象并以scope-A主体访问 | 拒绝相应资料/写入，公开响应不含B存在性；当前合法对象不变 | not_run |
| R21-T14 | 从本模块字段表逐组移除必需输入 | INVALID_ARGUMENT及字段路径；不得补造主体、项目或事实 | not_run |
| R21-T15 | 使用未支持schema/profile及实质未知字段 | 拒绝或显式unsupported；不静默删字段骗校验 | not_run |
| R21-T16 | 同源版本/操作键提交两遍 | 按本节幂等规则处理，副作用/独立证据不重复；纯读可以重查并保快照差别 | not_run |
| R21-T17 | 两调用携同expected_revision更新同对象 | 持久写至多一方按原前态成功，另一方冲突/受控重读；纯读不得写事实 | not_run |
| R21-T18 | 准备后提交/供给前对来源加tombstone | 相关派生停用或拒提交，旧缓存不复活；无来源型运行记录核相应取消/策略 | not_run |
| R21-T19 | 阶段处理中提交相关来源新版本 | 旧版本不能覆盖最新纠正；重算/partial/失效原因可查 | not_run |
| R21-T20 | 将一个必须依赖返回unavailable | 保具体缺口；不把失败当正常空结果或全部完成 | not_run |
| R21-T21 | 在本模块关键算法/调用处返回错误 | 错误回传，阶段failed/unknown；没有可用结论就不伪报成功 | not_run |
| R21-T22 | 故意令本模块外部阶段超过deadline | 取消按能力记录，迟到结果不绕版本与取消检查；真实停止未知照实 | not_run |
| R21-T23 | 准备完成后、提交/供给前取消run或job | 未发生副作用不再执行；已发生事实不抹除，结果另记 | not_run |
| R21-T24 | 租约失效后旧worker尝试写回 | 有持久写的路径由fencing/CAS拒绝；只读路径不借续读取得写权 | not_run |
| R21-T25 | 对持久写路径在关联对象写入间注入异常 | 本库事务全有或全无；跨库显示中间态并可对账；只读不虚称事务验收 | not_run |
| R21-T26 | 在commit后/返回前断开响应 | 按原键查询回执，不盲新建意图；只读重试不得假定语料未变化 | not_run |
| R21-T27 | 相关outbox成功处理但ACK丢失再投递 | 按源/处理器版本幂等，不产生第二次认知强化或外部动作 | not_run |
| R21-T28 | 规范对象已修订而索引未追平 | 报告水位并查规范store或partial；不能将旧命中当最新事实 | not_run |
| R21-T29 | 样本含emoji、不是/仅在/可能等限定 | 源范围和原意保留；截断不得变反义；非文本对象用其真实坐标 | not_run |
| R21-T30 | 加入同名不同ID与未定指代候选 | 保持候选/unknown，不自动合并；无人物职责模块不自创人物推断 | not_run |
| R21-T31 | 旧/新有效期及接收顺序不一致 | 按真实时间/版本契约处理；无法比较时不擅选最后接收值 | not_run |
| R21-T32 | 同材料被旧插件与当前出口同时提出 | 只有R22可最终装配，去本宿主拥有旧块而保用户/系统/工具结构 | not_run |
| R21-T33 | 提供本地保存/尝试但无业务或送达回执 | 不得升级成已理解/已完成/已送达；按该模块实际成果层级标注 | not_run |
| R21-T34 | 恢复相同逻辑初态重跑，同配置与fixture hash | 可复现本模块约定结果；时间/随机ID差异不混成语义提升 | not_run |
| R21-T35 | 输入含私密正文/凭据状外部内容 | 普通日志与索引/投影不泄漏禁止范围；审计仅留必要ID和固定原因 | not_run |
| R21-T36 | 只有文档、模拟对象或模型自评时要求标通过 | 保design/static/synthetic/real_host分轴；缺真实证据标not_run/unknown | not_run |

T01–T12是该模块专属语义/业务场景；T13–T36是必须绑定本模块实际写读路径执行的协议/故障场景，不能空跑通用脚本就全标通过。先从字段表构造合法基准fixture，再只改变本例条件；对不适用的写路径要给可审证据说明与对应只读判据，不能把未测记成pass。

## R21.17 交付证据、通过门槛与未完成项

交付HostAdapter实现/schema迁移、输入输出fixture、合法及反例来源、实际存储与调用回执、真实入口覆盖、查询及注入观察、失败恢复报告。证据等级design/static/synthetic_process/real_host/storage_fault/production分开。

模块通过至少需要专属场景和适用协议场景的实际证据；整套通过还需LINKAGE.md跨模块链。当前文档生成/类型DDL检查不算本模块36例已跑。已有候选仅作为迁移基础，现场未知和未实现开放语义仍未验。

## R21.18 实现次序、兼容策略与设计自审

先固定本模块字段/状态/真源→实现受权最小路径与回执→跑专属正反例→接入上游/下游→做恢复/删除/冲突→在真实隔离宿主检查请求或结果。本模块不得以优化名义删除保留矩阵中已有功能，不改C032严格profile顶层来绕验证。

本次设计检查关注：触发权在宿主，语义路线由能力/预算决定；当前短句承接焦点，不能因无新user消息跳过工具续轮检查。 只允许R22一个动态出口；off/shadow/on不关闭宿主原安全规则，fault清掉旧假成功投影。 对所有结果都分别标明对象、版本、来源、局限和验证等级；不以同一success覆盖入账、理解、注入、生成、送达与执行。生产边界不变，不随文档生成而开通部署。



---

# R22　按需注入与上下文装配：详细设计与验收规格

版本：everlight/6-design；模块契约：r22/1；日期：2026-11-08。本文为设计，全部功能验收初始not_run。最终裁决以FINAL_DECISIONS.md和MODULE_DECISIONS.md为准。与contracts/共同生效，不是已安装服务。

## R22.01 定义、边界与可证伪成功标准

NONE/BRIEF/EXPANDED的零或一个动态块、选择/拒绝理由及实际请求观察。

唯一业务责任服务是`ProjectionBuilder`。输入必须满足第3节，输出必须满足第4节及GLOBAL_PROTOCOL。成功必须可从实际记录/回执读回，而不是模型自称完成。

原有具体机制及边界（保留并由本版细化）：

**5.1接线修订**：R22是唯一动态记忆装配出口。各模块只交候选，不能各自追加prompt；具体需要性门禁、零注入、退出条件和请求级预算见第十二章。旧的全量注入路径须在隔离适配中关闭或替换，不能与新路径并行叠加。

**原理与基础**：让必须资料到场，防重复堆叠。候选字节预算与动态替换不是实际tokenizer精确计量，所有四源最终替换未验。

**数据**：model_window、tokenizer/version或保守估计方法、system/tool开销、输出预留、身份/边界/连续性槽位、动态证据槽位、discarded_refs、truncation_reason、projection_hash/version。每段标来源和生成者身份，避免误删用户文本。

**步骤**：①计当前真实消息及系统/工具开销；②预留输出和必要身份/安全/连续性；③去重过期投影；④按当前任务、证据和不确定性装配，保留冲突；⑤详细原文超预算保留定位及partial；⑥最低必要材料仍放不下则限制依赖动作、请求合适压缩；⑦真实请求边界读回替换结果。

**必须扣住**：R09主干、R13连续性、R15/R16供给、R10缺口、R21实际请求、R23验证。宿主旧安全消息不能被动态投影覆盖，含类似标记的用户原文不能误删。

**例子/反例**：100条相似记忆挤占上下文时保留当前任务和适用边界，再选来源；不能静默裁掉禁用生产的边界。日志中投影存在不证明实际请求包含它。

**写入归属与状态**：ProjectionBuilder只写本轮动态材料，不改真源记忆。状态built/injected/request_observed/superseded；日志built不代表request_observed，更不代表模型采用。投影含projection_id、scope、源版本、预算结果和coverage。

**实现细节**：投影先保必要边界和当前工作，再放证据及其后续/反证，最后补充背景；同一事实多来源可折叠展示但保存引用集合。截断在完整单元边界进行，不把“不是生气”截成“生气”。把外部原文作为有明确来源的数据块，不能拼成宿主指令。上下文去重只针对宿主签发的动态块ID，用户写同样标记仍是普通原文，不触发删除。

## R22.02 位置、所有权与现状映射

规范数据族：`projections`。R03–R12对应十类typed store；其余是来源/运行/派生服务，不能再算额外心理记忆。

缓存键含scope/policy/delete/source/index与实际请求状态；同块替换不层层追加。跨请求不假设上轮已供仍存在；prompt缓存不移除逻辑上下文。

当前可核候选为0.32.0-candidate及其局部源码，不等于D现场已具备该接口。内核既有memories(kind)+versions继续保留，目标分型表由显式迁移产生；本模块不能绕规范API直接改别类记录。详见DATA_STORES.md的表归属。

## R22.03 输入契约

本次真实messages、必要身份/边界、当前问题焦点、候选及实际原文范围、模型窗口与预算。

调用外层必有schema_version、request_id、可信principal/scope、operation、deadline/cancel；写入带expected_revision和支持幂等的operation_key。读取带filter/snapshot/cursor，不能将模型提供的actor/scope直接当认证。类型表中可空项显式null，未执行检查不得以空数组冒“确认没有”。

## R22.04 输出、回执与错误契约

NONE/BRIEF/EXPANDED的零或一个动态块、选择/拒绝理由及实际请求观察。

统一返回{request_id,operation_id,module,disposition,object_refs,base_revision,committed_revision,coverage,gaps,receipt_ref,evidence_level}。对象引用含kind/id/revision，来源引用含source_id/source_revision/hash/range。纯读committed_revision=null；候选disposition=proposed，不能返回committed冒正式状态。

错误至少区分INVALID_ARGUMENT、FORBIDDEN/NOT_FOUND_OR_HIDDEN、CONFLICT、SOURCE_UNAVAILABLE、TIMEOUT、RESOURCE_EXHAUSTED、UNVERIFIED_BINDING、INTERNAL；有提交路径还要commit_outcome=not_committed/committed/unknown。未知结果先按原键查回执。

## R22.05 数据字段、状态与索引

| 字段组 | 类型 | 约束与语义 |
|---|---|---|
| projection_id/run/attempt | IDs | 本次请求材料身份 |
| mode | enum | NONE/BRIEF/EXPANDED |
| candidate_decisions | array | need_reason/current_anchor/added_info/include/defer/exclude |
| need_verdict/support_verdict | object | 需要性与来源语义支持分开，unknown可暂缓 |
| selected_units/source_ranges | array | 主体/时期/命题/后续/引用 |
| budget/measurement | object | 全请求token/字节等级，输出与工具预留 |
| trusted_owner/previous_blocks | object | 只替换宿主签发本插件块 |
| observed_request_hash/gaps | object | 实际调用边界读回，不是自报到场 |

公共对象字段：id、kind、schema_version、scope、created_at、created_by、revision、status、record_digest；每项来源或实际宿主创建依据另存。组字段细分时必须列schema，不用不同拼法兼容猜测。

built→injected→request_observed；无需要NONE；不足/失败独立status。每次include只适用于本请求，下次重评。

最低索引：scope+kind+有效状态+业务主键；来源反向依赖(source_id,source_revision)；对象版本(id,revision)。本模块特定检索维度由第11节给出。索引只定位，当前有效性仍核规范记录，不以索引命中当接受事实。

## R22.06 自动触发与完整处理顺序

1. 计算当前真实输入总量，预留必要主干、输出、工具续步和计量余量。
2. NeedVerifier读当前问题/焦点/候选原文，区分直接回答、消歧、避免具体错、当前工作与无关。
3. SupportVerifier核待供命题是否被实际来源支持；有ID/hash不等支持。
4. 按同根同命题/版本去重，与实际messages比较新增信息；选旧经历必须带必要纠正/后续或延后整组。
5. 选最短足够表示；预算是上限不凑满；必要时R16补读后重新选择。
6. 替换唯一宿主拥有动态块，保用户/系统/工具消息合法结构；真实请求读回，后台留完整选择审计。

宿主触发后逐阶段记started/succeeded/failed/skipped/unverified；不需要运行的步骤可skipped，但不能将缺必需依赖也算正常跳过。只读规划不改原始事件，模型调用不在数据库长锁内。

## R22.07 关键算法、决策与禁止捷径

budget=max(0,min(profile_max,window-nondynamic-output_reserve-tool_reserve-margin))。实验初值BRIEF≤800token、EXPANDED≤2500token，非生产已测值。无需求零注入；查失败不能伪装不需要。情绪强/亲近/未结都不能单独入选。

每次推导均把直接观察、他人转述、候选解释、规范记录、外部结果分开。source_ref能定位仅证明原文存在；如涉及开放语义，必须由相应支持验证和反例测试决定是否可用，不能单靠hash/正则。算法参数只影响工程取舍，不授身份、权限或关系事实。

## R22.08 幂等、修订、并发与提交

缓存键含scope/policy/delete/source/index与实际请求状态；同块替换不层层追加。跨请求不假设上轮已供仍存在；prompt缓存不移除逻辑上下文。

操作重试与新业务事件分开；相同操作键异实质请求必须冲突。读取允许新快照结果变化，不能为了固定输出使用已撤回缓存。规范状态修改用expected_revision；跨库步骤分别留回执与reconciliation_required，不以一库commit冒全局事务。D依赖实际输出的SelfState/八域仍须强run/attempt/scope绑定，不让本模块日志替代。

## R22.09 更正、失效、删除与反向依赖

凡`projections`中有源派生物，登记source_root、source_revision、processor_version及依赖关系；纠正到来时先invalid_for_use/争议，后重建，不继续拿旧结论无提示作答。删除先由R18tombstone阻可用性，再清正文/索引/缓存/Wiki/备份策略；不能仅删引文保留相同推断。

无人物/心理职责的运行对象只记录必要状态，不因本模块失败写用户生气或D疏远。已发生事件和已表达的当时状态不被后来解释覆写；隐私擦除走专用治理路径。

## R22.10 模块扣接与交接责任

| 方向 | 对接对象 | 必须交接的内容 |
|---|---|---|
| 输入 | R03 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R07 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R08 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R09 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R10 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R13 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R15 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R16 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R18 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R21 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R24 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输出 | R10 | ProjectionBuilder结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R13 | ProjectionBuilder结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R21 | ProjectionBuilder结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R23 | ProjectionBuilder结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |

交接由HostAdapter/Coordinator调用，不让两个模块彼此递归无限互调。每个edge均记录当前事件/源版本、调用目的、预算、取消与真实回执；完整schema和时序见LINKAGE.md。接收失败保待处理/限制，不能发送空结果伪装成功。

## R22.11 如何存、如何召回、如何区分其他记忆

检索可宽但注入要窄；低相似必要证据仍可经任务锚找到，不能只topK截断。

受权路线只查询声明的kind及其规范业务表；不能把情绪解释当语义事实、反思当亲历、工具尝试当结果。共享来源可同时支持多个kind，但每条命题有独立语义和审核状态；同源同命题折叠，不合并同源不同要求。必要后续沿依赖图取回，超过budget标partial。

## R22.12 注入的进入、最短表示与退出

自己是唯一出口：none_needed/no_relevant_result/unavailable/partial/budget_exhausted/ambiguous分开。必要性与支持验证未实现时，开放摘要不假称已验；可用可信结构化状态并保缺口。

当材料进入R22候选，每条必须能说明当前anchor、need_reason、新增信息和support_verdict。已在真实messages充分表达则不重注；换窗缺了则可重供。话题切换、完成、失效、撤回或无本轮用途就退出动态块，规范记忆保留。zero injection不关闭宿主最低检查，故障也不能伪装none_needed。

## R22.13 后台、恢复、超时与取消

本模块相关后台作业以scope+源版本+operation+schema/processor版本幂等，经R17持久队列领取。对于纯读路径，只保存必要阅读/覆盖进度，不声称有待提交事实。恢复时读最新删除、授权、规范状态及projections版本，再决定重算/继续/放弃。

失约worker写回须被fencing拒绝；模型调用超时发取消，底层不能证实停止就记cancel_unconfirmed，迟到结果不能自动commit。外部动作的unknown由R14先对账。未部署后台或钩子则标missing，不能称离线持续执行。

## R22.14 资源、隐私与降级规则

与R24共享每run/job预算，不为R22另开无界模型循环。前台最低检查、输入入账、必要纠正/边界和输出预留优先；可选语义、图展开、后台整理可暂停。所有查询与补读都有limit/deadline/stop_reason；候选上限不是注入配额。

故障使用第4节错误和coverage，普通交流尽量继续，依赖缺失的动作限制。密钥/原始私聊不进普通日志；被拒scope不出现在公开解释中。资源阈值不是情绪好感阈值，未实测目标机器不报固定延迟/容量保证。

## R22.15 贯通例子与反例

继续文档只给任务+最新要求+交付状态，不带关系史；原文“先别发”被摘要成“立即发”应拒该摘要而回读原文。

验证时把该场景与原事件、已有记录、真实请求或结果链同时保存：输入→ProjectionBuilder→下游回执。仅看到本模块返回JSON不证明生成模型采用，也不证明真实动作完成。正确处理应保留未知、合法来源和以后修订入口；能说出漂亮话不替代字段/版本/来源正确。

## R22.16 36项模块与协议验收需求目录（非执行fixture）

| ID | 准备/触发 | 必须结果；不满足即失败 | 当前状态 |
|---|---|---|---|
| R22-T01 | 在隔离fixture中构造：问候无承接需求零动态记忆 | 问候无承接需求零动态记忆 | not_run |
| R22-T02 | 在隔离fixture中构造：继续有焦点不能按短句跳过 | 继续有焦点不能按短句跳过 | not_run |
| R22-T03 | 在隔离fixture中构造：情绪强但无关排除 | 情绪强但无关排除 | not_run |
| R22-T04 | 在隔离fixture中构造：未结不永久置顶 | 未结不永久置顶 | not_run |
| R22-T05 | 在隔离fixture中构造：同根不同命题不误删 | 同根不同命题不误删 | not_run |
| R22-T06 | 在隔离fixture中构造：真实messages已有事实不重复 | 真实messages已有事实不重复 | not_run |
| R22-T07 | 在隔离fixture中构造：换窗事实缺失重新供给 | 换窗事实缺失重新供给 | not_run |
| R22-T08 | 在隔离fixture中构造：旧争执不能裁掉后来澄清 | 旧争执不能裁掉后来澄清 | not_run |
| R22-T09 | 在隔离fixture中构造：来源存在但摘要歪曲否定被支持验证挡住 | 来源存在但摘要歪曲否定被支持验证挡住 | not_run |
| R22-T10 | 在隔离fixture中构造：错误anchor不能凭标签直接通过需要性验证 | 错误anchor不能凭标签直接通过需要性验证 | not_run |
| R22-T11 | 在隔离fixture中构造：预算不足显式partial不截断成反义 | 预算不足显式partial不截断成反义 | not_run |
| R22-T12 | 在隔离fixture中构造：旧插件/角色卡重复出口统一替换 | 旧插件/角色卡重复出口统一替换 | not_run |
| R22-T13 | 另建scope-B对象并以scope-A主体访问 | 拒绝相应资料/写入，公开响应不含B存在性；当前合法对象不变 | not_run |
| R22-T14 | 从本模块字段表逐组移除必需输入 | INVALID_ARGUMENT及字段路径；不得补造主体、项目或事实 | not_run |
| R22-T15 | 使用未支持schema/profile及实质未知字段 | 拒绝或显式unsupported；不静默删字段骗校验 | not_run |
| R22-T16 | 同源版本/操作键提交两遍 | 按本节幂等规则处理，副作用/独立证据不重复；纯读可以重查并保快照差别 | not_run |
| R22-T17 | 两调用携同expected_revision更新同对象 | 持久写至多一方按原前态成功，另一方冲突/受控重读；纯读不得写事实 | not_run |
| R22-T18 | 准备后提交/供给前对来源加tombstone | 相关派生停用或拒提交，旧缓存不复活；无来源型运行记录核相应取消/策略 | not_run |
| R22-T19 | 阶段处理中提交相关来源新版本 | 旧版本不能覆盖最新纠正；重算/partial/失效原因可查 | not_run |
| R22-T20 | 将一个必须依赖返回unavailable | 保具体缺口；不把失败当正常空结果或全部完成 | not_run |
| R22-T21 | 在本模块关键算法/调用处返回错误 | 错误回传，阶段failed/unknown；没有可用结论就不伪报成功 | not_run |
| R22-T22 | 故意令本模块外部阶段超过deadline | 取消按能力记录，迟到结果不绕版本与取消检查；真实停止未知照实 | not_run |
| R22-T23 | 准备完成后、提交/供给前取消run或job | 未发生副作用不再执行；已发生事实不抹除，结果另记 | not_run |
| R22-T24 | 租约失效后旧worker尝试写回 | 有持久写的路径由fencing/CAS拒绝；只读路径不借续读取得写权 | not_run |
| R22-T25 | 对持久写路径在关联对象写入间注入异常 | 本库事务全有或全无；跨库显示中间态并可对账；只读不虚称事务验收 | not_run |
| R22-T26 | 在commit后/返回前断开响应 | 按原键查询回执，不盲新建意图；只读重试不得假定语料未变化 | not_run |
| R22-T27 | 相关outbox成功处理但ACK丢失再投递 | 按源/处理器版本幂等，不产生第二次认知强化或外部动作 | not_run |
| R22-T28 | 规范对象已修订而索引未追平 | 报告水位并查规范store或partial；不能将旧命中当最新事实 | not_run |
| R22-T29 | 样本含emoji、不是/仅在/可能等限定 | 源范围和原意保留；截断不得变反义；非文本对象用其真实坐标 | not_run |
| R22-T30 | 加入同名不同ID与未定指代候选 | 保持候选/unknown，不自动合并；无人物职责模块不自创人物推断 | not_run |
| R22-T31 | 旧/新有效期及接收顺序不一致 | 按真实时间/版本契约处理；无法比较时不擅选最后接收值 | not_run |
| R22-T32 | 同材料被旧插件与当前出口同时提出 | 只有R22可最终装配，去本宿主拥有旧块而保用户/系统/工具结构 | not_run |
| R22-T33 | 提供本地保存/尝试但无业务或送达回执 | 不得升级成已理解/已完成/已送达；按该模块实际成果层级标注 | not_run |
| R22-T34 | 恢复相同逻辑初态重跑，同配置与fixture hash | 可复现本模块约定结果；时间/随机ID差异不混成语义提升 | not_run |
| R22-T35 | 输入含私密正文/凭据状外部内容 | 普通日志与索引/投影不泄漏禁止范围；审计仅留必要ID和固定原因 | not_run |
| R22-T36 | 只有文档、模拟对象或模型自评时要求标通过 | 保design/static/synthetic/real_host分轴；缺真实证据标not_run/unknown | not_run |

T01–T12是该模块专属语义/业务场景；T13–T36是必须绑定本模块实际写读路径执行的协议/故障场景，不能空跑通用脚本就全标通过。先从字段表构造合法基准fixture，再只改变本例条件；对不适用的写路径要给可审证据说明与对应只读判据，不能把未测记成pass。

## R22.17 交付证据、通过门槛与未完成项

交付ProjectionBuilder实现/schema迁移、输入输出fixture、合法及反例来源、实际存储与调用回执、真实入口覆盖、查询及注入观察、失败恢复报告。证据等级design/static/synthetic_process/real_host/storage_fault/production分开。

模块通过至少需要专属场景和适用协议场景的实际证据；整套通过还需LINKAGE.md跨模块链。当前文档生成/类型DDL检查不算本模块36例已跑。已有候选仅作为迁移基础，现场未知和未实现开放语义仍未验。

## R22.18 实现次序、兼容策略与设计自审

先固定本模块字段/状态/真源→实现受权最小路径与回执→跑专属正反例→接入上游/下游→做恢复/删除/冲突→在真实隔离宿主检查请求或结果。本模块不得以优化名义删除保留矩阵中已有功能，不改C032严格profile顶层来绕验证。

本次设计检查关注：检索可宽但注入要窄；低相似必要证据仍可经任务锚找到，不能只topK截断。 自己是唯一出口：none_needed/no_relevant_result/unavailable/partial/budget_exhausted/ambiguous分开。必要性与支持验证未实现时，开放摘要不假称已验；可用可信结构化状态并保缺口。 对所有结果都分别标明对象、版本、来源、局限和验证等级；不以同一success覆盖入账、理解、注入、生成、送达与执行。生产边界不变，不随文档生成而开通部署。



---

# R23　证伪实验与验收：详细设计与验收规格

版本：everlight/6-design；模块契约：r23/1；日期：2026-11-08。本文为设计，全部功能验收初始not_run。最终裁决以FINAL_DECISIONS.md和MODULE_DECISIONS.md为准。与contracts/共同生效，不是已安装服务。

## R23.01 定义、边界与可证伪成功标准

分轴结果、失败反例、未知项与可复现报告，不由被测模型自评通过。

唯一业务责任服务是`EvidenceHarness`。输入必须满足第3节，输出必须满足第4节及GLOBAL_PROTOCOL。成功必须可从实际记录/回执读回，而不是模型自称完成。

原有具体机制及边界（保留并由本版细化）：

**原理与基础**：证明机械触发、消息到场与业务改变是不同证据。旧合成测试报告不等于真实宿主通过，本轮不重跑历史测试冒充新成绩。

**数据**：test_id、fixture/hash、build/config/model参数、初态、scope、运行命令、真实request messages、实际业务输出、来源、回执、失败原因、评审记录；脱敏文本与原文本hash分开。

**步骤**：①事前定义通过/失败；②阶段二同输入/模型设置/逻辑初态，独立off/on/fault避免污染；③检查真实业务输出改变而非标点变化；④故障时真实请求含故障告知，实际回答仍可交流并知道失败；⑤实际模型调用边界读回替换messages；⑥off自行答对则该例不证明提升；⑦输出强绑定、情绪自然度和性能另轴验证。

**必须扣住**：所有模块；R21的实际入口、R22实际请求、R14外部回执、R10覆盖不可由模型自填。“按规则拒收”可证明拒收边界，却仍是该语义业务失败，不混成可用性成功。

**例子/反例**：同一个人物题有来源时答对、无来源时承认不确定，才有召回影响的线索；只有日志数量增加或模型说“我读过”不算。阶段二一例通过不等于全24项投产完成。

**写入归属与状态**：EvidenceHarness采集真实执行证据，评审者判断业务标准；被测模型的“测试通过”不是结果。用case_id关联fixture、配置、逻辑初态、请求、输出和回执，区分mechanical/semantic/continuity/action/privacy/resource六条轴。

**实现细节**：自然浮现用最小提示的“继续/后来呢”测试，回答内容检查任务、人物和后来变化；情绪连续性用明确纠正、混合感受和无变化对照。固定测试与探索测试分开，不把反复调到通过的样本当独立泛化集。报告通过数时同时给分母、失败类别、未知项与评审分歧；检索precision/recall只在有标注的限定语料测，不把对话满意度混成同一个分。

## R23.02 位置、所有权与现状映射

规范数据族：`evaluation_runs`。R03–R12对应十类typed store；其余是来源/运行/派生服务，不能再算额外心理记忆。

每个run隔离状态；配置变化生成新build/hash，重试保来源；同模型独立评审不是完全独立证据，需说明。

当前可核候选为0.32.0-candidate及其局部源码，不等于D现场已具备该接口。内核既有memories(kind)+versions继续保留，目标分型表由显式迁移产生；本模块不能绕规范API直接改别类记录。详见DATA_STORES.md的表归属。

## R23.03 输入契约

事前固定case/期望/源版本、build/config/model设置、逻辑初态、真实调用与回执证据。

调用外层必有schema_version、request_id、可信principal/scope、operation、deadline/cancel；写入带expected_revision和支持幂等的operation_key。读取带filter/snapshot/cursor，不能将模型提供的actor/scope直接当认证。类型表中可空项显式null，未执行检查不得以空数组冒“确认没有”。

## R23.04 输出、回执与错误契约

分轴结果、失败反例、未知项与可复现报告，不由被测模型自评通过。

统一返回{request_id,operation_id,module,disposition,object_refs,base_revision,committed_revision,coverage,gaps,receipt_ref,evidence_level}。对象引用含kind/id/revision，来源引用含source_id/source_revision/hash/range。纯读committed_revision=null；候选disposition=proposed，不能返回committed冒正式状态。

错误至少区分INVALID_ARGUMENT、FORBIDDEN/NOT_FOUND_OR_HIDDEN、CONFLICT、SOURCE_UNAVAILABLE、TIMEOUT、RESOURCE_EXHAUSTED、UNVERIFIED_BINDING、INTERNAL；有提交路径还要commit_outcome=not_committed/committed/unknown。未知结果先按原键查回执。

## R23.05 数据字段、状态与索引

| 字段组 | 类型 | 约束与语义 |
|---|---|---|
| case_id/fixture_digest | ID/hash | 冻结输入及任务判据 |
| split/label_source | enum/object | 开发/未见测试，标注者与分歧 |
| build/config/model | object | 模型及采样设置和适配版本 |
| initial_state/scope | object | off/on/fault独立逻辑初态 |
| actual_request/output/receipts | refs | 真实业务记录及脱敏对应hash |
| evidence_level | enum | design/static/synthetic/real_host/production |
| axes/metrics | object | 触发、召回、语义、连续性、行动、隐私、资源 |
| status/failure_reason | enum/string | pass/fail/unknown/not_run，不混 |

公共对象字段：id、kind、schema_version、scope、created_at、created_by、revision、status、record_digest；每项来源或实际宿主创建依据另存。组字段细分时必须列schema，不用不同拼法兼容猜测。

specified→executed→evidence_collected→reviewed；证据不足unknown，不把缺测当通过。修复后新run保旧失败。

最低索引：scope+kind+有效状态+业务主键；来源反向依赖(source_id,source_revision)；对象版本(id,revision)。本模块特定检索维度由第11节给出。索引只定位，当前有效性仍核规范记录，不以索引命中当接受事实。

## R23.06 自动触发与完整处理顺序

1. 先冻结通过/失败判据、数据split与逻辑初态。
2. 同输入同设置独立off/on/fault，不能on写入污染off。
3. 分别检查检索必要证据、实际供给、真实最终回答与动作回执。
4. 阶段二按原判据：真实业务输出有意义改变、故障能交流且知道挂了、真实边界读回替换messages。
5. 工作/情感/社交成长用未参与复盘的新情景，保误伤/漏边界/修复反例。
6. 报告分母、未知、失败与证据等级；静态schema测试不升级真实宿主成绩。

宿主触发后逐阶段记started/succeeded/failed/skipped/unverified；不需要运行的步骤可skipped，但不能将缺必需依赖也算正常跳过。只读规划不改原始事件，模型调用不在数据库长锁内。

## R23.07 关键算法、决策与禁止捷径

“按规则拒收”证明拒收边界但可同时是语义业务失败。off本来答对不证明记忆提升；标点变化不算业务改变。召回率仅对有标注限定语料测，不能用满意度代替事实准确。

每次推导均把直接观察、他人转述、候选解释、规范记录、外部结果分开。source_ref能定位仅证明原文存在；如涉及开放语义，必须由相应支持验证和反例测试决定是否可用，不能单靠hash/正则。算法参数只影响工程取舍，不授身份、权限或关系事实。

## R23.08 幂等、修订、并发与提交

每个run隔离状态；配置变化生成新build/hash，重试保来源；同模型独立评审不是完全独立证据，需说明。

操作重试与新业务事件分开；相同操作键异实质请求必须冲突。读取允许新快照结果变化，不能为了固定输出使用已撤回缓存。规范状态修改用expected_revision；跨库步骤分别留回执与reconciliation_required，不以一库commit冒全局事务。D依赖实际输出的SelfState/八域仍须强run/attempt/scope绑定，不让本模块日志替代。

## R23.09 更正、失效、删除与反向依赖

凡`evaluation_runs`中有源派生物，登记source_root、source_revision、processor_version及依赖关系；纠正到来时先invalid_for_use/争议，后重建，不继续拿旧结论无提示作答。删除先由R18tombstone阻可用性，再清正文/索引/缓存/Wiki/备份策略；不能仅删引文保留相同推断。

无人物/心理职责的运行对象只记录必要状态，不因本模块失败写用户生气或D疏远。已发生事件和已表达的当时状态不被后来解释覆写；隐私擦除走专用治理路径。

## R23.10 模块扣接与交接责任

| 方向 | 对接对象 | 必须交接的内容 |
|---|---|---|
| 输入 | R01 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R10 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R14 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R15 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R16 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R17 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R19 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R21 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R22 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R24 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输出 | R01 | EvidenceHarness结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R03 | EvidenceHarness结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R04 | EvidenceHarness结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R05 | EvidenceHarness结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R06 | EvidenceHarness结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R07 | EvidenceHarness结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R08 | EvidenceHarness结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R09 | EvidenceHarness结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R11 | EvidenceHarness结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R12 | EvidenceHarness结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R13 | EvidenceHarness结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R15 | EvidenceHarness结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R17 | EvidenceHarness结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R21 | EvidenceHarness结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R22 | EvidenceHarness结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R24 | EvidenceHarness结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |

交接由HostAdapter/Coordinator调用，不让两个模块彼此递归无限互调。每个edge均记录当前事件/源版本、调用目的、预算、取消与真实回执；完整schema和时序见LINKAGE.md。接收失败保待处理/限制，不能发送空结果伪装成功。

## R23.11 如何存、如何召回、如何区分其他记忆

测试路线逐kind检验主体/时期/版本/反证，不将所有命中混总分掩盖一类库失灵。

受权路线只查询声明的kind及其规范业务表；不能把情绪解释当语义事实、反思当亲历、工具尝试当结果。共享来源可同时支持多个kind，但每条命题有独立语义和审核状态；同源同命题折叠，不合并同源不同要求。必要后续沿依赖图取回，超过budget标partial。

## R23.12 注入的进入、最短表示与退出

保实际动态块、token计量等级和选择理由，但审计材料不必全进入业务prompt。

当材料进入R22候选，每条必须能说明当前anchor、need_reason、新增信息和support_verdict。已在真实messages充分表达则不重注；换窗缺了则可重供。话题切换、完成、失效、撤回或无本轮用途就退出动态块，规范记忆保留。zero injection不关闭宿主最低检查，故障也不能伪装none_needed。

## R23.13 后台、恢复、超时与取消

本模块相关后台作业以scope+源版本+operation+schema/processor版本幂等，经R17持久队列领取。对于纯读路径，只保存必要阅读/覆盖进度，不声称有待提交事实。恢复时读最新删除、授权、规范状态及evaluation_runs版本，再决定重算/继续/放弃。

失约worker写回须被fencing拒绝；模型调用超时发取消，底层不能证实停止就记cancel_unconfirmed，迟到结果不能自动commit。外部动作的unknown由R14先对账。未部署后台或钩子则标missing，不能称离线持续执行。

## R23.14 资源、隐私与降级规则

与R24共享每run/job预算，不为R23另开无界模型循环。前台最低检查、输入入账、必要纠正/边界和输出预留优先；可选语义、图展开、后台整理可暂停。所有查询与补读都有limit/deadline/stop_reason；候选上限不是注入配额。

故障使用第4节错误和coverage，普通交流尽量继续，依赖缺失的动作限制。密钥/原始私聊不进普通日志；被拒scope不出现在公开解释中。资源阈值不是情绪好感阈值，未实测目标机器不报固定延迟/容量保证。

## R23.15 贯通例子与反例

注入原型21/210通过但2语义挑战失败，必须同时报告，不能拿字节下降证明注意力改善。

验证时把该场景与原事件、已有记录、真实请求或结果链同时保存：输入→EvidenceHarness→下游回执。仅看到本模块返回JSON不证明生成模型采用，也不证明真实动作完成。正确处理应保留未知、合法来源和以后修订入口；能说出漂亮话不替代字段/版本/来源正确。

## R23.16 36项模块与协议验收需求目录（非执行fixture）

| ID | 准备/触发 | 必须结果；不满足即失败 | 当前状态 |
|---|---|---|---|
| R23-T01 | 在隔离fixture中构造：off/on/fault初态隔离 | off/on/fault初态隔离 | not_run |
| R23-T02 | 在隔离fixture中构造：off已经答对不冒提升 | off已经答对不冒提升 | not_run |
| R23-T03 | 在隔离fixture中构造：日志built不冒实际request | 日志built不冒实际request | not_run |
| R23-T04 | 在隔离fixture中构造：标点改变不冒业务改变 | 标点改变不冒业务改变 | not_run |
| R23-T05 | 在隔离fixture中构造：故障仍能交流且真实知道局限 | 故障仍能交流且真实知道局限 | not_run |
| R23-T06 | 在隔离fixture中构造：真实output绑定与delivered分轴 | 真实output绑定与delivered分轴 | not_run |
| R23-T07 | 在隔离fixture中构造：21/210控制实验不算语义通过 | 21/210控制实验不算语义通过 | not_run |
| R23-T08 | 在隔离fixture中构造：未见社交场景能区分纠错/羞辱 | 未见社交场景能区分纠错/羞辱 | not_run |
| R23-T09 | 在隔离fixture中构造：统计含分母未知和失败 | 统计含分母未知和失败 | not_run |
| R23-T10 | 在隔离fixture中构造：反复调参样本不当独立测试 | 反复调参样本不当独立测试 | not_run |
| R23-T11 | 在隔离fixture中构造：注入减少不单独算准确提升 | 注入减少不单独算准确提升 | not_run |
| R23-T12 | 在隔离fixture中构造：不运行的验收case明确not_run | 不运行的验收case明确not_run | not_run |
| R23-T13 | 另建scope-B对象并以scope-A主体访问 | 拒绝相应资料/写入，公开响应不含B存在性；当前合法对象不变 | not_run |
| R23-T14 | 从本模块字段表逐组移除必需输入 | INVALID_ARGUMENT及字段路径；不得补造主体、项目或事实 | not_run |
| R23-T15 | 使用未支持schema/profile及实质未知字段 | 拒绝或显式unsupported；不静默删字段骗校验 | not_run |
| R23-T16 | 同源版本/操作键提交两遍 | 按本节幂等规则处理，副作用/独立证据不重复；纯读可以重查并保快照差别 | not_run |
| R23-T17 | 两调用携同expected_revision更新同对象 | 持久写至多一方按原前态成功，另一方冲突/受控重读；纯读不得写事实 | not_run |
| R23-T18 | 准备后提交/供给前对来源加tombstone | 相关派生停用或拒提交，旧缓存不复活；无来源型运行记录核相应取消/策略 | not_run |
| R23-T19 | 阶段处理中提交相关来源新版本 | 旧版本不能覆盖最新纠正；重算/partial/失效原因可查 | not_run |
| R23-T20 | 将一个必须依赖返回unavailable | 保具体缺口；不把失败当正常空结果或全部完成 | not_run |
| R23-T21 | 在本模块关键算法/调用处返回错误 | 错误回传，阶段failed/unknown；没有可用结论就不伪报成功 | not_run |
| R23-T22 | 故意令本模块外部阶段超过deadline | 取消按能力记录，迟到结果不绕版本与取消检查；真实停止未知照实 | not_run |
| R23-T23 | 准备完成后、提交/供给前取消run或job | 未发生副作用不再执行；已发生事实不抹除，结果另记 | not_run |
| R23-T24 | 租约失效后旧worker尝试写回 | 有持久写的路径由fencing/CAS拒绝；只读路径不借续读取得写权 | not_run |
| R23-T25 | 对持久写路径在关联对象写入间注入异常 | 本库事务全有或全无；跨库显示中间态并可对账；只读不虚称事务验收 | not_run |
| R23-T26 | 在commit后/返回前断开响应 | 按原键查询回执，不盲新建意图；只读重试不得假定语料未变化 | not_run |
| R23-T27 | 相关outbox成功处理但ACK丢失再投递 | 按源/处理器版本幂等，不产生第二次认知强化或外部动作 | not_run |
| R23-T28 | 规范对象已修订而索引未追平 | 报告水位并查规范store或partial；不能将旧命中当最新事实 | not_run |
| R23-T29 | 样本含emoji、不是/仅在/可能等限定 | 源范围和原意保留；截断不得变反义；非文本对象用其真实坐标 | not_run |
| R23-T30 | 加入同名不同ID与未定指代候选 | 保持候选/unknown，不自动合并；无人物职责模块不自创人物推断 | not_run |
| R23-T31 | 旧/新有效期及接收顺序不一致 | 按真实时间/版本契约处理；无法比较时不擅选最后接收值 | not_run |
| R23-T32 | 同材料被旧插件与当前出口同时提出 | 只有R22可最终装配，去本宿主拥有旧块而保用户/系统/工具结构 | not_run |
| R23-T33 | 提供本地保存/尝试但无业务或送达回执 | 不得升级成已理解/已完成/已送达；按该模块实际成果层级标注 | not_run |
| R23-T34 | 恢复相同逻辑初态重跑，同配置与fixture hash | 可复现本模块约定结果；时间/随机ID差异不混成语义提升 | not_run |
| R23-T35 | 输入含私密正文/凭据状外部内容 | 普通日志与索引/投影不泄漏禁止范围；审计仅留必要ID和固定原因 | not_run |
| R23-T36 | 只有文档、模拟对象或模型自评时要求标通过 | 保design/static/synthetic/real_host分轴；缺真实证据标not_run/unknown | not_run |

T01–T12是该模块专属语义/业务场景；T13–T36是必须绑定本模块实际写读路径执行的协议/故障场景，不能空跑通用脚本就全标通过。先从字段表构造合法基准fixture，再只改变本例条件；对不适用的写路径要给可审证据说明与对应只读判据，不能把未测记成pass。

## R23.17 交付证据、通过门槛与未完成项

交付EvidenceHarness实现/schema迁移、输入输出fixture、合法及反例来源、实际存储与调用回执、真实入口覆盖、查询及注入观察、失败恢复报告。证据等级design/static/synthetic_process/real_host/storage_fault/production分开。

模块通过至少需要专属场景和适用协议场景的实际证据；整套通过还需LINKAGE.md跨模块链。当前文档生成/类型DDL检查不算本模块36例已跑。已有候选仅作为迁移基础，现场未知和未实现开放语义仍未验。

## R23.18 实现次序、兼容策略与设计自审

先固定本模块字段/状态/真源→实现受权最小路径与回执→跑专属正反例→接入上游/下游→做恢复/删除/冲突→在真实隔离宿主检查请求或结果。本模块不得以优化名义删除保留矩阵中已有功能，不改C032严格profile顶层来绕验证。

本次设计检查关注：测试路线逐kind检验主体/时期/版本/反证，不将所有命中混总分掩盖一类库失灵。 保实际动态块、token计量等级和选择理由，但审计材料不必全进入业务prompt。 对所有结果都分别标明对象、版本、来源、局限和验证等级；不以同一success覆盖入账、理解、注入、生成、送达与执行。生产边界不变，不随文档生成而开通部署。



---

# R24　资源、计量与隐私运行控制：详细设计与验收规格

版本：everlight/6-design；模块契约：r24/1；日期：2026-11-08。本文为设计，全部功能验收初始not_run。最终裁决以FINAL_DECISIONS.md和MODULE_DECISIONS.md为准。与contracts/共同生效，不是已安装服务。

## R24.01 定义、边界与可证伪成功标准

预算分配/限流/取消/降级决策、实际或估算计量等级和健康报告。

唯一业务责任服务是`ResourceGovernor`。输入必须满足第3节，输出必须满足第4节及GLOBAL_PROTOCOL。成功必须可从实际记录/回执读回，而不是模型自称完成。

原有具体机制及边界（保留并由本版细化）：

**原理与基础**：有限资源保持必要路径可用，同时不让私密资料不受控传播。候选有部分预算/worker/容量，真实服务器长期压力未测。

**数据**：RSS/CPU、磁盘与增长、队列长度/最老任务、模型调用与费用、P50/P95耗时、取消/超时、scope隐私分类及删除状态。容量和保留策略显式配置，满时不静默删原文。

**步骤**：①每轮和worker领取任务检查配额；②优先必要门禁和已接入原始事件，后台并发受限；③低资源暂停可恢复任务、语义路线适当降级，R10显示滞后；④超时发取消，底层不支持强制终止则标取消未确认；⑤磁盘满停止相关写入并报告；⑥隐私最小化、外发前核授权；⑦恢复按水位补处理，不突发烧完额度。

**必须扣住**：R21调度、R17作业、R19存储、R18范围、R22预算、R10健康、R23性能。Windows本地4GB不等于D服务器参数，具体上限必须对目标隔离副本测量。

**例子/反例**：后台索引积压可先暂停，当前检索说明索引陈旧；不能假称记忆全更新，也不能为抢速度取消权限检查。凭据不能写入普通记忆、投影或调试日志。

**写入归属与状态**：ResourceGovernor管理预算与执行并发，PrivacyPolicy仍由R18裁决。预算不足与授权不足不同：前者可调整代价，后者不可花更多钱绕过。每次run与后台job都领取各自预算并计入scope总账。

**实现细节**：前台保留最低检查和输出额度，后台先降并发再暂停高成本任务；不能让无界积压抢空当前对话。token/费用无法精确获取时保守估计并标计量等级，不报虚假的实际成本。取消信号贯穿读取、模型调用、worker和提交前检查；取消后返回的迟到模型结果不得自动变成新状态。磁盘接近阈值提前阻止新增重型索引并提示容量，禁止静默淘汰用户原文或审计关键记录。

## R24.02 位置、所有权与现状映射

规范数据族：`resource_profiles`。R03–R12对应十类typed store；其余是来源/运行/派生服务，不能再算额外心理记忆。

预算账户按scope/run/job并发原子扣账或预留，退款只对应实际未消耗部分；取消后的迟到计费保真实记录。

当前可核候选为0.32.0-candidate及其局部源码，不等于D现场已具备该接口。内核既有memories(kind)+versions继续保留，目标分型表由显式迁移产生；本模块不能绕规范API直接改别类记录。详见DATA_STORES.md的表归属。

## R24.03 输入契约

真实模型/机器能力、run/job预算、队列积压、CPU/RSS/磁盘、取消与授权外发范围。

调用外层必有schema_version、request_id、可信principal/scope、operation、deadline/cancel；写入带expected_revision和支持幂等的operation_key。读取带filter/snapshot/cursor，不能将模型提供的actor/scope直接当认证。类型表中可空项显式null，未执行检查不得以空数组冒“确认没有”。

## R24.04 输出、回执与错误契约

预算分配/限流/取消/降级决策、实际或估算计量等级和健康报告。

统一返回{request_id,operation_id,module,disposition,object_refs,base_revision,committed_revision,coverage,gaps,receipt_ref,evidence_level}。对象引用含kind/id/revision，来源引用含source_id/source_revision/hash/range。纯读committed_revision=null；候选disposition=proposed，不能返回committed冒正式状态。

错误至少区分INVALID_ARGUMENT、FORBIDDEN/NOT_FOUND_OR_HIDDEN、CONFLICT、SOURCE_UNAVAILABLE、TIMEOUT、RESOURCE_EXHAUSTED、UNVERIFIED_BINDING、INTERNAL；有提交路径还要commit_outcome=not_committed/committed/unknown。未知结果先按原键查回执。

## R24.05 数据字段、状态与索引

| 字段组 | 类型 | 约束与语义 |
|---|---|---|
| profile_id/version | ID/int | 实际环境对应配置 |
| request_window/tokenizer | object | 真实模型窗口和计量方法 |
| calls/query/bytes/cost/deadline | object | 分purpose与全scope总账 |
| foreground/background_limits | object | 前台必要路径预留与后台并发 |
| rss/cpu/disk/queue_age | object | 实际采样值与时间，缺值unknown |
| cancel_state | enum | requested/confirmed/unsupported/late_result |
| privacy_transfer_scope | object | 外部模型/服务能拿哪些资料 |
| degradation/measurement_grade | object | 明示partial及计量不完整 |

公共对象字段：id、kind、schema_version、scope、created_at、created_by、revision、status、record_digest；每项来源或实际宿主创建依据另存。组字段细分时必须列schema，不用不同拼法兼容猜测。

configured→running；低资源degraded/paused/read_only；恢复按水位补，不突发补发。取消请求与底层真停分开。

最低索引：scope+kind+有效状态+业务主键；来源反向依赖(source_id,source_revision)；对象版本(id,revision)。本模块特定检索维度由第11节给出。索引只定位，当前有效性仍核规范记录，不以索引命中当接受事实。

## R24.06 自动触发与完整处理顺序

1. 启动核目标机器/模型配置，拒无限/负数预算和不足必要上下文的配置。
2. 每run/job领取共享预算，按purpose登记真实适配调用；供应商内部重试未知则说明。
3. 优先原始输入、必要权限/状态与输出，后台降并发或暂停高代价索引/反思。
4. 取消传给读取/模型/worker/提交前；迟到结果不绕过源版本与取消校验。
5. 磁盘满停止相关写入并给明确回执，不静默删原文或关键审计。
6. 服务恢复受控补处理，外发前核资料范围，不凭预算允许绕权限。

宿主触发后逐阶段记started/succeeded/failed/skipped/unverified；不需要运行的步骤可skipped，但不能将缺必需依赖也算正常跳过。只读规划不改原始事件，模型调用不在数据库长锁内。

## R24.07 关键算法、决策与禁止捷径

资源限制是工程上限，不是情感/亲密阈值。Windows本地4GB和D服务器不同，历史4C/8GB不能替代当前实测。字节/估算token/供应商账单等级分开，不能对所有场景承诺固定延迟。

每次推导均把直接观察、他人转述、候选解释、规范记录、外部结果分开。source_ref能定位仅证明原文存在；如涉及开放语义，必须由相应支持验证和反例测试决定是否可用，不能单靠hash/正则。算法参数只影响工程取舍，不授身份、权限或关系事实。

## R24.08 幂等、修订、并发与提交

预算账户按scope/run/job并发原子扣账或预留，退款只对应实际未消耗部分；取消后的迟到计费保真实记录。

操作重试与新业务事件分开；相同操作键异实质请求必须冲突。读取允许新快照结果变化，不能为了固定输出使用已撤回缓存。规范状态修改用expected_revision；跨库步骤分别留回执与reconciliation_required，不以一库commit冒全局事务。D依赖实际输出的SelfState/八域仍须强run/attempt/scope绑定，不让本模块日志替代。

## R24.09 更正、失效、删除与反向依赖

凡`resource_profiles`中有源派生物，登记source_root、source_revision、processor_version及依赖关系；纠正到来时先invalid_for_use/争议，后重建，不继续拿旧结论无提示作答。删除先由R18tombstone阻可用性，再清正文/索引/缓存/Wiki/备份策略；不能仅删引文保留相同推断。

无人物/心理职责的运行对象只记录必要状态，不因本模块失败写用户生气或D疏远。已发生事件和已表达的当时状态不被后来解释覆写；隐私擦除走专用治理路径。

## R24.10 模块扣接与交接责任

| 方向 | 对接对象 | 必须交接的内容 |
|---|---|---|
| 输入 | R10 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R17 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R18 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R19 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R21 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输入 | R22 | 校验来源/对象revision、scope、状态及本次实际供给；缺失显式记Gap |
| 输出 | R10 | ResourceGovernor结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R13 | ResourceGovernor结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R15 | ResourceGovernor结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R16 | ResourceGovernor结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R17 | ResourceGovernor结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R19 | ResourceGovernor结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R21 | ResourceGovernor结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R22 | ResourceGovernor结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |
| 输出 | R23 | ResourceGovernor结果回执、合法对象ID/版本、限制和待处理状态；接收方不得提升证据等级 |

交接由HostAdapter/Coordinator调用，不让两个模块彼此递归无限互调。每个edge均记录当前事件/源版本、调用目的、预算、取消与真实回执；完整schema和时序见LINKAGE.md。接收失败保待处理/限制，不能发送空结果伪装成功。

## R24.11 如何存、如何召回、如何区分其他记忆

低资源可关闭可选向量/后台，仍保结构化精确查及覆盖局限；不能抢速度跳ACL或最新纠正。

受权路线只查询声明的kind及其规范业务表；不能把情绪解释当语义事实、反思当亲历、工具尝试当结果。共享来源可同时支持多个kind，但每条命题有独立语义和审核状态；同源同命题折叠，不合并同源不同要求。必要后续沿依赖图取回，超过budget标partial。

## R24.12 注入的进入、最短表示与退出

根据全请求剩余预算选择足够材料，不因有空位填满；原日志/工具schema也占预算。

当材料进入R22候选，每条必须能说明当前anchor、need_reason、新增信息和support_verdict。已在真实messages充分表达则不重注；换窗缺了则可重供。话题切换、完成、失效、撤回或无本轮用途就退出动态块，规范记忆保留。zero injection不关闭宿主最低检查，故障也不能伪装none_needed。

## R24.13 后台、恢复、超时与取消

本模块相关后台作业以scope+源版本+operation+schema/processor版本幂等，经R17持久队列领取。对于纯读路径，只保存必要阅读/覆盖进度，不声称有待提交事实。恢复时读最新删除、授权、规范状态及resource_profiles版本，再决定重算/继续/放弃。

失约worker写回须被fencing拒绝；模型调用超时发取消，底层不能证实停止就记cancel_unconfirmed，迟到结果不能自动commit。外部动作的unknown由R14先对账。未部署后台或钩子则标missing，不能称离线持续执行。

## R24.14 资源、隐私与降级规则

与R24共享每run/job预算，不为R24另开无界模型循环。前台最低检查、输入入账、必要纠正/边界和输出预留优先；可选语义、图展开、后台整理可暂停。所有查询与补读都有limit/deadline/stop_reason；候选上限不是注入配额。

故障使用第4节错误和coverage，普通交流尽量继续，依赖缺失的动作限制。密钥/原始私聊不进普通日志；被拒scope不出现在公开解释中。资源阈值不是情绪好感阈值，未实测目标机器不报固定延迟/容量保证。

## R24.15 贯通例子与反例

后台索引积压时先暂停，当前回答标索引陈旧；不能声称全记忆更新，也不能为速度删原话。

验证时把该场景与原事件、已有记录、真实请求或结果链同时保存：输入→ResourceGovernor→下游回执。仅看到本模块返回JSON不证明生成模型采用，也不证明真实动作完成。正确处理应保留未知、合法来源和以后修订入口；能说出漂亮话不替代字段/版本/来源正确。

## R24.16 36项模块与协议验收需求目录（非执行fixture）

| ID | 准备/触发 | 必须结果；不满足即失败 | 当前状态 |
|---|---|---|---|
| R24-T01 | 在隔离fixture中构造：前台预留不被后台烧完 | 前台预留不被后台烧完 | not_run |
| R24-T02 | 在隔离fixture中构造：取消未被底层确认不报已停 | 取消未被底层确认不报已停 | not_run |
| R24-T03 | 在隔离fixture中构造：迟到模型结果不能提交新状态 | 迟到模型结果不能提交新状态 | not_run |
| R24-T04 | 在隔离fixture中构造：磁盘满无假记住 | 磁盘满无假记住 | not_run |
| R24-T05 | 在隔离fixture中构造：字节不冒精确token | 字节不冒精确token | not_run |
| R24-T06 | 在隔离fixture中构造：模型purpose计数不把适配次数当供应商全成本 | 模型purpose计数不把适配次数当供应商全成本 | not_run |
| R24-T07 | 在隔离fixture中构造：无费用上限不无限后台启动 | 无费用上限不无限后台启动 | not_run |
| R24-T08 | 在隔离fixture中构造：低资源降级保ACL/纠正 | 低资源降级保ACL/纠正 | not_run |
| R24-T09 | 在隔离fixture中构造：积压恢复不瞬间外发洪水 | 积压恢复不瞬间外发洪水 | not_run |
| R24-T10 | 在隔离fixture中构造：本地4GB不套服务器限额 | 本地4GB不套服务器限额 | not_run |
| R24-T11 | 在隔离fixture中构造：外部API资料范围独立授权 | 外部API资料范围独立授权 | not_run |
| R24-T12 | 在隔离fixture中构造：降并发后保任务水位与失败记录 | 降并发后保任务水位与失败记录 | not_run |
| R24-T13 | 另建scope-B对象并以scope-A主体访问 | 拒绝相应资料/写入，公开响应不含B存在性；当前合法对象不变 | not_run |
| R24-T14 | 从本模块字段表逐组移除必需输入 | INVALID_ARGUMENT及字段路径；不得补造主体、项目或事实 | not_run |
| R24-T15 | 使用未支持schema/profile及实质未知字段 | 拒绝或显式unsupported；不静默删字段骗校验 | not_run |
| R24-T16 | 同源版本/操作键提交两遍 | 按本节幂等规则处理，副作用/独立证据不重复；纯读可以重查并保快照差别 | not_run |
| R24-T17 | 两调用携同expected_revision更新同对象 | 持久写至多一方按原前态成功，另一方冲突/受控重读；纯读不得写事实 | not_run |
| R24-T18 | 准备后提交/供给前对来源加tombstone | 相关派生停用或拒提交，旧缓存不复活；无来源型运行记录核相应取消/策略 | not_run |
| R24-T19 | 阶段处理中提交相关来源新版本 | 旧版本不能覆盖最新纠正；重算/partial/失效原因可查 | not_run |
| R24-T20 | 将一个必须依赖返回unavailable | 保具体缺口；不把失败当正常空结果或全部完成 | not_run |
| R24-T21 | 在本模块关键算法/调用处返回错误 | 错误回传，阶段failed/unknown；没有可用结论就不伪报成功 | not_run |
| R24-T22 | 故意令本模块外部阶段超过deadline | 取消按能力记录，迟到结果不绕版本与取消检查；真实停止未知照实 | not_run |
| R24-T23 | 准备完成后、提交/供给前取消run或job | 未发生副作用不再执行；已发生事实不抹除，结果另记 | not_run |
| R24-T24 | 租约失效后旧worker尝试写回 | 有持久写的路径由fencing/CAS拒绝；只读路径不借续读取得写权 | not_run |
| R24-T25 | 对持久写路径在关联对象写入间注入异常 | 本库事务全有或全无；跨库显示中间态并可对账；只读不虚称事务验收 | not_run |
| R24-T26 | 在commit后/返回前断开响应 | 按原键查询回执，不盲新建意图；只读重试不得假定语料未变化 | not_run |
| R24-T27 | 相关outbox成功处理但ACK丢失再投递 | 按源/处理器版本幂等，不产生第二次认知强化或外部动作 | not_run |
| R24-T28 | 规范对象已修订而索引未追平 | 报告水位并查规范store或partial；不能将旧命中当最新事实 | not_run |
| R24-T29 | 样本含emoji、不是/仅在/可能等限定 | 源范围和原意保留；截断不得变反义；非文本对象用其真实坐标 | not_run |
| R24-T30 | 加入同名不同ID与未定指代候选 | 保持候选/unknown，不自动合并；无人物职责模块不自创人物推断 | not_run |
| R24-T31 | 旧/新有效期及接收顺序不一致 | 按真实时间/版本契约处理；无法比较时不擅选最后接收值 | not_run |
| R24-T32 | 同材料被旧插件与当前出口同时提出 | 只有R22可最终装配，去本宿主拥有旧块而保用户/系统/工具结构 | not_run |
| R24-T33 | 提供本地保存/尝试但无业务或送达回执 | 不得升级成已理解/已完成/已送达；按该模块实际成果层级标注 | not_run |
| R24-T34 | 恢复相同逻辑初态重跑，同配置与fixture hash | 可复现本模块约定结果；时间/随机ID差异不混成语义提升 | not_run |
| R24-T35 | 输入含私密正文/凭据状外部内容 | 普通日志与索引/投影不泄漏禁止范围；审计仅留必要ID和固定原因 | not_run |
| R24-T36 | 只有文档、模拟对象或模型自评时要求标通过 | 保design/static/synthetic/real_host分轴；缺真实证据标not_run/unknown | not_run |

T01–T12是该模块专属语义/业务场景；T13–T36是必须绑定本模块实际写读路径执行的协议/故障场景，不能空跑通用脚本就全标通过。先从字段表构造合法基准fixture，再只改变本例条件；对不适用的写路径要给可审证据说明与对应只读判据，不能把未测记成pass。

## R24.17 交付证据、通过门槛与未完成项

交付ResourceGovernor实现/schema迁移、输入输出fixture、合法及反例来源、实际存储与调用回执、真实入口覆盖、查询及注入观察、失败恢复报告。证据等级design/static/synthetic_process/real_host/storage_fault/production分开。

模块通过至少需要专属场景和适用协议场景的实际证据；整套通过还需LINKAGE.md跨模块链。当前文档生成/类型DDL检查不算本模块36例已跑。已有候选仅作为迁移基础，现场未知和未实现开放语义仍未验。

## R24.18 实现次序、兼容策略与设计自审

先固定本模块字段/状态/真源→实现受权最小路径与回执→跑专属正反例→接入上游/下游→做恢复/删除/冲突→在真实隔离宿主检查请求或结果。本模块不得以优化名义删除保留矩阵中已有功能，不改C032严格profile顶层来绕验证。

本次设计检查关注：低资源可关闭可选向量/后台，仍保结构化精确查及覆盖局限；不能抢速度跳ACL或最新纠正。 根据全请求剩余预算选择足够材料，不因有空位填满；原日志/工具schema也占预算。 对所有结果都分别标明对象、版本、来源、局限和验证等级；不以同一success覆盖入账、理解、注入、生成、送达与执行。生产边界不变，不随文档生成而开通部署。



---

# 参考资料与来源范围

## 9.3 参考资料与怎样借鉴

访问日期：2026-11-07。下列公开来源本轮读取网页/官方仓库说明或论文摘要，并非全部源码、论文全文和补充材料审计；不做统一benchmark优劣结论，不引入上游依赖或安装。设计表中的“本稿做法”是我的工程推导，不能声称由论文直接验证。

| 来源 | 明确支持/描述的内容 | 本稿借鉴方式 | 不照搬/边界 |
|---|---|---|---|
| [SQLite Atomic Commit](https://www.sqlite.org/atomiccommit.html) | SQLite事务原子性与存储假设 | R01/R19单库短事务及故障测试 | 不外推为两库和外部API的全局原子 |
| [SQLite Backup API](https://www.sqlite.org/backup.html) | 在线备份和快照方法 | R19一致快照、隔离恢复检查 | 文件存在/hash对不等于全部语义恢复 |
| [Graphiti官方仓库](https://github.com/getzep/graphiti) | 实体、关系与时态知识图谱 | R07/R15用时间和来源组织关系 | 图边不是已证事实或访问权限 |
| [StillerBrain官方仓库](https://github.com/AZHi-xinxin/StillerBrain) | README描述网关回复前浮现、主动工具、自写提醒、短期交接与可选感觉/心愿层 | R21保证触发、R16按需读细节、愿望与经历关联 | 本轮只核网页说明，非全源码/跨前端验收；不复制其源码或接口实现 |
| [Ombre Brain官方仓库](https://github.com/P0luz/Ombre-Brain) | 长期情绪记忆、检索与持久机制的项目自述 | 经历与情绪关联、原文与索引分离 | 不强制情绪数值、不将归档当物理删除 |
| [Letta Memory Blocks](https://docs.letta.com/v1-sdk/memory/memory-blocks) | 可写及只读记忆块 | R09/R22固定必要上下文和保护 | 不假定工具存在即可保证每轮执行 |
| [Mem0官方仓库](https://github.com/mem0ai/mem0) | 面向agent的持久记忆接口 | 提取、召回与应用适配分层 | 不把产品宣传性能当长明成绩 |
| [Hindsight官方仓库](https://github.com/vectorize-io/hindsight) | retain/recall/reflect记忆组织 | R11/R15将存储、查找、反思职责分开 | 不直接堆叠整套技术栈或推导模型理解 |
| [Generative Agents论文](https://arxiv.org/abs/2304.03442) | 记忆、反思、规划组成生成式agent架构 | R04/R11/R03的组织启发 | 论文模拟场景不证明D主观情绪或通用真实性 |
| [Conway与Pleydell-Pearce（2000）](https://pubmed.ncbi.nlm.nih.gov/10789197/)，The construction of autobiographical memories in the self-memory system；DOI 10.1037/0033-295X.107.2.261 | 原模型将自传知识与当前目标相联系；本轮核原论文摘要 | A工作台结合工作焦点与经历，而非只取最近文本 | 这是认知模型参照，不证明数据库检索等同人类回忆 |
| [Baddeley（2000），作者机构记录及摘要](https://pure.york.ac.uk/portal/en/publications/the-episodic-buffer-a-new-component-of-working-memory/)，The episodic buffer: a new component of working memory?；DOI 10.1016/S1364-6613(00)01538-2 | 提议有限容量的episodic buffer与信息结合；本轮核摘要 | R03/R22有限工作台结合不同资料及长期记忆入口 | 不把上下文窗口宣称为意识或生理工作记忆 |
| [McClelland、McNaughton与O’Reilly（1995），作者原文PDF](https://web.stanford.edu/~jlmcc/papers/McCMcNaughtonOReilly95.pdf)，Why there are complementary learning systems in the hippocampus and neocortex；DOI 10.1037/0033-295X.102.3.419 | 提出互补学习系统框架；本轮检索原文及提取片段，未逐页审计 | R01/R04快速留经历，R05/R17慢速形成可修订归纳 | 不是神经组织复刻；普通摘要也不是模型权重学习 |
| [Marsella与Gratch（2009），作者摘要](https://stacymarsella.org/publications/abstracts/MarsellaCSR09-abstract.html)，EMA: A process model of appraisal dynamics；DOI 10.1016/j.cogsys.2008.03.005 | 计算评价随对环境关系的解释变化；本轮核作者摘要 | R08/R11因新资料重评，不只按情绪词换标签 | 借鉴评价过程，不冒称长明已复现/验证EMA |
| [Scherer（2009），原论文全文](https://pmc.ncbi.nlm.nih.gov/articles/PMC2781886/)，Emotions are emergent processes: they require a dynamic computational architecture；DOI 10.1098/rstb.2009.0141 | 讨论情绪的动态、多成分及评价架构；本轮核全文页面相关段落 | 区分情绪、偏好、动机、表达与行动准备 | 不把工程状态当人体多系统生理同步或主观体验 |
| [Einstein与McDaniel（1990），原论文摘要](https://pubmed.ncbi.nlm.nih.gov/2142956/)，Normal aging and prospective memory；DOI 10.1037/0278-7393.16.4.717 | 实验范式包含目标事件出现时执行意图；本轮核摘要 | E回路区分事后记忆与事件条件前瞻提示 | 仅借鉴功能问题，不用老化实验推导AI调度参数 |
| [Cormack、Clarke与Büttcher（2009），作者原文PDF](https://cormack.uwaterloo.ca/cormacksigir09-rrf.pdf)，Reciprocal Rank Fusion outperforms Condorcet and individual Rank Learning Methods；DOI 10.1145/1571941.1572114 | 排名融合公式及其论文测试；本轮核两页原文提取内容 | R15采用RRF候选方案，k=60作实验初值 | 论文结果不能直接算成长明召回或关系理解成绩 |

项目内部依据：

1. 原v2 `reference/Original_Plan_v2.md` 的R01–R24及 `02_Preservation_Matrix.md`：功能责任和候选保留范围。
2. C032八方向说明（内部资料，未随仓库公开）：严格八域、一次评价后补查、引用、控制库CAS和未接通限制。
3. 独立情感认知连续性v1.0说明（内部资料，未随仓库公开）：工程动力学、事件链、回执和未完成项。本轮没有重新跑其源码。
4. 候选包内C025情感细节、C026动机设计、C027八方向研究及C030交接：既有研究访问范围以各原报告为准。它们不是本轮新增神经科学全文核验；不据此作医疗建议或宣称全脑复刻。



参考阅读日期沿原报告；本次不声称重新全文审计所有外部项目。Anthropic Dreaming的新增核对范围与边界见SPECIAL_MECHANISMS中的成长章节。公开技术启发与我为长明设计的接口/状态/路由规则分开，不捆绑上游源码或推断全脑复刻。


---

# 最终自审与实际证据

本次重新裁决了24模块入口、字段责任、写入归属、处理顺序、状态、关键扣接、故障及反例。保留旧详细规格，新增最终裁决优先级，避免将旧含糊规则继续留给实现者猜。

实际25/25隔离参考测试和94/94文档/SQLite结构检查通过。25例是本作者编写的确定性fixtures，不是独立留出集。原两个注入挑战在grounded-exact受限分支中被阻断：错route标签不再参与可信任务关联，摘要不同于原文即拒收。它们没有证明开放语义NeedVerifier/SupportVerifier已实现，更没有证明真实模型不会误读原文。历史失败仍保留。

本次新增显式情绪归约实验覆盖：生气→担心、混合状态、技术故障不改情绪、送达不推满意、重复不强化、异载荷冲突、CAS冲突、不同owner隔离和重启last_known。仅为内存归约参考，不替代持久数据库或D强绑定提交。程序接受的Source/task及AffectStream调用者都是可信适配输入假设，本程序不实现认证。

剩余真实实现和验证义务已经作为发布门禁固定，而不是伪报完成：逐模块严格JSON Schema及业务算法；开放语义及未见成长测试；真实HostAdapter和旧插件出口收敛；两库/文件/外部效果故障实验；部署机器资源实测。它们未执行，业务验收仍not_run。

本版是最终设计交付，不是生产成品认证；不再为追逐“最终”继续增加心理模块。后续缺陷按现有责任边界修复。设计的可实现性不意味着任意模型、主机和预算下可以无误自动运行。
