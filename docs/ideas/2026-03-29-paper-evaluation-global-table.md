# 全量论文评估四档总表

> 生成时间：2026-03-29 | 覆盖论文数：39 篇

本文件是所有评估批次的最终汇总，按落点章节 + 档位整理。

档位定义：
- **主证据**：直接支撑某章节的核心判断，建议纳入正文引用
- **补充证据**：支撑某章节的次要判断，可作为旁证或扩充
- **context material**：仅作背景/结构参考，不进正文主线
- **暂缓**：目前不建议纳入，待后续需要时回收

---

## 01-framework

| 档位 | 论文 | arXiv | 核心价值 |
|---|---|---|---|
| 主证据 | Evaluating Very Long-Term Conversational Memory of LLM Agents | 2501.13956（LoCoMo） | 跨 session 长期记忆评测基线，框架必引 |
| 主证据 | LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory | — | 长期交互记忆 benchmark，与 LoCoMo 并列 |

---

## 02-formation

| 档位 | 论文 | arXiv | 核心价值 |
|---|---|---|---|
| 主证据 | A-MEM: Agentic Memory for LLM Agents | 2502.12110 | Zettelkasten 式结构化写入 + 写入触发演化，v11 高可信 |
| 主证据 | MemSkill: Learning and Evolving Memory Skills for Self-Evolving Agents | 2602.02474 | learnable memory skills，controller+executor+designer 闭环 |
| 主证据 | MemAgent: Reshaping Long-Context LLM with Multi-Conv RL-based Memory Agent | 2507.02259 | RL-based memory policy，formation/evolution 全链路 |
| 主证据 | TeleMem: Building Long-Term and Multimodal Memory for Agentic AI | 2601.06037 | 结构化写入 + multimodal observe-think-act 闭环 |
| 主证据 | MemOCR: Layout-Aware Visual Memory for Efficient Long-Horizon Reasoning | 2601.21468 | layout-aware visual memory，budget-aware RL 压缩 |
| 补充证据 | R^3Mem: Bridging Memory Retention and Retrieval via Reversible Compression | 2502.15957 | retention/retrieval 双目标，hierarchical compression |

---

## 03-evolution

| 档位 | 论文 | arXiv | 核心价值 |
|---|---|---|---|
| 主证据 | Agentic Memory (AgeMem): Learning Unified LTM and STM Management | 2601.01885 | 三阶段 RL 统一 LTM/STM 管理，policy-level evolution |
| 主证据 | MemSkill | 2602.02474 | memory skills 可进化，闭环设计 |
| 主证据 | A-MEM | 2502.12110 | 写入触发已有记忆演化 |
| 补充证据 | AgentOrchestra（TEA Protocol） | 2506.12508 | version selection / rollback / closed feedback loop |
| 补充证据 | Experience-Driven Multi-Agent Earth Observers（GeoEvolver） | 2602.02559 | evolving memory bank，无参数更新自演化 |

---

## 04-retrieval

| 档位 | 论文 | arXiv | 核心价值 |
|---|---|---|---|
| 主证据 | Zep / Graphiti | 2501.13956 | 时间 KG，DMR 94.8%，LongMemEval +18.5% accuracy -90% latency |
| 主证据 | SYNAPSE | 2601.02744 | 动态图 + spreading activation + lateral inhibition + temporal decay |
| 主证据 | R^3Mem | 2502.15957 | reversible compression 统一 retention/retrieval |
| 主证据 | MSA: Memory Sparse Attention | — | latent sparse retrieval，端到端可训练，100M token 规模 |
| 补充证据 | Titans: Learning to Memorize at Test Time | 2501.00663 | test-time memorization，attention as short-term memory |
| 补充证据 | BMAM | 2601.20465 | 多信号融合检索，时间线式 episodic memory |
| 补充证据 | MAGMA | 2601.03236 | multi-graph 图记忆，节点分层 |
| 补充证据 | MIRIX | 2507.07957 | 多 agent 记忆系统，分布式检索 |

---

## 05-evaluation

| 档位 | 论文 | arXiv | 核心价值 |
|---|---|---|---|
| 主证据 | MemoryAgentBench | 2507.05257 | 多轮增量交互评测，覆盖 episodic/working |
| 主证据 | MemoryArena | 2602.16313 | 跨 session 相互依赖任务评测 |
| 主证据 | AMA-Bench | 2602.22769 | long-horizon agentic memory 评测 |
| 补充证据 | LongMemEval | — | 长期交互 chat 评测，时间推理任务 |
| 补充证据 | LoCoMo | — | 跨 session 对话记忆评测基线 |

---

## 06-systems-and-engineering

| 档位 | 论文 | arXiv | 核心价值 |
|---|---|---|---|
| 主证据 | Agentic Memory (AgeMem) | 2601.01885 | tool-based memory actions，policy-level control，端到端优化 |
| 主证据 | EverMemOS | 2601.02163 | Memory OS 范式，formation+evolution+retrieval 全链路 |
| 补充证据 | BMAM | 2601.20465 | 分层 memory subsystem，多组件协同 |
| 补充证据 | AgentOrchestra（TEA） | 2506.12508 | lifecycle/version management，traceability，rollback |
| 补充证据 | MAGMA | 2601.03236 | multi-graph 系统设计 |
| 补充证据 | MIRIX | 2507.07957 | 多 agent 记忆系统工程 |
| context | Graph-based Agent Memory: Taxonomy, Techniques, and Applications | 2602.05665 | 图记忆谱系整理，术语对齐用 |

---

## 07-frontiers

| 档位 | 论文 | arXiv | 核心价值 |
|---|---|---|---|
| 主证据 | TeleMem | 2601.06037 | 多模态长期记忆，narrative+structured 写入，闭环 |
| 主证据 | MemOCR | 2601.21468 | layout-aware visual memory，预算约束下 |
| 主证据 | See and Remember | 2603.02626 | multimodal web traversal，explicit memory stack，backtracking |
| 主证据 | M3-Agent（Seeing, Listening, Remembering） | 2508.09736 | 视听 long-term memory，entity-centric 多模态，M3-Bench |
| 主证据 | MEM: Multi-Scale Embodied Memory | 2603.03596 | 短时视频 + 长时文本分层，机器人多阶段任务 |
| 主证据 | RenderMem | 2603.14669 | rendering 作为空间 memory 检索接口，viewpoint-dependent |
| 主证据 | Vision to Geometry / 3DSPMR | 2512.02458 | FoV 几何先验，sequential embodied reasoning |
| 补充证据 | Think3D | 2601.13029 | active spatial exploration，3D chain-of-thought，RL spatial tool |
| 补充证据 | GSMem | 2603.19137 | 3DGS persistent spatial memory，zero-shot embodied exploration |
| 补充证据 | Experience-Driven Earth Observers | 2602.02559 | multi-agent，多模态 long-horizon，experience memory bank |
| 补充证据 | MemVerse | 2512.03627 | multimodal lifelong learning agents |

---

## 暂缓 / context only

| 档位 | 论文 | 原因 |
|---|---|---|
| 暂缓 | Rethinking Memory Mechanisms of Foundation Agents in the Second Half | 再综述，无独立实证结论 |
| 暂缓 | Memory in the Age of AI Agents（2512.13564） | 大型综述（47作者），仅作背景参考 |
| context | Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers | 结构参考，不进主线 |
| context | Memory as Ontology / 1. Introduction（2603.04740） | governance-first 极端案例，主线不同 |
| context | Graph-based Agent Memory: Taxonomy（2602.05665） | 分类参考，不作实证主证据 |

---

## 落点汇总统计

| 章节 | 主证据数 | 补充证据数 |
|---|---|---|
| 01-framework | 2 | 0 |
| 02-formation | 5 | 1 |
| 03-evolution | 3 | 2 |
| 04-retrieval | 4 | 4 |
| 05-evaluation | 3 | 2 |
| 06-systems | 2 | 4 |
| 07-frontiers | 7 | 4 |

> 注：部分论文跨多章节，各章节单独计入。暂缓/context 共 5 篇不计入上表。
