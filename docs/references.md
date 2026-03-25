# Agent Memory 参考文献库

> v1.0 | 2026-03-24

## 综述论文

- **"A Survey on the Memory Mechanism of Large Language Model-based Agents"**
  ACM TOIS, 2025 | [ACM](https://dl.acm.org/doi/10.1145/3748302) | [GitHub](https://github.com/nuster1128/LLM_Agent_Memory_Survey)

- **"Memory in the Age of AI Agents"**
  arXiv:2512.13564, 2025 | [arXiv](https://arxiv.org/abs/2512.13564) | [GitHub](https://github.com/Shichun-Liu/Agent-Memory-Paper-List)

- **"From Storage to Experience: A Survey on the Evolution of LLM Agent Memory Mechanisms"**
  ICLR 2026 MemAgents Workshop | [OpenReview](https://openreview.net/forum?id=l9Ly41xxPb)

- **"Memory in LLM-based Multi-agent Systems"**
  TechRxiv, 2025 | 多智能体记忆综述

---

## 已有论文 (ref/ 目录)

- **AgentOrchestra: TEA Protocol** — `ref/2506.12508v5.pdf`
  Skywork AI & NTU, 2026 | arXiv:2506.12508 | #多智能体 #协议 #记忆管理

- **Recursive Language Models (RLM)** — `ref/2512.24601v2.pdf`
  MIT CSAIL, 2026 | arXiv:2512.24601 | [GitHub](https://github.com/alexzhang13/rlm) | #工作记忆 #递归 #长上下文

- **MSA: Memory Sparse Attention** — `ref/MSA__*.pdf`
  Evermind & PKU, 2025 | #隐状态记忆 #稀疏注意力 #100M tokens

---

## Agentic Memory 系统

- **A-MEM: Agentic Memory for LLM Agents**
  NeurIPS'25 | arXiv:2502.12110 | [GitHub](https://github.com/agiresearch/A-mem) | #Zettelkasten #知识网络

- **AgeMem: Agentic Memory**
  arXiv:2601.01885, 2026 | #RL #记忆工具动作 #GRPO

- **MemGPT → Letta**
  arXiv:2310.08560 | [Letta](https://docs.letta.com) | #OS式记忆 #虚拟上下文 #自编辑

- **Memory³ (Memory Cubed)**
  JML, 2024 | arXiv:2407.01178 | #显式记忆 #三种记忆形式

- **MemoRAG**
  TheWebConf'25 | arXiv:2409.05591 | [GitHub](https://github.com/qhjqhj00/MemoRAG) | #双系统 #全局记忆

- **MemWalker**
  arXiv:2310.05029 | #记忆树 #交互式导航 #回溯

- **Memory-R1**
  2025 | #RL #双Agent #主动记忆管理

---

## 记忆检索与图结构

- **Zep/Graphiti**
  arXiv:2501.13956 | #时序知识图谱 #三种搜索

- **MAGMA: Multi-Graph Agentic Memory**
  2026.01 | #多图架构

- **LightRAG**
  #双检索器 #本地+全局

- **HippoRAG2**
  #知识图谱增强RAG

- **MemR3: Memory Retrieval via Reflective Reasoning**
  arXiv:2512.20237 | #全局证据差距

---

## 记忆类型专题

### 情景记忆
- **"Position: Episodic Memory is the Missing Piece for Long-Term LLM Agents"**
  arXiv:2502.06975, 2025 | #情景记忆 #五个属性

- **AriGraph**
  IJCAI'25 | #情景记忆 #知识图谱

- **MemRL**
  2026 | #运行时RL #情景记忆自进化

### 程序性记忆
- **Mem^p: Exploring Agent Procedural Memory**
  arXiv:2508.06433, 2025

- **"Remember Me, Refine Me"**
  2025 | #动态程序性记忆

### 多类型记忆
- **MIRIX**
  arXiv:2507.07957, 2025 | #六组件记忆架构

---

## 记忆管理与压缩

- **LightMem**
  arXiv:2510.18866, 2025 | #睡眠巩固 #离线压缩

- **SimpleMem**
  [GitHub](https://github.com/aiming-lab/SimpleMem) | #去噪压缩 #高层抽象

---

## 多智能体协作记忆

- **"Collaborative Memory: Multi-User Memory Sharing with Dynamic Access Control"**
  ICML'25 | arXiv:2505.18279

- **"Memory as a Service (MaaS)"**
  arXiv:2506.22815, 2025

- **Intrinsic Memory Agents**
  [OpenReview](https://openreview.net/forum?id=UbSUxAK3BI)

---

## 参数记忆与隐状态记忆

- **Titans**: Test-time training 记忆模块
- **FLEXOLMO**: 混合专家框架
- **Engram**: N-gram 稀疏嵌入
- **MLP-Memory**: 参数化检索器
- **RWKV**: 线性递推注意力 | arXiv (ref [33] in MSA)
- **DeltaNet**: Delta rule 记忆状态更新 | arXiv (ref [34,45] in MSA)
- **MemGen**: 自回归合成压缩 | arXiv (ref [50] in MSA)
- **DSA**: 密集稀疏注意力 | arXiv (ref [28] in MSA)
- **ParallelComp**: KV cache 驱逐策略 | arXiv (ref [40] in MSA)

---

## 认知科学启发

- **ACT-R 启发架构** — HAI'25 | [ACM](https://dl.acm.org/doi/10.1145/3765766.3765803)
- **MIRAS**: 统一递归和联想记忆抽象
- Tulving, E. (1972). Episodic and Semantic Memory
- Ebbinghaus 遗忘曲线

---

## 工程框架

| 框架 | 链接 |
|------|------|
| Letta (MemGPT) | https://docs.letta.com |
| LangChain Memory | https://python.langchain.com |
| LlamaIndex | https://docs.llamaindex.ai |
| CrewAI | https://docs.crewai.com |
| Mem0.ai | https://mem0.ai |
| Zep | https://www.getzep.com |

---

## Workshop & 社区

- **ICLR 2026 MemAgents Workshop** | [OpenReview](https://openreview.net/pdf?id=U51WxL382H)
- **Agent Memory Paper List** | [GitHub](https://github.com/Shichun-Liu/Agent-Memory-Paper-List)
- **LLM Agent Memory Survey** | [GitHub](https://github.com/nuster1128/LLM_Agent_Memory_Survey)
