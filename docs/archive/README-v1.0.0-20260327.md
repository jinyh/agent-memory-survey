# AgentResearch 研究版 BMAD 方法层

> v1.0.0 | 2026-03-26

本目录是 `AgentResearch` 的研究工作流总入口，用来把研究问题、证据整理、架构决策、原型实现、实验评测与 survey 回写串成一条可复用的方法链。

它不替代现有目录职责，只负责规定：

- 什么时候进入 `docs/survey`、`docs/architecture`、`docs/plans`、`src/`、`tests/`
- 进入前需要哪些工件
- 产出后需要回写哪些文档
- 哪些节点必须经过评审

## 适用范围

本方法层当前只服务于 `AgentResearch` 项目，面向小团队协作场景，优先解决以下问题：

- 研究判断与原型实现脱节
- 架构决策与实验评测断开
- survey 结论无法追溯到证据和实验

## 方法结构

- [workflow.md](./workflow.md)：主流程和阶段入口
- [roles.md](./roles.md)：角色边界与交接关系
- [artifacts.md](./artifacts.md)：标准工件与命名约定
- [gates.md](./gates.md)：关键评审门与回退规则
- [traceability.md](./traceability.md)：跨文档追踪字段与引用规则

## 与现有目录的关系

- `ref/`：原始资料层
- `docs/references*`：证据索引层
- `docs/survey/`：研究判断与叙述层
- `docs/architecture/`：架构决策层
- `docs/plans/`：研究计划与实验计划层
- `src/`：原型与工具链实现层
- `tests/`：验证层

## 默认使用顺序

1. 在 `docs/plans/` 创建 `research-brief`
2. 整理 `evidence-map`
3. 在 `docs/architecture/` 记录 `architecture-decision`
4. 在 `docs/plans/` 创建 `experiment-spec`
5. 执行原型与评测，产出 `evaluation-report`
6. 将结果回写到 `docs/survey/`，并补 `survey-update-note`

## 默认原则

- `paper` 是主证据，`blog` 只做工程补充，`DeepResearch` 只做线索
- 关键研究判断进入实现前，必须先完成架构决策
- 实验结论进入 survey 前，必须明确证据边界与适用范围
- 先追求文档驱动的一致性，再考虑 skill 化或命令化
