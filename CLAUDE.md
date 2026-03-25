# AgentResearch - Agent Memory 研究项目

## 项目概述
研究 LLM Agent 记忆层的最新进展、思路和实现。包含研究综述文档和概念原型代码。

## 项目结构
- `ref/` — 参考论文 PDF
- `docs/survey/` — 研究综述文档
- `docs/references.md` — 参考文献库
- `src/memory/` — 概念原型代码
- `tests/` — 单元测试

## 技术栈
- Python 3.10+, uv
- 依赖: chromadb, networkx, sentence-transformers

## 环境约定
- 为保持根目录整洁，虚拟环境默认放在仓库外，例如 `$HOME/.venvs/agentresearch`
- 推荐流程: `uv venv "$HOME/.venvs/agentresearch"` → `source "$HOME/.venvs/agentresearch/bin/activate"` → `uv sync --active --extra dev`

## 开发命令
```bash
uv run --active --extra dev pytest tests/   # 运行测试
uv run --active python -m src.memory.agent  # 运行 Agent 示例
```
