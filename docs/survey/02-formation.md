# Formation：记忆形成与写入

> v3.2.0 | 2026-04-27
> Changelog: 补充 A-MEM 的 Zettelkasten 式 inter-memory linking 与写入触发演化作为新关键概念条目；更新代表工作定位与证据来源。

## 本章核心判断

Formation 的核心不是“把什么存下来”，而是“把 observation 变成哪一种可持续管理的记忆对象”。这是一个筛选、抽象、结构化和赋权的过程。当前许多系统把 formation 做得过于轻量，导致后续的更新、检索和治理都被迫补锅。

## 研究矩阵：formation 在哪里分化

| 路线 | 写入对象 | 控制权中心 | 优势 | 局限 | 当前证据强度 |
| --- | --- | --- | --- | --- | --- |
| 抽取式 formation | fact-level 事实、偏好、属性 | 外部规则与 LLM 抽取器 | 降噪明显，适合稳定偏好与长期事实 | 易丢证据链与事件结构 | 高 |
| 学习式 memory policy | 写入/保留/删除动作 | 训练出的策略网络或 agent policy | 有机会学出任务相关的写入决策 | 训练成本高，跨域泛化不足 | 中 |
| active state 分层 | 当前目标、决策、待办、上下文板 | 系统状态管理器 | 把短期工作记忆从长期库剥离，工程收益高 | 若与 archive 边界不清，会出现状态漂移 | 中高 |
| 图式或结构化写入 | 实体、关系、时间锚点 | schema 与构图逻辑 | 利于后续更新、关系查询与治理 | ingestion 成本高，建模门槛高 | 中 |
| 多模态/空间 formation | 对象、片段、场景、轨迹 | 感知模块与跨模态索引 | 适合视觉、视频和环境状态 | 统一记忆单位与 provenance 设计仍不稳 | 中低 |

## 关键概念与代表引用

- extractive formation
  本文语义：长期记忆写入前先做抽取、筛选和结构化。
  主代表引用：`Mem0`
  证据类型：`主证据`
  边界说明：支撑 selective write 的必要性，不支撑复杂 experience 已被充分保真。
- active state
  本文语义：当前目标、待办与上下文板应从长期 archive 中分离。
  主代表引用：`Agentic Memory: Learning Unified Long-Term and Short-Term Memory Management for Large Language Model Agents`
  证据类型：`主证据`
  边界说明：支撑 short-term / long-term 分层，不直接证明某种 STM 管理策略最优。
- provenance
  本文语义：来源、时间和主体是写入对象的一部分，不是附属 metadata。
  主代表引用：`Mem0`
  证据类型：`主证据`
  边界说明：支撑 formation 必须保留证据边界，不支撑删除治理已闭环。
- abstraction vs specificity
  本文语义：长期记忆既要抽象出稳定偏好，也要保留足够具体的证据上下文。
  主代表引用：`Memora（论文题名 Memoria）`
  证据类型：`主证据`
  边界说明：支撑个性化 agentic memory 需要在 profile 与 evidence 间折中，不支撑跨任务泛化已经充分验证。
- learnable memory operations
  本文语义：写入、巩固、裁剪不必只能依赖手写规则。
  主代表引用：`MemSkill: Learning and Evolving Memory Skills for Self-Evolving Agents`
  证据类型：`主证据`
  边界说明：支撑 memory operation 可学习化，不支撑训练成本与稳定性问题已解决。
- inter-memory linking with write-triggered evolution
  本文语义：新记忆写入时自动建立跨记忆链接（keywords / tags / contextual descriptions），且写入过程同时触发对已有记忆的更新，使记忆网络随每次新增而自我精炼。
  主代表引用：`A-MEM: Agentic Memory for LLM Agents`
  证据类型：`主证据`
  边界说明：支撑 formation 不只是写入单条事实，而是维护一个可自我精炼的 interconnected memory network；不支撑跨任务 linking 质量已充分验证，也不支撑写入触发演化可替代显式治理策略。

## 问题定义：formation 到底解决什么

一个成熟的 formation 模块至少要回答四个问题：

1. 哪些信息值得进入长期层，哪些应留在会话层或活跃态。
2. 进入长期层前要不要抽取、摘要、结构化、去重或打标签。
3. 写入对象是自由文本、事实三元组、图节点、程序状态，还是多模态片段。
4. 这条记忆写进去以后，后续系统是否知道它来自谁、何时写入、可否被修正。

如果这四件事不明确，后面的 retrieval 往往只能基于模糊文本搜索，而 evolution 也无法判断该覆盖还是版本化。

## 当前主流路线

### 1. 抽取式 formation

Mem0、LangMem 是最典型的代表。它们不直接把原始对话块存入长期库，而是让模型先抽取“值得记住的事实”，再执行 add/update/delete/noop 一类操作。它的优势很明显：

- 显著降低长期库中的冗余文本。
- 比原始 chunk 存储更利于精确召回。
- 对用户偏好、稳定事实和短句式知识效果好。

但这条路线也有边界。它倾向于把记忆压平成“单句事实”，对复杂经历、任务轨迹、带冲突的 belief 和上下文依赖很强的 observation 处理较弱。换句话说，它擅长“记住结论”，不擅长“保留证据结构”。

### 2. Agent 学习写入策略

MemAgent 这类工作把 formation 从规则工程推进到策略学习。其关键不在“有个 memory agent”，而在于写入、删除、保留、读取这些动作被视为可学习决策，而不是纯手写 heuristic。优点是可在任务中优化 memory policy；缺点是对训练环境和奖励设计依赖强，跨域泛化仍待验证。

### 3. 活跃态文档与状态板

工程界越来越重视 active state 的原因，是很多信息根本不该直接进长期库。例如当前项目目标、最近决策、待办、进行中的工具上下文，这些更像工作记忆。它们需要始终加载、频繁更新，并在任务结束后被压缩或部分下沉到长期层。

这一点常被忽视。很多所谓长期记忆问题，本质上是 working state 管理失败。把短期状态都打散进 archive，会让长期库背负它不该承受的高频更新和高噪声检索。

### 4. 多模态与空间 formation

TeleMem、MEM、MemOCR、M3-Agent、Think3D、GSMem、RenderMem 等前沿工作把 formation 从文本事实扩展到视觉片段、对象状态、场景布局、空间锚点和时间序列。这里最重要的启发不是“多模态更复杂”，而是 formation 的对象不再是句子，而是带位置、视角、持续时间和跨帧关系的 observation。

其中，MEM 额外强调了一种很有代表性的 formation 分层：短期保留高密度视觉观察，长期保留更可压缩的语言化任务进展与环境状态。这种长期层并不是原始日志，而是 semantic event summary，用于跟踪 recipe progress、object-state 和 environment-state。这里的 compression 也不是单纯降 token，而是 formation 阶段对“写成什么表示”的直接回答：只有把长时经历压缩成可持续更新的状态摘要，后续策略才不会因长序列历史直接输入而遭遇明显的 latency 压力与训练-推理分布漂移。这说明 formation 不只是“写不写入”，还包括“同一经历在不同时间尺度上写成什么表示”。

这意味着文本式抽取 pipeline 不能简单复用。它需要引入对象级索引、轨迹摘要、视觉摘要与空间坐标等新表示。

## Formation 的关键设计取舍

### 1. 记忆粒度

记忆粒度越细，越利于局部更新和精确召回，但也更容易产生海量碎片；粒度越粗，越利于保留上下文，但更新与检索成本更高。当前系统大致有三种折中：

- `fact-level`：适合稳定偏好与明确属性。
- `event-level`：适合经历、任务轨迹和时间相关问题。
- `profile-level`：适合用户画像、belief 汇总和主题摘要。

一个合理的结论是：没有单一最佳粒度。成熟系统往往需要多粒度并存，而不是强迫所有内容都进同一 schema。

### 2. 表示形式

Formation 阶段的表示直接影响后续所有环节：

- 文本块易接入，但不利于显式关系和可控更新。
- 图表示利于多跳关系、时间链和实体治理，但构建与维护成本更高。
- KV / latent 表示在规模和速度上有潜力，但外部可解释性和删除治理弱。
- 状态文档最适合 active context，但不适合作为唯一长期库。

因此，“写成什么”不只是存储问题，而是后续可治理性与可推理性的预判。

### 3. 来源与时间戳

Formation 最容易被低估的字段不是 embedding，而是 provenance。很多系统把事实写进去，却没有稳定地保留：

- 来源主体。
- 写入时间。
- 证据上下文。
- 是否来自用户陈述、工具观测、模型推断或系统总结。

这会直接导致后续无法处理时间敏感问题、权限隔离、冲突回溯和解释责任。Mem0 论文中对时间问题的强调，以及 Zep/图记忆对时间锚定的重视，反过来都说明 provenance 不是附属字段，而是 formation 的核心产物。

## 当前证据说明了什么

现有材料支持几个相对稳的结论：

- 抽取式 formation 比简单对话 chunk 存储更高效，也更容易得到可用长期记忆。
- 时间与主体信息若缺失，会显著损害 chronologically-aware retrieval。
- 将短期活跃状态与长期 archive 分层，是工程上极高收益的设计。

但还有几件事证据不足：

- 何种抽取策略对复杂 belief 更稳。
- 学习式 memory policy 在跨任务上的泛化能力。
- 多模态 formation 的最佳单位是对象、事件还是场景图。

## 工程含义

对工程实现而言，本章最重要的结论不是“选择向量库还是图”，而是：

1. 先把 working state 和长期记忆分开。
2. 长期写入前至少做一次选择性抽取或结构化。
3. 写入对象必须带来源与时间。
4. 不同记忆粒度需要不同表示，而不是统一扁平化。

这决定了后面 evolution 和 retrieval 是否还有空间做对。

## 代表工作定位

- `Mem0`：抽取式 formation 的代表，突出 add/update/delete/noop 语义。
- `Agentic Memory`：代表 long-term / short-term 一体化管理对 active state 的提升。
- `Memora（论文题名 Memoria）`：代表 personalization 中 abstraction 与 specificity 的平衡路线。
- `MemSkill`：代表 formation 阶段的 memory operation 可学习化。
- `A-MEM`：代表 Zettelkasten 式 inter-memory linking 与写入触发演化，新记忆写入同时自动建立关联并更新已有记忆的 contextual representations（v11，已充分迭代）。
- `MemAgent`：代表把 memory policy 视作可学习动作。
- `Elastic memory architecture`：代表生产系统里 formation 对 metadata、identity 与过滤条件的要求。
- `TeleMem / MEM / MemOCR / M3-Agent`：代表多模态 formation 开始从文本事实扩展到片段、对象和场景状态；其中 MEM 进一步强调短期观察与长期任务状态的分层写入，以及 semantic event summary 作为长期状态表示的价值。

## 本章主要证据来源

- `paper`：Mem0、Agentic Memory、Memoria、MemSkill、A-MEM、MemAgent、TeleMem、MEM、MemOCR、M3-Agent 相关论文与索引条目。
- `blog`：Elastic 关于 managed memory 的工程文章。
- `综合推断`：active state 与长期库应分层，是对抽取式系统与生产实践共同问题的总结。
