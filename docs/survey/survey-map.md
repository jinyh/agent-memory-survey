# Agent Memory Survey 证据地图

> v3.3 | 2026-03-27 — 新增 `survey ↔ code ↔ gap` 长期映射表

这份地图不是正文替代品，而是正文的索引层。它回答两个问题：

1. 某个 survey 模块主要对应 lifecycle 的哪个阶段。
2. 该模块对应的代码实现到了哪里，还缺什么。

## 按模块映射

| survey 模块 | 子模块/关键概念 | 对应代码 | 已实现什么 | 仍需完善什么 |
| --- | --- | --- | --- | --- |
| 01-framework | lifecycle 主线 | `src/memory/base.py`, `src/memory/manager.py`, `src/memory/agent.py` | 定义统一记忆接口、总调度器和最小 agent 闭环 | 缺少真正的控制平面与策略编排 |
| 02-formation | 写入选择 | `src/memory/base.py`, `src/memory/episodic.py`, `src/memory/manager.py`, `src/memory/agent.py` | 支持 episodic 写入、importance、tags、observe/learn 入口 | 缺少模型驱动的写入判定 |
| 03-evolution | 更新 / 巩固 / 遗忘 | `src/memory/manager.py`, `src/memory/episodic.py`, `src/memory/graph_store.py`, `src/memory/vector_store.py` | 支持 update/delete/consolidate/snapshot | 缺少版本化与 belief-aware 更新 |
| 04-retrieval | 向量 / 图 / 混合检索 / 分层路由 | `src/memory/episodic.py`, `src/memory/graph_store.py`, `src/memory/vector_store.py`, `src/memory/manager.py` | 支持三路检索与 rank fusion，可作为分层/路由式 retrieval 的最小骨架 | 缺少显式 active state、层次化路由与图推理 |
| 05-evaluation | benchmark 口径 | `src/memory/evaluation.py`, `tests/test_memory.py` | 可跑评测与报告输出，支持数据集 case 归一化 | 缺少更严格的 lifecycle benchmark |
| 06-systems-and-engineering | 分层治理 | `src/memory/manager.py`, `src/memory/graph_store.py`, `src/memory/vector_store.py` | 提供最小分层记忆骨架 | 缺少生产级隔离、审计、权限与成本治理 |
| 07-frontiers | 多模态 / 空间 / 安全 | `src/memory/evaluation.py`（仅评测侧相关） | 只覆盖少量数据集入口 | 尚未实现多模态、空间与安全能力 |

## 按系统映射

| 系统/工作 | Formation | Evolution | Retrieval | Evaluation | Systems | Frontier |
| --- | --- | --- | --- | --- | --- | --- |
| Mem0 | 高 | 中 | 高 | 高 | 高 | 低 |
| LangMem | 高 | 中 | 中 | 中 | 高 | 低 |
| Zep / Graphiti | 中 | 中 | 高 | 中 | 高 | 低 |
| Letta / MemGPT | 中 | 中 | 高 | 中 | 高 | 低 |
| Hindsight | 中 | 高 | 高 | 高 | 高 | 中 |
| MemAgent | 高 | 高 | 高 | 中 | 中 | 低 |
| RLM | 中 | 低 | 高 | 中 | 中 | 低 |
| MSA | 低 | 高 | 高 | 中 | 中 | 中 |
| TeleMem | 中 | 中 | 高 | 低 | 高 | 高 |
| Synapse | 中 | 高 | 高 | 中 | 中 | 中 |
| Elastic memory architecture | 高 | 中 | 高 | 中 | 高 | 低 |
| Think3D / GSMem / RenderMem | 低 | 中 | 高 | 低 | 中 | 高 |
| MemoryAgentBench | 低 | 低 | 低 | 高 | 低 | 中 |
| MemoryArena | 低 | 低 | 中 | 高 | 低 | 中 |
| AMA-Bench | 低 | 低 | 中 | 高 | 低 | 中 |

说明：

- `高/中/低` 表示该工作对该章节问题的相关度，不代表质量排名。
- 某些工作在单一阶段特别强，但不意味着它已经覆盖完整 memory lifecycle。

## 按子模块映射

| survey 模块 | 子模块/关键概念 | 对应代码 | 已实现什么 | 仍需完善什么 |
| --- | --- | --- | --- | --- |
| 04-retrieval | vector retrieval | `src/memory/vector_store.py` | 余弦相似度 + 时间衰减 | 缺少外部 ANN / 数据库级索引 |
| 04-retrieval | graph retrieval | `src/memory/graph_store.py` | tag / links / 邻居扩展 | 缺少路径推理与子图匹配 |
| 03-evolution | episodic→semantic consolidation | `src/memory/manager.py`, `src/memory/episodic.py` | 简单模式抽取与合并 | 缺少真正的摘要 / 抽象质量评估 |
| 03-evolution | update / delete | `src/memory/manager.py`, `src/memory/episodic.py`, `src/memory/graph_store.py`, `src/memory/vector_store.py` | 支持字段更新、删除与简单巩固 | 缺少 version semantics、provenance 和 belief-aware 更新 |
| 05-evaluation | LoCoMo / LongMemEval | `src/memory/evaluation.py` | 统一归一化为 retrieval case | 主要还是 retrieval hit 信号 |
| 05-evaluation | MemoryAgentBench / MemoryArena / AMA-Bench | `src/memory/evaluation.py` | 支持多轮 / 轨迹 / 背景拼接的 case 入口 | 仍不足以替代严格 formation / evolution 评测 |

## 章节主证据清单

### 01-framework

- `src/memory/base.py`
- `src/memory/manager.py`
- `src/memory/agent.py`

### 02-formation

- `src/memory/base.py`
- `src/memory/episodic.py`
- `src/memory/manager.py`
- `src/memory/agent.py`

### 03-evolution

- `src/memory/manager.py`
- `src/memory/episodic.py`
- `src/memory/graph_store.py`
- `src/memory/vector_store.py`

### 04-retrieval

- `src/memory/vector_store.py`
- `src/memory/graph_store.py`
- `src/memory/episodic.py`
- `src/memory/manager.py`

### 05-evaluation

- `src/memory/evaluation.py`
- `tests/test_memory.py`

### 06-systems-and-engineering

- `src/memory/manager.py`
- `src/memory/graph_store.py`
- `src/memory/vector_store.py`

### 07-frontiers

- `src/memory/evaluation.py`

## 维护规则

- `survey-map.md` 只记录已确认事实，不写推测。
- 先改 survey 正文，再更新 map。
- 当 survey 章节新增 / 重命名、`src/memory/*` 新增关键模块、或 benchmark 适配范围变化时，必须同步更新本文件。
- 大版本变更时先归档旧 map，再写新版本。

归档命名：`docs/archive/survey-map-v<major>.<minor>-YYYYMMDD.md`
