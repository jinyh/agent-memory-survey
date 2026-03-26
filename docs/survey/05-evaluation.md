# Evaluation：Agent Memory 到底在评测什么

> v3.0 | 2026-03-26

## 本章核心判断

当前 Agent Memory 评测的最大问题，不是缺基准，而是经常没有把“评测什么”说清楚。很多结果看起来在比较 memory system，实际比较的是：

- 召回器质量。
- prompt 装配。
- 基座模型能力。
- 框架实现细节。
- 特定 benchmark 的偏置。

因此，本章的第一原则是：在看分数前，先问它究竟在评测什么。

## 研究矩阵：不同评测口径分别回答什么

| 评测层次 | 主要问题 | 典型指标/任务 | 优势 | 局限 | 当前证据强度 |
| --- | --- | --- | --- | --- | --- |
| retrieval hit | 能否从长历史中命中相关证据 | recall、QA accuracy、time-aware QA | 可标准化、易复现、易比较 | 不能证明记忆被真正使用 | 高 |
| memory-in-use | agent 是否据记忆改变行为 | 跨会话任务成功率、一致性决策 | 更接近真实 agent 行为 | 变量多，实验控制难 | 中 |
| 长期管理能力 | 能否处理更新、belief、删除、隔离 | versioning、deletion、conflict handling | 能直接暴露部署风险 | 缺少成熟公共 benchmark | 低 |
| 成本与治理 | 系统是否可落地 | latency、token、索引成本、审计能力 | 回答“能不能上线” | 常被论文忽略，口径不统一 | 低中 |
| 系统内 benchmark | 是否在特定设计目标下有效 | 厂商或框架自定义 leaderboard | 能对齐系统自有假设 | 易发生 benchmark alignment | 中 |

## 关键概念与代表引用

- retrieval hit
  本文语义：评测系统能否从长历史中命中相关证据。
  主代表引用：`LoCoMo`
  证据类型：`主证据`
  边界说明：支撑 recall/time-aware QA 的可比较性，不支撑记忆已真正影响行为。
- multi-session loop
  本文语义：评测对象应包含持续交互中的 `memory-agent-environment loop`。
  主代表引用：`MemoryArena: Benchmarking Agent Memory in Interdependent Multi-Session Agentic Tasks`
  证据类型：`主证据`
  边界说明：支撑多 session、互依任务下的 memory-in-use，不支撑治理与删除问题已覆盖。
- trajectory-based evaluation
  本文语义：agent memory 应在真实或合成 trajectory 中评测，而不是只看对话回放。
  主代表引用：`AMA-Bench: Evaluating Long-Horizon Memory for Agentic Applications`
  证据类型：`主证据`
  边界说明：支撑 agent trajectory + tool use 的评测对象升级，不支撑所有应用场景都能被统一抽象。
- test-time learning / selective forgetting
  本文语义：memory benchmark 应同时测 incremental learning、long-range understanding 与 selective forgetting。
  主代表引用：`MemoryAgentBench: Evaluating Memory in LLM Agents via Incremental Multi-Turn Interactions`
  证据类型：`主证据`
  边界说明：支撑四类核心能力的评测拆分，不支撑某一 memory architecture 已全面领先。

## 评测对象的四个层次

### 1. 评测检索命中

这类基准主要关心：系统能否从长历史中找出相关片段。LoCoMo、部分 LongMemEval 子任务，以及许多厂商对比，本质都偏向这一层。它们有价值，但只能证明“retrieval 可能有效”，不能证明 memory management 已经成熟。

### 2. 评测 memory-in-use

这类评测关心的不是命中，而是 agent 是否真的据记忆改写行为。例如跨会话完成任务、在长期工具使用中保持一致、根据历史 preference 做稳定决策。这类评测更接近真实 agent memory，但设计难度也更高。

### 3. 评测长期管理能力

这是最被忽视的一层。一个系统是否能处理：

- 冲突事实更新。
- 时间敏感问题。
- 多用户隔离。
- belief 修正。
- 删除与审计。

大多数公开 benchmark 对这些问题覆盖不足，因此大量“高分系统”在真实部署时仍会翻车。

### 4. 评测治理与成本

生产环境里 memory 不只是准确率问题，还包括：

- 写入和查询延迟。
- token 开销。
- 索引成本。
- 冷热数据管理。
- 权限边界。
- 删除权与审计成本。

这部分往往不在学术 benchmark 中体现，但却直接决定系统能否落地。

## 现有基准分别测到了什么

### LoCoMo

LoCoMo 的价值在于控制较好、对话历史长、问题类型清晰，因此很适合比较第一代 memory system 的 retrieval 与时间建模能力。Mem0 等系统在这里展示出的优势，至少说明抽取式记忆比 naïve full-context 更有效率。

但它的局限也明显：

- 对 memory update / deletion 的覆盖不足。
- 对复杂 agent 行为链条覆盖有限。
- 更像问答式回忆，而非长期行动中的 memory use。

### LongMemEval

LongMemEval 更长、更难，也更贴近“超长会话/跨会话记忆”压力测试，因此受到 Hindsight、Zep、Cortex 等系统偏爱。它更能暴露多 session、时间复杂度和长期推理问题。

但它依然主要回答“从长历史中回答问题”，而不是完整回答“这个 agent 的记忆层是否健壮”。尤其在治理、权限与记忆污染方面，覆盖仍然有限。

### MemoryAgentBench

MemoryAgentBench 的贡献，是把 memory benchmark 从“长文档 recall”推进到 incremental multi-turn interactions，并显式拆出 accurate retrieval、test-time learning、long-range understanding、selective forgetting 四类能力。这让它不再只是 LoCoMo 的更长版本，而是更接近 memory policy 本身的评测。

它的边界在于：虽然已经把 selective forgetting 纳入，但评测对象仍主要是受控交互，而不是完整 agent-environment loop。

### MemoryArena

MemoryArena 代表另一种更强的评测对象：不再把“记住”和“行动”拆开，而是在 interdependent multi-session agentic tasks 中联合评估。它支撑本章的关键判断，即 memory benchmark 需要覆盖 multi-session agent-environment loop，而不只是长对话问答。

它的局限是 benchmark 设计更复杂、变量更多，因此更适合作为 memory-in-use 主证据，而不是最易标准化的 baseline。

### AMA-Bench

AMA-Bench 进一步把评测对象推进到 `agent trajectory + tool use`，强调真实 agentic applications 中机器生成轨迹的长程记忆。它说明很多 memory system 在对话类 benchmark 上表现尚可，但一进入长时程任务轨迹就会暴露 causality 和 objective signal 缺失的问题。

### 系统内 benchmark / 厂商 benchmark

Letta、部分产品博客和工程报告会给出自定义 leaderboard。这类评测的好处是能把自己的系统假设固定下来，减少实验噪音；坏处是容易出现 benchmark alignment，即系统被优化成擅长答那套题，而非擅长普遍意义上的长期记忆。

## 为什么 benchmark 争议会不断出现

争议并不只是市场营销造成的，它有结构性原因。

### 1. memory system 是复合对象

它同时包括 formation、retrieval、prompt assembly、tool policy、schema design 和 base model interaction。任何一环差异都可能被外部看成“memory 强弱”。

### 2. 不同系统的目标函数并不一样

Mem0 一类系统追求低延迟、低 token、高性价比个性化记忆；Hindsight 更强调 belief-aware structured memory；MSA、RLM 更关注原生长上下文或内生记忆机制。拿同一 benchmark 直排，天然会压扁设计目标差异。

### 3. 评测通常比系统更短期

真正的 memory 问题常在长时间部署后出现，例如版本漂移、知识陈旧、权限泄漏与解释责任。但 benchmark 多在有限数据和有限轮数内完成，很难暴露这些系统性问题。

## 一个更有用的评价框架

对本项目而言，更实用的评估框架应同时覆盖以下问题：

### A. 写入质量

- 是否只保留了有价值的长期信息。
- 是否保留来源、时间和主体。
- 是否能区分事实、belief 和临时状态。

### B. 更新质量

- 面对冲突新证据时是否能正确覆盖、版本化或并存。
- 是否能解释为什么当前采用这个版本。

### C. 读取质量

- 是否召回了真正与任务相关的内容。
- 是否以合适表示进入上下文。
- agent 是否真的利用这些记忆改变行为。

### D. 系统质量

- 延迟、token 成本、索引成本是否可接受。
- 是否支持权限边界、删除与审计。
- 是否能在多用户、多 session、多 agent 情况下保持隔离与一致性。

## 评测什么，是这章最重要的问题

这也是本章最重要的一句：在 Agent Memory 里，先问“评测什么”，再看“谁分数更高”。如果一个 benchmark 只测长对话 recall，它给不出对 belief management 或 governance 的结论；如果一个系统只公布某一套自定义基准成绩，也不能直接推断它是更成熟的 memory layer。

因此，本综述不会把 retrieval 分数当作 memory 全貌，而是把它当作一个必要但远远不充分的信号。

## 代表工作定位

- `LoCoMo`：代表对长对话 recall 与时间问题的标准化测试。
- `LongMemEval`：代表更长跨度、多 session 的压力测试。
- `MemoryAgentBench`：代表把评测维度扩展到 test-time learning、long-range understanding 与 selective forgetting。
- `MemoryArena`：代表 multi-session memory-agent-environment loop 的评测对象升级。
- `AMA-Bench`：代表 memory benchmark 从对话历史问答走向 `agent trajectory + tool use`。

## 当前 benchmark 未覆盖的评测维度

> 本节基于 RQ-001 实验 E-20260326-lifecycle-eval 的评测覆盖矩阵分析，evidence_refs 见 `docs/plans/2026-03-26-memory-lifecycle-eval-evaluation-report.md`。

将上述 5 个主流 benchmark 按生命周期三阶段（formation / evolution / retrieval）交叉比对，覆盖情况如下：

| Benchmark | Formation 质量 | Evolution 正确性 | Retrieval 忠实度 |
|---|---|---|---|
| LoCoMo | 不覆盖 | 不覆盖 | 覆盖 |
| LongMemEval | 不覆盖 | 不覆盖 | 覆盖 |
| MemoryAgentBench | 部分覆盖 | 部分覆盖 | 覆盖 |
| MemoryArena | 不覆盖 | 部分覆盖 | 覆盖 |
| AMA-Bench | 不覆盖 | 不覆盖 | 覆盖 |

其中，MemoryAgentBench（arXiv:2507.05257）通过 selective forgetting 维度最接近 evolution 正确性评测，但仍依赖最终 retrieval 结果间接判断，未直接测量 evolution 中间状态（如更新前后记忆库的差异对比）。

这一覆盖空白意味着：现有 benchmark 能检测「agent 是否能从历史中找到正确答案」，但无法单独归因「写入选择是否正确」（formation 质量）或「冲突更新是否准确」（evolution 正确性）。当系统在 demo 和基准上表现良好但在长期部署中出现记忆污染和冲突事实时，现有评测缺乏定位根因的能力。

**证据边界**：上表中各 benchmark 的覆盖判断来自其论文评测协议描述。「无法单独归因写入错误 vs 检索错误」这一判断属于综合推断，基于 5 个 benchmark 评测协议的交叉对比，而非某一论文的直接声明。

## 本章主要证据来源

- `paper`：LoCoMo、LongMemEval、MemoryAgentBench、MemoryArena、AMA-Bench 及相关系统论文中的评测部分。
- `blog`：Letta、Mem0、benchmark 比较文章，仅作工程补充。
- `综合推断`：评测对象必须拆层看，是基于 benchmark 覆盖面与部署问题错位得出的判断。评测覆盖矩阵中的归因分析同样属于综合推断。
