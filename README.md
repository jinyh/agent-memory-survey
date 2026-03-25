# AgentResearch

Agent Memory 研究项目，当前重构为三层结构：

- `docs/`：生命周期主线的综述、论文笔记与参考资料入口
- `ref/`：原始研究资料，按 `paper / blog / DeepResearch` 分层
- `src/`：最小研究原型与资料索引工具

## 目录结构

- `docs/survey/`：新版综述，按 Formation / Evolution / Retrieval / Evaluation / Frontier 组织
- `docs/references.md`：参考资料入口页
- `docs/references/`：自动生成的 paper/blog/deepresearch 索引与质量评估
- `ref/paper/`：本地 PDF 论文库
- `ref/blog/`：工程文章与行业资料
- `ref/DeepResearch/`：研究报告与待摄取引用线索
- `src/memory/`：记忆层概念原型
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

## 根目录约定

根目录只保留高信号文件与主目录入口，不放临时脚本、重复入口和本地缓存产物。本地虚拟环境、测试缓存和系统垃圾文件不应留在仓库根目录。
