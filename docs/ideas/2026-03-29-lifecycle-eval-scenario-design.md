# Agent Memory 全生命周期评测：指标定义与场景设计

> type: ideas | 2026-03-29 | 关联 RQ-001

## 一、Formation 与 Evolution 需要什么指标

### 1.1 Formation 质量指标

**核心问题**：在一段对话中，哪些信息应该被写入记忆，写入了多少，写多了什么？

| 指标 | 定义 | 计算方式 |
|---|---|---|
| `formation_precision` | 实际写入中属于应写入集合的比例 | \|actual ∩ expected\| / \|actual\| |
| `formation_recall` | 应写入集合中被实际写入的比例 | \|actual ∩ expected\| / \|expected\| |
| `formation_spurious_rate` | 实际写入中不应写入的比例 | \|actual \ expected\| / \|actual\| |

**有意义的 formation ground truth 需要满足**：
- 写入决策不能由简单规则（重要性阈值 + 字数）完全决定
- 应包含需要语义判断的正例（隐式偏好、行为推断）和负例（情绪陈述、助手回复内容）
- 同一条信息在不同上下文下的写入决策可能不同（置信度、时效性）

### 1.2 Evolution 正确性指标

**核心问题**：当新信息到来时，已有记忆是否被正确更新、替换或遗忘？

| 指标 | 定义 | 计算方式 |
|---|---|---|
| `evolution_accuracy` | 应存续的记忆中内容正确的比例 | \|correct_survived\| / \|should_survive\| |
| `forgetting_precision` | 应遗忘的记忆中实际被遗忘的比例 | \|actual_forgotten\| / \|should_forget\| |
| `conflict_resolution_accuracy` | 存在语义冲突时选择正确事实的比例 | \|correct_resolved\| / \|total_conflicts\| |
| `spurious_duplication_rate` | 同一事实被写入多次的比例 | \|duplicate_entries\| / \|total_entries\| |

**有意义的 evolution ground truth 需要满足**：
- 冲突事实之间存在语义矛盾（不是同一 key 的直接替换）
- 包含"扩展"（extend）、"替换"（replace）、"遗忘"（forget）、"新建"（new）四种冲突类型
- 覆盖中间状态：expected_state 能区分更新前后的差异

---

## 二、当前 Benchmark 为何无法提供这些指标

| Benchmark | Formation 缺口 | Evolution 缺口 |
|---|---|---|
| LoCoMo | 只提供问答对，无写入决策标注 | 无跨会话更新协议，问答为快照式 |
| LongMemEval | 只测最终检索准确率，无写入过程记录 | 无中间状态标注，冲突解决不可观测 |
| MemoryAgentBench | Selective Forgetting 维度最接近，但仍通过最终结果反推 | 未直接测更新前后状态差异 |
| MemoryArena | Multi-session 设计暴露 evolution 症状，但无法定位根因 | 无显式 conflict ground truth |
| AMA-Bench | Agent trajectory 视角，不测写入决策 | 不测记忆状态变化 |

**共同缺陷**：所有 benchmark 均从 retrieval 结果出发，以端到端准确率为代理指标。当系统在 benchmark 上失败时，无法区分是「写入错误」、「更新错误」还是「检索错误」。

---

## 三、场景设计原则

### 好场景的标准
1. **Formation 有歧义**：写入决策不能被阈值规则完全覆盖
2. **Evolution 有语义冲突**：更新需要理解语义，不是机械替换
3. **Retrieval 依赖前两阶段**：任一阶段失败会导致 Retrieval 答错
4. **Failure mode 可分析**：能明确指出哪个阶段的错误导致最终失败
5. **基于真实数据集**：场景文本源于 LoCoMo / LongMemEval / MemoryAgentBench 真实内容

### 坏场景的典型模式
1. **机械阈值可解**：importance > 0.8 直接写入，无需语义判断
2. **无 Formation 也能 Retrieval**：答案在最后一轮对话中，不需要记忆
3. **Evolution 不影响 Retrieval**：更新后检索结果与更新前相同
4. **Ground truth 需要外部知识**：非数据集内可验证的事实
5. **各阶段独立**：lifecycle chain 断裂，不体现全链路依赖

---

## 四、场景数据文件

- **路径**：`ref/datasets/lifecycle-eval/scenarios.jsonl`
- **格式**：每行一个 JSON 对象，包含完整 lifecycle 链
- **规模**：30 条好场景 + 10 条坏场景
- **来源**：locomo / longmemeval / memoryagentbench / synthetic
- **字段说明**：
  - `quality`: `good` | `bad`
  - `bad_reason`: null（好场景）或坏场景的失效原因
  - `lifecycle.formation.ground_truth.should_write/should_not_write`：显式 formation GT
  - `lifecycle.evolution.conflict_type`: `extend` | `replace` | `forget` | `new`
  - `lifecycle.evolution.expected_state`: key 为 memory_id，value 为期望内容（null = 应遗忘）
  - `lifecycle.evaluation.failure_mode`: 描述任一阶段失败的连锁效应

---

## 五、边界声明

- 本场景集用于验证生命周期评测框架的结构可行性，**不代表框架已具备区分度**
- formation/evolution 指标在这些场景上的满分结果，仅证明规则被正确实现，不证明模型预测能力
- 引入模型预测写入决策（替换规则 ground truth）是让指标有实际区分度的下一步，超出当前 RQ-001 范围
