# Traceability 规则

> v1.0.0 | 2026-03-26

本项目的追踪规则采用轻量文档约定，不引入额外数据库或状态系统。

目标只有一个：让任何一条研究结论都能追回答案、证据、设计和实验。

## 最小追踪字段

所有关键工件至少维护以下字段中的相关子集：

- `question_id`
- `decision_id`
- `experiment_id`
- `evidence_refs`
- `affected_survey_sections`

## 追踪关系

### 研究问题到证据

- `research-brief` 必须定义 `question_id`
- `evidence-map` 必须引用对应 `question_id`

### 证据到决策

- `architecture-decision` 必须带 `decision_id`
- 每个关键决策必须列出 `evidence_refs`

### 决策到实验

- `experiment-spec` 必须同时引用 `experiment_id` 与 `decision_id`
- 一个实验可以验证多个决策，但必须显式列出

### 实验到叙述

- `evaluation-report` 必须标注其验证的 `experiment_id`
- `survey-update-note` 必须标注受影响章节 `affected_survey_sections`
- `docs/survey/` 中引用仓库内实验结果时，应能回到相应 `experiment_id`

## evidence_refs 约定

`evidence_refs` 可以引用：

- `docs/references/papers-index.md` 或 `.json` 中的条目
- `docs/references/blogs-index.md` 或 `.json` 中的条目
- `ref/` 中明确命名的本地资料
- survey 中已定义的代表引用名称

默认要求：

- 关键判断优先绑定 `paper`
- `blog` 只作为工程补充
- `DeepResearch` 只作为线索，不直接承担主判断

## survey 引用要求

当 `docs/survey/` 使用仓库内原型或实验结果时，至少补充以下信息：

- 该结论来自哪个 `experiment_id`
- 该实验验证了哪个问题或决策
- 该结果属于论文证据、工程判断还是综合推断

## 默认检查问题

每次跨阶段修改时，至少回答：

1. 这次改动对应哪个 `question_id`。
2. 这次设计决策是否有明确 `evidence_refs`。
3. 这次实验是否绑定了有效 `decision_id`。
4. 这次 survey 更新能否追到 `experiment_id` 或代表引用。
