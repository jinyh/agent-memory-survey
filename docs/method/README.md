# AgentResearch 研究版 BMAD 方法层

> v1.2.0 | 2026-03-29 — 补充项目工作流总览与非论文外部输入判定入口

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

## 项目工作流总览

整个项目当前按“外部输入 → 证据整理 → 研究判断 → 原型验证 → survey 回写”的闭环推进，默认可按下面的收敛版口径理解：

1. 收集外部输入，并先判断材料角色。
   - `paper`：主研究证据
   - `blog / engineering post / release note`：工程补充证据
   - `GitHub project / open-source implementation`：工程参照
   - `benchmark / eval repo / leaderboard implementation`：评测参照
   - `DeepResearch / ideas / defer`：线索与候选
2. 将资料放入对应层级：`ref/` 保存原始材料，`docs/references/` 维护索引与初判，必要时进入 `docs/ideas/` 做轻量孵化。
3. 对需要进入正式研究链路的内容，先完成最小分类与边界判定，再整理为 `research-brief` / `evidence-map`。
4. 当研究判断需要落到实现或评测时，在 `docs/architecture/` 记录 `architecture-decision`，并在 `docs/plans/` 中补 `experiment-spec`、`evaluation-report`、`survey-update-note`。
5. 最终把稳定结论回写到 `docs/survey/`，并用 `docs/survey/survey-map.md` 维护 survey ↔ code ↔ gap 的索引映射。

更细的阶段定义见 [workflow.md](./workflow.md)，外部材料的分类与边界判定见 [blog-survey-calibration-template.md](./blog-survey-calibration-template.md)。

## 默认使用顺序

1. 在 `docs/plans/` 创建 `research-brief`
2. 整理 `evidence-map`
3. 在 `docs/architecture/` 记录 `architecture-decision`
4. 在 `docs/plans/` 创建 `experiment-spec`
5. 执行原型与评测，产出 `evaluation-report`
6. 将结果回写到 `docs/survey/`，并补 `survey-update-note`

## 默认原则

- `paper` 是主证据，`blog` 只做工程补充，`DeepResearch` 只做线索
- GitHub project / open-source implementation 默认作为工程参照，不直接替代 `paper` 成为主研究证据
- 非论文外部输入进入正式文档前，先按 [`blog-survey-calibration-template.md`](./blog-survey-calibration-template.md) 完成最小分类与边界判定
- 关键研究判断进入实现前，必须先完成架构决策
- 实验结论进入 survey 前，必须明确证据边界与适用范围
- `/architect` 不是日常默认流程；仅在跨代码原型、survey、工具链等多个层次的重大改动前，作为专项架构评审使用
- 先追求文档驱动的一致性，再考虑 skill 化或命令化
- 研究主线优先级高于协作流程；如果一个改动只让流程更复杂、却不能让 memory 机制、原型或评测更清楚，就不应优先做
- 项目级 skills 默认只承担两类职责：材料摄取/证据映射，以及低频专项评审；其余流程能力优先收回到文档规则层
- hooks 只保留轻量提醒，不继续扩张为额外 workflow 层
