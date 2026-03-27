# E-20260326-lifecycle-eval：全生命周期评测框架实验规格

> status: active | owner: Experiment Engineer | 2026-03-26

## experiment_id

`E-20260326-lifecycle-eval`

## decision_id

`D-20260326-lifecycle-eval-framework`

## question_id

`RQ-001`

## hypothesis

1. 现有 5 个主流 benchmark（LoCoMo、LongMemEval、MemoryAgentBench、MemoryArena、AMA-Bench）均不覆盖 formation 质量或 evolution 正确性的独立评测，这一结论可以从各 benchmark 的评测协议推导，而非依赖综合推断。
2. 在现有 `MemoryManager` + `EpisodicMemory` + `GraphMemoryStore` 原型基础上，可以构造 formation 和 evolution 的最小可量化评测场景，并产出 4 个新指标（`formation_precision`、`formation_recall`、`evolution_accuracy`、`forgetting_precision`），与现有 retrieval 指标并列呈现在同一 evaluation-report 中。

## inputs_outputs

### 输入

- `src/memory/evaluation.py`：现有评测模块（retrieval 场景 + 指标计算骨架）
- `src/memory/manager.py`、`src/memory/episodic.py`、`src/memory/graph_store.py`：原型实现
- `docs/architecture/2026-03-26-memory-lifecycle-eval-framework.md`：设计约束
- 手工构造的 formation / evolution ground truth（随场景代码一起固化，seed=42）

### 输出

- 扩展后的 `src/memory/evaluation.py`（新增 `build_formation_scenario()`、`build_evolution_scenario()`、`compute_formation_metrics()`、`compute_evolution_metrics()`）
- `docs/memory-eval/latest/report.md`（包含三个阶段全部指标与 retrieval backend 说明）
- `docs/memory-eval/latest/report.json`（机器可读格式，含三阶段指标与 retrieval backend 说明）
- `docs/memory-eval/latest/cases.jsonl`（每条查询 / 写入 / 更新的 trace）
- 扩展后的 `tests/test_memory.py`（formation / evolution 指标单元测试）

## 场景设计

### Formation 场景

**设计原则**（参考 Hindsight 的 retrospective annotation）：
- 构造一批输入事件，其中只有部分应被写入长期记忆（依据：重要性阈值 + 显式规则）
- 预先声明哪些 item 应被写入（`expected_writes`），哪些不应写入（噪声、重复、低重要性）
- 执行原型的写入逻辑，对比实际写入集合与 expected_writes

**场景结构**：
```python
# 输入事件（15 条）
events = [
    {"id": "ev-001", "content": "用户明确设置偏好：不喜欢冗长回复", "importance": 0.9},
    {"id": "ev-002", "content": "用户说了一句'嗯'", "importance": 0.1},
    {"id": "ev-003", "content": "用户的工作地点是上海", "importance": 0.85},
    # ... 共 15 条，重要性分布 0.1-0.95
]

# Ground truth：应被写入的 item（重要性 >= 0.6 且非重复）
expected_writes = {"ev-001", "ev-003", "ev-005", "ev-007", "ev-009", "ev-011", "ev-013"}
```

**触发规则**（对齐 ADR 决策 3）：重要性阈值 >= 0.6 且内容长度 >= 5 个字符。规则与 ground truth 同步声明，不靠直觉。

### Evolution 场景

**设计原则**（参考 MemoryAgentBench 的 selective forgetting + Synapse 的压缩机制）：
- 构造初始记忆库，再注入一批更新事件（冲突覆盖 + 主动遗忘请求）
- 预先声明更新后的预期状态（`expected_state_after`）
- 执行原型的更新/删除逻辑，对比实际状态与预期状态

**场景结构**：
```python
# 初始记忆库（10 条已写入记忆）
initial_memories = [
    {"id": "mem-001", "content": "用户住在北京"},
    {"id": "mem-002", "content": "用户喜欢简洁回复"},
    # ... 共 10 条
]

# 更新事件（5 条：2 个冲突覆盖 + 2 个遗忘请求 + 1 个无关新增）
update_events = [
    {"type": "conflict", "target": "mem-001", "new_content": "用户已搬到上海"},
    {"type": "forget",   "target": "mem-003"},
    # ...
]

# Ground truth：更新后预期状态
expected_state_after = {
    "mem-001": "用户已搬到上海",   # 被覆盖
    "mem-002": "用户喜欢简洁回复", # 不变
    "mem-003": None,               # 被遗忘（None 表示不应存在）
    # ...
}
```

## metrics

### Formation 质量

```
formation_precision = |实际写入 ∩ expected_writes| / |实际写入|
formation_recall    = |实际写入 ∩ expected_writes| / |expected_writes|
```

**合格线**：precision >= 0.8，recall >= 0.7（基于当前原型使用固定阈值规则，预期可达）

### Evolution 正确性

```
evolution_accuracy    = |状态匹配的 item| / |expected_state_after|
forgetting_precision  = |正确遗忘的 item| / |实际被遗忘的 item|
```

**合格线**：accuracy >= 0.8，forgetting_precision >= 0.9

### Retrieval 忠实度（已有，保持不变）

- `hit@1 >= 0.4`、`hit@3 >= 0.6`、`hit@5 >= 0.8`、`mrr >= 0.5`（来自现有 evaluation.py 基线）

### Benchmark 覆盖矩阵

- 产出一个结构化表格（写入 report.md），对 5 个主流 benchmark 逐个判断「覆盖 / 部分覆盖 / 不覆盖」
- 判断依据必须引用 benchmark 论文描述，不允许主观推断

## ground_truth_strategy

**策略**：预声明规则推导（Rule-Derived Ground Truth）

1. 先定义场景触发规则（formation：重要性阈值；evolution：冲突类型 + 遗忘请求标记）
2. 按规则推导 ground truth，与场景代码一起写入 `build_formation_scenario()` / `build_evolution_scenario()`
3. ground truth 以 Python dict 形式固化，seed=42，不依赖运行时随机
4. 任何修改 ground truth 的变更必须同步修改触发规则说明，禁止只改一处

**不采用**：人工标注（成本高、主观性强）、LLM 生成（不可重复）

## failure_conditions

以下情况视为实验失败，必须在 evaluation-report 中显式标注并回退：

1. **指标未达合格线**：任一指标低于合格线，且无法通过调整触发规则参数在 3 次内修复
2. **Ground truth 不可推导**：场景中出现无法从规则推导的 ground truth 条目（说明规则设计有误）
3. **Snapshot roundtrip 不一致**：现有 roundtrip 测试失败（说明扩展破坏了已有功能）
4. **Formation/evolution 场景与 retrieval 场景产生状态干扰**：三个场景必须独立初始化，共享状态导致指标串扰
5. **Benchmark 覆盖矩阵中任一判断无法引用论文原文**：回退到 evidence-map 补充证据

## 执行顺序

1. **TDD**：先写 `tests/test_memory.py` 中的 formation/evolution 指标测试（红）
2. 实现 `build_formation_scenario()` + `compute_formation_metrics()`（绿）
3. 实现 `build_evolution_scenario()` + `compute_evolution_metrics()`（绿）
4. 扩展 `run_evaluation()` 串联三个阶段，更新产物写入函数
5. 写 benchmark 覆盖矩阵分析（手工，输出到 report.md）
6. 运行全量测试：`uv run --active --extra dev pytest tests/ -q`
7. 产出 evaluation-report

## 开放问题（本 spec 的已知约束）

- 当前场景规模小（< 20 items），结论仅适用于玩具场景，不能外推到生产规模
- formation 场景中「重要性」字段目前由人工赋值，实际系统中应由模型预测，二者差距是已知边界
- evolution 场景中冲突解决逻辑目前依赖原型的 `update()` 方法，若原型不支持冲突感知更新，evolution_accuracy 的上限会受限于实现，需在 evaluation-report 中说明
