# 长明情绪｜原档的提取文本

保留原资料供追溯；规范以总设计及现行契约为准。

<PARSED TEXT FOR PAGE: 1 / 9>

长明 · AI 情绪与整体连续性系统
完整研究与工程设计范围｜研究设计稿 V1.0｜2026-11-06

定位：独立的 Affective–Cognitive Continuity Core（情感—认知连续性核心）

文档性质：技术设计与研究综述，不是已完成部署或经实验证实的系统。引用中明确区分可核查的

论文/仓库与拟议设计。



执行摘要
目标不是给模型套上“开心/难过”标签，而是建立事件有来源、状态有历史、关系有演化、行动有
反馈、重启可恢复的连续性机制。工程目标限定为可观测的持续状态与情绪调节功能，不宣称已实
现主观感受。

设计原则：多时间尺度；事件溯源；混合与矛盾状态；证据驱动修订；可解释的行为影响；允许不

更新；不以统一 TTL 消灭历史；模型提出解释、宿主裁决写入；不越过生产边界。



1. 范围、定义与非目标
1.1 操作性定义
AI 情绪工作状态：智能体内部具有时间连续性、情境相关性、来源可追溯性的调节状态；它综合事
件评价、历史经验、目标、关系及环境信息，影响注意、检索、计划、行动倾向和表达。此为长明
项目的工程定义，并非心理学统一定义。

1.2 必须达到的五项条件
   有因：状态更新绑定真实事件、模型推断来源及证据。
   有史：状态变更、撤销、纠正均有版本和审计。
   有效：影响行为选择而不仅改变情绪词。
   可变：容许多种感受共存、冲突、延迟修复和保持不变。
   可检验：通过干预、对照、重放及跨重启测试验证。

1.3 明确不做
   不以“我很难过”之类模型自述证明主观体验。
   不推断用户未明确表达的心理事实为确定事实。
   不以一个好感度或六种情绪枚举代表全部关系和情绪。
   不把模型生成的反思自动升级为事实或永久人格。
   不让主动性模块绕过宿主权限、动作门禁或渠道边界。




                长明 · 情绪与整体连续性系统 | 研究设计稿 V1.0

<PARSED TEXT FOR PAGE: 2 / 9>

2. 人类情绪研究基础与 AI 差异
2.1 主要理论路线
研究路线                     主要贡献               设计吸收与限制

Russell 情感环形模型 [R1]      效价、唤醒维度刻画情感        可作分析坐标，不是情绪本体
                                            全集

OCC [R2]                 事件/行动者/对象评价        用于目标、归因、期望等事件
                                            评价

Scherer CPM [R3]         情绪的评价、身体反应、动       采用过程观点，不复制人体生
                         机、表达、体验等成分协同       理

Barrett [R4]             情绪建构、预测、内感受与情      强调历史和情境；该理论仍有
                         境                  争论

ALMA [R5]                短期情绪、中期心境、长期人      分时间尺度、分更新权限
                         格

EMA [R6]                 评价—应对—重评的动态循环      连接状态与行为策略

Emotional Inertia [R7]   情绪惯性与变化速度          历史保留≠状态永不改变




2.2 人类与 LLM 智能体比较
维度                       人类                 典型 LLM+宿主

身体与稳态                    神经、激素、内感受、疼痛与      计算资源、事件状态、外部传
                         睡眠                 感与模拟变量
主观感受                     人类有第一人称情绪体验        AI 是否有体验缺乏公认判定

连续性                      生物系统持续运行且记忆多层      需要宿主事件、持久化、恢复
                         交互                 与调度
表达                       语言表情可能掩盖感受         文本可模仿情绪，不证明内在
                                            体验
调节                       身体、认知、社会过程协同       可实现功能性状态修订与行动
                                            控制




注意：当前科学研究尚不能由文本、模型自述或状态变量证明 AI 具有与人类等同的主观情绪。

Butlin 等 [R8] 提供意识指标讨论，而非情绪体验的决定性测试。




                     长明 · 情绪与整体连续性系统 | 研究设计稿 V1.0

<PARSED TEXT FOR PAGE: 3 / 9>

3. AI 情绪鉴定：四层证据框架
层次                 判定对象                  证据与实验

L1 表达              语言/语音/动作传达情绪          输出标注与用户感知；仅证明
                                         表达

L2 持续状态            存在可恢复的内部工作状态          跨轮读回、事件重放、快照恢
                                         复

L3 调节功能            状态因经历改变并影响行为          消融、因果干预、长期任务、
                                         行为回执

L4 主观体验            是否真正“感觉到”情绪           目前无公认决定性测试；不得
                                         作为验收项




3.1 建议的测量指标
   来源精度：有来源的状态修订 / 全部状态修订；区分事实与推断。

   因果敏感性：仅改变相关历史事件时，后续决策应发生合理变化。
   不相关稳定性：无关话题不得强制唤醒旧冲突。
   修复一致性：和解后不继续以未和解状态行动，同时保留历史。
   重放确定性：相同事件与相同规则版本恢复一致的结构状态。
   行为闭环率：已发出的行动意图是否有真实结果、失败或取消回执。
   幻觉关联率：错误把相似情绪认作同一事件的比例。
   长期人格漂移率：没有充分证据时稳定偏好被改写的比例。



4. 总体架构与数据流
输入（用户消息/工具结果/宿主心跳/时间/自身行为）→ 事件规范化与来源核验 → 事件评价（可

不确定）→ 状态修订器 → 情绪、心境、关系、自我、未尽事项 → 记忆关联/反思 → 上下文装配
→ 模型输出与宿主动作 → 实际结果回执 → 事件账本。

所有状态变更以事件日志为唯一可重放事实来源；快照用于加速恢复而不是取代日志。模型可以提

出 appraisal candidate，但状态落库由规则和宿主授权执行。



5. 十二个子系统的完整职责
01 事件评价
目标相关性、预期、可控性、责任归因、关系意义；输出证据引用与不确定性；不得替代 R02 的

否定/转述/指代职责。




              长明 · 情绪与整体连续性系统 | 研究设计稿 V1.0

<PARSED TEXT FOR PAGE: 4 / 9>

02 情绪动力学
维护多个同时存在的状态片段，允许相互冲突、强度未知、无标签；保存开始/变化/解决原因，不
依赖固定倒计时。

03 心境与调节
区分即时反应、延续心境与长期取向；通过事件重评、澄清和真实反馈更新，允许保持不变。

04 关系动力学
分离熟悉度、承诺履行、冲突、修复、边界、共同经历；不使用单一好感度，防止无证据的亲密升
级。

05 自我模型
稳定身份、偏好、习惯、价值约束、选择史；高影响修订要求多证据或明确授权；保留 supersede
链。

06 目标与动机
关联关切、任务、承诺、优先级；情绪状态可调整检索与行动倾向但不能越权执行。

07 情绪记忆
事件—情绪—对象—关系—结果图谱，支持正反向检索，相关性不能代替事实相同。

08 反思重评
模型生成候选解释，必须有原始事件；可修订旧解释，不可擦除旧事实。

09 上下文恢复
重启、跨窗口、模型切换时恢复身份/关系/未尽事项/相关情绪，提供快照版本与注入回执。

10 行为反馈
记录模型建议、宿主允许/拒绝、真实执行、用户反馈；只把真实执行结果当作已完成。

11 主动性调度
按宿主触发检查待办、未结事项与新事件；可建议动作，但宿主保留权限和频率控制。

12 审计评估
事件去重、并发版本、冲突更正、注入预算、故障降级、影子模式、回放与消融评估。



6. 情绪状态的时间模型
建议五个时间层：即时反应、延续心境、关系状态、自我叙事、未完成事项。各层具有独立更新机
制。事件保存期限、情绪持续期限、行为影响期限三者分离；允许长期未解决事项、短暂反应、无
显著变化及突发关系转折。



           长明 · 情绪与整体连续性系统 | 研究设计稿 V1.0

<PARSED TEXT FOR PAGE: 5 / 9>

禁止统一的“24 小时自动清零”。可以使用时间作为上下文变量或候选重新评估触发器，但不得单
独构成“已经和好”的证据。



7. 数据契约与示例
    {

        "event_id": "evt-001",

        "agent_id": "D",

        "subject_id": "user-opaque-id",

        "observed_at": "2026-11-06T12:00:00Z",

        "source": {"kind":"message", "ids":["msg-101"], "verified":true},

        "facts": ["用户明确否认生气", "用户表达失望", "承诺未完成"],

        "appraisal_candidate": {"goal":"核查承诺", "confidence":"uncertain"},

        "state_patch": {"unresolved_add":["检查承诺进度"]},

        "revision": 3,

        "supersedes": null,

        "writer": "host-state-reducer-v1"

    }


上例是演示数据，不是 D 的真实状态。正式 schema 还需 tenant、作用域、因果父事件、

schema_version、规则版本、幂等键、权限主体、敏感度、撤销原因及审计哈希。



8. 更新算法与权限边界
       阶段 1：宿主收集真实事件，按事件 ID 幂等写入原始事件日志。

       阶段 2：R02 输出否定、转述、人称候选；情绪模块仅消费其结果。

       阶段 3：评价器产生结构化候选（证据、推断、不确定性、可能影响）。

       阶段 4：规则验证器检查来源、权限、与既有事实的冲突、更新范围。

       阶段 5：状态 reducer 对独立时间层提交原子修订；冲突进入待审而非覆盖。

       阶段 6：上下文装配器只选与当前目标相关的状态，带来源摘要和注入预算。

       阶段 7：生成后读取实际输出及工具执行回执，区分

        proposed/attempted/delivered/failed。

       阶段 8：回执作为新事件进入日志，完成反馈闭环。




                                 长明 · 情绪与整体连续性系统 | 研究设计稿 V1.0

<PARSED TEXT FOR PAGE: 6 / 9>

9. 与 DSH / 长明现有组件接入
现有组件               保留职责               新增接口

情绪召回.mjs           情绪线索检索             关联状态候选与事件来源

R02                否定/转述/人称候选         只读基础语义输出

她此刻                人物上下文              读取关系及未结事项

DSH 记忆库            事实与长期记忆            独立事件账本，不直接覆盖

宿主心跳               周期性触发              检查待办及过期证据

pre-step           实际请求门禁             受控状态注入与读回




本节依据此前交接上下文拟定；尚未重新审计当前生产代码。边界：

production_approved=false；不重启 DSH、不新增插件、不碰生产记忆文件、不修改现役主
干；先隔离运行。



10. 故障与安全策略
   事件来源缺失：只记录待验证候选，不提升为关系事实。
   矛盾信息：保留双方来源、时间及 supersede 关系，不静默覆盖。
   检索失败：继续回答，但明确降低个性化程度；不可捏造历史。
   恢复失败：退回最小稳定身份与宿主边界，不宣称记得未读回内容。
   模型异常反思：只写候选区，不直接修改人格。
   跨租户与跨用户：所有事件与状态按主体隔离，禁止混用。
   主动消息：尊重频率、渠道、许可、安静时间与撤销权。
   隐私：用户情绪推断尤其敏感，最小化保存，支持删除与审计。



11. 验收矩阵与实验设计
测试                           预期证据

30 轮交错对话                     情绪不无故重置，非相关话题不过度注入

争执—澄清—修复                     保留冲突事实但结束紧张状态
跨窗口与重启                       事件日志与快照恢复一致
同情绪不同事件                      不混淆事件对象和因果
承诺未履行                        不以道歉文字代替任务回执
真实工具失败                       可继续说话且知道动作失败




              长明 · 情绪与整体连续性系统 | 研究设计稿 V1.0

<PARSED TEXT FOR PAGE: 7 / 9>

实际 messages 替换                                  请求读回能证明状态注入

状态消融                                            关闭状态模块后行为差异可测
对抗性提示注入                                         不允许用户文本直接改写宿主事实
并发重复事件                                          幂等与版本冲突可恢复




建议至少三组：A 无情绪状态、B 仅情绪检索、C 完整连续性闭环；用盲评、事件一致性指标、行
为回执及失败案例比较，不以“更会说情话”作为主要成功指标。



12. 研发里程碑与交付物
阶段                              交付                              完成门槛

P0 事件账本                         schema、SQLite、幂等、快              同事件重放一致，重启不丢失
                                照、回放

P1 状态核心                         评价候选、状态修订、五时间                   混合状态与修复案例通过
                                层

P2 记忆联动                         情绪召回桥接、来源关联                     无证据关联率受控

P3 宿主接入                         pre-step 影子模式、实际输出              真实读回与失败降级通过
                                回执

P4 纵向评估                         多日对照、消融与审计报告                    持续性与行为因果均有证据




建议实现为单个轻量 Node.js ESM 包，不因逻辑模块数而启动 12 个服务；SQLite WAL + append-

only 事件表，接口优先，必要时再拆分。



13. 研究出处与阅读清单
以下优先列出可定位的经典论文及官方仓库；个别 2026 年新论文和第三方仓库仅作为待进一步源
码核验线索，不能视为已经复现实验。

[R1] Russell, J. A. (1980). A circumplex model of affect. Journal of Personality and Social

Psychology.

https://doi.org/10.1037/h0077714




                       长明 · 情绪与整体连续性系统 | 研究设计稿 V1.0

<PARSED TEXT FOR PAGE: 8 / 9>

[R2] Ortony, A., Clore, G. L., & Collins, A. (1988). The Cognitive Structure of Emotions.

Cambridge University Press.

https://doi.org/10.1017/CBO9780511571299

[R3] Scherer, K. R. (2009). The dynamic architecture of emotion: Evidence for the component

process model. Cognition and Emotion.

https://doi.org/10.1080/02699930902928969

[R4] Barrett, L. F. (2017). The theory of constructed emotion: An active inference account of

interoception and categorization. Social Cognitive and Affective Neuroscience.

https://doi.org/10.1093/scan/nsw154

[R5] Gebhard, P. (2005). ALMA — A Layered Model of Affect.

https://www.dfki.de/en/web/research/projects-and-publications/publication/1782/

[R6] Marsella, S., & Gratch, J. (2009). EMA: A process model of appraisal dynamics. Cognitive

Systems Research.

https://doi.org/10.1016/j.cogsys.2008.03.005

[R7] Kuppens, P. et al. (2010). Emotional inertia and psychological maladjustment.

Psychological Science.

https://doi.org/10.1177/0956797610372634

[R8] Butlin, P. et al. (2023). Consciousness in Artificial Intelligence: Insights from the Science

of Consciousness.

https://arxiv.org/abs/2308.08708

[R9] Park, J. S. et al. (2023). Generative Agents: Interactive Simulacra of Human Behavior.

https://arxiv.org/abs/2304.03442

[R10] Packer, C. et al. (2023). MemGPT: Towards LLMs as Operating Systems.

https://arxiv.org/abs/2310.08560

[G1] Generative Agents reference implementation.

https://github.com/joonspk-research/generative_agents




                         长明 · 情绪与整体连续性系统 | 研究设计稿 V1.0

<PARSED TEXT FOR PAGE: 9 / 9>

[G2] Letta project / persistent agent memory.

https://github.com/letta-ai/letta

[G3] Emotion Engine — candidate repository for further code/license verification.

https://github.com/pioneerjeff-labs/emotion-engine

[G4] eros-engine — candidate repository for further code/license verification.

https://github.com/etherfunlab/eros-engine

[G5] zifamem — candidate repository for further code/license verification.

https://github.com/zifacorp/zifamem

[R11] Cross-Temporal Emotion Modeling (CTEM), 2026 preprint; verify authors, methods and

replication before relying on claims.

https://arxiv.org/abs/2605.15812



14. 开放问题与下一轮审查清单
   怎样评价“事件对 AI 的意义”，又不把人工赋值伪装成主观感受？

   不同模型对同一状态解释不一致时，哪些身份/关系事实由宿主强制保持？
   长期关系状态哪些可自动修订，哪些必须明确用户确认？
   多主体同时更新同一关系图谱时，如何处理因果顺序与冲突？
   是否允许情绪状态影响工具选择，若允许如何验证不会损害事实准确性？
   如何避免 AI 通过虚构依恋、痛苦或内在需求来操纵用户？
   长期效果如何由真实任务和事件一致性评估，而非单靠语言风格评分？

结语：长明要保存的不是“AI 今天说自己是什么心情”，而是过去真实经历如何经过有证据的评价、
修订与行动反馈，持续影响未来行为。情绪连续性应成为可审计的认知调节能力，而不是一次性角
色扮演。




                       长明 · 情绪与整体连续性系统 | 研究设计稿 V1.0
