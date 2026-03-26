# AgentResearch

Agent Memory 研究项目，当前重构为三层结构：

- `docs/`：生命周期主线的综述、论文笔记与参考资料入口
- `ref/`：原始研究资料，按 `paper / blog / DeepResearch` 分层
- `src/`：最小研究原型与资料索引工具

## 目录结构

- `docs/method/`：研究版 BMAD 方法层（工作流、角色、工件、评审门、追踪规则）
- `docs/survey/`：新版综述，按 Formation / Evolution / Retrieval / Evaluation / Frontier 组织
- `docs/references.md`：参考资料入口页
- `docs/references/`：自动生成的 paper/blog/deepresearch 索引与质量评估
- `ref/paper/`：本地 PDF 论文库，默认不纳入版本控制
- `ref/blog/`：工程文章与行业资料
- `ref/DeepResearch/`：研究报告与待摄取引用线索
- `docs/plans/`：研究工件（research-brief、evidence-map、experiment-spec、evaluation-report、survey-update-note）
- `docs/architecture/`：架构决策记录（ADR）
- `src/memory/`：记忆层概念原型（含全生命周期评测框架）
- `src/references/`：资料索引、质量评估与下载工具
- `tests/`：单元测试

## 开发命令

推荐将虚拟环境放在仓库外，例如：

```bash
uv venv "$HOME/.venvs/agentresearch"
source "$HOME/.venvs/agentresearch/bin/activate"
uv sync --active --extra dev
```

日常开发命令：

```bash
uv run --active --extra dev pytest tests/
uv run --active python -m src.memory.agent
uv run --active python -m src.memory.evaluation --out docs/memory-eval/latest
uv run --active python -m src.references
```

## 资料更新流程

当 `ref/paper/` 或 `ref/blog/` 有新文件，或者 `ref/DeepResearch/` 的引文更新时，运行：

```bash
uv run --active python -m src.references
```

该命令会自动：

1. 扫描 `paper` 和 `blog` 新文件
2. 生成 `docs/references/` 下的结构化索引
3. 评估每条资料的质量字段
4. 对 `DeepResearch` 中支持直下的开放论文执行下载补齐

说明：`ref/paper/` 用于保存本地论文原文 PDF，供索引脚本和研究流程使用，但这些 PDF 默认不会提交到 Git 仓库。

## 根目录约定

根目录只保留高信号文件与主目录入口，不放临时脚本、重复入口和本地缓存产物。本地虚拟环境、测试缓存和系统垃圾文件不应留在仓库根目录。

代理说明文件采用单一事实源策略：共享项目约定统一维护在 `AGENTS.md`，`CLAUDE.md` 仅保留 Claude Code 的入口说明与必要差异。
