# Agent Memory 内核 v1 实施计划（单 Agent 本地）

> v1.1.0 | 2026-03-26 — Claude Code 审计修订版

## Summary
目标是在不引入 BMAD 重型安装/IDE 体系的前提下，把现有原型升级为”可比较检索 + 可恢复持久化 + 可重复评测”的 Memory 内核。
基于现状实现，优先修改 `src/memory/manager.py`、`src/memory/graph_store.py`、`tests/test_memory.py`。

## 审计修订（2026-03-26）

原计划由 Codex 基于 BMAD-METHOD 项目总结产出，Claude Code 审计后补充以下修正：

1. **FusionConfig 实现形式**：明确为 dataclass，放在 `base.py` 中与 `MemoryItem` 并列。
2. **Graph 边序列化多态**：`linked` 边只有 `created_at`，`tag_overlap` 边还有 `shared_tags`(list)。序列化统一为 `{source, target, relation, attrs: dict}`。
3. **评测 ground truth**：`hit@k`/`mrr` 需要每个 query 附带 `expected_ids` 作为正确答案。
4. **Store 序列化接口**：各 store 新增 `to_snapshot_dict()` / `from_snapshot_dict()` 方法。

## Implementation Changes
- 记忆融合策略（先做根因修复）
  - 在 `base.py` 新增 `FusionConfig` dataclass（`mode=”rank”`、`overfetch_factor=3`、`store_weights` 默认全 `1.0`）。
  - `recall()` 改为”各 store 先各取 `top_k * overfetch_factor`，再做 store 内 rank 归一化（`0~1`）”，最终分数 `fused_score = store_weight * normalized_rank`。
  - 保持 `recall()` 返回结构不变 `(MemoryItem, score, store_name)`，其中 `score` 改为 `fused_score`；新增 `recall_with_trace()` 返回调试信息（raw/rank/normalized/fused），供评测使用。
- 本地持久化与恢复语义（最小可用）
  - 在 `MemoryManager` 增加 `save_snapshot(path)` 与 `load_snapshot(path, strict=True, clear_before_load=True)`。
  - 快照统一 JSON 结构：`schema_version`、`manager`、`stores`、`created_at`。
  - `stores` 内每个后端通过 `to_snapshot_dict()` 导出全量数据；图存储额外保存边列表（统一 `{source, target, relation, attrs}` 格式）；情景存储额外保存 timeline。
  - `load_snapshot` 在 `strict=True` 时执行确定性校验：schema 版本、必填字段、ID 唯一性、graph 边端点存在性，不通过则抛错并拒绝部分加载。
- 可重复评测与产物输出
  - 新增 `src/memory/evaluation.py`（CLI）：固定 seed 构造小型场景，每个 query 附带 `expected_ids` 作为 ground truth。
  - 输出三类产物到指定目录：`report.json`（指标）、`report.md`（人读摘要）、`cases.jsonl`（逐 query 明细 + trace）。
  - 指标包含 `hit@k`、`mrr`、`store_distribution`、`snapshot_roundtrip_consistency`。

## Public API / Interface Changes
- `FusionConfig` dataclass（`base.py`）
- `MemoryManager.__init__(fusion_config: FusionConfig | None = None)`
- `MemoryManager.recall_with_trace(query, top_k=5, store_names=None, memory_type=None) -> dict`
- `MemoryManager.save_snapshot(path: str) -> dict`（返回 manifest 摘要）
- `MemoryManager.load_snapshot(path: str, strict: bool = True, clear_before_load: bool = True) -> dict`
- `MemoryStore.to_snapshot_dict() -> dict` / `MemoryStore.from_snapshot_dict(cls, data)` — 各 store 实现

## Test Plan
- 扩展 `tests/test_memory.py`：
  - 新增”跨 store 分数不可比”回归用例，验证 rank 融合后 top-k 稳定且不被单一 store 分数尺度劫持。
  - 新增快照 roundtrip 用例：保存→清空→恢复后，`total_memories`、关键 query 的 top1/top3 一致。
  - 新增 strict 校验失败用例：破坏 schema 或 graph 边，断言 `load_snapshot` 抛错。
  - 新增评测 CLI 冒烟测试。
- 运行命令（验收基线）：
  - `uv run --active --extra dev pytest tests/test_memory.py -q`
  - `uv run --active python -m src.memory.evaluation --out docs/memory-eval/latest`

## Assumptions & Defaults
- v1 仅支持单进程、单 Agent、本地文件系统；不处理并发写入冲突。
- `VectorMemoryStore` 若启用，使用当前模型与 embedding 结果，不做跨模型兼容迁移。
- 本阶段不改 BMAD 安装器/IDE 适配能力，不改 `references/indexing.py` 的规则体系（该项后续独立治理）。
