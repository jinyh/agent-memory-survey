# Agent Memory

AgentResearch 是一个以 **Agent Memory 机制与实现** 为中心的研究仓库。当前主线由三层组成：

- `ref/`：原始研究资料层（`paper / blog / DeepResearch / datasets`）
- `docs/`：研究工作流、survey、references 索引与正式研究工件
- `src/`：最小 memory 原型、references 工具与评测实现

## 从哪里开始

如果你第一次进入这个仓库，按下面顺序阅读：

1. `docs/method/README.md`：研究工作流总入口，说明材料如何进入正式研究链路
2. `docs/survey/README.md`：当前关于 Agent Memory 的核心判断与章节导航
3. `AGENTS.md`：共享项目约定、证据口径与目录边界细则

## 核心目录

- `docs/method/`：研究工作流、gate、traceability 与外部材料判定规则
- `docs/survey/`：围绕 `formation -> evolution -> retrieval -> evaluation` 主线组织的综述
- `docs/references/`：自动生成的 paper/blog/DeepResearch 索引
- `docs/plans/`：正式研究工件（如 research-brief、evidence-map、experiment-spec、evaluation-report）
- `docs/ideas/`：轻量孵化、候选映射、局部启发
- `docs/architecture/`：与 memory/evaluation/references 实现相关的架构决策
- `ref/`：原始资料层
- `src/memory/`：最小 memory 原型与评测相关实现
- `src/references/`：references 扫描、质量评估与索引工具
- `tests/`：代码、文档与索引相关测试

## 常用命令

```bash
uv venv "$HOME/.venvs/agentresearch"
source "$HOME/.venvs/agentresearch/bin/activate"
uv sync --active --extra dev

make test
make lint
make docs
make refs
make eval
```

## 资料更新

当 `ref/paper/`、`ref/blog/` 或 `ref/DeepResearch/` 更新时，运行：

```bash
uv run --active python -m src.references
```

它会重建 `docs/references/` 索引，并补齐可直接下载的开放论文。

## 入口与事实源

- 项目目标与导航：`README.md`
- 共享项目约定：`AGENTS.md`
- Claude Code 入口提醒：`CLAUDE.md`
- 研究工作流事实源：`docs/method/README.md`
- 研究结论入口：`docs/survey/README.md`
