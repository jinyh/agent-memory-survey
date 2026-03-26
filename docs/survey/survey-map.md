# Agent Memory Survey 证据地图

> v3.0 | 2026-03-26

这份地图不是正文替代品，而是正文的索引层。它回答两个问题：

1. 某个系统或论文主要对应 lifecycle 的哪个阶段。
2. 每章的核心判断主要由哪些代表工作支撑。

## 按问题映射

| 问题 | 重点章节 | 代表工作 |
| --- | --- | --- |
| 为什么 memory 不能约化为 RAG | `01-framework` `04-retrieval` `05-evaluation` | Mem0, Hindsight, Letta/MemGPT, RLM, MSA |
| 什么信息应进入长期记忆 | `02-formation` | Mem0, LangMem, MemAgent, Elastic |
| 记忆如何更新、压缩与遗忘 | `03-evolution` | Hindsight, Synapse, MSA, AgentOrchestra |
| 如何从长期历史中真正用上记忆 | `04-retrieval` | Mem0, Zep, Letta/MemGPT, RLM, MSA |
| 当前 benchmark 到底在测什么 | `05-evaluation` | LoCoMo, LongMemEval, Letta benchmark, Cortex/Hindsight 叙事 |
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

说明：

- `高/中/低` 表示该工作对该章节问题的相关度，不代表质量排名。
- 某些工作在单一阶段特别强，但不意味着它已经覆盖完整 memory lifecycle。

## 章节主证据清单

### 01-framework

- Mem0
- Hindsight
- Letta / MemGPT
- RLM
- MSA
- TeleMem

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
- Mem0 benchmark 叙事
- Hindsight / Cortex / Letta 的评测叙事

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
