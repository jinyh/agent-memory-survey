# AgentResearch

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 仓库概览

AgentResearch 是一个面向 Agent Memory 的研究型仓库，整体由三层组成：

- `docs/`：survey、method、plans、架构决策与 references 索引
- `ref/`：原始材料（`paper`、`blog`、`DeepResearch`、datasets）
- `src/`：最小原型实现与 references 索引工具

项目工作流的事实源在 `docs/method/README.md` 和 `docs/method/workflow.md`。判断新工作应该落到哪里时，优先以这两份文档为准。

共享项目约定以 `AGENTS.md` 为准。编辑 survey 时必须遵守 `AGENTS.md` 的关键概念引用规则。

## 常用命令

### 环境初始化

```bash
uv venv "$HOME/.venvs/agentresearch"
source "$HOME/.venvs/agentresearch/bin/activate"
uv sync --active --extra dev
```

### 测试

```bash
uv run --active --extra dev pytest tests/
uv run --active --extra dev pytest tests/test_memory.py -q
uv run --active --extra dev pytest tests/test_memory.py -q -k recall
uv run --active --extra dev ruff check .
```

`tests/test_memory.py -q` 是本仓库最常用的记忆层回归验证命令。

### 运行原型与索引

```bash
uv run --active python -m src.memory.agent
uv run --active python -m src.memory.evaluation --out docs/memory-eval/latest
uv run --active python -m src.references
```

当 `ref/paper/` 或 `ref/blog/` 有新文件，或 `ref/DeepResearch/` 的引文发生变化时，运行 `python -m src.references` 重建 references 层。

### Lint

```bash
uv run --active --extra dev ruff check .
```

## 高层架构

### 1. 研究工作流层（`docs/`）

这个仓库不是 code-first 开发流，而是文档驱动的研究闭环：

1. 收集并分类外部输入
2. 将证据整理为正式研究工件
3. 将稳定研究判断落成架构/实验决策
4. 把原型代码与评测结果回写到 survey

关键位置：

- `docs/method/`：workflow、artifacts、gates、traceability，以及外部输入分类规则
- `docs/survey/`：survey 正文
- `docs/survey/survey-map.md`：长期维护的 survey ↔ code ↔ gap 索引层；它不是正文替代品
- `docs/plans/`：`research-brief`、`evidence-map`、`experiment-spec`、`evaluation-report`、`survey-update-note`
- `docs/architecture/`：把研究判断连接到实现的架构决策
- `docs/references/`：来源材料的自动索引与质量元数据

修改 survey 章节时，通常要同步检查 `docs/survey/README.md` 和 `docs/survey/survey-map.md`。

### 2. 记忆原型层（`src/memory/`）

`src/memory/` 是一个刻意保持最小化的多 store 记忆系统。理解结构时，重点看这些职责分层：

- `base.py`：`MemoryItem`、`MemoryType`、`FusionConfig` 等共享类型
- `episodic.py`：episodic memory store 与 consolidation 原语
- `graph_store.py`：图式 semantic store
- `vector_store.py`：向量检索 store
- `manager.py`：统一 orchestrator，负责 store 注册、跨 store recall、更新/删除、consolidation
- `agent.py`：使用记忆系统的最小 agent 闭环
- `evaluation.py`：可重复评测 harness 与 `ref/datasets` 的数据集适配层

关键实现细节：`MemoryManager.recall()` 使用的是 rank-based fusion，不是 raw score 直排。调试检索行为时，优先看 `recall_with_trace()`。

### 3. 评测与数据集

`src/memory/evaluation.py` 的职责是把 `ref/datasets` 中的数据集归一化成 benchmark case。这里要严格区分：

- `evaluation.py` 中的数据集适配是“把原始数据转成可比较 case”
- retrieval-heavy 数据集不能被表述成完整 lifecycle benchmark

评测 harness 目前覆盖：场景构造、数据集归一化、检索指标，以及 snapshot roundtrip 检查。

### 4. References 摄取层（`src/references/`）

`src/references/__main__.py` 是重建 references 层的入口。它会：

- 从 DeepResearch 报告中提取条目
- 下载其中可直接获取的开放论文
- 扫描仓库中的 reference library
- 把更新后的索引写入 `docs/references/`

这一层是 `ref/` 原始材料到 `docs/references/` 结构化索引之间的桥。

## 仓库特有规则

- 非论文外部输入在进入正式工件前，先经过 `docs/method/blog-survey-calibration-template.md` 的分类与边界判定。
- GitHub project / open-source implementation 默认作为工程参照，不作为主研究证据。
- `docs/survey/survey-map.md` 只做索引层维护，不要把它改写成 survey 正文替代品。
- `docs/ideas/` 与 `docs/plans/` 的维护规则以 `AGENTS.md` 为准；`CLAUDE.md` 只保留入口级提醒。
- 如果需要判断是新建还是更新 Claude 指南文件，先运行：
  `find . -name "CLAUDE.md" -o -name ".claude.local.md"`
