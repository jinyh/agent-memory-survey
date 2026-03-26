# Agent Memory 统一研究框架

> v2.0 | 2026-03-25

## 核心判断

Agent Memory 不再适合只按“工作记忆 / 情景记忆 / 语义记忆 / 程序性记忆”静态分类。2025-2026 年的研究更稳定的组织方式，是把记忆视为一个持续运行的生命周期系统：

`Formation -> Evolution -> Retrieval -> Evaluation`

这个主线可以同时容纳：

- 学术机制：如 MSA、RLM、MemAgent
- 系统框架：如 Letta、Mem0、Zep、Hindsight、TeleMem
- 工程实现：memory service、活跃态文档、数据库融合、访问控制
- 多模态前沿：视频记忆、空间记忆、具身推理

## 三个正交维度

### 1. 记忆形式

- `external`：向量库、图数据库、文件系统、结构化数据库
- `latent`：隐状态、KV、稀疏注意力、压缩表征
- `parametric`：模型参数内化
- `hybrid`：多种形式协同

### 2. 记忆功能

- `working`
- `episodic`
- `semantic`
- `procedural`
- `multimodal_spatial`

### 3. 记忆生命周期

- `formation`：写入、抽取、结构化、索引建立
- `evolution`：巩固、更新、压缩、遗忘、版本化
- `retrieval`：检索、路由、上下文装配、agentic memory use
- `evaluation`：基准、任务表现、记忆管理质量、系统可靠性

## 为什么以生命周期为主线

- 新资料已经不只是在讨论“记忆存在哪里”，而是在讨论“如何写入、如何演化、如何被 agent 真正使用”。
- benchmark 争议说明，仅看 retrieval 已不足以评价 agent memory。
- 多模态和空间记忆进一步要求把 memory 当成持续维护的认知层，而不是简单外挂检索器。
