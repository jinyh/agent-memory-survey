# Evolution：记忆演化、压缩与治理

> v3.0 | 2026-03-26

## 本章核心判断

如果 formation 决定了记忆如何进入系统，那么 evolution 决定了系统能否长期活下去。多数 memory demo 看起来能工作，是因为它们只展示了“第一次记住”；真正把系统拖垮的，是第二次、第三次、第一百次写入之后，旧记忆如何被修正、压缩、抽象、隔离和撤销。

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
- `episodic -> procedural`：把经验转成工作流、策略或调用规则。

这一步的难点在于避免过早抽象。系统若太快把局部经历提升为稳定知识，就会制造高置信度错误。

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

MSA 的贡献之一，是说明 latent route + sparse generation 可以把极大规模记忆压进可计算形态。它与传统 external summarization 的差异在于，压缩后的表示仍是生成过程可直接利用的 memory substrate，而不是只给检索器看的索引副本。

### 4. 遗忘与治理：把 memory 当作受监管对象

遗忘不等于删除。一个成熟系统至少要区分：

- `relevance decay`：因为过时而降低读取优先级。
- `summarized away`：被压缩成更高层表征，但仍可追溯。
- `revoked/deleted`：因隐私、权限或错误而被明确移除。

多数论文对这部分讨论还不够，反而是工程 blog 和产品实践更早暴露问题，例如权限隔离、删除权、审计链、租户隔离、记忆投毒与跨用户污染。这说明 evolution 迟早会从“模型问题”变成“系统治理问题”。

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

- `Hindsight`：belief-aware evolution 的最强代表，强调 evidence 与 opinion 分层。
- `Synapse`：代表 episodic 与 semantic 之间的激活和重组。
- `MSA`：代表压缩与稀疏读取结合的内生 memory 演化方向。
- `AgentOrchestra`：代表多 agent 场景下 versioning 与组件演化的协议化思路。
- `工程治理材料`：帮助说明删除、撤销、审计和权限不是附属问题。

## 本章主要证据来源

- `paper`：Hindsight、Synapse、MSA、AgentOrchestra。
- `blog`：工程系统关于 memory 更新、治理、权限和审计的讨论。
- `综合推断`：evolution 是长期能力本身，而不是后台优化，这是对现有 demo 与真实部署鸿沟的归纳。
