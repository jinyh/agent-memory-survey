# Evaluation：Agent Memory 如何被评价

> v2.0 | 2026-03-25

## 现状

评测已经成为 Agent Memory 研究里的独立问题。核心争议不在“谁分数更高”，而在“到底在测 retrieval 还是在测 agentic memory”。

## 当前几类评测

### 1. 长对话 QA 基准

- LoCoMo
- LongMemEval

这类基准擅长测召回和长程问答，但不能完整覆盖记忆管理策略。

### 2. 系统内 benchmark

- Letta leaderboard 一类做法更接近“固定框架下比较模型”
- 价值在于减少工具与系统差异带来的噪音

### 3. 任务型评测

- 长时工具使用
- 编程 bench
- 具身探索与空间推理

这类评测更接近真正的 memory-in-use。

## 本项目的评价立场

- 不把 retrieval 分数当作 memory 全貌
- 需要同时看：写入质量、更新策略、冲突处理、时间敏感性、可解释性
- 多模态和具身 agent 的 memory 评测会越来越重要
