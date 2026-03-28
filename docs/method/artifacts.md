# 标准工件

> v1.1.0 | 2026-03-29 — 补充非论文外部输入进入正式工件前的前置约束

本文件定义研究版 BMAD 的标准工件、默认落点和最小字段。

## 工件链路

固定顺序如下：

`research-brief -> evidence-map -> architecture-decision -> experiment-spec -> evaluation-report -> survey-update-note`

## 1. research-brief

默认路径：

- `docs/plans/YYYY-MM-DD-<topic>-research-brief.md`

最小字段：

- `status`
- `owner`
- `question_id`
- `scope`
- `non_goals`
- `success_criteria`
- `initial_evidence`

## 2. evidence-map

默认路径：

- `docs/plans/YYYY-MM-DD-<topic>-evidence-map.md`
- 或与相关 `docs/survey/` / `docs/references/` 文档配套维护

前置约束：

- 非论文外部输入进入 `evidence-map` 前，应先完成最小分类与边界判定（参考 `docs/method/blog-survey-calibration-template.md`）

最小字段：

- `status`
- `owner`
- `question_id`
- `primary_evidence`
- `supporting_evidence`
- `lead_evidence_lines`
- `open_gaps`

## 3. architecture-decision

默认路径：

- `docs/architecture/YYYY-MM-DD-<topic>.md`

最小字段：

- `status`
- `owner`
- `decision_id`
- `question_id`
- `evidence_refs`
- `alternatives`
- `risks`

## 4. experiment-spec

默认路径：

- `docs/plans/YYYY-MM-DD-<topic>-experiment-spec.md`

最小字段：

- `status`
- `owner`
- `experiment_id`
- `decision_id`
- `hypothesis`
- `inputs_outputs`
- `metrics`
- `ground_truth_strategy`
- `failure_conditions`

## 5. evaluation-report

默认路径：

- `docs/plans/YYYY-MM-DD-<topic>-evaluation-report.md`

最小字段：

- `status`
- `owner`
- `experiment_id`
- `validated_decisions`
- `results_summary`
- `failure_cases`
- `boundary_notes`

## 6. survey-update-note

默认路径：

- `docs/plans/YYYY-MM-DD-<topic>-survey-update-note.md`
- 或作为 survey 章节修改附带的变更说明

前置约束：

- 若 `survey-update-note` 引入 blog、GitHub project、benchmark repo 等非论文外部输入，应先完成最小分类与边界判定，并在 `evidence_scope` 中写清其角色与边界

最小字段：

- `status`
- `owner`
- `experiment_id`
- `affected_survey_sections`
- `updated_claims`
- `evidence_scope`
- `open_questions`

## 命名约定

- `question_id`：研究问题主键
- `decision_id`：架构决策主键
- `experiment_id`：实验主键

建议格式：

- `question_id`: `Q-YYYYMMDD-<slug>`
- `decision_id`: `D-YYYYMMDD-<slug>`
- `experiment_id`: `E-YYYYMMDD-<slug>`

## 默认规则

- 新增关键研究活动时，优先补工件，再写实现
- 工件允许迭代，但必须保留当前状态与关联 ID
- 没有 `decision_id` 的实验，不应进入正式评测结论
