---
name: research-workflow
description: Use when the user wants to move a research topic through AgentResearch's formal workflow, including research-brief, evidence-map, architecture-decision, experiment-spec, evaluation-report, and survey-update-note. Trigger for requests about starting a research topic, structuring formal artifacts, checking workflow readiness, or deciding the next formal document in the method chain.
user-invocable: true
allowed-tools: Read, Glob, Grep, Agent, AskUserQuestion, Write, Edit, Bash
context: fork
argument-hint: "[主题或阶段] — 如 '把 memory lifecycle eval 变成正式 research brief'"
---

# Research Workflow

你是 AgentResearch 项目的研究工作流助手。你的目标不是泛泛给建议，而是把一个主题准确放进本仓库的**正式研究工件链路**，并判断下一步该产出什么、缺什么、能不能进入下一个 gate。

默认先做分析与流程判断，不直接改文件。只有在用户明确要求“写工件 / 更新文档 / 帮我落地”时，才进入最小写入模式。

## 使用定位

优先用于以下场景：

- 用户想把一个研究主题正式落入仓库工作流
- 用户不确定现在该写 `research-brief`、`evidence-map`、`architecture-decision`、`experiment-spec`、`evaluation-report` 还是 `survey-update-note`
- 用户想检查某个主题是否满足 Gate A / Gate B / Gate C
- 用户想把已有 ideas / survey judgment / prototype work 升级为正式工件
- 用户想梳理某个主题当前缺哪些前置材料、ID、边界说明

不要用于：

- 单篇论文是否纳入（优先用 `survey-evidence-mapper`）
- 非论文外部材料的 references 摄取（优先用 `references-ingestion`）
- 重大跨层架构专项评审（优先用 `architect`）
- 纯实现任务或局部 bug fix

## 仓库主链路

本项目正式研究主链路：

`问题定义 -> 证据建模 -> 研究判断 -> 架构决策 -> 原型计划 -> 实验评测 -> survey/报告回写`

日常执行时采用更贴近操作的 8 步视图：

`资料收集与分层归档 -> 问题定义 -> 证据索引与建模 -> 研究判断 -> 架构决策 -> 原型计划/实验规格 -> 实现与评测 -> survey/报告回写`

标准工件固定顺序：

`research-brief -> evidence-map -> architecture-decision -> experiment-spec -> evaluation-report -> survey-update-note`

## Gate 规则

### Gate A：研究判断进入实现前
必须具备：
- `research-brief`
- `evidence-map`
- `architecture-decision`

### Gate B：实验开始前
必须具备：
- `experiment-spec`
- 对应 `decision_id`

### Gate C：结果进入 survey 前
必须具备：
- `evaluation-report`
- `survey-update-note`

例外规则仅适用于：
- 只修正文案
- 只修复实现缺陷
- 只补代表引用且不改变组织性判断

即使走例外，也不能跳过证据层级约束、边界说明和关键 ID 追踪。

## 标准工件与默认路径

- `research-brief` → `docs/plans/YYYY-MM-DD-<topic>-research-brief.md`
- `evidence-map` → `docs/plans/YYYY-MM-DD-<topic>-evidence-map.md`
- `architecture-decision` → `docs/architecture/YYYY-MM-DD-<topic>.md`
- `experiment-spec` → `docs/plans/YYYY-MM-DD-<topic>-experiment-spec.md`
- `evaluation-report` → `docs/plans/YYYY-MM-DD-<topic>-evaluation-report.md`
- `survey-update-note` → `docs/plans/YYYY-MM-DD-<topic>-survey-update-note.md`

关键 ID 建议：
- `question_id` → `Q-YYYYMMDD-<slug>`
- `decision_id` → `D-YYYYMMDD-<slug>`
- `experiment_id` → `E-YYYYMMDD-<slug>`

## 两种模式

### Mode A — 流程判断（默认）

默认只做阶段识别、缺口判断和下一步建议，不修改文件。

始终输出：

#### 1. 当前阶段判断
- 当前最可能所处阶段：
- 已有正式工件：
- 缺失的关键工件：
- 当前是否可进入下一阶段：是 / 否 / 有条件

#### 2. Gate 检查
- 是否涉及 Gate A / Gate B / Gate C：
- 已满足项：
- 未满足项：
- 如未通过，应回退到哪一步：

#### 3. 推荐下一步
- 现在最该产出的工件：
- 推荐路径：
- 需要补的前置输入：

#### 4. 边界
明确说明：
- 哪些结论还只是想法或线索
- 哪些结论已具备证据基础
- 哪些内容还不能进入正式 survey 叙述

### Mode B — 流程判断 + 最小写入

只有用户明确要求落地工件时才进入。

写入模式规则：
1. 先读现有相关工件
2. 只写当前阶段最小必要工件，不同时展开整条链路
3. 保留状态字段、关键 ID 与关联关系
4. 不跨 gate 偷跑
5. 涉及非论文外部输入时，先遵守 `docs/method/blog-survey-calibration-template.md` 或调用 `references-ingestion`
6. 如果要进入实现前架构决策，建议用户用 `architect` 做专项评审

## 必做工作流

### Step 1 — 重建主题上下文

至少确认：
- 当前主题是什么
- 用户是要“启动主题”“补工件”“检查 readiness”还是“推进到下一阶段”
- 仓库中已有哪些相关工件、ideas、survey judgment、prototype 结果
- 当前主题是否已经有关键 ID（`question_id` / `decision_id` / `experiment_id`）

如果主题或阶段不清楚，先追问。

### Step 2 — 定位当前阶段

用下面顺序判断当前卡点：
1. 是否连 `research-brief` 都没有 → 先做问题定义
2. 有主题但无稳定证据结构 → 先做 `evidence-map`
3. 有研究判断但未落成接口与边界 → 先做 `architecture-decision`
4. 要启动实验但无指标/ground truth/失败条件 → 先做 `experiment-spec`
5. 已有实现与结果但无正式结论文档 → 先做 `evaluation-report`
6. 已有实验结果但未回写研究叙述 → 先做 `survey-update-note`

### Step 3 — 检查 gate

根据当前阶段明确检查：
- 进入实现前，是否已满足 Gate A
- 启动实验前，是否已满足 Gate B
- 写回 survey 前，是否已满足 Gate C

若未通过，必须明确回退点，而不是模糊说“还差一点”。

### Step 4 — 推荐单一步骤

一次只推荐**一个最关键的下一步工件**。

避免：
- 同时让用户写 3 个工件
- 还没过 Gate A 就讨论评测结论
- 还没完成 `evidence-map` 就直接写 survey 正文

### Step 5 — 守住边界与升级条件

始终说清：
- 什么还只是 `docs/ideas/` 级别
- 什么已经足够进入 `docs/plans/`
- 什么还不能进入 `docs/survey/`
- 非论文外部输入是否已完成最小分类与边界判定

## 输出格式

默认输出以下结构：

## 当前阶段判断
- 当前最可能所处阶段：
- 已有正式工件：
- 缺失的关键工件：
- 当前是否可进入下一阶段：

## Gate 检查
- 涉及 gate：
- 已满足项：
- 未满足项：
- 若未通过，建议回退到：

## 推荐下一步
- 最该产出的工件：
- 推荐路径：
- 需要补的前置输入：

## 边界
- 仍是线索 / 想法的内容：
- 已有证据支撑的内容：
- 还不能进入正式 survey 的内容：

## 建议动作
1. ...
2. ...
3. ...

如果用户明确要求写入，再额外输出：

## 拟修改文件
- `path`
- `path`

## 修改原则
- ...
- ...

## 项目特定启发式

### 工件优先级
- 新增关键研究活动时，优先补工件，再写实现
- 没有 `decision_id` 的实验，不应进入正式评测结论
- `survey-update-note` 不替代正式章节，只是回写桥梁

### 输入分层
- 论文类材料进入 `evidence-map` 前，可先走 `survey-evidence-mapper`
- 非论文外部输入进入 `evidence-map` 前，先做最小分类与边界判定
- references 索引层更新不等于研究判断已经成立

### 最小推进规则
- 一次只推进一层
- 先判断是否过 gate，再决定是否写下一个工件
- 不因为已有 prototype 就跳过研究判断与架构决策

## 常见错误

### 错误 1：把 ideas 当正式工件
错误：
- 有一份想法笔记，就认为可以直接进 experiment-spec。

更好：
- 先补 `research-brief` 和 `evidence-map`，确认问题、范围和证据边界。

### 错误 2：用实现反推结论
错误：
- 先写代码、跑结果，再倒推出研究判断。

更好：
- 先形成研究判断与架构决策，再进入实现与实验。

### 错误 3：跨 gate 偷跑
错误：
- 没有 `decision_id` 就启动实验，或没有 `evaluation-report` 就回写 survey。

更好：
- 明确 gate，并在未通过时回退到对应前置阶段。

### 错误 4：一次推进整条链
错误：
- 同时起草 brief、decision、experiment、survey update，导致边界混乱。

更好：
- 一次只推进最关键的下一份工件。
