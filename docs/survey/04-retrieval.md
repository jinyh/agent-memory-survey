# Retrieval：记忆读取与上下文装配

> v2.0 | 2026-03-25

## 关注问题

Retrieval 不只是 top-k 检索，而是“agent 如何找到、理解并使用记忆”。

## 主要机制

### 1. 向量与混合检索

- 适合高召回的语义相似搜索
- 企业实现通常叠加 keyword、metadata filter 和时间过滤

### 2. 图检索

- 适合实体关系、时间链与多跳推理
- Zep、Graphiti、TeleMem、Graph-based surveys 都把图作为长期记忆骨架

### 3. 层次化和路由式读取

- MemWalker、RLM、MSA、MemAgent 的共同点都是避免“一次把所有历史塞进上下文”
- 关键差别在于读取控制权归谁：系统规则、模型注意力、还是 agent 自主工具调用

### 4. 活跃态 + 长期态

- 对当前优先级、近期决策、活跃项目，应优先用 always-loaded active state
- 对稳定知识和远期历史，使用长期检索
- 这条分层是当前工程实践里最容易落地、也最容易被忽视的改进
