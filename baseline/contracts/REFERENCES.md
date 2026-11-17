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
