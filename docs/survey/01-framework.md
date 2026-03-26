# Agent Memory 统一研究框架

> v3.0 | 2026-03-26

## 本章核心判断

Agent Memory 研究已经不适合再以“工作记忆 / 语义记忆 / 情景记忆 / 程序性记忆”的静态分类作为主线。那些类别仍然重要，但它们解释的是“记忆承担什么功能”，而不是“记忆系统如何持续运作”。对于今天的 agent，后者才是决定系统质量的关键。

本章主张一个更有解释力的组织方式：把 memory 看作一个持续运行的生命周期系统：

`formation -> evolution -> retrieval -> evaluation`

核心原因不是概念新鲜，而是这个视角更能解释最近两年的分化。Mem0、LangMem、Zep、Letta/MemGPT、Hindsight、MemAgent、RLM、MSA、TeleMem、Synapse 这些工作表面上分属不同流派，但真正分歧并不在“是不是 episodic memory”，而在它们分别如何处理写入、更新、读取和评测。

## 为什么生命周期比静态分类更有效

静态分类有一个隐含前提：记忆类型先于系统流程被定义好，例如某段信息天然属于 episodic、semantic 或 procedural。这个前提在认知建模里合理，但放到 agent engineering 就不够用了，因为同一条信息在不同阶段可以扮演不同角色。

例如，“用户今天说自己更偏好简洁回答”最初是一条带时间戳的对话事件，属于情景性 observation；如果在多轮交互中被反复验证，它可能被巩固成较稳定的用户偏好；若再被上升为系统规则，甚至会进一步进入 procedural 层。也就是说，memory type 更像演化结果，而不是系统入口。

生命周期框架更有效，是因为它直接面向以下工程问题：

- 什么时候把 observation 升格为长期记忆。
- 新证据到来时是覆盖、版本化还是并存。
- 读取时优先召回稳定知识、最近经历还是可执行策略。
- 评估时到底该测召回、推理、还是长期管理质量。

这些问题都不是静态分类能单独回答的。

## 三个正交维度

生命周期不是要取代所有分类，而是要作为主线，把其他分类降为辅助维度。对当前材料而言，至少有三个正交维度仍然重要。

### 1. 记忆形式

- `external`：向量库、数据库、文件系统、图数据库、对象存储。
- `latent`：KV cache、稀疏注意力、压缩隐状态、原生长记忆机制。
- `parametric`：模型参数中的内化知识。
- `hybrid`：图 + 向量、active state + archive、external + latent。

这一维决定 memory 的存放介质和访问成本。MSA、RLM 更靠近 latent/programmatic memory；Mem0、Zep、Elastic 方案更靠近 external memory；Letta、TeleMem、Hindsight 实际都在做 hybrid。

### 2. 记忆功能

- `working`：当前任务或会话中需要随时可用的状态。
- `episodic`：带时间和主体的经历与事件。
- `semantic`：抽象化、跨会话稳定的知识。
- `procedural`：使用记忆、调用工具、管理上下文的规则或策略。
- `multimodal_spatial`：视觉对象、轨迹、环境拓扑、视频段落等。

这维帮助我们理解“记忆是用来干什么的”。但它不能直接说明这些记忆如何写入与更新，因此只能做配角。

### 3. 生命周期阶段

- `formation`：从 observation 到可持续保存的记忆表示。
- `evolution`：随着新证据到来而更新、压缩、巩固或遗忘。
- `retrieval`：在任务中找到并装配真正有用的记忆。
- `evaluation`：验证 memory layer 是否改善了行为，而不仅是命中了基准。

这维是本文主线，因为它最能解释当前研究的真实矛盾。

## 当前研究的真正分歧：控制权归谁

如果只看论文标题，会误以为当前 memory research 的分歧在表示形式；但从系统设计上看，更关键的是控制权的分配问题。

### 1. 系统规则主导

Mem0、LangMem、Elastic 一类系统通常把控制权放在外部 pipeline：先抽取，再决定 add/update/delete/noop，再基于 metadata + embedding 检索。优点是可解释、易工程化；缺点是高度依赖外部规则质量，且对复杂冲突、长期演化和多跳推理支持不足。

### 2. 模型注意力主导

MSA、部分长上下文原生 memory 模型把检索与读取内化进注意力机制里。优点是端到端、在长上下文任务上可能更优；缺点是管理、审计、权限、删除和跨会话可治理性仍然薄弱。

### 3. Agent 程序主导

RLM 把长输入和中间结果交给 REPL 环境管理，允许 agent 通过代码主动展开、筛选和递归处理。这里的关键不是“有更长上下文”，而是 agent 被赋予了显式操作上下文与中间变量的能力。它让工作记忆从 prompt 变成可编程状态。

### 4. 分层混合主导

Letta/MemGPT、Hindsight、TeleMem 等系统代表的是混合路线：把活跃态、长期库、图、belief、经验轨迹、多模态缓存等分开管理，再通过 memory policy 或工具调用把它们接起来。这类系统最接近长期可部署形态，但复杂度也最高。

## 为什么今天不能把 memory 约化为 RAG

“memory 就是把历史存到向量库里，再按需召回”是第一代工程解法，但它忽略了三个持续扩大的问题。

### 1. 事实会变化

用户搬家、改偏好、换角色、撤回授权都意味着旧记忆不能简单累积。只会 append 的系统会迅速堆出冲突事实；只会 overwrite 的系统则失去历史和审计。

### 2. 记忆不仅是事实，还包括状态与 belief

Hindsight 把 world、experience、opinion、entity/observation 分开，就是因为“我观察到 X”与“我因此相信 Y”不该混放。前者是证据，后者是带置信度的推断。很多系统出问题，正是因为把两者都塞成同类文本块。

### 3. 记忆价值取决于是否被正确使用

大量 benchmark 测的是“有没有把正确片段找回来”，但真正难的是“agent 是否据此改变行为”。如果系统召回了正确记忆，但 agent 仍然没用上，那问题其实出在 context assembly、tool policy 或 deliberation，而不只是 retrieval。

## 证据与局限

从当前资料看，检索阶段的实验最充分。Mem0、MSA、MemAgent、RLM 等至少给出了相对清晰的基准与对比。相较之下，formation 与 evolution 往往只有局部实验或系统叙事，尤其是关于冲突更新、遗忘治理、删除权和权限边界的证据仍弱。

这意味着一个常见误区必须避免：不要把 retrieval 上的高分直接当作 memory layer 成熟的证据。很多系统在 benchmark 上表现不错，但还没有充分证明它们能够长期处理 versioning、belief correction、auditability 或 multi-agent consistency。

## 对本仓库的意义

这套框架给本项目三个直接约束：

1. survey 主线继续按生命周期组织，而不是按记忆类型罗列。
2. `paper` 作为主证据，优先用于支持生命周期判断与方法对比。
3. 任何概念原型都不应只展示“存了和取了”，而应至少能体现 formation、evolution、retrieval 的最小闭环。

## 代表工作定位

- `Mem0 / LangMem`：代表 retrieval-centric memory service，帮助说明为什么 lifecycle 不能被压缩成单一检索问题。
- `Letta / MemGPT`：代表 memory management 被提升为 agent 行为本身的路线。
- `Hindsight`：代表 belief-aware 分层记忆，对“事实 vs belief”区分最有启发。
- `RLM / MSA`：代表程序化工作记忆与内生长记忆机制，说明 memory 不只存在于外部库。
- `TeleMem`：代表多模态长期记忆开始改写 memory 对象边界。

## 本章主要证据来源

- `paper`：Mem0、Hindsight、RLM、MSA、TeleMem、Agent memory survey 类论文。
- `blog`：Elastic 的 memory architecture 实践、Letta 的 stateful agents 叙事、benchmark 比较文章。
- `综合推断`：生命周期优于静态分类，是基于以上系统控制权分布与证据强弱做出的组织性判断。
