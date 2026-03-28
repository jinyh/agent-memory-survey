---
name: survey-evidence-mapper
description: Use when the user provides a paper PDF, arXiv ID, or local paper path and wants to judge whether it is worth incorporating into this AgentResearch repository. Trigger for requests about whether a paper is relevant, what it supports or does not support, which survey chapter it belongs to, whether it should be a main or supplemental citation, or whether to update docs/ideas, docs/survey, ref/paper, or survey-map based on the paper.
---

# Survey Evidence Mapper

## Overview

This is a project-level skill for AgentResearch.

Use it to map a new paper into this repository's existing evidence structure instead of producing a generic paper summary. The goal is to decide whether the paper is worth borrowing from, what exact claims it supports, what it does **not** support, and where it should land in the repo.

Default to analysis only. Only modify files if the user explicitly asks to update the repository.

## Repository Context

This repository has distinct evidence layers:

- `ref/paper/` — local paper library
- `docs/ideas/` — working judgments, hypotheses, and reusable intermediate analysis
- `docs/survey/*.md` — formal survey chapters
- `docs/survey/survey-map.md` — index layer for survey ↔ code ↔ gaps; never a substitute for chapter prose

Important project rules:

- Prefer minimal changes
- Read target chapters before suggesting edits
- Update survey prose before survey-map
- Do not overstate evidence strength
- Follow document versioning and archive rules when modifying formal docs

## When to Use

Use this skill when the user wants any of the following:

- evaluate whether a paper is worth incorporating
- decide which survey chapter a paper belongs to
- determine whether a paper is a main citation, supplemental citation, or engineering/context material
- extract only the most reusable insights from a paper
- understand what a paper supports vs what it must not be used to support
- map a paper into `ref/paper`, `docs/ideas`, `docs/survey/*.md`, or `docs/survey/survey-map.md`
- update repository docs based on a paper after analysis

Do **not** use this skill for:

- generic literature review with no repository context
- full paper translation
- paper reproduction or implementation
- broad web research unrelated to the project’s survey/evidence structure

## Two Modes

### Mode A — Analysis Only (default)

Default behavior is to analyze and recommend, without editing files.

Always produce:

#### 1. Quick judgment
- Worth incorporating: yes / no / maybe later
- Recommended evidence role: main evidence / supplemental evidence / engineering/context material
- Recommended landing zone: specific survey chapter, `docs/ideas`, `ref/paper`, `survey-map`, or nowhere yet

#### 2. Borrowable insights
Extract only 2-5 project-relevant insights.
Prefer structural takeaways over generic summary.
Good examples:
- representation split
- memory/object/state boundary
- evaluation implication
- systems implication
- evidence-strength implication

#### 3. Boundary check
State explicitly:
- what this paper supports
- what it only weakly reinforces
- what it does **not** support

This is mandatory. A paper that is merely related must not be upgraded into evidence for claims it never studied.

#### 4. Recommended next actions
Choose from:
- add to `ref/paper`
- record judgment in `docs/ideas`
- minimally patch a chapter in `docs/survey`
- update `survey-map` only after chapter changes
- defer, with reason

### Mode B — Analysis + Minimal Writing

Only enter this mode if the user explicitly asks to update the repository, with phrases like:
- write this into the survey
- update the ideas doc
- patch the chapter
- add it to the map
- go ahead and update the docs

In writing mode:

1. Read the relevant existing files first
2. Preserve current anchor structure unless the user explicitly asks to reorganize it
3. Make the smallest viable change
4. Keep evidence language precise
5. If editing formal docs, follow versioning and archive conventions
6. If survey prose changes, update `survey-map.md` afterward if needed
7. Review the final diff before claiming the update is ready

## Required Workflow

### Step 1 — Reconstruct local context

Read the paper and recover the current local context before making any claim.

At minimum, identify:

- whether the paper already exists in `ref/paper/`
- whether there is an existing idea note about it in `docs/ideas/`
- which survey chapter is most likely relevant
- whether the user already framed the target chapter or question

If the user gave no target chapter, infer likely landing zones and say so explicitly.

### Step 2 — Extract only project-relevant structure

Do **not** produce a broad summary first.

Instead, identify:
- the paper’s main representational move
- the control point or system role it changes
- the strongest transferable insight for this repository
- the nearest existing survey concept it maps to

Use the chapter’s vocabulary where possible, not the paper’s marketing language.

### Step 3 — Assign evidence role

Classify the paper into one of these roles:

- **Main evidence** — central citation for a chapter concept
- **Supplemental evidence** — strengthens an existing line without replacing anchor papers
- **Engineering/context material** — useful for interpretation, motivation, system explanation, or implementation framing
- **Not worth incorporating yet** — interesting but not load-bearing for this repo

Prefer conservative placement. Relatedness is not enough for main-evidence status.

### Step 4 — State the boundary

Always say what the paper must **not** be used to support.

Common failure cases to guard against:
- turning a systems paper into governance evidence
- turning a benchmark/demo into mature methodology evidence
- turning a blog/explainer page into an independent academic source
- turning “adjacent to belief/state” into “solves belief revision”
- turning “uses memory in a domain” into “solves memory lifecycle broadly”

### Step 5 — Recommend the repository landing zone

Make concrete recommendations such as:
- `ref/paper/<file>.pdf`
- `docs/ideas/<date>-<topic>.md`
- `docs/survey/07-frontiers.md`
- `docs/survey/02-formation.md`
- `docs/survey/06-systems-and-engineering.md`
- `docs/survey/survey-map.md`

Explain why this layer is the right one.

## Output Format

In analysis mode, default to this exact structure. Only deviate if the user explicitly asks for another format:

## 快速判断
- 是否值得纳入：
- 推荐证据定位：
- 推荐落点：

## 可借鉴点
1. ...
2. ...
3. ...

## 边界
- 支撑：
- 补强但不主导：
- 不支撑：

## 建议动作
1. ...
2. ...
3. ...

If writing mode was requested, add:

## 拟修改文件
- `path`
- `path`

## 修改原则
- ...
- ...

## Project-Specific Heuristics

### Evidence placement heuristics
- Put reusable but not-yet-final judgments in `docs/ideas`
- Put formal claims in `docs/survey/*.md`
- Treat `survey-map.md` as an index layer, not a reasoning dump
- Use `ref/paper` for papers worth keeping locally even if they are only supplemental

### Chapter mapping heuristics
When a paper is relevant to multiple chapters, choose:
- the **primary** chapter where it carries the most explanatory weight
- optionally mention secondary chapters only if the mapping is strong and non-confusing

### Anchor-preservation heuristic
If a chapter already has stable anchor papers, prefer adding a paper as a supplemental line unless it clearly replaces the old anchor.

## Common Mistakes

### Mistake 1: Generic paper summary
Wrong:
- summarizing the paper section by section without repo-specific judgment

Better:
- extract only what changes the survey’s evidence structure

### Mistake 2: Overclaiming
Wrong:
- “this paper proves X” when it only suggests or reinforces X

Better:
- separate support, reinforcement, and non-support explicitly

### Mistake 3: Writing before reading local context
Wrong:
- editing a survey chapter without reading its current anchor structure

Better:
- read chapter first, then patch minimally

### Mistake 4: Confusing ideas with implementation
Wrong:
- writing repo docs as if the code already supports the paper’s capability

Better:
- keep “research inspiration” distinct from “implemented system capability”

## Examples

### Example 1
User: “帮我看看这篇 paper 值不值得进 survey，不要泛泛总结，只看借鉴价值。”

Use this skill.

### Example 2
User: “`2603.03596` 这篇论文应该挂到哪个章节？是主证据还是补充证据？”

Use this skill.

### Example 3
User: “这篇论文我已经放进 `ref/paper` 了，顺手帮我判断要不要更新 `docs/ideas` 和 `07-frontiers.md`。”

Use this skill. Start in analysis mode, then enter writing mode because the user explicitly requested repository updates.
