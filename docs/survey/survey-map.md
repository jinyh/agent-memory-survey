# Agent Memory Survey 证据地图

> v3.2 | 2026-03-27 — 收紧 benchmark 覆盖映射，明确 formation/evolution 空白

这份地图不是正文替代品，而是正文的索引层。它回答两个问题：

1. 某个系统或论文主要对应 lifecycle 的哪个阶段。
2. 每章的核心判断主要由哪些代表工作支撑。

## 按问题映射

| 问题 | 重点章节 | 代表工作 |
| --- | --- | --- |
| 为什么 memory 不能约化为 RAG | `01-framework` `04-retrieval` `05-evaluation` | Mem0, Hindsight, Letta/MemGPT, RLM, MSA |
| reasoning thinking 与 agentic thinking 的迁移对 memory 意味着什么 | `01-framework` | From "Reasoning" Thinking to "Agentic" Thinking (blog) |
| skill 作为 procedural memory 的定位 | `01-framework` `03-evolution` | MemSkill |
| 什么信息应进入长期记忆 | `02-formation` | Mem0, LangMem, MemAgent, Elastic |
| 记忆如何更新、压缩与遗忘 | `03-evolution` | Hindsight, Synapse, MSA, AgentOrchestra |
| 如何从长期历史中真正用上记忆 | `04-retrieval` | Mem0, Zep, Letta/MemGPT, RLM, MSA |
| 当前 benchmark 到底在测什么 | `05-evaluation` | LoCoMo, LongMemEval, MemoryAgentBench, MemoryArena, AMA-Bench |
| benchmark 未覆盖的 formation/evolution 评测 | `05-evaluation` | 5 个主流 benchmark 主要覆盖 retrieval；其中仅 MemoryAgentBench 通过 selective forgetting 部分触及 evolution，其余 4 个不覆盖 |
| 生产系统如何做分层和治理 | `06-systems-and-engineering` | Mem0, Zep, Letta/MemGPT, Hindsight, Elastic |
| 多模态、空间与安全的 frontier 在哪 | `07-frontiers` | TeleMem, M3-Agent, MemVerse, MemOCR, Think3D, GSMem, RenderMem |

## 按系统映射

| 系统/工作 | Formation | Evolution | Retrieval | Evaluation | Systems | Frontier |
| --- | --- | --- | --- | --- | --- | --- |
| Mem0 | 高 | 中 | 高 | 高 | 高 | 低 |
| LangMem | 高 | 中 | 中 | 中 | 高 | 低 |
| Zep / Graphiti | 中 | 中 | 高 | 中 | 高 | 低 |
| Letta / MemGPT | 中 | 中 | 高 | 中 | 高 | 低 |
| Hindsight | 中 | 高 | 高 | 高 | 高 | 中 |
| MemAgent | 高 | 高 | 高 | 中 | 中 | 低 |
| RLM | 中 | 低 | 高 | 中 | 中 | 低 |
| MSA | 低 | 高 | 高 | 中 | 中 | 中 |
| TeleMem | 中 | 中 | 高 | 低 | 高 | 高 |
| Synapse | 中 | 高 | 高 | 中 | 中 | 中 |
| Elastic memory architecture | 高 | 中 | 高 | 中 | 高 | 低 |
| Think3D / GSMem / RenderMem | 低 | 中 | 高 | 低 | 中 | 高 |
| MemoryAgentBench | 低 | 低 | 低 | 高 | 低 | 中 |
| MemoryArena | 低 | 低 | 中 | 高 | 低 | 中 |
| AMA-Bench | 低 | 低 | 中 | 高 | 低 | 中 |

说明：

- `高/中/低` 表示该工作对该章节问题的相关度，不代表质量排名。
- 某些工作在单一阶段特别强，但不意味着它已经覆盖完整 memory lifecycle。

## 章节主证据清单

### 01-framework

- Mem0
- Hindsight
- Recursive Language Models
- MemSkill
- Memory in the Age of AI Agents: A Survey
- From "Reasoning" Thinking to "Agentic" Thinking (blog)

### 02-formation

- Mem0
- LangMem
- MemAgent
- Elastic memory architecture
- TeleMem / MemOCR / M3-Agent

### 03-evolution

- Hindsight
- Synapse
- MSA
- AgentOrchestra
- 多模态与系统治理类工程材料

### 04-retrieval

- Mem0 / LangMem
- Zep / Graphiti
- Letta / MemGPT
- RLM
- MSA

### 05-evaluation

- LoCoMo
- LongMemEval
- MemoryAgentBench
- MemoryArena
- AMA-Bench
- Hindsight / Cortex / Letta 的评测叙事（工程补充）

### 06-systems-and-engineering

- Mem0
- Zep / Graphiti
- Letta / MemGPT
- Hindsight
- Elastic memory architecture

### 07-frontiers

- TeleMem
- M3-Agent
- MemVerse
- MemOCR
- Think3D
- GSMem
- RenderMem
