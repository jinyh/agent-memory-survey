# WorldMM Frontiers Note

## 背景
WorldMM 是一篇面向长视频 reasoning 的多模态 memory agent。
它最重要的不是单点 benchmark 分数，而是把记忆对象拆成：
- episodic memory
- semantic memory
- visual memory

这使它更适合放在 frontier 章节，而不是 systems 主线。

## 核心判断
- 角色：补充证据
- 推荐落点：`07-frontiers.md`
- 不建议直接替代的主锚点：TeleMem、Think3D、RenderMem

## 最值得借鉴的结构
1. 记忆对象不只是文本事实，而是视觉证据、事件与高层语义的组合。
2. 推理过程通过 adaptive retrieval agent 在多个 memory source 间选择。
3. 长视频场景强调多粒度 temporal memory，而不是单一摘要或固定窗口。

## 适合支撑的论点
- 多模态 memory 需要保留视觉细节与高层语义的双层结构。
- frontier 方向正在从 caption/summary 检索转向长时程视觉状态组织。
- adaptive retrieval 比固定检索窗口更适合长视频 reasoning。

## 不能支撑的论点
- 不能说明统一评测标准已经稳定。
- 不能说明治理、删除、审计问题已成熟解决。
- 不能说明它已经成为 frontiers 主锚点。

## 结论
- WorldMM 适合作为 `07-frontiers.md` 的多模态视频记忆补充证据。
- 它的价值在于说明：frontier memory 已经进入 long-video / multi-source retrieval / visual-state organization 的阶段。
- 现阶段不建议把它升为主锚点。
