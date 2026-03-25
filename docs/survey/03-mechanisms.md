# Agent Memory 管理机制

> v1.0 | 2026-03-24

## 1. 概述

Agent Memory 的管理不仅仅是存取，而是一个完整的生命周期：**形成 → 演化 → 检索**。本文档深入分析每个阶段的机制和最新进展。

---

## 2. 记忆形成 (Formation)

### 2.1 信息提取

从 Agent 的交互轨迹中提取值得记忆的信息：

- **全量存储**: 保留完整交互历史（简单但不经济）
- **选择性存储**: LLM 判断信息重要性后存储
  - A-MEM: LLM 自动为新信息创建结构化笔记（标题、标签、内容、链接）
  - AgeMem: Agent 通过 RL 学习何时触发 Store 动作
- **事件驱动存储**: 特定事件（成功/失败/惊讶）触发记忆创建
  - MemRL: 任务成功/失败后更新情景记忆

### 2.2 结构化表示

提取的信息需要转化为可存储、可检索的格式：

| 表示形式 | 示例 | 适用场景 |
|---------|------|---------|
| 原始文本 | 对话记录原文 | 简单回溯 |
| 嵌入向量 | sentence-transformers 编码 | 语义检索 |
| KV 对 | Transformer KV cache 压缩 | MSA, MemoRAG |
| 结构化笔记 | {标题, 内容, 标签, 链接} | A-MEM |
| 知识三元组 | (实体, 关系, 实体, 时间) | Zep/Graphiti |
| 记忆树节点 | {内容, 摘要, 子节点} | MemWalker |

### 2.3 索引构建

- **向量索引**: FAISS/ChromaDB/Milvus，支持 ANN 检索
- **图索引**: 知识图谱 + 实体链接
- **分层索引**: 记忆树、层次化摘要
- **混合索引**: A-MEM 的向量 + 图链接组合

---

## 3. 记忆演化 (Evolution)

### 3.1 巩固 (Consolidation)

将短期/情景记忆转化为长期/语义记忆：

**类比人类**: 海马体中的情景记忆通过睡眠期间的重放（replay）逐步转移到新皮层的语义记忆中。

- **LightMem** (2025): "睡眠时间"巩固
  - 离线过程：总结和压缩积累的情景记忆
  - 结果：准确率提升 10.9%，token 使用减少 117x
  - 关键创新：将巩固与在线推理解耦

- **ACT-R 启发架构** (HAI'25):
  - 复现人类记忆特征：重复引用的主题被选择性强化
  - 不常用的记忆逐渐衰减

- **"From Storage to Experience"** (ICLR'26):
  - 提出三阶段演化框架: Storage → Reflection → Experience
  - Reflection: 对轨迹进行自我评估和模式提取
  - Experience: 将模式抽象为可复用的策略

### 3.2 遗忘 (Forgetting)

并非所有信息都值得永久保留，选择性遗忘是必要的：

- **基于衰减的遗忘**: 记忆随时间衰减，长期不访问的记忆被清理
  - 指数衰减: `relevance(t) = base_score * exp(-λ * (now - last_access))`
  - 幂律衰减: `relevance(t) = base_score * (1 + t)^(-α)` （更符合人类记忆曲线）

- **基于容量的遗忘**: 达到存储上限时淘汰最不重要的记忆
  - LRU (最近最少使用)
  - 基于重要性评分的淘汰

- **RL 驱动的遗忘**: Agent 学习何时丢弃
  - AgeMem: Discard 作为可学习的工具动作
  - 通过 RL reward 信号学习最优丢弃策略

### 3.3 压缩 (Compression)

在不丢失关键信息的前提下减少记忆占用：

- **摘要压缩**: LLM 对旧记忆生成摘要替换原文
  - LangChain Summary Memory: 超过阈值时自动摘要
  - MemGPT/Letta: Agent 自主决定何时压缩

- **合并压缩**: 将相似记忆合并为高层抽象
  - SimpleMem: 相关记忆单元合成为高层表示
  - 去噪：压缩重复或结构相似的经验

- **KV 压缩**: 在隐状态空间压缩
  - MSA: chunk-wise mean pooling 压缩 KV 矩阵
  - MemoRAG: KV 压缩创建全局记忆

- **RLM 的隐式压缩**: 通过递归处理，中间结果存储在 REPL 变量中而非上下文中

### 3.4 更新 (Updating)

当新信息与旧记忆矛盾或需要修正时：

- **覆盖更新**: 新信息替换旧信息（简单但可能丢失历史）
- **版本化更新**: 保留历史版本，标记时间有效期
  - Zep/Graphiti: 知识图谱的非有损动态更新
  - AgentOrchestra/TEA: Version Manager 维护演化历史
- **上下文触发更新**: 新记忆整合触发相关旧记忆的更新
  - A-MEM: 新笔记链接到旧笔记时，更新旧笔记的上下文表示

---

## 4. 记忆检索 (Retrieval)

### 4.1 向量检索 (Vector Retrieval)

- **机制**: 将查询和记忆编码为稠密向量，计算余弦相似度
- **工具**: FAISS, ChromaDB, Milvus, Pinecone
- **优势**: 语义理解好，对同义改写鲁棒
- **劣势**: 缺乏结构感知，难以处理多跳推理
- **增强**: Reranking (交叉编码器重排)、HyDE (假设文档嵌入)

### 4.2 图检索 (Graph Retrieval)

- **机制**: 在知识图谱上进行结构化遍历
- **方法**:
  - 全文搜索（词汇相似）
  - 余弦相似度（语义相似）
  - BFS/DFS（图结构相似）
- **代表**: Zep/Graphiti (三种搜索组合), LightRAG (双检索器)
- **优势**: 能捕捉实体关系、支持多跳推理
- **劣势**: 图构建和维护成本高

### 4.3 层次化检索 (Hierarchical Retrieval)

- **机制**: 从粗到细逐层缩小搜索范围
- **代表**:
  - MemWalker: 记忆树导航 + 回溯
  - MemGAS: 多粒度自适应检索
  - MemR3: 全局证据差距跟踪器路由不同检索动作
- **优势**: 效率与精度的良好平衡
- **劣势**: 树/层次结构的构建和维护

### 4.4 稀疏注意力路由 (Sparse Attention Routing)

- **机制**: 在注意力层内部完成检索和生成
- **代表**: MSA 的 Router Projector + top-k 选择
- **优势**: 端到端可训练，检索与生成无缝整合
- **劣势**: 需要修改模型架构

### 4.5 Agent 自主检索 (Agentic Retrieval)

- **机制**: Agent 通过工具调用主动决定检索策略
- **代表**: AgeMem (Retrieve 作为工具动作), MemGPT (自编辑)
- **优势**: 最灵活，可适应不同场景
- **劣势**: 依赖 Agent 的检索决策质量

---

## 5. 端到端优化

传统记忆系统的一个核心问题是**检索与生成的目标不对齐**：检索优化相似度，生成优化下游任务。

新趋势是端到端优化记忆管道：

- **MSA**: 检索（路由）和生成在同一注意力机制中，通过 L_aux 联合优化
- **MemAgent (RL)**: 通过 RL 的 reward 信号反向优化记忆策略
- **MemoRAG (RLGF)**: 从生成质量反馈到记忆模块
- **Memory-R1**: RL 框架训练双 Agent 协同优化记忆管理

---

## 参考文献

- A-MEM (arXiv:2502.12110)
- AgeMem (arXiv:2601.01885)
- LightMem (arXiv:2510.18866)
- MemWalker (arXiv:2310.05029)
- MSA (Memory Sparse Attention)
- "From Storage to Experience" (ICLR'26 MemAgents)
