# EverMemOS Systems Note

## 背景
EverMemOS 是近期一篇很典型的 memory OS 路线论文。
它的摘要明确把 memory 组织成一个自组织的操作系统，并提出：
- Episodic Trace Formation
- Semantic Consolidation
- Reconstructive Recollection

这份笔记用于判断它在本仓库里应该作为哪一层证据使用。

## 核心判断
- 角色：强补充证据
- 推荐落点：`06-systems-and-engineering.md`
- 不建议直接替代的主锚点：Letta / MemGPT、Hindsight、Mem0

## 最值得借鉴的结构
1. 它不是只做 retrieval，而是显式把 memory 写成 lifecycle。
2. 它把 memory object 化为 `MemCells -> MemScenes`，这比简单 vector store 更接近系统架构。
3. 它把 formation、consolidation、recollection 串成一个可运行的 Memory OS 视角。
4. 它隐含支持 active state / archive 分层，这和本仓库 `06-systems-and-engineering.md` 的 control plane 讨论很接近。

## 适合支撑的论点
- memory layer 正在从外挂检索器变成状态管理与认知控制层
- 系统层开始显式内化 lifecycle，而不是只做召回
- 结构化 memory object 比纯文本池更适合长期组织

## 不能支撑的论点
- 不能说明治理、审计、删除、隔离已经成熟
- 不能说明它已经替代 Letta/MemGPT 成为主线
- 不能说明 benchmark 上的表现就能推出完整 lifecycle 健壮性
- 不能说明 belief-aware architecture 已经被系统性解决

## 结论
- EverMemOS 值得保留为 `06-systems-and-engineering.md` 的强补充证据。
- 它最适合用于说明：Memory OS 路线仍在演化，而且已经开始把 lifecycle object 化、结构化。
- 现阶段不建议把它升级为 systems 章节主锚点。
