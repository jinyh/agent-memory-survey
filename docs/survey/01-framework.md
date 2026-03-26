# Agent Memory 统一研究框架

> v3.1 | 2026-03-27

## 本章核心判断

如果说 2024-2025 年上半年的主问题是“如何让模型在回答前想得更久”，那么 2025-2026 年真正抬头的问题已经变成：如何让系统为了行动而思考，并在环境反馈下持续修正。这个变化意味着，今天只讨论 Agent Memory 已经不够，也不能把它和 agentic thinking 混为一谈。

本文采用一个更高一层的框架来组织这两个问题：

- `Agent Memory` 是状态连续性层，负责跨时间保存、更新、读取和治理状态。
- `Agentic Thinking` 是闭环行动控制层，负责为了行动而思考、调用工具、吸收反馈并修正计划。
- `Skill` 是可复用程序化策略层，负责把经验和规则沉淀为可重复调用的行动模式。

在这个框架下，memory 仍然不是 retrieval 的同义词；但 lifecycle 也不再是整个 agent system 的全部。更准确地说，`formation -> evolution -> retrieval -> evaluation` 描述的是 memory layer 的内部生命周期，而不是整个 agent 的全部 cognition loop。

## 研究矩阵：本章在比较什么

| 维度 | 典型对象 | 控制权中心 | 优势 | 局限 | 当前证据强度 |
| --- | --- | --- | --- | --- | --- |
| reasoning thinking | 长推理链、延长推理预算、静态 benchmark 求解 | 模型内部 deliberation | 易度量、适合 RL 和可验证任务 | 对环境交互、状态延续和长期执行解释不足 | 高 |
| agentic thinking | 工具调用、环境反馈、计划修订、长程任务推进 | agent 与 harness | 更贴近真实任务与生产环境 | 评测更难，环境和系统工程复杂度更高 | 中高 |
| memory lifecycle | formation / evolution / retrieval / evaluation | 记忆策略与控制平面 | 能直接解释写入、更新、读取和治理问题 | 不能单独解释行动控制与多步执行 | 中高 |
| skill / procedural reuse | 策略模板、操作规则、经验沉淀 | agent policy 或 skill loader | 降低重复推理成本，提升执行一致性 | skill 发现、装载和更新仍不稳定 | 中 |

## 关键概念与代表引用

- 生命周期框架
  本文语义：把 memory 视为 `formation -> evolution -> retrieval -> evaluation` 的连续系统。
  主代表引用：`Memory in the Age of AI Agents: A Survey`
  证据类型：`主证据`
  边界说明：支撑 memory 应按生命周期而非静态类型组织，不直接支撑整个 agent system 的最优设计。
- agentic thinking
  本文语义：为了行动而思考，在工具、环境和反馈中持续调整计划。
  主代表引用：`From "Reasoning" Thinking to "Agentic" Thinking`
  证据类型：`工程补充`
  边界说明：支撑问题从静态 reasoning 转向闭环 action 的工程判断，不替代 memory 主证据。
- retrieval-centric 系统观
  本文语义：把长期记忆主要实现为可检索外部存储与上下文装配。
  主代表引用：`Mem0`
  证据类型：`主证据`
  边界说明：支撑“检索足够成熟但不等于全部 memory”的判断，不支撑 belief 管理已解决。
- memory management 系统观
  本文语义：把 active state、version、belief、policy 与 control plane 视为一等对象。
  主代表引用：`Hindsight is 20/20: Building Agent Memory that Retains, Recalls, and Reflects`
  证据类型：`主证据`
  边界说明：支撑 evidence 与 belief 分层的重要性，不支撑所有治理问题已有统一标准。
- programmatic working memory
  本文语义：working memory 可以是可编程状态，而不只是 prompt 中的短期上下文。
  主代表引用：`Recursive Language Models`
  证据类型：`主证据`
  边界说明：支撑程序化 working memory 与 recursive retrieval 的独立路线，不支撑企业级治理已经成熟。
- skill as procedural memory
  本文语义：skill 是可复用的程序化策略单元，可作为 procedural memory 的显式载体，也可由经验巩固而来。
  主代表引用：`MemSkill: Learning and Evolving Memory Skills for Self-Evolving Agents`
  证据类型：`主证据`
  边界说明：支撑 procedural memory 与可学习 memory operation 的连接，不支撑通用 skill library 已成熟。

## 从 Reasoning Thinking 到 Agentic Thinking

新加入的 blog 提出一个很有用的区分：`reasoning thinking` 的优化目标，通常是让模型在给出最终答案前做更强的内部 deliberation；`agentic thinking` 的优化目标，则是让模型在与环境交互时持续推进任务。[ref/blog/From "Reasoning" Thinking to "Agentic" Thinking.md](../../ref/blog/From%20%22Reasoning%22%20Thinking%20to%20%22Agentic%22%20Thinking.md)

两者最本质的差别不在“有没有思考”，而在优化对象不同：

- reasoning thinking 更关心单次求解质量，例如定理、代码、可验证 benchmark。
- agentic thinking 更关心在环境中是否能持续产生有效动作。

因此，问题会从“模型能否想得更久”转向“模型能否以支持行动的方式去想”。这会把研究重心从单一模型推理轨迹，推向 `model-plus-environment` 的系统问题：工具服务器、浏览器、终端、执行沙箱、memory systems 和 orchestration framework 都进入能力定义本身。

这也是本文为何要把 memory 放到更大的 agent system 里讨论。因为一旦目标从静态求解变成闭环行动，memory 就不再只是“存历史”，而是行动持续性的基础设施。

## Agent Memory 和 Agentic Thinking 的区别

两者最容易混淆的地方，是它们都在处理“跨多步任务的持续性”。但它们负责的不是同一件事。

### 1. Agent Memory 解决状态连续性

Agent Memory 的核心问题仍然是：

- 什么值得写入长期层。
- 新证据到来时如何更新、版本化、压缩或遗忘。
- 当前任务中应读取哪些记忆，以及以何种表示读取。
- 如何证明这些记忆真的改善了行为。

也就是说，memory 的对象首先是 `state`，包括事实、偏好、经历、belief、active state，以及更广义的环境状态。它负责让系统在时间上不失忆。

### 2. Agentic Thinking 解决闭环行动控制

Agentic thinking 的核心问题则是：

- 什么时候停止思考并采取动作。
- 该调用哪个工具、按什么顺序调用。
- 如何整合不完整、带噪声的环境观察。
- 失败后如何修订计划。
- 如何在长链路执行中维持目标一致性。

也就是说，agentic thinking 的对象首先是 `action policy`。它负责让系统不只是“知道”，而是“持续推进”。

一句话概括：`memory` 负责跨时间保存和组织状态，`agentic thinking` 负责基于这些状态持续做出有效动作。

## 两者的联系：状态层与控制层的耦合

虽然不是同一层，但两者高度耦合。

### 1. 没有 memory 的 agentic thinking 会变得短视

如果系统不能跨回合保留用户偏好、任务进度、失败经验、环境变化和中间结论，那么再强的在线推理也只能在局部窗口内做决策。它能行动，但难以维持长期一致性。

### 2. 没有 agentic thinking 的 memory 会变成被动存储

如果系统只会存和取，却不知道何时该读、该写、该更新，也不知道如何把取回的内容转成下一步动作，那么 memory 只能充当外挂知识库，而不是真正的记忆层。

### 3. 两者主要在三个接口上耦合

- `active state`
  当前目标、待办、最近决策和工作上下文既属于 memory 管理问题，也直接塑造 agent 的下一步行动。
- `retrieval in use`
  retrieval 的关键不只是召回命中，而是记忆是否在当前行动链中被真正消费。[docs/survey/04-retrieval.md](./04-retrieval.md)
- `policy revision`
  环境反馈会改变计划，也会触发记忆更新。失败经验、冲突证据和新状态需要同时进入 deliberation loop 与 memory evolution。

因此，更合理的关系不是“memory 包含 agentic thinking”或“agentic thinking 取代 memory”，而是：

- memory 提供跨时间连续性；
- agentic thinking 把连续状态转成闭环行动；
- 两者通过 active state、retrieval 和 update policy 相互约束。

## Skill 在其中起什么作用

`skill` 最适合被理解为 memory 和 action 之间的中间层，而不是事实记忆本身。

### 1. Skill 不是 tool，也不是普通 fact memory

- `tool` 是外部能力接口，例如搜索、浏览器、终端、数据库。
- `memory` 是关于用户、世界、任务和经验的状态。
- `skill` 是在某类情境下如何组织步骤、调用工具、利用记忆的可复用策略单元。

因此，skill 处理的是“怎么做”，而不是“知道什么”。

### 2. Skill 是 procedural memory 的显式载体

在静态分类里，procedural memory 指的是调用工具、管理上下文、执行工作流和维持策略的规则。把这些规则显式打包成 skill，有两个直接收益：

- 让 agent 不必在高频任务上每次都从零推理。
- 让程序化经验可以被检索、装载、复用和更新。

这使 skill 成为 procedural memory 最工程化的形态之一。

### 3. Skill 也可以是 episodic 经验演化后的结果

从 lifecycle 视角看，skill 不只是先验写死的 prompt 或 workflow，也可以来自经验巩固：

- `episodic -> procedural`
  把一次次执行经历中稳定有效的模式沉淀为可复用策略。

这正对应 `MemSkill` 所强调的方向：memory operation 本身可以学习，经验不只沉淀为 semantic facts，也可以沉淀为行动技能。[docs/survey/03-evolution.md](./03-evolution.md)

### 4. Skill 帮 agentic thinking 降低在线复杂度

如果没有 skill，agentic thinking 往往只能依赖每次在线 deliberation 现想步骤，成本高且不稳定。skill 的作用是把已经验证过的行动模式压缩成可复用单元，让 agent 把更多在线计算留给真正的新情况、异常情况和策略修订。

因此，skill 的位置可以概括为：

- 对 memory 来说，它是 procedural memory 的主要产物之一。
- 对 agentic thinking 来说，它是降低重复推理成本的执行先验。
- 对系统工程来说，它是连接记忆沉淀与行动复用的桥。

## 为什么生命周期比静态分类更有效

即便本章把视角抬高到 `Memory / Agentic Thinking / Skill` 三层，生命周期框架仍然比“working / episodic / semantic / procedural”静态分类更适合作为 memory 研究主线。

原因不是静态分类失效，而是它更适合回答“记忆承担什么功能”，不适合回答“记忆系统如何持续运作”。同一条信息在时间中完全可能跨类型迁移：一条带时间戳的 observation 可以先作为 episodic 事件存在，随后被巩固为 semantic 偏好，最后再沉淀成 procedural 规则或 skill。

因此，真正决定 memory layer 质量的，不是给记忆贴上哪一种认知标签，而是系统如何处理以下四个问题：

- 何时写入。
- 如何更新、版本化或遗忘。
- 如何在任务中读取并真正用上。
- 如何证明这些机制改善了 agent 行为。

这也就是为什么本项目仍以 `formation -> evolution -> retrieval -> evaluation` 作为 memory 主线。静态分类保留为辅助视角，生命周期继续承担主要组织框架。

## 为什么 lifecycle 仍然是本项目的主线

引入 agentic thinking 之后，并不意味着要放弃当前 survey 的 lifecycle 组织。相反，lifecycle 现在的边界更清楚了：

- 它不是整个 agent system 的总框架。
- 它是 memory layer 的内部分析框架。

这仍然是本项目最有效的研究主线，因为它直接回答：

- 记忆如何进入系统。
- 记忆如何在时间中演化。
- 记忆如何在任务中被真正用上。
- 记忆是否改善了 agent 行为。

换句话说，agentic thinking 把问题域扩大到了“如何行动”，而 lifecycle 继续回答“memory 这层如何支撑行动”。

## 对本仓库的意义

这个更新后的框架给本项目增加了三个直接约束：

1. survey 仍按 lifecycle 组织 memory 主线，但在总论中明确区分状态层、控制层和程序化策略层。
2. 讨论 memory 时，不再把它缩减成 retrieval，也不把它泛化成整个 agent loop。
3. 讨论 skill 时，优先把它放在 `procedural memory / reusable policy` 的位置，而不是当作杂项工具集合。

## 代表工作定位

- `Mem0 / LangMem`：代表 retrieval-centric memory service，说明为什么 memory 不能被压缩成单一检索问题。
- `Hindsight`：代表 belief-aware memory management，说明 evidence、belief 和 update semantics 应分层。
- `Recursive Language Models`：代表程序化 working memory，说明部分“记忆使用”本质上是可编程状态操作。
- `MemSkill`：代表 procedural memory 与 learned skill 的连接，说明经验可以沉淀为可复用策略。
- `From "Reasoning" Thinking to "Agentic" Thinking`：作为工程补充，帮助定义 reasoning 到 agentic 的问题迁移。

## 本章主要证据来源

- `paper`：Mem0、Hindsight、Recursive Language Models、MemSkill、`Memory in the Age of AI Agents: A Survey`。
- `blog`：`From "Reasoning" Thinking to "Agentic" Thinking`，以及工程界关于 stateful agents、context engineering 与 memory management 的材料。
- `综合推断`：Agent Memory、Agentic Thinking 和 Skill 应被视为状态层、控制层与程序化策略层的分工，这是基于现有论文证据与工程趋势做出的组织性判断。
