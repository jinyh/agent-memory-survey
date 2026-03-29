# AgentResearch 当前改动摘要

## 背景

这次整理的目标是把本轮仓库改动收束成可复查的记录，便于后续回看、继续推进或升级为正式工件。

## 已完成的主要改动

- 修复了 `docs/plans/README.md` 的错链，指向正确的 architecture 文档。
- 统一了 `README.md`、`AGENTS.md`、`CLAUDE.md` 的开发命令口径。
- 新增 `Makefile`、CI 工作流与文档链接检查脚本。
- 在 `pyproject.toml` 中补齐了 `pytest` / `ruff` 的基础配置。
- 将 `src/references/` 的入口编排拆分到独立的 `ingest.py`。
- 将 `src/memory/evaluation.py` 的检索指标改为按真实排序计算。
- 新增 `tests/test_store_contracts.py`，覆盖 memory store 的契约行为。

## 观察到的目录状态

- `docs/plans/` 目前看起来都属于正式计划或研究工件，没有明显错放。
- `docs/ideas/` 更适合承载本轮这种“过程性整理、候选映射、待升级判断”。
- 其中 `2026-03-28-memory-lifecycle-closed-loop-from-benchmarks.md` 已经升级到 `docs/plans/`，说明这类笔记在形成稳定判断后可以直接收口。

## 下一步

- 若需要正式落地，可以把更成熟的 ideas 升级到 `docs/plans/`。
- 若只做过程记录，则继续保留在 `docs/ideas/`，并用 README 维持索引清晰。
