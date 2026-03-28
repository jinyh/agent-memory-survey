# 07-frontiers 外部材料评估：MEM 论文与 PI memory 页面

## 背景

这条记录用于评估两份外部材料对 `docs/survey/07-frontiers.md` 的价值，并明确它们在本仓库中的落点：

- `arXiv:2603.03596`：`MEM: Multi-Scale Embodied Memory for Vision Language Action Models`
- `https://www.pi.website/research/memory`

当前 `07-frontiers.md` 的主轴是多模态长期记忆、空间 / 具身记忆、belief-aware world state、安全与权限治理、删除与可撤销性。因此，这次关注的不是“这两份材料是否有趣”，而是：

1. 它们是否真的补强了 frontiers 章节的核心判断。
2. 它们更适合作为主证据、补充证据，还是工程说明。
3. 是否值得进入 `ref/paper`。

## 核心内容

### 一、适合借到 survey 的部分

#### 1. `2603.03596` 对 `07-frontiers` 有直接启发

这篇论文最有价值的地方，不是泛泛地说明“机器人也需要记忆”，而是把 frontier 中的一个关键分支讲得更具体：

- memory 可以同时分成短期视频记忆与长期语言记忆
- 短期视频记忆负责最近观察、遮挡、自遮挡、细粒度操作动态与即时 re-grasp 等问题
- 长期语言记忆负责压缩后的语义事件摘要，用来维持 recipe progress、object-state、environment-state 这类长时任务状态
- memory 服务的不只是回忆事实，而是长时任务中的行动状态维持
- world-state memory 不一定表现为显式 3D 地图，也可以表现为 task-progress / object-state / environment-state 的持续表示

因此，它对 `07-frontiers.md` 至少补强了三点：

- `多模态长期记忆`：说明记忆对象确实已经从文本扩展到视频观察与任务状态
- `空间 / 具身记忆`：说明 memory 与 action loop 已形成闭环，重点不只是检索，而是执行中的状态维持
- `belief-aware world state` 的邻近语义：虽然它不直接解决 belief revision，但强化了“memory layer 正在变成 agent 的持续状态层”这个总判断

更合适的定位是：`07-frontiers` 的**补充证据**，而不是替换 `TeleMem`、`Think3D`、`RenderMem` 的主锚点。

#### 2. `pi.website/research/memory` 适合作为同研究线的解释页

这个页面最大的价值不是新增独立证据，而是把同一条研究线的直觉讲得更清楚：

- 为什么需要 multi-scale memory
- 为什么短期保留视觉细节、长期保留语言抽象是合理分工
- 为什么 partial observability、长时任务、in-context adaptation 会把 memory 从“附加模块”推向“状态层”

它更像研究介绍页或系统说明页，适合作为理解论文动机与任务设置的补充材料，而不是正式 paper evidence。

### 二、适合借到 code 设计理解的部分

这条研究线对本项目的启发，主要不是让代码立刻去复制机器人系统，而是帮助澄清几个设计概念：

1. **多尺度 memory**
   - 不是所有 memory 都应该用同一种表示与时间尺度处理。
   - 高频 observation 与低频 summary 更适合分层管理。
   - 短期视频记忆与长期语言记忆的分工，说明“不同时间尺度 + 不同表示”的组合在 agent memory 中是第一性设计，而不是后期优化。

2. **memory 作为状态层，而非静态事实库**
   - 在 embodied / long-horizon 任务里，memory 保存的是“当前世界推进到了哪里”，而不只是“过去说过什么”。
   - 这有助于区分 active state、episodic trace、semantic summary。
   - MEM 的长期语言记忆本质上是 semantic event summary，而不是完整观测日志。

3. **memory 与 action 的闭环**
   - 看见什么会影响写入什么。
   - 已写入什么又决定下一步采取什么动作。
   - 这类闭环比纯文本 chatbot 的长期记忆更接近 frontier 所说的 world-state layer。

4. **compression 是 memory 设计本身，不只是系统优化**
   - 论文里语言记忆的 summarization / compression 不是附带技巧，而是为了避免把长序列历史直接塞入策略后带来的 latency 失控。
   - 它同时减少训练阶段与推理阶段的分布漂移：训练里常见的是一次成功的子任务指令序列，推理里却可能出现反复失败和重试，因此需要 memory 主动压缩并丢弃不再相关的信息。

这些启发适合保留在 ideas 或后续设计文档中，但不应被误写成“当前代码已经支持 embodied multi-scale memory”。

### 三、不建议直接迁移的部分

#### 1. 不应把 `2603.03596` 写成治理或 belief revision 证据

这篇论文与 frontiers 高度相关，但它主要覆盖的是：

- embodied multimodal memory
- long-horizon task state
- short-term observation 与 long-term semantic memory 的分层
- 通过 memory compression 控制 latency，并缓解长时任务中的训练-推理分布漂移

它**不直接支撑**以下结论：

- 删除与可撤销性已有成熟机制
- 审计、权限治理、安全隔离已有稳定方案
- observation / hypothesis / experience 的 revision schema 已被系统性解决

#### 2. 不应把 `pi.website/research/memory` 当成论文证据

这个页面和论文同线，但本质上仍是研究介绍页。它可用于帮助理解，不应和 arXiv 论文并列计作两份独立学术证据。

#### 3. 不应因为这篇论文相关度高，就改写现有主锚点结构

`07-frontiers.md` 当前的主代表工作定位仍然成立：

- `TeleMem`：多模态长期 memory 的系统级主证据
- `Think3D`：空间 / 主动探索路线主锚点
- `RenderMem`：rendering as retrieval 的世界状态主锚点

`2603.03596` 更适合作为补充线索，用来补强“具身任务中的多尺度状态记忆”这一侧面。

## 结论

结论很明确：

- `2603.03596` 值得纳入 `ref/paper`，因为它对 `07-frontiers` 的 embodied multimodal memory / task-progress world-state 分支有直接补强作用。
- `pi.website/research/memory` 有启发，但更适合作为工程 / 项目说明，不建议进入 `ref/paper`。
- 本次最合理的做法是：把论文纳入本地论文库，把这组判断记录到 `docs/ideas`，并以补充证据的方式最小化更新 `07-frontiers.md`。

## 可能的下一步

1. 如果后续要增强 `07-frontiers.md` 的 embodied 证据链，可把 `2603.03596` 写入“补充线索”或“代表工作定位”的邻近说明中。
2. 若未来继续积累同类论文，可以单独整理一个“task-progress / world-state memory”小专题，而不把它混写成纯空间记忆路线。
3. 如果后续代码原型要扩展 frontier 方向，可进一步讨论 active state、multi-scale memory、task-progress state 是否值得进入实现层。

## 待确认事项

- 是否要在后续版本把 `2603.03596` 显式挂到 `07-frontiers.md` 的补充证据位置。
- 是否要把这条研究线同时映射到 `02-formation.md` 或 `06-systems-and-engineering.md`，用于解释 active state 与 long-term state 的边界。
- 是否需要未来为 `pi.website/research/memory` 这类页面单独建立 project/blog 参考入口，而不是混入 paper 层。