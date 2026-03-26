# ADR：Agent Memory 全生命周期评测框架

> status: active | owner: Architect | 2026-03-26

## decision_id

`D-20260326-lifecycle-eval-framework`

## question_id

`RQ-001`

## evidence_refs

- MemAgent（arXiv:2507.02259）：RL 写入选择可优化，说明 formation 质量是可量化目标
- MemoryAgentBench（arXiv:2507.05257）：selective forgetting 作为独立测试维度，是 evolution 评测的最近参照
- Hindsight：retrospective annotation 框架，提供 formation 缺口的因果归因方法
- Synapse：episodic 压缩实验，evolution 中间状态的唯一论文级参照
- 当前 `src/memory/evaluation.py`：已有 retrieval hit@k / MRR / snapshot roundtrip 实现，可直接扩展

## 核心决策

### 决策 1：在现有 `evaluation.py` 中扩展，而非新建独立模块

**选择**：扩展 `src/memory/evaluation.py`，新增 `build_formation_scenario()`、`build_evolution_scenario()` 和对应 metrics 计算函数，与现有 `build_scenario()` + `compute_metrics()` 并列。

**理由**：
- 现有模块已有固定 seed 场景构造、产物写入和 CLI 入口的完整骨架，不重复建设
- formation 和 evolution 场景共用 `MemoryManager`、`EpisodicMemory`、`GraphMemoryStore`，无需额外依赖
- 评测产物格式统一（JSON + Markdown + JSONL），保持可比性

### 决策 2：使用直接计算指标，不引入 LLM-judge

**选择**：formation 和 evolution 指标全部基于手工构造的 ground truth + 确定性计算，不用 LLM 打分。

**理由**：
- LLM-judge 不可重复（相同输入不同轮次结果可能不同），违反 success_criteria 中的「结果可复现（固定 seed）」要求
- 当前原型场景规模小（< 100 记忆项），手工 ground truth 构造可行
- LLM-judge 适合 scale-out 阶段，不适合当前最小验证目标

### 决策 3：ground truth 策略——预声明写入集合与更新规则

**选择**：在场景构造时同时定义「预期写入集合」（formation ground truth）和「预期更新状态」（evolution ground truth），作为独立数据结构与场景一起固化。

**具体形态**：
```python
# formation ground truth
expected_writes: dict[str, bool]  # item_id -> 应被写入

# evolution ground truth
expected_state_after: dict[str, str | None]  # item_id -> 更新后内容 / None 表示应被遗忘
```

**理由**：
- 与 Hindsight 的 retrospective annotation 思路一致——明确「本该写入什么」
- 不依赖外部工具，ground truth 与场景代码共存，易于复现和审查

### 决策 4：最小指标集

**Formation 质量**（2 个）：
- `formation_precision`：实际写入的记忆中，属于 ground truth 预期写入集合的比例
- `formation_recall`：ground truth 预期写入集合中，被实际写入的比例

**Evolution 正确性**（2 个）：
- `evolution_accuracy`：更新后记忆库状态与 expected_state_after 的匹配率
- `forgetting_precision`：被遗忘/删除的记忆中，属于 ground truth 应删除集合的比例

**Retrieval 忠实度**（已有，保持不变）：
- `hit@1`、`hit@3`、`hit@5`、`mrr`

## 影响面

| 文件 | 变动类型 | 说明 |
|---|---|---|
| `src/memory/evaluation.py` | 修改 | 新增 formation/evolution 场景构造和指标计算函数 |
| `tests/test_memory.py` | 修改 | 新增 formation/evolution 指标的单元测试 |
| `docs/survey/05-evaluation.md` | 修改 | 补充「当前 benchmark 未覆盖范围」一节，引用本决策 |
| `docs/plans/`（experiment-spec、evaluation-report） | 新增 | 后续工件，本 ADR 通过后创建 |

不影响：`base.py`、`manager.py`、`episodic.py`、`vector_store.py`、`graph_store.py`、`agent.py`

## 替代方案

### 替代 A：新建独立评测模块 `src/memory/lifecycle_eval.py`
- 拒绝原因：现有 `evaluation.py` 骨架完整，分拆只增加维护负担，不符合 YAGNI 原则

### 替代 B：用 LLM-judge 打分 formation 和 evolution 质量
- 拒绝原因：不可重复，引入外部 API 依赖，与当前无外网原型约束冲突

### 替代 C：用端到端检索指标代理 formation/evolution（只测最终 retrieval）
- 拒绝原因：无法区分「写入错误」和「检索错误」，不能回答 RQ-001 的核心问题

### 替代 D：采用 MemoryAgentBench 的 selective forgetting 测试协议
- 部分采纳：`forgetting_precision` 指标设计参考其思路，但不完整复现其协议（benchmark 数据集不在本地）

## 风险

| 风险 | 严重性 | 缓解 |
|---|---|---|
| Ground truth 构造主观性高（谁决定「应被写入」） | 中 | 场景设计时明确写入触发规则，ground truth 随规则推导，不靠直觉 |
| Formation/evolution 指标只在玩具场景下有效，不能外推 | 高 | evaluation-report 必须明确写明适用边界，不允许将结果上升为一般性结论 |
| 扩展 `evaluation.py` 后文件变长，维护难度增加 | 低 | 控制三个场景构造函数各自独立，不共享内部状态 |

## 开放问题（留给 experiment-spec 决定）

1. formation 场景中，「写入触发规则」的具体形态：基于关键词匹配、重要性阈值还是显式标注？
2. evolution 场景中，冲突事实的构造方式：直接覆盖同一 item 还是插入矛盾 item？
3. 是否需要多轮会话场景（跨 session 的 evolution）或单轮足够？
