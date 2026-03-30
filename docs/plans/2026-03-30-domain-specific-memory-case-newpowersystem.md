# Domain-Specific Memory Case：以 NewPowerSystem 为例的垂直知识库型 Agent Memory

> status: draft | owner: Claude | 2026-03-30

## question_id

`RQ-001`

## related_refs

- `docs/ideas/2026-03-30-lifecycle-benchmark-construction-rules.md`
- `docs/plans/2026-03-28-memory-lifecycle-closed-loop-from-benchmarks.md`
- `docs/architecture/2026-03-29-memory-system-overview.md`
- `/Users/jinyh/Documents/AIprojects/NewPowerSystem/README.md`
- `/Users/jinyh/Documents/AIprojects/NewPowerSystem/CLAUDE.md`
- `/Users/jinyh/Documents/AIprojects/NewPowerSystem/docs/plans/2026-03-10-gridclaw-skill-lib-design.md`

## 这份文档回答什么

这不是一个面向 `AgentResearch/src/memory` 立即实现的代码设计稿，而是一份**研究版 architecture note**，回答三个问题：

1. `AgentResearch` 中关于 formation / evolution / retrieval / memory-in-use 的 lifecycle 框架，如何落到一个具体垂直领域项目中。
2. 对于 `NewPowerSystem` 这类结构化知识库项目，什么样的 memory 才真正有用，什么样的 memory 只是检索增强的错觉。
3. 领域型 memory 应如何与项目 skill lib 对齐，使其成为 knowledge state layer，而不是另一套孤立系统。

## 核心判断

### 判断 1：`NewPowerSystem` 是一个适合观察 domain-specific memory 的真实样本

`NewPowerSystem` 当前不是以任务执行为主的 agent 系统，而更像一个：

- 结构化知识库
- 面向多类读者的教学/解释系统
- 具备 source registry、专题分层、案例、代码示例与学习路径的内容工程

因此，它不是“通用聊天记忆”的天然样本，而是**垂直知识库型 agent memory** 的代表样本。

### 判断 2：这类项目的 memory 重点不应是会话偏好，而应是知识状态

在 `NewPowerSystem` 中，memory 的核心不是：

- 用户今天喜欢什么语气
- 上一轮对话提到什么临时约束

而是：

- 哪些领域知识单元应进入长期状态
- 这些知识单元处于哪一篇文章、哪一个专题、哪一条学习路径中
- 它们和哪些概念有桥接、对比或依赖关系
- 面向不同读者应如何解释同一事实

因此，`NewPowerSystem` 对应的是一种 **knowledge-state-centric memory**，而不是 preference-centric memory。

### 判断 3：它能补充 AgentResearch 对 memory-in-use 的理解

当前很多 agent memory 讨论天然偏向：

- retrieval
- chat preference
- task state

但 `NewPowerSystem` 显示，memory-in-use 还可以是：

> 将取回的事实、脉络与解释视图组织为面向特定读者的教学型回答。

这说明在垂直知识库型场景里，memory-in-use 的关键不只是“回忆成功”，而是“组织解释成功”。

## 与 AgentResearch lifecycle 的对应关系

`AgentResearch` 的 lifecycle 框架可以在 `NewPowerSystem` 中被重新翻译为：

| lifecycle 阶段 | 在通用 memory 中常见含义 | 在 NewPowerSystem 中的具体对应 |
|---|---|---|
| formation | 写入用户偏好、事件或任务状态 | 将高价值领域知识单元、来源关系、章节位置、解释视图写入长期状态 |
| evolution | 用户偏好变化、冲突事实更新、遗忘 | 政策变化、技术判断变化、来源修订、概念桥接修正、教学视图更新 |
| retrieval | 为回答问题召回相关历史 | 同时召回事实段落、章节脉络、概念桥接与教学视图 |
| memory-in-use | 在当前任务中利用取回记忆 | 组织成适合电力从业者 / AI 背景 / 跨学科读者的解释、对比与导学回答 |

这个映射表明：

- `NewPowerSystem` 不是对 lifecycle 的机械套用；
- 它把 lifecycle 变成了**领域知识系统中的版本**；
- 因而可以作为 `AgentResearch` 中一个重要的 domain-specific case。

## 领域型 memory 的推荐形态

### 不推荐的路线

以下路线都不适合作为 `NewPowerSystem` 的第一阶段 memory 方案：

1. **纯 benchmark 泛化路线**
   - 只讨论怎么评测，不回答项目中 memory 到底存什么
2. **重图谱优先路线**
   - 长期有价值，但第一阶段建模成本过高
3. **对话/用户优先路线**
   - 更适合教学应用层，而不适合作为共享内核起点
4. **三套独立 memory 路线**
   - 知识助手、研究协作、任务执行各建一套，后续会导致状态分裂

### 推荐路线：共享内核 + 知识助手视图

推荐方案是：

- **总蓝图**：分层共享内核
- **第一阶段落点**：知识助手视图
- **组织路线**：文档中心型 memory
- **回答优先场景**：解释与教学
- **粒度**：以段落为主，但保留完整脉络
- **解释策略**：一个事实，多种解释视图

也就是：

> 先以段落作为最小事实单元，再在其上叠加章节脉络、概念脉络、学习脉络与读者适配视图。

## 推荐 schema（研究抽象层）

第一阶段的共享内核可以抽象为四类对象：

### 1. `ParagraphMemory`

作用：最小事实载体。

代表字段：
- `memory_id`
- `content`
- `doc_path`
- `section_path`
- `topic_id`
- `paragraph_index`
- `source_refs`
- `keywords`
- `term_refs`
- `updated_at`
- `version`

### 2. `ContextEnvelope`

作用：章节脉络层，恢复“这段话在整体中的位置”。

代表字段：
- `parent_doc`
- `chapter_title`
- `section_title`
- `article_role`
- `previous_context`
- `next_context`
- `belongs_to_learning_stage`
- `reader_relevance`

### 3. `ConceptLink`

作用：轻量概念脉络层，不要求第一阶段即构成完整图谱。

代表字段：
- `concepts`
- `bridges_to`
- `related_topics`
- `contrast_with`
- `depends_on`
- `extends_to`

### 4. `TeachingView`

作用：支持“一个事实，多种解释视图”。

代表字段：
- `audience_views.power_practitioner`
- `audience_views.ai_reader`
- `audience_views.cross_disciplinary`
- 每个视图下的：
  - `explain_focus`
  - `preferred_analogy`
  - `avoid_terms`
  - `prerequisites`
  - `next_topics`

## 数据流（研究版抽象）

推荐的数据流是：

`文档形成 -> 结构补全 -> 视图派生 -> skill 使用`

### 阶段 1：文档形成

从：
- `docs/zh/*`
- `README.md`
- `CLAUDE.md`
- `references/`

中抽取段落级单元，形成 `ParagraphMemory`。

### 阶段 2：结构补全

为每条段落补章节与专题位置，形成 `ContextEnvelope`。

### 阶段 3：视图派生

从段落和结构中补：
- `ConceptLink`
- `TeachingView`

### 阶段 4：skill 使用

skill 不直接面向原始 markdown，而是通过 memory 核心暴露的能力工作。

## 与 skill lib 的关系

研究上最关键的原则是：

> **Skill 面向任务，Memory 面向知识状态；Skill 不应直接依赖文件路径，而应依赖 Memory 提供的事实、脉络、桥接和教学视图能力。**

因此，`NewPowerSystem` 中的 skill lib 可以理解为 `memory-in-use` 的操作面，而不是 memory 本体。

推荐抽象出四类 memory ability：

1. `resolve_facts`
2. `resolve_context`
3. `resolve_teaching_view`
4. `resolve_bridges`

这四类能力分别支撑：

- 解释型 skill
- 溯源型 skill
- 对比/桥接型 skill
- 导学型 skill

## 研究价值

把 `NewPowerSystem` 作为 domain-specific memory case，有三层研究价值：

### 1. 补充 benchmark 之外的真实 memory 场景

它提醒我们：很多有价值的 memory 行为，并不天然表现为 benchmark QA，而表现为：

- 教学型解释
- 来源追溯
- 跨主题桥接
- 学习路径组织

### 2. 扩展 memory-in-use 的定义

在该场景里，memory-in-use 的成功标准不是“命中一条相关文本”，而是：

- 能否讲清楚
- 能否讲成体系
- 能否按读者类型切换解释方式

### 3. 为后续 evaluation 提供新任务来源

未来如果要扩展 AgentResearch 的 evaluation，这类场景可以派生出新的领域型任务，例如：

- 同概念多读者解释任务
- 来源可追溯回答任务
- 跨章节桥接任务
- 更新后知识修订任务

## 第一阶段边界

这份研究 note 明确主张：

### 第一阶段要做的

- 以段落为最小事实单元
- 补章节脉络
- 补轻量概念桥接
- 为高价值知识单元补多读者解释视图
- 让 skill 通过 memory ability 层工作

### 第一阶段不做的

- 不做完整概念图谱
- 不做任务执行型 memory
- 不做重自动化 evolution
- 不把它直接上升为“通用 benchmark”

## 对 AgentResearch 的建议落点

这份 note 最适合在 `AgentResearch` 中作为：

- 一份 `domain-specific memory architecture note`
- 一份连接 lifecycle 理论与垂直知识库实践的中间工件

它不替代：

- `research-brief`
- `experiment-spec`
- `evaluation-report`

但它可以为这些正式工件提供：

- 领域案例
- 问题实例
- memory-in-use 的新定义来源
- 未来 evaluation task 的设计参照

## 最终结论

`NewPowerSystem` 说明，在垂直知识库型场景中，memory 的核心不是聊天偏好，也不是单层检索，而是：

> **以知识事实为底座，以章节/概念/学习脉络为组织层，以多读者解释视图为适配层，并通过 skill 将这些状态转化为教学型行为。**

这使它成为 `AgentResearch` 中一个有代表性的 **domain-specific memory case**：

- 它把 lifecycle 理论翻译成领域知识系统语言；
- 它补足了 memory-in-use 在教学/解释任务中的具体形态；
- 它为未来的领域型 evaluation 提供了真实任务来源。
