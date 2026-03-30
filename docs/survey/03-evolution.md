# Evolution：记忆演化、压缩与治理

> v3.1 | 2026-03-30
> Changelog: 新增 experience replay / 海马回放类比、持续学习与 stability-plasticity 交叉定位、缓存淘汰策略类比、meta-learning 定位。

## 本章核心判断

如果 formation 决定了记忆如何进入系统，那么 evolution 决定了系统能否长期活下去。多数 memory demo 看起来能工作，是因为它们只展示了“第一次记住”；真正把系统拖垮的，是第二次、第三次、第一百次写入之后，旧记忆如何被修正、压缩、抽象、隔离和撤销。

## 研究矩阵：evolution 的核心矛盾

| 机制 | 主要对象 | 控制权中心 | 优势 | 局限 | 当前证据强度 |
| --- | --- | --- | --- | --- | --- |
| 巩固 consolidation | episodic -> semantic / procedural | 总结器、聚合器或 agent policy | 让经验变成可复用知识，降低碎片化 | 过早抽象会放大错误 belief | 中 |
| 覆盖式更新 | 稳定属性、明确新旧替代关系 | update policy | 实现简单，适合少量高确定性事实 | 丢历史边界，不利审计与解释 | 中 |
| 版本化更新 | 时间敏感事实、可追溯状态 | version semantics 与 provenance | 便于回溯、解释和时间推理 | 存储与检索复杂度更高 | 中低 |
| 压缩与摘要 | 长轨迹、重复 observation、冷数据 | summarizer 或 latent compressor | 降低上下文与存储成本 | 易牺牲细节，摘要偏差难检测 | 中 |
| 遗忘与治理 | 过时、错误、越权或撤销内容 | governance policy | 面向长期部署的关键能力 | benchmark 与公开实证仍明显不足 | 低 |

## 关键概念与代表引用

- consolidation
  本文语义：把 episodic 经验提升为可复用 semantic 或 procedural memory。
  主代表引用：`Hindsight is 20/20: Building Agent Memory that Retains, Recalls, and Reflects`
  证据类型：`主证据`
  边界说明：支撑 retain / reflect 的结构化演化，不支撑所有巩固策略已有统一 benchmark。
- version semantics
  本文语义：更新不是数据库覆盖，而是显式记录新旧边界与采用条件。
  主代表引用：`Hindsight is 20/20: Building Agent Memory that Retains, Recalls, and Reflects`
  证据类型：`主证据`
  边界说明：支撑 evolution 必须保留版本语义，不支撑存储成本问题已解决。
- belief-aware update
  本文语义：evidence、belief、summary、policy 应以不同更新逻辑演化。
  主代表引用：`Hindsight is 20/20: Building Agent Memory that Retains, Recalls, and Reflects`
  证据类型：`主证据`
  边界说明：支撑 belief correction 的必要性，不支撑公共评测已充分覆盖。
- abstraction vs specificity
  本文语义：压缩和抽象不能抹掉后续修正所需的证据颗粒度。
  主代表引用：`Memora（论文题名 Memoria）`
  证据类型：`主证据`
  边界说明：支撑 personalization memory 的演化边界，不承担本章核心 versioning 论证。
- learnable memory operations
  本文语义：巩固、修订、裁剪可以由可学习技能驱动，而非纯启发式。这在本质上是一个元学习（meta-learning）问题——"学习如何记忆"，即 agent 不仅在记忆内容层面学习，还在记忆操作策略层面学习。MemSkill 和 MemAgent 的贡献正在于此：它们不只是优化某次检索或某条记忆的质量，而是优化记忆系统本身的运作方式。与经典 meta-learning（MAML、Reptile 等）的区别在于：后者通过梯度方法学习初始化参数，前者通过 LLM 生成和评估学习显式策略——但"学习如何学习"的结构是相同的。
  主代表引用：`MemSkill: Learning and Evolving Memory Skills for Self-Evolving Agents`
  证据类型：`主证据`
  边界说明：支撑 evolution 可学习化，不支撑大规模部署稳定性已验证。
- spreading activation
  本文语义：episodic 与 semantic 的联动可通过图激活增强，但它更像补充机制而非主演化主线。
  主代表引用：`Synapse: Empowering LLM Agents with Episodic-Semantic Memory via Spreading Activation`
  证据类型：`工程补充`
  边界说明：支撑联动式 retrieval/evolution 案例，不支撑 version semantics。
- multi-agent protocol evolution
  本文语义：多 agent 协议会引入状态协同问题，但不应被当作 evolution 章节的主锚点。
  主代表引用：`AgentOrchestra: Orchestrating Multi-Agent Intelligence with the TEA Protocol`
  证据类型：`工程补充`
  边界说明：支撑多 agent 协调背景，不承担本章核心主判断。

## Evolution 不是“后台优化”，而是长期能力本身

很多工程实现把 evolution 当作后处理任务，例如定期 summarization、离线 reindex 或记忆清理。这样做短期可行，但从系统视角看，evolution 实际承担的是长期能力定义：

- 用户偏好会变化，系统必须知道该修正什么。
- 经历会积累，系统必须知道哪些 episodic 该巩固成 semantic。
- 上下文会膨胀，系统必须知道哪些该压缩、哪些该保真。
- 记忆会出错或被投毒，系统必须知道哪些该撤销、审计或限权。

如果没有 evolution，任何长期记忆系统都只是 append-only 日志。

## 四类关键机制

### 1. 巩固：从经历到可复用知识

认知上最经典的问题在 agent memory 中仍然成立：并非所有 episodic 都该永久保留，但重复出现的模式往往值得被抽象出来。LightMem、Synapse、M3-Agent 等工作都隐含这一方向，即把分散经历重组为更稳定的 semantic 或策略结构。

从工程上看，巩固有两个常见结果：

- `episodic -> semantic`：把多次重复经验压缩成偏好、稳定事实或对象画像。
- `episodic -> procedural`：把经验转成工作流、策略或调用规则。这对应 [01-framework](./01-framework.md) 中 skill 作为 procedural memory 显式载体的定位。

这一步的难点在于避免过早抽象。系统若太快把局部经历提升为稳定知识，就会制造高置信度错误。

**与 experience replay 的类比**：强化学习中的 experience replay buffer 是"从过去经验中有策略地采样和回放"的经典机制。Agent memory 的 consolidation 可以被视为"语义层的 experience replay"——两者共享同一个核心洞察：不是存储全部历史，而是有选择地从历史中提取模式并回放到当前决策中。区别在于 RL replay 采样的是 (state, action, reward) 元组并用于梯度更新，而 agent memory consolidation 采样的是 episodic 经验并用 LLM 生成摘要或策略。神经科学中的海马回放（hippocampal replay）也指向类似机制：睡眠期间对白天经验的选择性重放被认为是记忆巩固的关键过程，与 agent memory 的离线 consolidation 有结构对应。

### 2. 更新：覆盖、版本化还是并存

更新是 memory layer 最容易被低估的决策。面对新证据，系统至少有三种选择：

- `overwrite`：旧事实失效，新事实替换。
- `version`：保留新旧版本及时间边界。
- `coexist`：允许多视角或多来源并存，等待后续 disambiguation。

没有普适最优策略。用户年龄、现住址、当前公司这类事实适合覆盖或版本化；主观偏好、情绪倾向、意见判断则更适合保留证据链与置信度。Hindsight 把 belief 和 evidence 分层，正是为了避免把推断类内容与客观事实混成一种更新逻辑。

### 3. 压缩：在可用性与保真度之间取舍

压缩不是简单摘要。它至少包括：

- 对长对话或事件轨迹做总结。
- 对重复片段做聚类合并。
- 把冷数据迁移到低成本存储。
- 在 latent memory 中做内部压缩表示。

工程 blog 里还常出现另一种较实用的压缩范式：先把原始材料递归切分成层次节点，再自底向上生成多层摘要，让上层节点只保留足够导航的信息，下层节点保留原始细节。这类方法更像“面向读取的压缩”，价值不在生成一个最终摘要，而在保留一条可继续下钻的证据路径。它可以作为 evolution 与 retrieval 的接口参考，但不能直接等同于完整的 lifecycle 方案。

MSA 的贡献之一，是说明 latent route + sparse generation 可以把极大规模记忆压进可计算形态。它与传统 external summarization 的差异在于，压缩后的表示仍是生成过程可直接利用的 memory substrate，而不是只给检索器看的索引副本。

### 4. 遗忘与治理：把 memory 当作受监管对象

遗忘不等于删除。一个成熟系统至少要区分：

- `relevance decay`：因为过时而降低读取优先级。
- `summarized away`：被压缩成更高层表征，但仍可追溯。
- `revoked/deleted`：因隐私、权限或错误而被明确移除。

多数论文对这部分讨论还不够，反而是工程 blog 和产品实践更早暴露问题，例如权限隔离、删除权、审计链、租户隔离、记忆投毒与跨用户污染。这说明 evolution 迟早会从”模型问题”变成”系统治理问题”。

### 交叉定位：持续学习与缓存淘汰

Agent memory 的 evolution 机制与两个成熟领域有深层结构对应，值得明确。

**持续学习（continual learning）与 stability-plasticity 困境**：持续学习领域的核心问题是灾难性遗忘（catastrophic forgetting）——模型在学习新任务时丢失旧任务的能力，其根源是 stability-plasticity tradeoff。Agent memory 的 evolution 面对的是同一个困境的外化版本：新记忆不断写入时，如何避免覆盖或稀释仍然有用的旧记忆。持续学习的经典策略——replay（回放旧样本）、regularization（约束参数变动）、architectural isolation（为不同任务分配不同参数）——在 agent memory 中都有对应物：consolidation 是语义层的 replay，version semantics 是显式的 regularization（保留旧边界而非覆盖），belief/evidence 分层是 architectural isolation 的外部化实现。但关键差异在于：持续学习处理的是参数空间的连续优化，agent memory 处理的是符号/文本空间的离散更新——后者可以做到精确的版本回溯和选择性删除，这是参数空间做不到的。

**缓存淘汰策略（cache eviction）类比**：Agent memory 的遗忘和检索预算问题在形式上与 cache replacement policy 高度同构——都是在有限资源（token budget / cache size）下决定保留什么、淘汰什么。经典策略（LRU 按最近访问、LFU 按访问频率、ARC 自适应平衡两者）提供了一个有用的分析框架。当前 agent memory 系统中的 recency decay 本质上是 LRU，importance scoring 本质上是 LFU 的变体。但 agent memory 的淘汰决策需要语义感知——一条低频但关键的用户偏好不应因为”最近没被访问”就被淘汰——这是纯频率/时间策略无法处理的。这也解释了为什么 Hindsight 等工作要把 evidence 和 belief 分层：不同语义类别的记忆需要不同的淘汰策略，而不是统一的 LRU/LFU。

## 当前方法的主要缺口

### 1. 多数系统仍缺少显式 version semantics

即便系统支持 update/delete，很多实现也只是把它当数据库操作，而不是显式的 memory semantics。问题在于，一旦没有 version boundary，系统就难以回答：

- 用户何时改变了看法。
- 之前为何会做出那个决策。
- 当前结论基于哪一批证据。

这会直接影响解释性和审计性。

### 2. belief 管理仍明显滞后

对 agent 来说，“我知道什么”与“我相信什么”并不一样。前者可以有外部证据，后者往往是从多次 observation 归纳而来，且应带不确定性。现有大量系统仍把这两类内容统一写成自然语言事实，这在短期上省事，但长期上会让系统难以纠错。

### 3. forgetting 的研究深度仍不足

很多工作会提 decay 或 summarization，但很少系统真正解释：为什么这个记忆应该变冷、被压缩、或被撤销；更少有工作证明不同 forgetting policy 对长期任务结果的系统影响。换句话说，遗忘还是一个被广泛承认重要、但证据积累不足的方向。

## 工程含义

对构建 memory layer 的团队，本章有三个直接结论：

1. 必须把 update semantics 设计成一等概念，而不是数据库细节。
2. 需要区分 evidence、belief、summary 和 policy 四类不同可演化对象。
3. 要从一开始就预留 provenance、version 和 deletion 的接口，否则后续治理会非常昂贵。

如果说 formation 决定了记忆“怎么进入系统”，那么 evolution 决定了系统是否还能在半年后保持一致、可信和可控。

## 代表工作定位

- `Hindsight`：belief-aware evolution 的最强代表，强调 evidence 与 opinion 分层，是本章主证据。
- `Memora（论文题名 Memoria） / MemSkill`：补足 abstraction 与可学习 memory operation 两条演化路线。
- `Synapse`：代表 episodic 与 semantic 之间的激活和重组，但降为补充案例。
- `MSA`：代表压缩与稀疏读取结合的内生 memory 演化方向。
- `AgentOrchestra`：保留为多 agent 协调补充，不再承担 evolution 主线。
- `工程治理材料`：帮助说明删除、撤销、审计和权限不是附属问题。

## 本章主要证据来源

- `paper`：Hindsight、Memoria、MemSkill、MSA、Synapse、AgentOrchestra。
- `blog`：工程系统关于 memory 更新、治理、权限和审计的讨论。
- `综合推断`：evolution 是长期能力本身，而不是后台优化，这是对现有 demo 与真实部署鸿沟的归纳。
