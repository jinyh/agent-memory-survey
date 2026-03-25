# Agent Memory 参考资料入口

> v2.0 | 2026-03-25

本页不再维护全量手工文献表，而是作为研究资料入口。`ref/` 中的 `paper` 与 `blog` 会被自动扫描，并生成结构化索引与质量评估。

## 索引文件

- `docs/references/papers-index.json`
- `docs/references/papers-index.md`
- `docs/references/blogs-index.json`
- `docs/references/blogs-index.md`
- `docs/references/deepresearch-ingestion.json`
- `docs/references/deepresearch-ingestion.md`

## 更新方式

当以下内容发生变化时，需要重新生成索引：

- `ref/paper/` 新增、替换或删除 PDF
- `ref/blog/` 新增或修改 Markdown
- `ref/DeepResearch/` 中的研究报告更新了引用列表

统一命令：

```bash
uv run --active python -m src.references
```

该命令会执行三件事：

1. 扫描 `ref/paper/` 与 `ref/blog/`，重建论文与博客索引。
2. 解析 `ref/DeepResearch/多模态Agent空间推理记忆研究.md`，更新摄取跟踪表。
3. 对可直接下载的开放论文来源（当前支持 `arXiv` 与 `OpenReview`）尝试补齐到 `ref/paper/`。

## 质量评估口径

### Paper

- 核心看学术证据：`evidence_strength`、`method_rigor`、`experiment_coverage`、`reproducibility`
- 同时给出：`timeliness`、`project_relevance`、`risk_notes`、`recommended_use`

### Blog

- 核心看工程信号与可验证性：`credibility`、`verifiability`、`engineering_signal`
- 同时标记：`marketing_bias_risk`、`timeliness`、`project_relevance`、`risk_notes`、`recommended_use`

## 当前使用原则

- `paper` 是综述中的主证据。
- `blog` 用于补充工程实践、产品比较、benchmark 争议与实现经验。
- `DeepResearch` 是“待摄取线索”，不是直接等价于高质量主证据。
