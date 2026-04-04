# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with this repository.

## 先看哪里

- 项目目标与目录导航：`README.md`
- 共享项目约定与细则：`AGENTS.md`
- 研究工作流事实源：`docs/method/README.md`
- 当前研究结论入口：`docs/survey/README.md`

## 对 Claude Code 最重要的项目提醒

1. `AgentResearch` 的核心目标是**研究 Agent Memory 的机制与实现**，不要让流程设计、技能设计或支线案例压过主线。
2. 共享项目约定以 `AGENTS.md` 为准；编辑 survey 时必须遵守 `AGENTS.md` 的关键概念引用规则。
3. `CLAUDE.md` 只保留 Claude Code 入口级提醒，不重复维护完整规则。
4. 判断新工作应该落到哪里时，优先看：
   - `docs/method/README.md`
   - `docs/method/workflow.md`
4. 修改 survey 章节时，通常要同步检查：
   - `docs/survey/README.md`
   - `docs/survey/survey-map.md`
5. 当 `ref/paper/`、`ref/blog/` 或 `ref/DeepResearch/` 更新时，运行：
   - `uv run --active python -m src.references`

## 目录别名

| 简写 | 真实路径 |
|------|---------|
| `paper` | `ref/paper/` |
| `blog` | `ref/blog/` |
| `DeepResearch` | `ref/DeepResearch/` |
| `ideas` | `docs/ideas/` |
| `survey-map` | `docs/survey/survey-map.md` |

## 仅保留的仓库特有提醒

- 非论文外部输入进入正式工件前，先按 `docs/method/blog-survey-calibration-template.md` 做最小分类与边界判定。
- GitHub project / open-source implementation 默认作为工程参照，不作为主研究证据。
- `docs/survey/survey-map.md` 只做索引层维护，不改写成 survey 正文替代品。
- `/architect` 仅用于跨代码原型、survey、工具链等多个层次的重大改动前，不是日常默认流程。
