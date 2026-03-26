# RQ-001 Evidence Map：Agent Memory 全生命周期评测

> status: active | owner: Evidence Analyst | 2026-03-26
> question_id: RQ-001

## 说明

本 evidence-map 回答 RQ-001 的核心问题：现有证据能在多大程度上支撑「formation → evolution → retrieval 全生命周期评测框架」的设计？每条证据标注类型、覆盖阶段、支撑内容和边界限制。

---

## 一、评测覆盖矩阵

| 工作 | Formation 质量 | Evolution 正确性 | Retrieval 忠实度 | 评测类型 | 证据强度 |
|---|---|---|---|---|---|
| MemoryAgentBench (arXiv:2507.05257) | 部分 | 部分（selective forgetting） | 是 | benchmark | 高 |
| MemoryArena | 否 | 部分（multi-session drift） | 是 | benchmark | 中 |
| AMA-Bench | 否 | 否 | 是（agent trajectory） | benchmark | 中 |
| LongMemEval | 否 | 否 | 是（长对话 QA） | benchmark | 高 |
| LoCoMo | 否 | 否 | 是（对话检索） | benchmark | 高 |
| Hindsight | 部分（因果归因） | 中（retrospective） | 是 | 系统+评测 | 高 |
| MemAgent (arXiv:2507.02259) | 是（RL 写入选择） | 是（RL 更新策略） | 是 | 系统 | 高 |
| Synapse | 否 | 是（压缩+巩固） | 是 | 系统 | 中 |
| MemSkill | 否 | 是（operation 可学习） | 部分 | 系统 | 中 |
| Mem0 | 部分（规则触发） | 部分（冲突去重） | 是 | 工程 | 低（主判断不用） |
| AgentOrchestra (arXiv:2506.12508) | 否 | 是（TEA 协议演化） | 是 | 系统 | 高 |

---

## 二、按阶段的证据清单

### 2.1 Formation 质量

**核心问题**：什么信息应该写入记忆？写入质量如何衡量？

#### 主证据

- **MemAgent（arXiv:2507.02259）**
  - 证据类型：论文证据
  - 支撑内容：RL-based 写入选择策略，证明 formation 决策可学习、可优化，而非只能靠规则
  - 边界：实验场景是 long-context QA，不直接等价于多轮对话场景的 formation 评测
  - 推荐用途：formation 可学习化的主证据

- **Hindsight**
  - 证据类型：论文证据
  - 支撑内容：提出 retrospective annotation，允许事后归因哪些信息本该被写入但被遗漏
  - 边界：以评测框架为主，不提供 formation 质量的独立指标体系
  - 推荐用途：formation 质量因果分析的参照框架

#### 次级证据（工程补充）

- **Mem0**：规则触发写入（用户意图检测 + 信息抽取），是工程基线但无独立 formation 质量实验
- **LangMem**：结构化记忆抽取，工程实践补充
- **Elastic memory architecture**：分层写入设计，system/session/event 层级，工程判断

#### 证据缺口

- 无独立的 formation 质量 benchmark（写入准确率、冗余率、结构一致性均无标准化测集）
- 现有系统的 formation 评测均为端到端，无法单独归因写入错误 vs 检索错误

---

### 2.2 Evolution 正确性

**核心问题**：记忆如何更新、冲突如何解决、遗忘边界如何控制？

#### 主证据

- **MemAgent（arXiv:2507.02259）**
  - 证据类型：论文证据
  - 支撑内容：RL 策略同时覆盖写入与更新，证明 evolution 可以作为可优化目标
  - 边界：RL 训练成本高，实验复现难度中等

- **MemoryAgentBench（arXiv:2507.05257）**
  - 证据类型：论文证据
  - 支撑内容：将 selective forgetting 作为独立测试维度，是已知最接近 evolution 正确性评测的 benchmark
  - 边界：selective forgetting 的测试仍依赖最终 retrieval 结果，未直接测 evolution 中间状态

- **Synapse**
  - 证据类型：论文证据
  - 支撑内容：episodic 压缩与巩固机制，提供 evolution 中「保留什么 / 压缩什么」的实验依据
  - 边界：只覆盖压缩场景，不处理冲突事实和主动遗忘

- **AgentOrchestra（arXiv:2506.12508）**
  - 证据类型：论文证据
  - 支撑内容：TEA 协议（Task-Experience-Archive）提供 evolution 的三级状态转移框架，有多 agent 协作实验
  - 边界：多 agent 场景，与单 agent 长期记忆的 evolution 不完全可类比

#### 次级证据（工程补充）

- **MemSkill**：memory operation 可学习化（CRUD-like），工程视角补充 evolution 的操作粒度
- **MSA（Memory Sparse Attention）**：latent memory 演化的注意力机制视角，属于模型层而非外挂记忆层

#### 证据缺口

- 冲突事实解决（两条矛盾记忆如何选择保留哪条）几乎无论文级实验，现有系统均为启发式规则
- 遗忘边界（何时删除记忆、删除后是否可恢复）无公开 benchmark，是最大证据盲区
- evolution 的中间状态（更新前 vs 更新后的记忆库对比）无标准化评测协议

---

### 2.3 Retrieval 忠实度

**核心问题**：agent 能否在正确时机取回正确记忆？

#### 主证据（已有较强基线，此处只做边界标注）

- **LongMemEval**：长对话 QA，覆盖最广，是 retrieval 忠实度的主基线
- **LoCoMo**：对话检索，强调时间顺序和跨会话一致性
- **Letta / MemGPT**：工具化 retrieval（agent 主动调用 memory tools），提供 routing 视角
- **RLM（Recursive Language Models）**：latent memory retrieval，模型层而非外挂检索

#### 补充

- **Mem0**、**Zep / Graphiti**：工程基线，vector + graph hybrid retrieval 的主流实现

#### 边界说明

- retrieval 是三个阶段中证据最充分的，但现有 benchmark 几乎都以端到端 QA 准确率为代理指标
- 「记忆被检索到但被 agent 错误使用」与「记忆未被检索到」在现有评测中无法区分

---

## 三、证据层级汇总

| 阶段 | 主证据数量 | 独立 benchmark | 证据强度综合 | 最大缺口 |
|---|---|---|---|---|
| Formation 质量 | 2（MemAgent、Hindsight） | 无 | 弱 | 无标准化写入质量测集 |
| Evolution 正确性 | 4（MemAgent、MemoryAgentBench、Synapse、AgentOrchestra） | 部分（MemoryAgentBench） | 中 | 冲突解决与遗忘边界无实验 |
| Retrieval 忠实度 | 5+（LongMemEval、LoCoMo 等） | 多个 | 强 | 端到端代理指标掩盖中间错误 |

---

## 四、代表引用与证据边界声明

**论文证据（可直接支撑方法判断）：**
- MemAgent（arXiv:2507.02259）：formation + evolution 可学习化
- MemoryAgentBench（arXiv:2507.05257）：最接近全生命周期评测的 benchmark
- Hindsight：formation 质量的因果归因框架
- Synapse：evolution 压缩与巩固机制
- AgentOrchestra（arXiv:2506.12508）：evolution 状态转移的多 agent 实验

**工程判断（不作主证据，只作工程补充）：**
- Mem0、LangMem、Zep：formation/retrieval 工程基线
- MemSkill：evolution 操作粒度的工程视角

**综合推断（本 evidence-map 的判断，需明确标注）：**
- 三阶段联合评测目前尚无公开工作，这一判断基于对现有 benchmark 覆盖范围的交叉对比，而非单一论文声明
- formation 和 evolution 的证据弱于 retrieval，这一判断基于论文数量、实验覆盖和 benchmark 成熟度的综合评估
