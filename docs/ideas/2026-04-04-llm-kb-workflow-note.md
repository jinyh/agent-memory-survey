# LLM Knowledge Bases Workflow Note

## 背景
这份记录用于评估 `ref/blog/LLM Knowledge Bases.md` 在 AgentResearch 中的角色与边界。该材料提出的是一种由 LLM 持续编译 markdown/wiki 的个人研究知识库 workflow，而不是完整的 Agent Memory 生命周期方案。

## 核心判断
- 角色：`engineering supplement` + `implementation inspiration`
- 主落点：`docs/ideas/`
- 次落点：未来若证据增强，可最小补入 `docs/survey/06-systems-and-engineering.md`
- 不建议直接进入 `docs/survey/01-framework.md`
- 它更像 knowledge-base workflow，而不是完整 Agent Memory lifecycle 方案。

## 适合支撑的论点
1. LLM-compiled wiki 是一种自然的知识组织工程路径。
2. `summary / index / backlinks` 可作为小规模知识库中的轻量 retrieval substrate。
3. 查询结果回写知识库，可视作轻量 knowledge evolution 机制。
4. consistency / health checks 可启发 KB 完整性维护与 control plane 补充设计。

## 不能支撑的论点
1. 不能支撑新的 Agent Memory 主框架判断。
2. 不能说明 formation / evolution / evaluation 已被系统性解决。
3. 不能把“小规模下无需 fancy RAG”推广成一般研究结论。
4. 不能把个人研究知识库 workflow 直接提升为通用 memory architecture。

## 对本仓库的启发
1. 可作为 `LLM-compiled knowledge base as memory-adjacent workflow` 候选主题保留在 `docs/ideas/`。
2. 若后续进入研究验证，可设计 `raw docs vs compiled wiki` 的对比实验。
3. 若后续进入 survey，只适合 systems 工程补充位。
4. 若后续落到实现，需优先补 provenance、versioning、污染控制与撤销机制约束。

## 结论
- 这篇 blog 值得保留，但应按工程补充与设计启发处理。
- 当前最合适的做法是先沉淀到 `docs/ideas/`。
- 只有在补足更多证据或实验后，再考虑升级到 survey 或正式研究工件。
