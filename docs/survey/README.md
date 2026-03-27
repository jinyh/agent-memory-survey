# Agent Memory 深入 Survey

> v3.0 | 2026-03-26

这是一套面向研究导向工程师的分析型综述，不再满足于“有哪些系统、有哪些分类”的提纲式总结，而是试图回答三个更难的问题：

1. Agent Memory 的真正难点到底是存储、检索，还是记忆管理本身。
2. 2025-2026 年的代表工作分别把控制权交给了谁，是系统规则、外部检索器、模型注意力，还是 agent 自己。
3. 哪些结论已经有较强证据，哪些仍主要停留在工程叙事、厂商基准或尚未被充分验证的前沿尝试。

## 阅读立场

本综述采用一个明确立场：`memory != retrieval`。检索只是记忆层的一个阶段。真正决定 agent 是否“有记忆”的，是以下闭环是否成立：

`formation -> evolution -> retrieval -> evaluation`

如果一个系统只擅长把历史片段找回来，但不处理写入选择、冲突更新、时间敏感性、压缩、遗忘、可解释性与治理，它更像一个增强版上下文外挂，而不是成熟的 memory layer。

## 证据口径

- `paper` 是主证据，用来支撑方法判断、实验结论和系统能力。
- `blog` 用于补充工程实践、基准争议、系统运维和产品化取舍。
- `DeepResearch` 提供前沿线索，但不直接等价于正式证据。

因此，文中会刻意区分三类内容：

- `论文证据`：已有实验、消融、基准或方法论支持。
- `工程判断`：来自系统实现经验和产品实践。
- `综合推断`：本综述基于多源材料做出的判断，会明确说明证据边界。

## 全文结构

- [01-framework.md](./01-framework.md)：统一框架，以 reasoning→agentic 的问题迁移为背景，定义 memory layer 的边界与 lifecycle 主线。
- [02-formation.md](./02-formation.md)：记忆形成，讨论什么该写、怎么写、写成什么结构。
- [03-evolution.md](./03-evolution.md)：记忆演化，讨论更新、压缩、巩固、遗忘与治理。
- [04-retrieval.md](./04-retrieval.md)：记忆读取，比较 vector、graph、routing、latent 和记忆工具化。
- [05-evaluation.md](./05-evaluation.md)：评测问题，区分在评测什么、没有评测什么、为什么会争议不断。
- [06-systems-and-engineering.md](./06-systems-and-engineering.md)：系统谱系与工程落地。
- [07-frontiers.md](./07-frontiers.md)：多模态、空间记忆、安全与可审计性。
- [survey-map.md](./survey-map.md)：跨章节证据地图，按问题和按系统快速跳转。

## 核心判断

### 1. 生命周期框架比“工作记忆/语义记忆/情景记忆”静态分类更能解释新工作

后者依然有价值，但它更像是功能标签，而不是设计框架。新一代工作真正拉开差距的地方，不是“记忆叫 episodic 还是 semantic”，而是系统如何决定：

- 何时写入。
- 如何合并或修正旧记忆。
- 如何在不同任务尺度下读取。
- 怎样评价记忆是否真的被 agent 用到了。

### 2. 当前研究在检索端最热，在写入与演化端最欠账

从现有 paper 与系统看，`retrieval` 是论文最密集、结果最可量化的部分。相对地，`formation` 和 `evolution` 往往只给启发式规则或薄弱实验。也因此，许多系统在 demo 和基准上显得强，但在长期部署时会遇到冲突事实、记忆污染、权限隔离和删除治理问题。

### 3. 工程界正在从“向量库存记忆”转向“状态分层 + 多表示协同”

Mem0、LangMem 一类系统证明抽取式记忆很有价值，但也暴露了单一 retrieval-centric 架构的边界。之后出现的 Hindsight、图记忆、active state、latent memory 和 memory OS 思路，本质上都在争同一个问题的控制权：谁负责决定该保留什么、如何解释什么、什么时候忘记什么。

### 4. 前沿工作把 memory 从文本事实扩展到环境状态

多模态记忆、空间记忆、视频流记忆和具身探索，都说明“长期事实库”只是起点。未来 memory layer 要管理的不仅是用户说过什么，还包括 agent 看见了什么、做过什么、环境怎样变化、哪些 belief 曾经被修正。

## 使用方式

如果你只想快速抓主线，先读：

1. [01-framework.md](./01-framework.md)
2. [04-retrieval.md](./04-retrieval.md)
3. [05-evaluation.md](./05-evaluation.md)
4. [06-systems-and-engineering.md](./06-systems-and-engineering.md)

如果你要设计自己的 memory layer，建议把 `02 + 03 + 04 + 05` 连起来读，因为实际系统失败最常见的根因，恰恰出在这几个章节的接口处。

先看研究矩阵，再看关键概念与代表引用，再读正文论证。

## 按问题读

- 如果你在追问“memory 为什么不等于检索”或“memory 和 agentic thinking 到底差在哪”，从 [01-framework.md](./01-framework.md) 开始，再读 [04-retrieval.md](./04-retrieval.md) 和 [05-evaluation.md](./05-evaluation.md)。
- 如果你在设计写入策略，优先读 [02-formation.md](./02-formation.md) 和 [03-evolution.md](./03-evolution.md)。
- 如果你在做生产系统选型，优先读 [06-systems-and-engineering.md](./06-systems-and-engineering.md)、[05-evaluation.md](./05-evaluation.md) 和 [survey-map.md](./survey-map.md)。
- 如果你在关注多模态或具身 agent，优先读 [07-frontiers.md](./07-frontiers.md)，再回看 [02-formation.md](./02-formation.md) 与 [04-retrieval.md](./04-retrieval.md)。

## 按系统读

- `Mem0 / LangMem`：从 [02-formation.md](./02-formation.md)、[04-retrieval.md](./04-retrieval.md)、[06-systems-and-engineering.md](./06-systems-and-engineering.md) 切入。
- `Zep / Graphiti`：优先看 [04-retrieval.md](./04-retrieval.md)、[06-systems-and-engineering.md](./06-systems-and-engineering.md)。
- `Letta / MemGPT`：优先看 [01-framework.md](./01-framework.md)、[04-retrieval.md](./04-retrieval.md)、[06-systems-and-engineering.md](./06-systems-and-engineering.md)。
- `Hindsight`：优先看 [01-framework.md](./01-framework.md)、[03-evolution.md](./03-evolution.md)、[05-evaluation.md](./05-evaluation.md)。
- `Recursive Language Models`：优先看 [01-framework.md](./01-framework.md)、[04-retrieval.md](./04-retrieval.md)、[06-systems-and-engineering.md](./06-systems-and-engineering.md)。
- `MSA`：优先看 [04-retrieval.md](./04-retrieval.md)、[06-systems-and-engineering.md](./06-systems-and-engineering.md)。
- `TeleMem / MemVerse / M3-Agent / MemOCR`：优先看 [02-formation.md](./02-formation.md)、[07-frontiers.md](./07-frontiers.md)。

## 证据地图

如果你想先看“这章的判断是由哪些工作支撑”，直接打开 [survey-map.md](./survey-map.md)。正文负责论证，地图负责追索。

## 如何使用研究矩阵

每章开头现在都补了一个“研究矩阵”。它负责横向比较，不是摘要版目录，而是把该章争论压到同一比较口径下：

- 比较的对象到底是什么。
- 控制权交给了谁。
- 优势与局限分别落在哪个生命周期接口。
- 当前结论的证据强度处在什么水平。

## 如何使用关键概念与代表引用

每章矩阵之后的“关键概念与代表引用”负责定义概念、标注代表作品，并明确它支撑什么、不支撑什么。它的作用是把正文里的组织性判断绑定回可追溯证据，而不是用泛称或缩写替代引用。

如果你已经熟悉正文，可直接先看各章矩阵，再跳到对应的小节做深入追索。
