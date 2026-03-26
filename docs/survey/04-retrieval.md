# Retrieval：记忆读取与上下文装配

> v3.0 | 2026-03-26

## 本章核心判断

Retrieval 不是“从库里 top-k 拿几条最相似文本”这么简单。对 agent 来说，retrieval 真正解决的是三件事：

1. 在当前任务下，哪些记忆值得被读取。
2. 这些记忆应以什么顺序、粒度和表示进入当前推理回路。
3. agent 是否真的用上了这些记忆，而不是把它们静静塞进 prompt。

当前研究之所以热衷 retrieval，是因为这里最容易量化，也最容易做基准；但也因此，这一阶段最容易被误认为 memory 的全部。

## 读取机制的四条主线

### 1. 向量与混合检索

这是工程界最主流的路线。向量检索解决语义相似，keyword 与 metadata filter 提供可控约束，时间过滤与 reranking 提升结果质量。Elastic 的 managed memory 方案基本代表了这一路线的成熟工程形态：先按主体、角色、时间、memory type 过滤，再做 hybrid retrieval。

这条路线的优势是可部署、可解释、与现有数据系统兼容。缺点也明确：

- 语义相似不等于任务相关。
- 时间与关系若不显式建模，复杂推理容易失败。
- top-k 是固定预算，而真实任务需要的是自适应证据量。

### 2. 图检索

Zep、Graphiti 以及图记忆综述类工作主张将长期记忆组织成实体、关系和时间链，读取时进行多跳或邻域扩展。其真正价值不在“图很高级”，而在于它显式暴露了语义连接、时序依赖和对象身份。

图检索在以下任务上尤其自然：

- 关系追踪。
- 时间顺序问题。
- 多实体、多跳推理。
- belief 与 observation 的追根溯源。

但图的代价也高：构图成本、异步更新、即时可用性、索引延迟和系统复杂度都显著更重。很多图系统的实际问题不是答案质量，而是 ingestion 到可检索之间的工程时延。

### 3. 层次化、路由式和 agentic retrieval

MemWalker、MemAgent、RLM、MSA 在表面机制上很不一样，但它们共享一个核心思想：不是一次性把所有历史塞进上下文，而是让系统逐步决定要不要继续取、取多少、从哪里取。

这里存在三个层次的控制权差异：

- `system-routed`：外部规则决定先检索哪一层，再检索哪一层。
- `model-routed`：注意力路由或 learned router 决定哪部分记忆参与生成。
- `agent-routed`：agent 通过工具调用或代码生成主动展开读取链。

RLM 的关键贡献，是把“读取记忆”转化为“编程式操纵上下文与变量”；MSA 的关键贡献，是把 retrieval 进一步内化为可训练稀疏注意力。两者都在弱化固定 top-k 的传统范式。

### 4. 活跃态 + 长期态

这是目前最具工程价值、却常被学术叙事低估的一条分层：将当前目标、近期决策、待办、工作上下文放进 always-loaded active state，而把稳定知识和远期历史放进长期库。许多系统表面上的 retrieval 成功，其实首先依赖 active state 把真正重要的当前上下文固定住了。

这一层若缺失，长期库就不得不频繁承担短期状态读取，最终会把召回质量和上下文预算一起拖垮。

## Retrieval 真正难在哪里

### 1. 相关性不是单一分数

对 agent 任务而言，相关性至少包括：

- 语义相似。
- 时间接近性。
- 任务当前目标的因果相关性。
- 数据来源可信度。
- 是否已经被较新记忆覆盖。

单一 embedding similarity 难以同时编码这些维度。因此，成熟系统通常会叠加 metadata、time, recency, role, confidence, graph neighborhood 或 belief score。

### 2. 读取量应当自适应

固定 top-k 是最方便的接口，但不是最好的 memory policy。复杂任务需要多轮证据展开，简单任务只需极少上下文。MSA 的 Memory Interleave、RLM 的递归子调用，本质上都在说明：读取预算应该由任务状态动态决定。

### 3. 读取结果必须能被消费

这也是 retrieval benchmark 最大的盲点之一。系统可能召回了正确证据，但 agent 没有把它整合进决策。问题可能出在：

- prompt 装配不当。
- 证据格式不适合模型消化。
- active state 与 archival state 冲突。
- 工具调用链中断。

因此，“能检索到”与“被真正用到”不是同一件事。

## 代表工作比较

### Mem0 / LangMem 路线

强在轻量、易部署、抽取式记忆适合用户偏好和稳定事实；弱在多跳、时间链、belief 冲突和复杂 evidence tracing。

### Zep / 图记忆路线

强在 temporal reasoning 与关系显式化；弱在构图和更新成本，且系统工程复杂度更高。

### Letta / memory OS 路线

强在把 memory management 暴露成 agent 行为的一部分；弱在行为环开销和调试复杂度。

### RLM / MSA 路线

强在长上下文和程序化/内生读取；弱在治理、权限、删除、跨会话审计等外部系统问题仍未充分解决。

## 工程含义

本章给出的工程判断是：

1. 不要把 retrieval 设计成单一数据库查询接口。
2. 把 active state 当成一级组件，而不是 prompt 拼装细节。
3. 对复杂任务，优先考虑分层或迭代式读取，而非固定 top-k。
4. 若系统需要解释性、时间推理或实体关系，图或显式结构值得引入。

换句话说，retrieval 的核心不是“搜得准”，而是“让 agent 在正确时刻拿到正确表示的记忆，并真正据此行动”。

## 代表工作定位

- `Mem0 / LangMem`：代表主流外部检索与抽取式长期记忆。
- `Zep / Graphiti`：代表关系和时间显式化的图检索路线。
- `Letta / MemGPT`：代表 memory management 被 agent 工具化与显式化。
- `RLM`：代表程序化上下文访问与递归式 retrieval。
- `MSA`：代表把 retrieval 内化为稀疏注意力与 learned routing。

## 本章主要证据来源

- `paper`：Mem0、RLM、MSA、图记忆综述、Letta/MemGPT 相关工作。
- `blog`：Elastic 的 hybrid retrieval 实践、benchmark 对比文章。
- `综合推断`：retrieval 的核心是“memory in use”，而不是单次 top-k 命中率。
