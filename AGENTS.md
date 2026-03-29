# AgentResearch - Agent Memory 研究项目

## 项目概述
研究 LLM Agent 记忆层的最新进展、思路和实现。当前仓库包含三类核心产物：

- 生命周期主线的研究综述
- 按 `paper / blog / DeepResearch` 组织的参考资料库
- 面向研究验证的最小记忆原型与资料索引工具

## 项目结构
- `ref/paper/` — 本地 PDF 论文库，默认不纳入版本控制（`ref/paper/README.md` 为占位说明）
- `ref/blog/` — 工程文章、产品解读和行业资料
- `ref/DeepResearch/` — 研究报告与待摄取引用线索
- `docs/survey/` — 研究综述文档，按 Formation / Evolution / Retrieval / Evaluation / Frontier 组织
  - `README.md` — 综述总览与章节导航
  - `survey-map.md` — 章节研究矩阵与证据地图
- `docs/references.md` — 参考资料入口页（含质量评估口径定义）
- `docs/references/` — 自动生成的论文、博客、DeepResearch 摄取索引与质量评估
- `docs/method/` — 研究版 BMAD 方法层（工作流、角色、工件、评审门、追踪规则）
- `docs/plans/` — 研究规划与设计文档
- `docs/ideas/` — 记录与 Claude 交互过程中产生的想法、临时洞察和后续可执行点，文件名使用 `YYYY-MM-DD-<short-slug>.md`
- `docs/architecture/` — 架构决策记录（ADR）
- `src/memory/` — 概念原型代码
- `src/references/` — 资料索引、质量评估与开放论文下载工具
- `tests/` — 单元测试

## 技术栈
- Python 3.10+, uv
- 依赖: chromadb, networkx, sentence-transformers

## 环境约定
- 为保持根目录整洁，虚拟环境默认放在仓库外，例如 `$HOME/.venvs/agentresearch`
- 推荐流程: `uv venv "$HOME/.venvs/agentresearch"` → `source "$HOME/.venvs/agentresearch/bin/activate"` → `uv sync --active --extra dev`

## 开发命令
```bash
uv run --active --extra dev pytest tests/              # 运行测试
uv run --active --extra dev pytest tests/test_memory.py -q  # 记忆层回归
uv run --active python -m src.memory.agent             # 运行 Agent 示例
uv run --active python -m src.memory.evaluation --out docs/memory-eval/latest  # 全生命周期评测
uv run --active python -m src.references               # 重建资料索引并补齐开放论文
uv run --active --extra dev ruff check .               # 代码检查
```

## 资料维护约定
- `ref/paper/` 与 `ref/blog/` 的新增、删除、替换都应通过 `uv run --active python -m src.references` 重新生成索引。
- `ref/paper/` 中的论文原文 PDF 默认仅保留在本地工作区，不提交到 Git；如需共享，优先共享索引、元数据与引用，不直接提交原文。
- `ref/DeepResearch/` 中新增或更新的研究报告，默认作为“摄取线索”处理，不直接等价于主证据。
- `src.references` 会自动扫描 `paper` 和 `blog`，生成 `docs/references/` 下的结构化索引与质量评估。
- 当前开放论文自动下载仅保证 `arXiv` 与 `OpenReview` 直链；其他来源允许保留元数据与缺失原因。
- `paper` 是综述中的主证据；`blog` 主要用于补充工程实践、系统选型和 benchmark 争议背景。

## Survey 写作约束
- 进入实现或实验前，遵守 `docs/method/gates.md` 定义的评审门要求（Gate A：进实现前；Gate B：实验前；Gate C：进 survey 前）。
- `docs/survey/` 中关键概念、方法范式、系统路线、评测对象、组织性判断，必须绑定明确代表引用。
- 代表引用优先 `paper`；`blog` 只能做工程补充；`DeepResearch` 只能做线索。
- 如果正文出现缩写或系统名并承担论证功能，首次必须写出明确作品名，不允许只用泛称或缩写承担主判断。
- `docs/survey/survey-map.md` 作为 survey ↔ code ↔ gap 的长期索引层维护，不替代正文。
- `docs/ideas/` 只放轻量记录、临时洞察和候选映射；一旦形成明确研究问题、证据地图、实验规格或可直接引用的稳定判断，就升级到 `docs/plans/`。
- `docs/plans/` 优先使用日期前缀命名；若发现无日期前缀但已属正式工件的文件，先补命名再更新索引。
- `src/memory/evaluation.py` 的数据集适配只负责把 `ref/datasets` 归一化成 benchmark case；不要把 retrieval 数据集误写成完整 lifecycle benchmark。
- `MemoryManager.recall()` 采用 rank 融合，不是 raw score 直排；调试检索时优先看 `recall_with_trace()`。
- `tests/test_memory.py -q` 是本仓库最常用的记忆层回归验证命令。
- `find . -name "CLAUDE.md" -o -name ".claude.local.md"` 可先确认是否已有 Claude 说明文件，再决定是更新还是新建。
- survey 章节更新时，优先同步 `docs/survey/README.md` 和 `docs/survey/survey-map.md`。
- 更新共享写作规则时，必须同步检查 `CLAUDE.md`，并保持 `AGENTS.md` 为单一细则真源。
