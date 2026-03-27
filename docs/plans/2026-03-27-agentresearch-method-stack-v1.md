# AgentResearch 推荐方法栈 v1

> v1.1.0 | 2026-03-27 — 增补 harness engineering 增强层结论
>
> status: proposed
> owner: Research Lead

## Summary

本项目当前更适合采用“**研究版 BMAD 作为主方法框架，轻量 harness engineering 作为实验与验证增强层**”的组合，而不是在二者之间二选一。

原因很明确：

- `AgentResearch` 的核心目标是把研究问题、证据边界、架构决策、原型实验与 survey 回写串成闭环，而不是把仓库升级为一个以 agent 自主执行和自动交付为中心的工程平台。
- `docs/method/README.md`、`docs/method/gates.md` 与 `docs/method/traceability.md` 已经给出了适合研究工作的主链路、评审门与追踪规则。
- `ref/DeepResearch/bmad-vs-harness-engineering-gap-list.md` 所指出的 harness engineering 优势，更多落在实验可重复性、失败证据归档、约束机械校验和运行期可观测性上；这些能力在本项目中有价值，但不应取代研究主线。

因此，本项目的推荐方法栈是：

- 上层方法：`research-brief -> evidence-map -> architecture-decision -> experiment-spec -> evaluation-report -> survey-update-note`
- 下层增强：围绕 `evaluation`、`traceability` 和 artifact 管理，吸收最小必要的 harness engineering 思想

## Why BMAD Is The Primary Framework

研究项目首先要解决的不是“agent 能否更自动地完成任务”，而是“研究判断能否被证据、实验和叙述稳定追溯”。在这一点上，当前仓库内的研究版 BMAD 更对题。

一方面，`docs/method/README.md` 已经把方法层定义为研究工作流总入口，明确服务于以下问题：

- 研究判断与原型实现脱节
- 架构决策与实验评测断开
- survey 结论无法追溯到证据和实验

另一方面，`docs/method/gates.md` 通过 Gate A / B / C 把三个最关键的风险点显式化：

- 未完成研究判断与架构决策时，不进入实现
- 未定义指标、ground truth 与失败条件时，不启动实验
- 未区分论文证据、工程判断与综合推断时，不把结果写入 survey

再结合 `docs/method/traceability.md` 的最小追踪字段约定，可以看到本项目已经把研究最需要的三类约束放在优先级最高的位置：

- 问题与证据的绑定
- 决策与实验的绑定
- 实验与叙述的绑定

这正是研究项目的核心控制面。

相较之下，`ref/DeepResearch/bmad-vs-harness-engineering-gap-list.md` 对 harness engineering 的总结虽然指出了 BMAD 在环境、验证与失败闭环上的不足，但这些不足主要是从“agent-first 工程执行系统”的视角提出的。对于当前仓库而言，这些点不是完全无关，但它们不应压过研究主线。

换句话说：

- 若目标是“做研究并沉淀可追溯结论”，BMAD 更适合作为主框架
- 若目标是“让 agent 在真实工程环境里稳定自治交付”，harness engineering 更适合作为主框架

`AgentResearch` 当前显然属于前者。

## What To Borrow From Harness Engineering

虽然 BMAD 更适合做主框架，但 harness engineering 中有三类能力值得被明确吸收，而且它们都与本项目现有基础能够对接。

### 1. 实验可重复性 harness

`src/memory/evaluation.py` 已经具备固定 seed、固定场景、指标产物输出和 roundtrip 检查，这说明仓库里已经有一层很轻的实验 harness 雏形。下一步值得借鉴的，不是把它升级成复杂 runtime，而是把实验工件标准化得更彻底。

建议默认补齐以下约定：

- `experiment-spec` 写明 seed、场景版本、执行命令和预期产物
- `evaluation-report` 附带最小运行摘要，而不是只保留结论
- 新实验默认复用统一 artifact 结构，便于横向比较

这类增强直接服务于研究复现性，与 `docs/survey/05-evaluation.md` 中对“评测什么、如何归因”的强调一致。

### 2. 追踪与约束的半自动校验

当前 `docs/method/traceability.md` 仍然是文档约定，已经足够作为 v1 方法层，但从 harness engineering 视角看，最值得补的一步是把少量高价值约束变成机械检查。

适合本项目的第一批检查应保持克制：

- `experiment-spec` 必须引用有效 `decision_id`
- `evaluation-report` 必须引用有效 `experiment_id`
- survey 中引用仓库实验结果时，必须能追到对应 `experiment_id`
- `DeepResearch` 资料不能直接承担主判断

这一步的目的不是把研究流程工具化到很重，而是降低断链和误用证据的概率。

### 3. 失败证据包与 artifact bundling

`ref/DeepResearch/bmad-vs-harness-engineering-gap-list.md` 明确指出，BMAD 风格的方法通常缺“失败证据归档机制”。这条批评对本项目也成立，尤其是在原型实验阶段。

当前 `src/memory/evaluation.py` 已能产出：

- `report.json`
- `report.md`
- `cases.jsonl`

这已经是很好的起点。下一步最值得借的 harness 思想是把失败证据组织成统一包，至少包含：

- 输入场景或关键配置摘要
- 实际执行命令
- 指标结果
- 失败 case
- trace 摘要
- 环境信息

这样做的价值不在“更工程化”本身，而在于：

- 更容易复核实验结论
- 更容易比较不同策略
- 更容易把实验结果安全地回写到 survey

## What Not To Borrow Now

本项目不应把 harness engineering 的所有方向都吸收进来。以下几项，当前阶段不建议作为主投入。

### 1. 不把方法层改造成自治执行流

`docs/method/README.md` 已明确写出“先追求文档驱动的一致性，再考虑 skill 化或命令化”。这意味着当前方法层的第一目标，是让研究问题、证据和实验闭环，而不是让 agent 自主完成实现、验证、修复、交付。

如果现在把方法层主轴改成自治执行流，会直接稀释 Gate A / B / C 对研究边界的控制价值。

### 2. 不优先投入浏览器/CDP/UI 调试 harness

差距清单中提到的浏览器调试、运行期观测、端到端修复闭环，对前端或全栈应用仓库很重要；但本项目当前核心资产是：

- survey
- 资料索引
- memory 原型
- lifecycle evaluation

因此，这类能力目前不是高优先级。

### 3. 不把 worktree / 多 agent 流水线设为默认模型

隔离 worktree、多 agent 并发和自动修复流水线，适合高频实现型仓库。当前 `AgentResearch` 的工作负载仍以研究判断、文档回写和原型验证为主，这类基础设施投入暂时很难形成同等价值回报。

## Recommended Next Steps

基于当前仓库状态，后续行动建议按以下顺序推进。

1. 为 `experiment-spec` 和 `evaluation-report` 增补最小运行契约。
   重点加入 `seed`、`runner command`、`artifact manifest`、`failure evidence` 约定。

2. 为 `traceability` 增加轻量机械检查。
   初期可先用脚本或文档测试检查 `decision_id`、`experiment_id`、`affected_survey_sections` 等字段是否断链。

3. 为 `src/memory/evaluation.py` 产物定义统一 failure evidence bundle。
   在现有 `report.json`、`report.md`、`cases.jsonl` 基础上，补最小环境摘要和失败样例组织规范。

## Assumptions And Defaults

- 本建议只适用于当前阶段的 `AgentResearch`，不外推到通用 agent 工程框架。
- 默认目标是“提升研究闭环质量”，不是“提升 agent 自治交付能力”。
- 默认不替换现有 BMAD 方法层，只做下层增强。
- 默认优先级是：
  1. 实验可重复性
  2. 追踪与约束校验
  3. 失败证据包
  4. 更重的执行环境 harness
