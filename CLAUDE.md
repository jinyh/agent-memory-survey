# AgentResearch

> v1.0.0 | 2026-03-27

## 使用约定

- `docs/survey/survey-map.md` 作为 survey ↔ code ↔ gap 的长期索引层维护，不替代正文。
- `src/memory/evaluation.py` 里的数据集适配只负责把 `ref/datasets` 归一化成 benchmark case；不要把 retrieval 数据集误写成完整 lifecycle benchmark。
- `MemoryManager.recall()` 采用 rank 融合，不是 raw score 直排；调试检索时优先看 `recall_with_trace()`。
- `tests/test_memory.py -q` 是本仓库最常用的记忆层回归验证命令。
- `find . -name "CLAUDE.md" -o -name ".claude.local.md"` 可先确认是否已有 Claude 说明文件，再决定是更新还是新建。
- survey 章节更新时，优先同步 `docs/survey/README.md` 和 `docs/survey/survey-map.md`。
