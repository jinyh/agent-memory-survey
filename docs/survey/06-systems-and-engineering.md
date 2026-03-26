# Systems And Engineering：系统谱系与工程落地

> v3.0 | 2026-03-26

## 本章核心判断

系统实现层面的真正趋势，不是“大家都在做 memory”，而是大家在围绕不同失败模式做不同补偿。有人想降低 token 和延迟，有人想显式管理 belief，有人想把 memory 变成 OS，有人想让模型原生具备超长工作记忆。理解这些系统，关键是看它们在补哪一类缺口。

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

代表：MSA、RLM，以及其他长上下文原生 memory 机制。

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
