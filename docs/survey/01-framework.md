# Agent Memory 统一研究框架

> v3.5 | 2026-03-30
> Changelog: 新增"与经典认知架构的对照"小节，将 ACT-R/Soar 的记忆模型与本 survey lifecycle 框架做对比定位。

## 问题的迁移：从"想得更久"到"为了行动而想"

2024-2025 年上半年，LLM 研究的主问题是"如何让模型在回答前想得更久"——延长推理链、增大推理预算、用 RL 优化可验证任务上的内部 deliberation。这就是 `reasoning thinking`：优化目标是单次求解质量，控制权在模型内部。

但 2025-2026 年真正抬头的问题已经不同：如何让系统为了行动而思考，并在环境反馈下持续修正。这就是 `agentic thinking`。它的优化目标不是"想得更久"，而是"能否以支持行动的方式去想"。[ref/blog/From "Reasoning" Thinking to "Agentic" Thinking.md](../../ref/blog/From%20%22Reasoning%22%20Thinking%20to%20%22Agentic%22%20Thinking.md)

两者最本质的差别不在"有没有思考"，而在优化对象不同：

- reasoning thinking 更关心单次求解质量，例如定理、代码、可验证 benchmark。
- agentic thinking 更关心在环境中是否能持续产生有效动作——决定何时停止思考并行动、该调用哪个工具、如何整合带噪声的环境观察、失败后如何修订计划。

这个迁移把研究重心从单一模型推理轨迹，推向 `model-plus-environment` 的系统问题：工具服务器、浏览器、终端、执行沙箱、memory systems 和 orchestration framework 都进入能力定义本身。

**这也是本章为什么要把 memory 放到更大的上下文里讨论。** 一旦目标从静态求解变成闭环行动，memory 就不再只是"存历史"，而是行动持续性的基础设施。不理解这个迁移，就无法理解为什么 memory 需要 lifecycle 管理，而不只是一个检索接口。

### 研究矩阵

| 维度 | 典型对象 | 控制权中心 | 优势 | 局限 | 当前证据强度 |
| --- | --- | --- | --- | --- | --- |
| reasoning thinking | 长推理链、延长推理预算、静态 benchmark 求解 | 模型内部 deliberation | 易度量、适合 RL 和可验证任务 | 对环境交互、状态延续和长期执行解释不足 | 高 |
| agentic thinking | 工具调用、环境反馈、计划修订、长程任务推进 | agent 与 harness | 更贴近真实任务与生产环境 | 评测更难，环境和系统工程复杂度更高 | 中高 |
| memory lifecycle | formation / evolution / retrieval / evaluation | 记忆策略与控制平面 | 能直接解释写入、更新、读取和治理问题 | 不能单独解释行动控制与多步执行 | 中高 |
| skill / procedural reuse | 策略模板、操作规则、经验沉淀 | agent policy 或 skill loader | 降低重复推理成本，提升执行一致性 | skill 发现、装载和更新仍不稳定 | 中 |

## Memory、Agentic Thinking 与 Skill 的分工

理解了 reasoning → agentic 的迁移之后，可以看到 agent system 中有三个不同层次的问题。**本 survey 聚焦其中的 memory layer，但需要先说清它与另外两层的边界，以免混淆。**

### Memory：状态连续性

Agent Memory 的核心问题是：

- 什么值得写入长期层。
- 新证据到来时如何更新、版本化、压缩或遗忘。
- 当前任务中应读取哪些记忆，以及以何种表示读取。
- 如何证明这些记忆真的改善了行为。

Memory 的对象首先是 `state`——事实、偏好、经历、belief、active state，以及更广义的环境状态。它负责让系统在时间上不失忆。

### Agentic Thinking：闭环行动控制

Agentic thinking 的核心问题则是：

- 什么时候停止思考并采取动作。
- 该调用哪个工具、按什么顺序调用。
- 如何整合不完整、带噪声的环境观察。
- 失败后如何修订计划。
- 如何在长链路执行中维持目标一致性。

Agentic thinking 的对象首先是 `action policy`。它负责让系统不只是"知道"，而是"持续推进"。

### Skill：程序化策略复用

Skill 不是 tool（外部能力接口），也不是普通 fact memory。它是在某类情境下如何组织步骤、调用工具、利用记忆的可复用策略单元。Skill 处理的是"怎么做"，而不是"知道什么"。

从 memory 视角看，skill 是 procedural memory 的显式载体。它既可以先验写入，也可以从经验巩固而来——把一次次执行经历中稳定有效的模式沉淀为可复用策略（`episodic -> procedural`）。这正对应 MemSkill 所强调的方向：memory operation 本身可以学习，经验不只沉淀为 semantic facts，也可以沉淀为行动技能。[docs/survey/03-evolution.md](./03-evolution.md)

对 agentic thinking 来说，skill 的作用是把已经验证过的行动模式压缩成可复用单元，让 agent 把更多在线计算留给真正的新情况和策略修订。

### 三者的耦合

虽然分属不同层，但三者高度耦合，主要在三个接口上：

- **active state**：当前目标、待办、最近决策和工作上下文既属于 memory 管理问题，也直接塑造 agent 的下一步行动。
- **retrieval in use**：retrieval 的关键不只是召回命中，而是记忆是否在当前行动链中被真正消费。[docs/survey/04-retrieval.md](./04-retrieval.md)
- **policy revision**：环境反馈会改变计划，也会触发记忆更新。失败经验、冲突证据和新状态需要同时进入 deliberation loop 与 memory evolution。

一句话概括：memory 提供跨时间连续性，agentic thinking 把连续状态转成闭环行动，skill 降低行动中的重复推理成本。没有 memory 的 agentic thinking 会变得短视；没有 agentic thinking 的 memory 会变成被动存储。

## 为什么 lifecycle 是 memory 主线

引入 agentic thinking 的上下文之后，一个自然的问题是：memory 层内部应该用什么框架组织？

本 survey 的答案仍然是生命周期框架——`formation -> evolution -> retrieval -> evaluation`，而不是"working / episodic / semantic / procedural"静态分类。

原因不是静态分类失效，而是它更适合回答"记忆承担什么功能"，不适合回答"记忆系统如何持续运作"。同一条信息在时间中完全可能跨类型迁移：一条带时间戳的 observation 可以先作为 episodic 事件存在，随后被巩固为 semantic 偏好，最后再沉淀成 procedural 规则或 skill。

真正决定 memory layer 质量的，不是给记忆贴上哪一种认知标签，而是系统如何处理四个问题：

- 何时写入。
- 如何更新、版本化或遗忘。
- 如何在任务中读取并真正用上。
- 如何证明这些机制改善了 agent 行为。

同时，lifecycle 框架现在有了更清楚的边界：

- 它不是整个 agent system 的总框架。
- 它是 memory layer 的内部分析框架。

Agentic thinking 把问题域扩大到了"如何行动"，而 lifecycle 继续回答"memory 这层如何支撑行动"。静态分类保留为辅助视角

## 记忆类型的操作性定义

episodic、semantic、procedural、working 这四个标签在后续各章反复出现。本节统一定义它们在 agent 系统中的操作含义。需要特别说明的是：这些术语来自认知科学，但其原始含义在移植到 agent 系统时发生了实质性的语义位移。本 survey 使用的是适配后的含义，与认知科学教材中的定义并不完全对应。

| 类型 | 认知科学原型 | Agent 系统中的操作含义 | lifecycle 主要阶段 |
| --- | --- | --- | --- |
| Episodic | 有时空标记的自传式事件，可被重新体验（re-experiencing） | 带 provenance（时间戳、主体、上下文）的观察记录；不要求可重新体验，要求可追溯；是写入长期层前最原始的事件形态 | formation（主写入期）、retrieval（时序查询） |
| Semantic | 去语境化的通用知识与概念，不含时空锚点 | 从多次 episodic 巩固而来的稳定偏好、事实、用户属性；被窄化为可提取的结构化事实，不包含 LLM 参数中的百科知识 | evolution（巩固产物）、retrieval（稳定事实查询） |
| Procedural | 隐性的操作技能（如骑车、打字），无法直接言说 | 显式的 skill、workflow、策略模板；与认知科学原型相反，agent 的 procedural 是可序列化、可载入、可更新的显式结构 | evolution（从 episodic 巩固或先验写入）、retrieval（按情境激活 skill） |
| Working | 容量有限的短时工作空间（约 7±2 组块） | 当前任务目标、待办、上下文板等活跃态；无容量上限约束，但有明确生命周期边界（任务或会话结束后归档或清除），常驻使用无需检索 | formation（active state 分层） |

### 三个关键语义位移

使用这些术语时，有三处与认知科学直觉的偏差值得特别注意：

1. **Procedural 从隐性到显式**：认知科学中的 procedural 是无法言说的身体技能；agent 系统中的 procedural 是可序列化、可载入、可更新的显式策略——两者共享名字，但工程含义完全不同。
2. **Semantic 范围被窄化**：认知科学中 semantic 涵盖所有去语境化知识；agent 系统中通常只指从用户交互中抽取的偏好和事实，不包含 LLM 参数中已编码的世界知识。
3. **类型是状态，不是永久标签**：同一条记忆可以跨类型迁移。一条 observation 先以 episodic 形式存在，巩固后变为 semantic，若形成稳定操作模式再变为 procedural。这正是 lifecycle 框架优于静态分类的核心理由——类型描述记忆在某一时刻的形态，而非其永久属性。

各类型如何在 lifecycle 各阶段具体运作，详见对应章节（02-formation、03-evolution、04-retrieval）。

### 与经典认知架构的对照

上述四类记忆标签来自认知科学，而认知科学中已有成熟的计算建模传统——特别是 ACT-R 和 Soar 两大认知架构。它们各自包含了 working memory、declarative memory（对应 episodic + semantic）和 procedural memory 的形式化模型，并通过激活传播（spreading activation）和冲突解决机制将记忆与行动绑定。本 survey 的 lifecycle 框架与这些经典架构有继承也有偏离，值得明确。

| 维度 | ACT-R | Soar | 本 survey 的 lifecycle 框架 |
| --- | --- | --- | --- |
| 记忆分类 | declarative（chunk）+ procedural（production rule） | working memory + long-term（semantic / episodic / procedural） | episodic / semantic / procedural / working，按操作含义重新定义 |
| 核心机制 | 基于激活值（base-level + spreading）的检索 | impasse-driven chunking 与 elaboration | formation → evolution → retrieval → evaluation 的显式生命周期 |
| 学习方式 | 声明性编码 + 程序化编译（knowledge compilation） | chunking（从 impasse 解决中提取新 production） | 从 episodic 巩固为 semantic/procedural，或由可学习策略驱动 |
| 遗忘 | 基于激活衰减（power law of forgetting） | 无内建遗忘机制 | 显式治理：relevance decay、summarization、revocation |
| 行动耦合 | production 匹配触发行动 | operator proposal → selection → application | 通过 agentic thinking 层耦合，memory 提供状态而非直接触发行动 |

**继承了什么**：记忆类型的基本划分（episodic / semantic / procedural / working）、激活传播作为检索机制的思路（Synapse 即此路线）、以及"经验可以巩固为可复用规则"的核心洞察。

**偏离了什么，以及为什么**：经典认知架构把记忆嵌入固定的认知循环（ACT-R 的 production cycle、Soar 的 decision cycle），记忆的行为由架构约束决定。而 LLM-based agent 系统中，记忆更像是松耦合的外部状态层——没有固定的匹配-执行循环，检索不靠激活值公式而靠 embedding 相似度或图查询，巩固不靠 knowledge compilation 而靠 LLM 生成的摘要或抽象。这种差异不是退步，而是因为 LLM agent 的"推理引擎"本身就是通用语言模型，不需要也不适合硬编码认知循环。lifecycle 框架正是在这个背景下提出的：它保留了认知架构"记忆有生命周期"的核心直觉，但用工程可操作的阶段划分（何时写、如何更新、如何读、如何评估）替代了形式化的认知循环。

## 知识图谱与 Agent Memory 的定位

知识图谱（Knowledge Graph，KG）在 agent memory 文献中频繁出现，但两者的关系常被混淆。本节明确其定位：KG 是 agent memory 系统中的一种**存储与检索基础设施**，而非 memory 系统的替代框架。

### 核心区别

| 维度 | 传统知识图谱 | Agent Memory 系统 |
| --- | --- | --- |
| 核心关注 | 实体与关系的结构化表示 | 经验的存储、演化与检索全生命周期 |
| 时间性 | 通常为静态快照 | 必须处理时序演化、遗忘、巩固 |
| 记忆类型 | 单一（事实三元组） | 多类型：episodic、semantic、procedural、working |
| 检索目标 | 精确查询（多跳推理、SPARQL） | 上下文相关性（融合 recency、importance、relevance） |
| 数据来源 | 预定义 schema 与结构化抽取 | Agent 交互中动态产生的非结构化经验 |
| 评价标准 | 图的完备性、查询准确率 | 记忆对 Agent 行为的实际影响 |

### KG 在 Memory 系统中的价值

KG 作为 memory 的结构化存储层，在以下场景有明确优势：

- **关系追踪**：实体间关系需要显式建模时（人物、事件、因果链）
- **时序推理**：跨 session 的时间依赖，Zep 和 Graphiti 的 temporal KG 是代表性实现
- **多跳检索**：单次 embedding 查询无法覆盖的关联链
- **溯源与解释**：需要回答「为什么」时，图的路径比向量距离更可解释

本项目 `src/memory/graph_store.py` 即为此路线的实现：用 NetworkX 存储实体-关系-实体三元组，由 `manager.py` 与 vector store、episodic store 并列编排，结果通过 rank-based fusion 统一合并。

### KG 不能替代 Memory 系统的理由

KG 覆盖不到 memory lifecycle 的核心议题：

1. **记忆巩固**：episodic 如何演化为 semantic/procedural，KG 无内建机制
2. **遗忘与衰减**：importance 衰减和 temporal decay 策略，KG 不处理
3. **多 store 融合**：把 graph、vector、episodic 结果按相关性统一排序的编排层，在传统 KG 中不存在
4. **行为评测**：记忆对 agent 决策的影响评估，而非图的完备性度量

**结论**：KG 是 agent memory 的重要组件（尤其在关系推理和时序追踪上），但 agent memory 的范畴远大于 KG。选择 KG 路线是 storage/retrieval 层的工程决策，不是 memory system 的架构选择。


## 本章主要证据来源

- `paper`：`Memory in the Age of AI Agents: A Survey`
- `blog`：用于补充 agentic thinking、工程实现与方法论争议
- `DeepResearch`：仅作线索

## 为什么生命周期比静态分类更有效

生命周期框架能直接描述写入、更新、读取和治理四个接口，因此比静态分类更适合解释新工作。

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
  边界说明：支撑"检索足够成熟但不等于全部 memory"的判断，不支撑 belief 管理已解决。
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

## 代表工作定位与证据来源

### 代表工作定位

- `Mem0 / LangMem`：代表 retrieval-centric memory service，说明为什么 memory 不能被压缩成单一检索问题。
- `Hindsight`：代表 belief-aware memory management，说明 evidence、belief 和 update semantics 应分层。
- `Recursive Language Models`：代表程序化 working memory，说明部分"记忆使用"本质上是可编程状态操作。
- `MemSkill`：代表 procedural memory 与 learned skill 的连接，说明经验可以沉淀为可复用策略。
- `From "Reasoning" Thinking to "Agentic" Thinking`：作为工程补充，帮助定义 reasoning 到 agentic 的问题迁移。

### 证据来源

- `paper`：Mem0、Hindsight、Recursive Language Models、MemSkill、`Memory in the Age of AI Agents: A Survey`。
- `blog`：`From "Reasoning" Thinking to "Agentic" Thinking`，以及工程界关于 stateful agents、context engineering 与 memory management 的材料。
- `综合推断`：Memory、Agentic Thinking 和 Skill 应被视为状态层、控制层与程序化策略层的分工，这是基于现有论文证据与工程趋势做出的组织性判断。

### 对本项目的约束

这个框架给本项目增加了三个直接约束：

1. Survey 仍按 lifecycle 组织 memory 主线，但在本章明确区分状态层、控制层和程序化策略层的边界，后续章节聚焦 memory layer。
2. 讨论 memory 时，不再把它缩减成 retrieval，也不把它泛化成整个 agent loop。
3. 讨论 skill 时，优先把它放在 `procedural memory / reusable policy` 的位置，而不是当作杂项工具集合。
