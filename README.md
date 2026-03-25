# AgentResearch

Agent Memory 研究项目，包含两部分内容：

- `docs/`：研究综述、论文笔记与参考资料整理
- `src/`：面向概念验证的记忆层原型实现

## 目录结构

- `docs/survey/`：Agent Memory 综述文档
- `docs/references.md`：参考文献索引
- `ref/`：论文 PDF 与补充资料
- `src/memory/`：情景记忆、图记忆、管理器等原型代码
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
```

## 根目录约定

根目录只保留高信号文件与主目录入口，不放临时脚本、重复入口和本地缓存产物。
本地虚拟环境、测试缓存和系统垃圾文件不应留在仓库根目录。
