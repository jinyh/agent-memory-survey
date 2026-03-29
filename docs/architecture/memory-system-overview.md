# Agent Memory System — 全景概览

> v1.0.0 | 2026-04-27 — 初始版本

本文档是 `src/memory/` 的单一入口。任何读者（人或 AI 助手）读完这一篇，即可建立对该系统的完整心智模型。详细内容由各引用文档承载，本文只做导航与摘要。

---

## 1. 研究动机

这个 memory 系统不是通用存储库，而是**研究工件**——用于验证 RQ-001：

> 当前主流 agent memory benchmark 是否覆盖了 formation 和 evolution 阶段？若未覆盖，差距在哪里？

因此，系统的设计目标是「可比较检索 + 可恢复持久化 + 可重复评测」，而不是生产可用性。

→ 完整问题定义见 [`docs/plans/2026-03-26-memory-lifecycle-eval-research-brief.md`](../plans/2026-03-26-memory-lifecycle-eval-research-brief.md)

---

## 2. 生命周期框架

系统围绕四阶段生命周期组织：

```
formation ──► evolution ──► retrieval ──► evaluation
   │              │              │              │
 写什么        怎么变         怎么取         怎么测
```

| 阶段 | 含义 | 关键机制 |
|---|---|---|
| **formation** | 决定哪些信息值得写入记忆 | importance 阈值、episodic observe/learn |
| **evolution** | 已有记忆随新信息更新、巩固或遗忘 | update/delete/consolidate、snapshot |
| **retrieval** | 从多个 store 中取回相关记忆 | rank fusion（episodic + vector + graph）|
| **evaluation** | 量化系统质量，回答研究问题 | formation/evolution/retrieval 指标 + 报告输出 |

→ 理论框架详见 [`docs/survey/01-framework.md`](../survey/01-framework.md)

---

## 3. 模块地图

`src/memory/` 共 7 个文件：

| 文件 | 职责 | 关键接口 | 被谁依赖 |
|---|---|---|---|
| `base.py` | 数据契约层：`MemoryItem`、`MemoryStore` 抽象基类、`FusionConfig` | `MemoryItem`、`MemoryStore.search()` | 所有其他模块 |
| `episodic.py` | 基于时间顺序的情节记忆，支持 importance 过滤和 tag 索引 | `add()`、`search()`、`consolidate_to_semantic()` | `manager.py` |
| `vector_store.py` | 基于嵌入向量的语义相似度检索 | `add()`、`search(query_text)`、快照接口 | `manager.py` |
| `graph_store.py` | 基于实体关系图的结构化记忆，支持 tag_overlap 边 | `add()`、`search()`、`add_edge()` | `manager.py` |
| `manager.py` | 总调度器：多 store 注册、rank fusion 召回、快照持久化 | `recall()`、`recall_with_trace()`、`save_snapshot()`、`load_snapshot()` | `agent.py`、`evaluation.py` |
| `evaluation.py` | 评测 CLI：构造场景、计算指标、输出报告产物 | `run_evaluation()`、`export_memoryagentbench()` | 独立运行 / 测试 |
| `agent.py` | 最小 agent 闭环演示：observe → recall → learn | `SimpleMemoryAgent` | 仅用于演示，未纳入测试 |

---

## 4. 关键设计决策

以下三条决策定义了系统的核心行为，取舍与替代方案见 ADR：

1. **Rank fusion 而非 score fusion**：各 store 先独立检索 `top_k × overfetch_factor` 条，再归一化排名后加权合并为 `fused_score`。避免不同 store 分数量纲不一致导致的偏向问题。

2. **快照严格校验（`strict=True`）**：`load_snapshot` 默认拒绝部分加载——schema 版本不符、ID 重复、graph 边端点悬空均抛错。保证实验可复现，防止静默数据损坏。

3. **Ground truth 基于规则推导**：formation/evolution 场景的正确答案由明确写入规则（importance 阈值、冲突覆盖规则）机械推导，不依赖人工标注或 LLM-judge。保证评测可重复，与「无外网原型」约束一致。

→ 完整决策过程见 [`docs/architecture/2026-03-26-memory-lifecycle-eval-framework.md`](./2026-03-26-memory-lifecycle-eval-framework.md)

---

## 5. v1 边界

v1 明确**不在**支持范围内：

- **多进程 / 分布式**：所有 store 运行在单一 Python 进程内，无锁、无网络传输
- **多 agent 共享记忆**：无并发写入保护，无权限隔离
- **持久化后端**：仅支持本地 JSON 快照，无数据库
- **LLM-judge 评测**：不调用外部 API，不依赖模型打分
- **多模态输入**：仅支持文本

---

## 6. v2 方向

以下能力在 v1 中有意缺失，是下一轮研究的候选方向（来源：`survey-map.md` gap 列表）：

| 方向 | 对应 survey 模块 | 当前缺口 |
|---|---|---|
| 模型驱动的写入判定 | 02-formation | 缺少 LLM-based formation 决策 |
| 版本化与 belief-aware 更新 | 03-evolution | 只有覆盖式更新，无版本历史 |
| 层次化路由与图推理 | 04-retrieval | 无显式 active state、无多跳图推理 |
| 更严格的 lifecycle benchmark 接入 | 05-evaluation | 当前 benchmark 覆盖 retrieval 为主，formation/evolution 自建场景 |
| 多模态、空间与安全能力 | 07-frontiers | 尚未实现 |

→ 完整 gap 分析见 [`docs/survey/survey-map.md`](../survey/survey-map.md)
