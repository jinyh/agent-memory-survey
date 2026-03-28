# Agentic Memory 与 Vectorless RAG 的可借鉴点映射

## 背景

对照了两篇未提交博客草稿：

- `ref/blog/Agentic Memory- A Detailed Breakdown.md`
- `ref/blog/Building Vectorless RAG System (No Embeddings, No Vector DB.md`

它们都和本项目的 agent memory 主线相关，但作用层次不同：前者更适合作为 lifecycle 叙事与系统边界补充，后者更适合作为 retrieval / compression 结构设计灵感。

## 核心内容

### 一、适合借到 survey 的部分

#### 1. `Agentic Memory` 可强化 lifecycle 叙事

最值得借的是三个视角：

- `continuity / context / learning` 三分法，有助于解释 memory 为什么不只是长期事实库
- `retrieval before, writing after`，很适合作为 memory 闭环的直观表达
- `system prompt / conversation / tool results / retrieved memories / scratchpad` 的上下文分层，有助于说明 active state 与长期态的区别

这些内容更适合作为 survey 中的工程补充与组织性叙事，而不是正式主证据。

#### 2. `Vectorless RAG` 可补充 retrieval 的另一种范式

最值得借的是：

- hierarchical page indexing
- bottom-up summaries
- top-down routing
- retrieval 作为“逐层导航”而不是一次性 top-k

它的价值不是替代向量检索，而是说明 retrieval 还可以是结构化、可解释、可逐层展开的读取过程。

### 二、适合借到 code 设计理解的部分

#### 1. 对 `src/memory/manager.py` 的启发

当前 `MemoryManager` 已经提供：

- 多 store 调度
- rank fusion 检索
- update / delete
- episodic → semantic consolidation

因此它已经是一个不错的 lifecycle 最小骨架。

但如果用这两篇草稿反过来看，当前实现还缺几类更明确的一等概念：

- `active state`：始终装载的近期上下文层
- `hierarchical routing`：不是固定 top-k，而是按层逐步读取
- `version semantics`：更新不只是覆盖，而是显式记录新旧边界
- `belief-aware update`：区分 evidence、belief、summary 的演化逻辑

#### 2. 对 `src/memory/evaluation.py` 的启发

当前评测更偏 retrieval case 归一化与 hit@k / MRR 一类指标，这和项目既有判断一致：

- retrieval 最容易评测
- retrieval 命中不等于 memory 被真正用到
- retrieval benchmark 不能直接替代 lifecycle benchmark

`Vectorless RAG` 提醒了一个额外问题：即便检索过程可解释，也不代表它已经覆盖 formation / evolution / governance。

### 三、不建议直接迁移的部分

- 不应把 `Vectorless RAG` 直接写成 agent memory 方案，它更像文档级结构化检索范式
- 不应把 importance scoring、nightly consolidation、reflection loop 等 blog 经验直接写成已验证结论
- 不应把“能层次化检索”误写成“已经解决 memory in use”

## 结论

这两篇草稿都值得保留，但用途不同：

- `Agentic Memory` 更适合补 lifecycle、上下文分层和 memory 闭环叙事
- `Vectorless RAG` 更适合补 retrieval / compression 的结构设计视角

对 AgentResearch 来说，最合理的做法不是把它们并入同一理论，而是把它们分别挂到：

- survey 的工程补充层
- code 的设计启发层
- ideas 的轻量记录层

## 可能的下一步

1. 继续把 `Agentic Memory` 中的上下文分层对齐到 `06-systems-and-engineering.md`
2. 单独整理“分层 / 路由式 retrieval”小专题，对齐 `04-retrieval.md` 与 `src/memory/manager.py`
3. 若后续进入实现阶段，再讨论 active state 或 hierarchical routing 是否值得进入代码原型

## 待确认事项

- 是否要继续把这份记录扩写成 `docs/plans/` 里的正式研究条目
- 是否需要进一步同步 `docs/survey/README.md`，把这种“工程补充 vs 主证据”的边界写得更显式
