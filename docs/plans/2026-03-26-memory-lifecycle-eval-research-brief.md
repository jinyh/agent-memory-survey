# RQ-001：Agent Memory 全生命周期评测框架研究

> status: active | owner: Research Lead | 2026-03-26

## question_id

`RQ-001`

## 研究问题

当前 Agent Memory 研究在检索端论文最密集、结果最可量化，但 formation 与 evolution 端普遍只有启发式规则或薄弱实验。现有 benchmark（LoCoMo、LongMemEval、MemoryAgentBench、MemoryArena、AMA-Bench）大多只测「能否从历史中找到正确答案」，未能覆盖写入质量、更新一致性与遗忘正确性。

核心问题：**如何设计并实证一套能覆盖 `formation → evolution → retrieval` 全生命周期的最小可用评测框架，并明确每个阶段当前证据的边界在哪？**

## scope

- 分析现有 benchmark 的评测覆盖范围，建立「评了什么 / 没评什么」的结构化对比矩阵
- 提出覆盖三个生命周期阶段的最小指标集：
  - **formation 质量**：写入选择准确率、冗余率、结构一致性
  - **evolution 正确性**：冲突解决准确率、时效衰减可控性、遗忘边界清晰度
  - **retrieval 忠实度**：hit@k、MRR、跨会话一致性（已有基线，需对齐前两个阶段）
- 在 `src/memory/evaluation.py` 现有骨架基础上，扩展支持 formation 和 evolution 指标
- 将框架结论回写到 `docs/survey/05-evaluation.md`，补充「当前 benchmark 未覆盖范围」一节

## non_goals

- 不构建新的大规模 benchmark 数据集（仅复用或小规模扩展现有工件）
- 不评测多模态或空间记忆（frontier 方向，留给 RQ-002+）
- 不解决多 agent 并发写入的一致性问题（超出当前原型边界）
- 不改变 survey 的生命周期框架本身（RQ-001 只填评测缺口，不重构框架）

## success_criteria

1. 能对现有 5 个主流 benchmark 给出「覆盖 / 部分覆盖 / 不覆盖」的结构化判断，依据来自论文证据而非工程叙事
2. formation 和 evolution 至少各有 2 个可量化指标，并在 `src/memory/evaluation.py` 中有对应实现
3. `evaluation-report` 产物能同时呈现三个阶段指标，结果可复现（固定 seed + ground truth）
4. `docs/survey/05-evaluation.md` 中「benchmark 覆盖边界」一节有明确论文证据支撑，而非综合推断

## initial_evidence

### 直接相关

- `MemoryAgentBench`（arXiv:2507.05257）：将评测维度扩展到 test-time learning / long-range understanding / selective forgetting，是已知最接近 evolution 评测的 benchmark
- `MemoryArena`：multi-session agent-environment loop 评测设计，比单轮对话 QA 更能暴露 formation 和 evolution 缺陷
- `AMA-Bench`：agent trajectory + tool use 视角，覆盖 formation 后的使用效果
- `Hindsight`：提出了 memory 评测的因果视角（retrospective annotation），是 formation 质量分析的重要参照
- `LongMemEval`：长对话记忆 QA，目前覆盖最广但仍以 retrieval 为主

### 补充参照

- `Mem0`（工程）：formation 触发逻辑与写入选择策略的工程基线
- `MemAgent`（arXiv:2507.02259）：RL-based memory agent，evolution 可学习化的论文证据
- `MemSkill`：memory operation 可学习化，补充 evolution 的规则工程替代路线
- `Synapse`：evolution 中的 episodic 压缩与巩固机制

### 证据缺口（已知）

- formation 质量目前无独立 benchmark，现有系统评测多为端到端，无法单独归因写入错误
- evolution 正确性（特别是冲突解决和遗忘边界）几乎无论文级实验，主要停留在系统设计叙述
- 三阶段联合评测（同一场景下同时测 formation + evolution + retrieval）目前尚无公开工作
