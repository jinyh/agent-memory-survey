# MAGMA / MIRIX Systems Note

## 背景
这两篇都更适合放在 systems 章节，而不是主导 frontier 或 evaluation：
- MAGMA：multi-graph agentic memory architecture
- MIRIX：multi-agent memory system with layered memory types

它们共同说明，Agent Memory 正在从单一 retrieval store 演化为结构化 memory substrate 和协调式 control plane。

## 核心判断
### MAGMA
- 角色：补充证据
- 推荐落点：`06-systems-and-engineering.md`
- 次级落点：`04-retrieval.md`

#### 最值得借鉴的结构
1. 把 memory item 分解到 semantic / temporal / causal / entity 四个正交图上。
2. 把 retrieval 写成 policy-guided traversal，而不是简单 top-k 召回。
3. 明确 decouple memory representation 和 retrieval logic。

#### 适合支撑的论点
- 图记忆的价值不只是关系建模，而是 query-adaptive traversal 和透明 reasoning path。
- memory architecture 可以通过分离表示与检索获得更强控制力。

#### 不能支撑的论点
- 不能说明治理、删除、审计已成熟。
- 不能说明 formation / evolution 已被白盒充分评测。

### MIRIX
- 角色：强补充证据
- 推荐落点：`06-systems-and-engineering.md`
- 次级落点：可弱挂 `07-frontiers.md`

#### 最值得借鉴的结构
1. 六类 memory：Core / Episodic / Semantic / Procedural / Resource Memory / Knowledge Vault。
2. multi-agent 框架动态协调更新与检索。
3. 同时面向 multimodal 和 long-term personalization，而不是单一文本记忆。

#### 适合支撑的论点
- memory 作为系统资源，需要分层与协调，而不是单一 store。
- multi-agent 场景下 memory 需要显式更新控制与共享机制。

#### 不能支撑的论点
- 不能说明长期治理与删除问题已解决。
- 不能说明它已经替代现有 systems 主锚点。

## 结论
- MAGMA 更适合作为 graph memory / structural retrieval 的补充证据。
- MIRIX 更适合作为 multi-agent memory system 的强补充证据。
- 两者都应先作为 `docs/ideas` 候选判断，后续如写 survey 再决定是否进入正文。
