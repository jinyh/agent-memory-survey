# AgentResearch 研究版 BMAD 方法层实施方案 v1

> v1.0.0 | 2026-03-26
>
> status: completed — docs/method/ 6 文件已落地，AGENTS.md 已同步

## Summary

目标是在 `AgentResearch` 中建立一套项目内专用、文档驱动、面向小团队协作的“研究版 BMAD”方法层，优先解决“研究判断、架构决策、原型实现、评测结果彼此脱节”的问题。

默认方案如下：

- 承载方式：项目内方法层，不追求当前阶段可独立安装复用
- 入口方式：文档驱动
- 目录策略：新增集中方法目录，现有 `docs/survey`、`docs/architecture`、`docs/plans` 保持原职责
- 流程强度：只在关键门强制工件与评审，其余保持轻量
- 第一阶段重点：先建立研究工作流框架，再逐步补角色入口或 skill 化

## Key Changes

### 1. 新增“方法层总入口”

在 `docs/` 下新增一个集中入口目录，建议命名为 `docs/method/`，作为研究版 BMAD 的单一方法入口，不改写现有 survey/architecture/plans 的主体职责。

该目录包含最少 6 类文档：

- `README.md`
  说明研究版 BMAD 的目标、适用范围、角色、阶段和入口顺序
- `workflow.md`
  定义主流程：`问题定义 -> 证据建模 -> 研究判断 -> 架构决策 -> 原型计划 -> 实验评测 -> survey/报告回写`
- `roles.md`
  定义角色边界与交接关系
- `artifacts.md`
  定义每类工件的用途、必填字段、产出位置、进入下一阶段的条件
- `gates.md`
  定义关键评审门、阻塞条件和例外处理
- `traceability.md`
  定义 `survey ↔ architecture ↔ prototype ↔ evaluation` 的追踪规则

### 2. 将 BMAD 角色映射为研究角色

不沿用 PM/Dev/QA 的产品开发角色，改为研究闭环所需角色，并明确每个角色只负责“决策或产物”，不泛化为万能 agent。

角色定义固定为：

- `Research Lead`
  负责研究问题、边界、成功标准、阶段推进
- `Evidence Analyst`
  负责 paper/blog/DeepResearch 的证据分层、代表引用和证据地图
- `Architect`
  负责从研究判断到原型/工具链的架构决策
- `Experiment Engineer`
  负责实验方案、实现计划、评测执行和结果产物
- `Reviewer`
  负责跨文档一致性审查、证据边界和设计缺口质疑
- `Writer`
  负责 survey、报告、方法文档和结果回写表达

角色接口按“输入工件 / 输出工件 / 不负责什么”三段式定义，避免职责重叠。

### 3. 固定研究工件体系

新增一组标准工件模板，全部放在方法层说明中，实际产出仍落在现有目录：

- `research-brief`
  产出位置：`docs/plans/`
  内容：研究问题、范围、非目标、成功标准、首批证据入口
- `evidence-map`
  产出位置：`docs/references/` 或 `docs/survey/` 的附属文档
  内容：主证据、补充证据、线索证据、代表引用、争议点
- `architecture-decision`
  产出位置：`docs/architecture/`
  内容：决策、理由、替代方案、影响面、风险
- `experiment-spec`
  产出位置：`docs/plans/`
  内容：实验目标、假设、输入输出、指标、ground truth、失败条件
- `evaluation-report`
  产出位置：`docs/` 现有评测相关路径或约定新子目录
  内容：指标、案例、trace、结论边界、未解释现象
- `survey-update-note`
  产出位置：`docs/survey/` 附属说明或计划文档
  内容：本次改动回写了哪些判断、引用和证据边界

工件间关系固定为：
`research-brief -> evidence-map -> architecture-decision -> experiment-spec -> evaluation-report -> survey-update-note`

### 4. 建立关键评审门

只对关键节点强制，减少流程摩擦。

强制门固定为 3 个：

- `Gate A: 研究判断进入实现前`
  必须已有 `research-brief`、`evidence-map`、`architecture-decision`
  未通过时，不进入 `src/` 原型方案细化
- `Gate B: 实验开始前`
  必须已有 `experiment-spec`
  其中必须明确评价指标、query/case 范围、ground truth 或替代判定口径
- `Gate C: 结果进入 survey 前`
  必须已有 `evaluation-report`
  且要明确“论文证据 / 工程判断 / 综合推断”的归属，禁止把实验样例直接写成普遍结论

每个 gate 都记录：

- 进入条件
- 谁负责审查
- 允许的例外
- 未通过时回退到哪个阶段

### 5. 建立跨产物追踪规则

新增一套轻量 traceability 规则，不引入数据库或复杂状态系统，先用文档约定实现。

最小追踪字段统一为：

- `question_id`
- `decision_id`
- `experiment_id`
- `evidence_refs`
- `affected_survey_sections`

要求如下：

- `docs/architecture/` 中的关键决策必须指向其来源问题与证据
- `docs/plans/` 中的实验计划必须指向对应的架构决策
- `evaluation-report` 必须指向其验证的假设或设计决策
- `survey` 章节若引用仓库内原型或实验结论，必须能追到对应的 `experiment_id` 和边界说明

### 6. 与现有目录的衔接规则

不重构现有目录，只补“方法入口 + 连接约束”。

固定映射如下：

- `ref/`：原始资料层
- `docs/references*`：证据索引与证据层级
- `docs/survey/`：研究判断与叙述层
- `docs/architecture/`：架构决策层
- `docs/plans/`：实施与实验计划层
- `src/`：原型与工具链实现层
- `tests/`：验证层

方法层只定义“什么时候进入这些目录、进入前需要什么工件、完成后要回写什么”。

## Public Interfaces / Conventions

第一阶段不新增 CLI 或真正的 agent runtime 接口，先新增项目内约定接口：

- 新目录接口：`docs/method/`
- 新文档契约：`roles.md`、`workflow.md`、`artifacts.md`、`gates.md`、`traceability.md`
- 新工件命名规范：
  - `docs/plans/YYYY-MM-DD-<topic>-research-brief.md`
  - `docs/architecture/YYYY-MM-DD-<topic>.md`
  - `docs/plans/YYYY-MM-DD-<topic>-experiment-spec.md`
  - `docs/plans/YYYY-MM-DD-<topic>-evaluation-report.md`
- 新文档头部约定：
  每类工件应有统一元信息字段，至少包含 `status`、`owner`、`related_ids`、`evidence_scope`

如果后续要 skill 化，第二阶段再把这些契约映射成 `/research-lead`、`/architect`、`/reviewer` 等入口；本计划不先设计命令细节。

## Test Plan

### 文档与流程验证

- 检查方法层文档是否能完整描述从研究问题到 survey 回写的闭环
- 检查每个角色是否有明确输入、输出和非职责边界
- 检查每个 gate 是否定义了进入条件、审查责任和失败回退

### 仓库一致性验证

- 抽样验证现有文档能否映射到新工件体系：
  - `docs/architecture/2026-03-26-architect-skill-design.md`
  - `docs/plans/2026-03-26-memory-core-v1.md`
  - `docs/survey/README.md`
- 验证现有 `AGENTS.md` 与方法层是否无冲突，尤其是证据层级和 survey 写作约束

### 后续可自动化的检查点

- 增加文档测试，校验关键工件是否包含最小头部字段
- 增加 survey 约束测试，校验引用的仓库内实验结论是否带有 trace 信息
- 增加计划/架构交叉校验，检查 experiment spec 是否引用有效 decision id

## Assumptions And Defaults

- 当前阶段只为 `AgentResearch` 服务，不抽象成独立模块
- 先做文档驱动的方法层，不做安装器、交互命令或 IDE 集成
- 现有 `AGENTS.md` 继续作为项目共享约定真源；方法层只补研究工作流，不替代项目总规则
- 现有 `docs/survey`、`docs/architecture`、`docs/plans` 的历史文档不强制一次性迁移，只要求后续新增内容遵守新契约
- 第二阶段如要继续推进，优先顺序应是：
  1. 固化模板
  2. 补方法层索引
  3. 再决定是否 skill 化
