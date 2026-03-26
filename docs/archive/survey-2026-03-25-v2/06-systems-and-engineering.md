# Systems And Engineering：系统谱系与工程落地

> v2.0 | 2026-03-25

## 代表系统谱系

- `Letta / MemGPT`：分层上下文与 OS 式 memory management
- `Mem0 / LangMem`：抽取式 memory service
- `Zep / Graphiti`：时序图记忆
- `Hindsight`：多网络、belief-aware 记忆分层
- `TeleMem / M3-Agent`：多模态、长时、图和缓存协同

## 工程侧共识

- memory 不是单一数据库类型
- 生产场景普遍需要向量、结构化元数据、访问控制、时间过滤和审计
- benchmark 表现之外，还要关注可更新性、隔离性、治理和成本

## 本仓库原型的定位

本仓库的 `src/memory/` 不追求实现上述系统，而是保留最小研究原型，用来演示：

- 活跃态 vs 长期态
- 情景到语义的巩固
- 检索、更新、遗忘的最小闭环
