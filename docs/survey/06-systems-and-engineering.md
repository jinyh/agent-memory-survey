# Systems And Engineering：系统谱系与工程落地

> v3.2.0 | 2026-03-30
> Changelog: 新增 MANN/NTM 历史前身定位；新增多智能体记忆（共享/隔离/一致性/ToM）小节。

## 本章核心判断

系统实现层面的真正趋势，不是“大家都在做 memory”，而是大家在围绕不同失败模式做不同补偿。有人想降低 token 和延迟，有人想显式管理 belief，有人想把 memory 变成 OS，有人想让模型原生具备超长工作记忆。理解这些系统，关键是看它们在补哪一类缺口。

## 研究矩阵：主要系统路线怎么取舍

| 系统路线 | 核心 substrate | 控制权中心 | 优势 | 局限 | 当前证据强度 |
| --- | --- | --- | --- | --- | --- |
| 抽取式 memory service | vector + metadata + fact store | 外部服务与规则引擎 | 上手快，最适合产品化起步 | 难处理 belief、复杂演化与多跳依赖 | 高 |
| 图 / 时序 backbone | graph + temporal edges | 图层与同步管线 | 关系与时序可显式建模，便于追溯 | ingestion、同步、维护成本高 | 中 |
| Memory OS / 分层上下文 | active state + archive + paging | agent 自身与控制平面 | 把记忆使用变成显式行为 | 行为稳定性与调试成本是门槛 | 中 |
| belief-aware 多网络 | evidence / opinion / world / experience 分层 | memory object schema | 更适合冲突修正与解释 | 实现复杂，标准评测覆盖不足 | 中 |
| 原生长记忆 / 程序化 working memory | latent state、REPL、稀疏注意力 | 模型内部或程序环境 | 超长任务潜力强，working memory 表达丰富 | 企业级治理与隔离仍不成熟 | 中 |

## 关键概念与代表引用

- memory service
  本文语义：把 memory 封装为抽取、更新、检索和过滤的外部服务。
  主代表引用：`Mem0`
  证据类型：`主证据`
  边界说明：支撑产品化起步路径，不支撑 belief-aware 演化已充分解决。
- memory OS
  本文语义：把 memory paging、active state 与 archive 管理暴露给 agent 自身。
  主代表引用：`Letta / MemGPT`
  证据类型：`主证据`
  边界说明：支撑 memory management 进入 agent control loop，不支撑低延迟与高稳定性天然兼得。
- belief-aware architecture
  本文语义：事实、经验、总结和 belief 需要结构化分层。
  主代表引用：`Hindsight is 20/20: Building Agent Memory that Retains, Recalls, and Reflects`
  证据类型：`主证据`
  边界说明：支撑 conflict correction 与可解释性，不支撑公共 benchmark 已跟上。
- programmatic working memory
  本文语义：工作记忆可以由程序和 REPL 显式管理。
  主代表引用：`Recursive Language Models`
  证据类型：`主证据`
  边界说明：支撑 recursive/programmatic route，不支撑企业级治理能力。
- native long-memory mechanism
  本文语义：部分 memory function 可以内化为稀疏注意力或 latent substrate。
  主代表引用：`MSA: Memory Sparse Attention for Efficient End-to-End Memory Model Scaling to 100M Tokens`
  证据类型：`主证据`
  边界说明：支撑原生长记忆机制，不替代外部 control plane。
- control plane
  本文语义：权限、过滤、版本与路由是 memory architecture 的系统控制面。
  主代表引用：`BMAM: Brain-inspired Multi-Agent Memory Framework`
  证据类型：`工程补充`
  边界说明：支撑 brain-inspired architecture 作为补充路线，不承担本章最核心主线。

## 历史前身：Memory-Augmented Neural Networks

当前 agent memory 系统并非凭空出现。2014-2016 年间，Neural Turing Machine（NTM）和 Differentiable Neural Computer（DNC）开创了"让神经网络拥有可读写外部记忆"的研究方向。它们的核心思想——用可微的 attention 机制实现对外部记忆矩阵的寻址、读取和写入——与今天的 agent memory 系统在动机上一脉相承。

但两代系统之间存在结构性断裂：NTM/DNC 的记忆是连续向量空间中的低维矩阵，通过端到端梯度训练；当前 agent memory 系统的记忆是离散的自然语言文本或结构化知识，通过 LLM 生成和检索操作。这个断裂不是技术退步，而是因为 LLM agent 的推理引擎本身已经足够强大，不需要在参数空间中学习记忆操作——用自然语言作为记忆表示反而带来了可解释性、可编辑性和可审计性的优势。MSA 的 sparse attention 路线可以被视为对 NTM 传统的部分回归：它让模型内部重新承担一部分 memory function，但规模和机制已经与 NTM 的小矩阵完全不同。

## 一条粗略但有用的系统谱系

### 1. 抽取式 memory service

代表：Mem0、LangMem，以及大量企业侧个性化 memory 服务。

其共识是：

- 长期记忆不应等于原始聊天日志。
- 应先抽取 salient facts，再入库。
- 使用 vector + metadata + update policy 进行维护。

这条路线的最大优点是落地快、系统边界清晰，特别适合客服、助理、个性化问答、销售等场景。它也是今天多数团队最现实的起点。

它的短板同样稳定：

- belief 与 evidence 往往未充分区分。
- 对时间演化、多跳依赖和复杂任务链支持有限。
- memory 被视作 service，而不是认知控制层。

### 工程 blog 的价值与边界：retrieval-centric memory 的入门框架

这类工程 blog 往往采用一条非常容易被工程师接受的主线：context window 负责短期工作状态，external store 负责跨会话持久化，vector retrieval 负责按需召回，episodic log 负责沉淀过往任务经验，再辅以 importance scoring、recency decay 与 consolidation 等启发式策略维持系统可用性。`Agentic Memory: A Detailed Breakdown` 是这一写法的代表案例。它的价值不在于提出新的研究框架，而在于把 retrieval-centric memory system 的最小可运行形态讲得足够清楚，因此很适合作为工程入门材料和 baseline 架构参考。

这类 blog 之所以值得保留，不只是因为它们写得清楚，还因为它们代表了工程界对 Agent Memory 最自然的一种直觉：把 memory 理解为 retrieval-enhanced persistence，也就是在有限上下文之外补上一层可检索、可追加、可压缩的长期状态。这个视角解释了为什么第一代 memory system 会优先围绕 context overflow、semantic retrieval、episodic reuse 和 lightweight forgetting 展开，也解释了为什么许多产品化方案会先落在 vector + metadata + summary 这条路线。

但它的边界也同样明显。首先，这类框架通常会把 memory 的核心问题压缩成“如何把相关内容取回来”，因此更擅长解释 retrieval、context management 与轻量级 personalization，却较少处理 formation policy、version semantics、belief correction、deletion / revocation、tenant isolation 与 auditability 等长期部署问题。其次，它容易把 memory loop 近似为“调用前检索、调用后写入”的 read/write 闭环，从而弱化 evolution 与 evaluation 在 memory lifecycle 中的独立地位。也正因此，这类 blog 更适合作为工程补充和 baseline 描述，而不宜替代以 `formation -> evolution -> retrieval -> evaluation` 为主线的 lifecycle 框架。

换句话说，这类 blog 提供了一个很好的第一代工程视角：memory 作为 retrieval-enhanced state persistence；而当前更重要的问题已经转向 memory 如何成为可更新、可治理、可评估的状态管理与控制层。把它们放在 systems 章节里阅读是有价值的，但前提是明确它们解释的是“工程起步形态”，而不是 memory architecture 的终局。

### 2. 图与时序 memory backbone

代表：Zep / Graphiti，以及图记忆相关工作。

这条路线赌的是：长期记忆的核心不是“语义相似文本搜索”，而是对象、关系和时间。它在处理 temporal reasoning、entity-centric queries、多跳路径时更自然，也更利于解释与追溯。

但代价是工程复杂度更高，且 ingestion、graph build、background sync 的系统设计要求显著增加。它更像是长期记忆的骨架层，而不是开箱即用的聊天增强。

### 3. Memory OS / 分层上下文管理

代表：MemGPT / Letta。

其关键思想是把 memory management 暴露给 agent 自身：主上下文像 RAM，长期档案像 disk，agent 决定何时 page in/out。这个方向的贡献，不只是多了一层 storage，而是把“如何使用记忆”变成显式行为。

这对研究很重要，因为它把 retrieval 从后台实现细节提升为 agent cognition 的一部分；但工程上它也带来更多循环开销、调试复杂度与 prompt 行为敏感性。

### 4. Belief-aware / 多网络系统

代表：Hindsight。

其结构真正值得注意的点，不是“四张网络”本身，而是它把事实、经验、观察、意见拆分成不同的 memory object。这样做的收益非常明确：belief 可以更新、解释和降权，而不用和客观事实混成一个文本池。

从长期系统角度看，这可能比单纯提升 retrieval 分数更重要，因为它直接影响系统如何处理冲突、解释行为和控制错误传播。

### 5. 原生长记忆与程序化工作记忆

代表：MSA、Recursive Language Models，以及其他长上下文原生 memory 机制。

这些工作共同说明，未来 memory 不必全部依赖外部数据库。模型内部的稀疏注意力、路由键、REPL 状态和递归程序，都可以承担一部分 memory function。它们对“working memory”尤其有启发。

但当前看，这条路线更擅长解决超长上下文推理，不一定已经解决了部署级 memory governance、multi-tenant isolation 和 explicit deletion 等问题。

## 工程侧已经形成的共识

### 1. 单一存储类型不够

今天比较成熟的系统通常不会只用一种 memory substrate。实际工程里常见的组合是：

- active state / summary document
- vector retrieval
- metadata filters
- optional graph layer
- audit log or event history

MEM 这类具身系统虽然不直接等同于生产型 memory service，但它提供了一个很重要的工程提醒：active state / archive 的分层不只发生在文本 agent 中，也会在多模态控制系统里重新出现。短期视频记忆更像高频工作状态，长期语言记忆更像压缩后的 archive state。这个分层的价值不只是语义清晰，而是直接关系到 latency 是否可控，以及策略在长时任务里会不会因为历史过长而出现训练-推理分布漂移。

这背后不是“堆技术”，而是不同子系统在服务不同 memory function。

### 2. 访问控制与隔离不是企业附加需求

Elastic 的实践说明，memory 很快会碰到 identity-aware retrieval、tenant isolation、role-based filtering 等问题。这不是部署之后才出现的需求，而是只要 memory 跨 session、跨角色就会出现的基础要求。

### 3. latency、token 与可更新性是三角关系

外部检索越丰富，推理链越长，解释性越强，通常也意味着更高延迟和更复杂的同步成本。相反，极简记忆方案速度快，但对时间性、版本化和复杂任务支持弱。系统设计本质上是在这三者间找平衡。

## 多智能体记忆：共享、隔离与一致性

随着多 agent 协作成为主流范式，memory 系统面临的一个新维度是：多个 agent 之间的记忆如何共享、同步和隔离。当前 survey 覆盖的工作中，AgentOrchestra（TEA 协议）、MIRIX 和 MAGMA 涉及这个方向，但系统性讨论仍然不足。

多智能体记忆的核心问题可以归纳为三个：

1. **共享 vs. 隔离**：哪些记忆应该跨 agent 可见（共享的任务目标、环境观察），哪些应该隔离（agent 的内部 belief、策略偏好）。AgentOrchestra 通过协议层定义了共享边界，但更细粒度的权限模型仍未成熟。
2. **一致性保证**：多个 agent 同时更新同一条记忆时，如何处理冲突？这在形式上类似分布式系统的一致性问题——强一致性代价高但安全，最终一致性更灵活但可能导致 agent 间 belief 分歧。当前没有工作系统性地处理这个问题。
3. **心智理论（Theory of Mind）的工程化**：一个 agent 不仅需要自己的记忆，还需要对其他 agent "知道什么"和"相信什么"建模。这在认知科学中对应 Theory of Mind，在工程上意味着维护他人 belief 的近似表示。当前 agent memory 系统几乎完全是单 agent 视角，尚未系统性地处理这个问题。

多智能体记忆的证据目前处于中低水平：有少量系统级探索，但缺少独立的 benchmark 和可对比的实验。随着多 agent 框架的普及，这很可能成为下一个需要系统性回答的 memory 问题。

## 对本仓库原型的启发

本仓库的 `src/memory/` 不应追求复制某个完整系统，而更适合作为研究型最小原型，用来验证几个高价值判断：

1. active state 与 archive 分层是否能明显改善当前上下文质量。
2. episodic 到 semantic 的最小巩固机制如何定义。
3. 更新与遗忘若没有 provenance，会在哪些地方立即出错。

## 本章结论

从工程角度看，memory layer 正在从“外挂检索器”演化为“状态管理与认知控制层”。不同系统的真实差异，在于它们把 control plane 放在哪里。凡是只强调 storage，而不处理 policy、evolution 和 governance 的方案，都更像 memory feature，而不是成熟 memory architecture。

## 代表工作定位

- `Mem0 / LangMem`：代表抽取式 memory service 的主流工程起点。
- `Zep / Graphiti`：代表图作为长期记忆骨架的路线。
- `Letta / MemGPT`：代表 memory OS 与分层上下文管理。
- `Hindsight`：代表 belief-aware 多网络系统。
- `Recursive Language Models`：代表程序化 working memory 与 recursive control。
- `MSA`：代表原生长记忆机制。
- `BMAM`：作为 brain-inspired memory architecture 的补充证据保留。
- `Elastic memory architecture`：代表生产级过滤、隔离、权限与 hybrid retrieval 的工程约束。
- `MEM`：作为补充证据保留，强调多尺度 memory system 中短期工作状态与长期压缩状态的工程分层，但不承担治理与控制面的主锚点。

## 本章主要证据来源

- `paper`：Mem0、Letta/MemGPT、Hindsight、Recursive Language Models、MSA、BMAM、图记忆综述等系统论文。
- `blog`：Elastic、Letta、benchmark 比较类工程文章，仅作工程补充。
- `综合推断`：memory layer 正在向 control plane 演化，是从系统分层与治理压力共同抽出的结论。
