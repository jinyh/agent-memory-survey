# AgentResearch

> v1.1.0 | 2026-03-26

Claude Code 入口说明。该仓库用于研究 Agent Memory，产物包括研究综述、参考资料库和最小记忆原型。

## 共享约定

本仓库的共享项目约定以 `AGENTS.md` 为准。

- 目录结构、开发命令、资料维护流程等公共规则只在 `AGENTS.md` 维护。
- 若 `CLAUDE.md` 与 `AGENTS.md` 出现冲突，以 `AGENTS.md` 为准。
- 更新共享项目说明时，先改 `AGENTS.md`；`CLAUDE.md` 仅保留 Claude Code 入口说明和必要差异。
- 编辑 survey 时必须遵守 `AGENTS.md` 的关键概念引用规则。

## Claude Code 能力指引

- **Plan Mode**：survey 章节编辑、原型架构变更、涉及 3+ 文件时进入 Plan Mode。
- **Agent 子进程**：并行探索多篇论文、并行审查多个 survey 章节、并行跑测试+lint 时使用。
- **PDF 直读**：可直接读取 `ref/paper/` 中的 PDF 论文原文，无需预处理或文本提取。
- **代码导航**：优先用 LSP（Go to Definition / Find References），回退到 Grep/Glob。

## Memory 使用指引

以下指引适用于 Claude Code 的 auto memory 系统：

**该存**：
- 新发现的关键论文线索（尚未入库到 `ref/paper/`）
- 研究方向决策与取舍理由
- 用户对工作流的偏好和纠正

**不该存**：
- 已在 `docs/references/` 索引中的论文元数据 — 直接读索引文件
- survey 章节内容摘要 — 直接读 `docs/survey/` 源文件
- 项目结构和命令 — 已在 `AGENTS.md` 维护

## Claude Code 使用提示

- 进入仓库后，先阅读 `AGENTS.md` 获取完整项目上下文。
- 涉及 `ref/paper/`、`ref/blog/`、`ref/DeepResearch/` 的资料变更时，遵循 `AGENTS.md` 中的资料维护约定执行。
