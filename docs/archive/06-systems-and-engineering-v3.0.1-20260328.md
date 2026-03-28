# Systems And Engineering：系统谱系与工程落地

> v3.0.1 | 2026-03-28
> Changelog: 增补 MEM 作为具身多尺度 memory system 的工程启发，补充 active state / archive 分层与 latency 约束的关联。

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
