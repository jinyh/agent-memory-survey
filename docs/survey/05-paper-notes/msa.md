# MSA: Memory Sparse Attention for Efficient End-to-End Memory Model Scaling to 100M Tokens

> Evermind, Shanda Group, Peking University | 2025

## 核心贡献

1. **MSA 架构**: 端到端可训练的稀疏注意力，支持 100M token 记忆，<9% 性能退化
2. **Document-wise RoPE**: 解耦文档间位置编码，实现 train-on-short, infer-on-long
3. **Memory Interleave**: 迭代式多跳推理机制
4. **Memory Parallel**: 分层存储 + 分布式推理，2×A800 GPU 即可处理 100M tokens

## 架构详解

### Sparse Attention Mechanism
- **Router K Projector**: 为每个文档生成路由键 K^R
- **Chunk-wise Mean Pooling**: 压缩 K, V, K^R 为紧凑表示
- **Top-k 选择**: 基于路由键相似度选择最相关的 k 个文档
- **稀疏生成**: 仅对选中文档的 KV 做注意力

### 位置编码策略
- **Document-wise RoPE** (记忆文档): 每个文档独立从 0 开始编码位置
  - 解耦文档数量与位置语义
  - 训练时少量文档 → 推理时海量文档
- **Global RoPE** (查询/生成): 查询 token 使用全局位置编码
  - position = k (retrieved docs count) 开始，保持因果依赖

### 训练
- **持续预训练**: 158.95B token，Generative Retrieval 目标
- **辅助损失 L_aux**: 对比学习，引导路由器区分正负文档
- **两阶段优化**: 先侧重路由器训练 → 再侧重生成训练
- **课程学习**: 8k context → 64k context

### 推理三阶段
1. **Global Memory Encoding (离线)**: 预计算所有文档的 K, V, K^R
2. **Routing and Context Assembly (在线)**: 路由匹配 + 加载选中文档 KV
3. **Sparse Generation (在线)**: 基于稀疏上下文自回归生成

### Memory Parallel
- **GPU 常驻**: 路由键 K^R (~56GB for 100M tokens)
- **CPU 存储**: 内容 KV (K̄, V̄)，按需异步加载到 GPU
- **分布式评分**: 多 GPU 并行计算路由相似度

### Memory Interleave
- 对多跳问题：迭代执行 路由→检索→生成文档ID → 追加到上下文 → 继续
- 模型自适应决定每轮检索的文档数量
- 直到模型判断证据充分，转为生成最终答案

## 实验结果

### QA 任务 (9 个基准)
- 平均比 same-backbone RAG 提升 16.0%
- 比 RAG+Reranking 提升 11.5%
- 比 HippoRAG2 提升 14.8%

### NIAH (RULER 基准, 32K-1M)
- 16K→100M tokens 保持 <9% 退化
- 超越 Qwen3-Next-80B, MemAgent-14B 等

## 三大范式中的定位

MSA 属于**隐状态记忆**范式，但首次突破该范式的传统限制：
- ✅ 终生记忆（100M tokens）
- ✅ 高精度
- ✅ 与主流 LLM 兼容（基于 Qwen3-4B-Instruct）
- ✅ 端到端可训练
- ✅ 近线性复杂度 O(L̄)
- ✅ 易于记忆管理

## 对 Agent Memory 的启发

1. **检索-生成一体化**: 不再需要独立的检索管道，注意力机制本身完成检索
2. **可扩展的终生记忆**: 证明模型原生的记忆可以扩展到人类认知量级
3. **分层存储思想**: 热数据（路由键）常驻 GPU，冷数据（内容 KV）在 CPU，按需加载
4. **自适应检索量**: 模型自主决定需要多少上下文，而非预设固定的 top-k
