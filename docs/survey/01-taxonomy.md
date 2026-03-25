# Agent Memory 分类体系与范式对比

> v1.0 | 2026-03-24

## 1. 概述

Agent Memory 是 LLM Agent 系统中负责信息持久化、检索和演化的核心组件。不同于传统数据库，Agent Memory 需要在语义理解、时序感知和推理支持之间取得平衡。

本文档从**记忆类型**和**实现范式**两个维度对 Agent Memory 进行系统分类。

---

## 2. 记忆类型分类

借鉴认知科学中的人类记忆理论（Tulving, 1972; Squire, 2004），LLM Agent 的记忆可分为以下类型：

### 2.1 工作记忆 (Working Memory)

- **定义**: LLM 上下文窗口内的即时信息，类似人类的短时注意力缓冲区
- **特征**: 容量有限（受上下文窗口约束）、即时可用、读写速度最快
- **实现**: 直接利用 Transformer 的 KV cache
- **代表工作**:
  - **RLM** (Zhang et al., 2026): 通过 REPL 环境将长 prompt 符号化，突破单次上下文限制
  - **MSA** (Chen et al., 2025): 稀疏注意力机制，在 100M token 规模保持工作记忆精度
  - **MemGPT/Letta** (Packer et al., 2023): 虚拟上下文管理，Agent 自主管理"主上下文"

### 2.2 情景记忆 (Episodic Memory)

- **定义**: 记录具体事件、交互和经历的时序记忆，保留"何时、何地、发生了什么"
- **特征**: 时间戳索引、单次学习（one-shot）、上下文敏感
- **功能**: 支持从过去经验中学习、避免重复错误、提供决策参考
- **代表工作**:
  - **"Episodic Memory is the Missing Piece"** (arXiv:2502.06975, 2025): 提出情景记忆的五个关键属性，论证其对长期 Agent 不可或缺
  - **AriGraph** (IJCAI'25): 情景记忆 + 知识图谱结合，在文本游戏中显著提升表现
  - **MemRL** (2026): 基于运行时 RL 的情景记忆自进化

### 2.3 语义记忆 (Semantic Memory)

- **定义**: 抽象的世界知识、事实和概念，脱离具体时间和场景
- **特征**: 高度结构化、可共享、稳定持久
- **功能**: 提供通用知识库、支持推理和泛化
- **代表工作**:
  - **Zep/Graphiti**: 时序知识图谱维护事实及其有效时间段
  - **RAG 系统**: 通过向量数据库存储和检索知识块
  - **Knowledge Graph 增强**: LightRAG, HippoRAG2 等

### 2.4 程序性记忆 (Procedural Memory)

- **定义**: 执行任务的步骤、技能和操作模式，类似"肌肉记忆"
- **特征**: 可能隐含在 LLM 权重中，也可显式存储为指令/SOP
- **功能**: 加速重复任务、保持行为一致性
- **代表工作**:
  - **Mem^p** (arXiv:2508.06433, 2025): 系统探索 Agent 程序性记忆
  - **"Remember Me, Refine Me"** (2025): 动态程序性记忆框架，支持经验驱动的 Agent 进化

### 2.5 类型间的关系与转化

```
情景记忆 ──巩固──→ 语义记忆
  │                    │
  │                    │
  ↓                    ↓
程序性记忆 ←──抽象──── 语义记忆
  │
  ↓
工作记忆 ←── 按需检索 ── 所有长期记忆类型
```

关键路径:
- **情景→语义巩固**: 多次相似经历抽象为通用知识（类似人类睡眠时的记忆整合）
- **语义→程序性抽象**: 知识转化为可执行的操作模式
- **长期→工作记忆检索**: 根据当前任务按需加载相关记忆到上下文

---

## 3. 实现范式

### 3.1 参数记忆 (Parameter-Based Memory)

将知识直接编码到模型权重中。

| 方法 | 机制 | 优势 | 劣势 |
|------|------|------|------|
| LoRA/CPT | 微调/持续预训练 | 高精度、深度整合 | 灾难性遗忘、训练开销 |
| Titans | Test-time training | 推理时动态更新 | 精度中等 |
| FLEXOLMO | 混合专家框架 | 模块化知识整合 | 复杂度高 |
| Engram | N-gram 稀疏嵌入 | 大规模记忆结构 | 与密集层的瓶颈 |
| MLP-Memory | 参数化检索器 | MLP 作为可微分记忆 | 容量有限 |

**核心挑战**: 灾难性遗忘（新知识覆盖旧知识）、容量不可动态扩展

### 3.2 外部存储记忆 (External Storage-Based Memory)

将记忆存储在模型外部的数据库/索引中。

| 方法 | 存储方式 | 检索方式 | 特点 |
|------|---------|---------|------|
| RAG | 向量数据库 | 密集向量相似度 | 通用、成熟 |
| MemAgent | 外部存储 | RL 策略驱动 | 主动管理 |
| MemoRAG | KV 压缩 + 向量 | 双系统：草稿+精确 | 非QA任务优势 |
| Memory³ | 显式记忆块 | 稀疏化检索 | 2.4B 超越大模型 |
| A-MEM | Zettelkasten 笔记 | 动态索引+链接 | 互联知识网络 |
| MemGPT/Letta | 分层上下文 | Agent 自编辑 | OS 式管理 |

**核心挑战**: 检索与生成的优化目标不对齐（retrieval-generation gap）

### 3.3 隐状态记忆 (Latent State-Based Memory)

直接在模型的内部表示空间中操作记忆。

| 方法 | 机制 | 容量 | 精度 |
|------|------|------|------|
| MSA | 稀疏注意力 + top-k 路由 | 100M tokens | 高 |
| DSA | 密集稀疏注意力 | 有限 | 高 |
| MemGen | 自回归合成压缩 | 中等 | 高 |
| RWKV/DeltaNet | 线性注意力/递推 | O(L) 压缩 | 低 |
| Memory³ KV | 预编码 KV 对 | 大 | 中 |

**核心挑战**: 容量与效率的权衡——高精度方法难以扩展，高效率方法精度下降

---

## 4. 三大范式对比

| 维度 | 参数记忆 | 外部存储记忆 | 隐状态记忆 |
|------|---------|------------|----------|
| **终生记忆** | 否 | 是 | 部分（MSA: 是）|
| **精度** | 高 | 中 | 高 |
| **与主流 LLM 兼容** | 高 | 中 | 需架构修改 |
| **计算复杂度** | 训练高/推理低 | O(L) 检索 | 亚线性~线性 |
| **记忆管理** | 困难 | 容易 | 容易 |
| **灾难性遗忘** | 是 | 否 | 部分 |
| **端到端可训练** | 是 | 否 | 部分（MSA: 是）|

**MSA 的突破**: 首次在隐状态范式中同时实现终生记忆 + 高精度 + 端到端可训练 + 近线性复杂度。

---

## 5. 新兴混合范式

当前趋势是**混合多种范式**以取长补短：

1. **MemoRAG**: 隐状态（KV 压缩全局记忆）+ 外部存储（精确检索）
2. **Memory³**: 参数记忆（模型权重）+ 显式记忆（外化知识块）+ 工作记忆（KV cache）
3. **MIRIX**: 六组件架构，整合 Core/Episodic/Semantic/Procedural/Resource/Knowledge Vault
4. **AgentOrchestra/TEA**: 系统层面统一管理，Memory Manager + Version Manager + Self-Evolution

---

## 参考文献

- Tulving, E. (1972). Episodic and Semantic Memory
- Squire, L.R. (2004). Memory systems of the brain
- "A Survey on the Memory Mechanism of LLM-based Agents" (ACM TOIS, 2025)
- "Memory in the Age of AI Agents" (arXiv:2512.13564, 2025)
- MSA (Memory Sparse Attention), Chen et al.
- RLM (Recursive Language Models), Zhang et al., 2026
- AgentOrchestra, Zhang et al., 2026
