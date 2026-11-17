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
