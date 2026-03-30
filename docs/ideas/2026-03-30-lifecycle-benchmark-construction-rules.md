# Memory Lifecycle Benchmark 构造规则

> type: ideas | 2026-03-30 | 关联 RQ-001
> 替代 2026-03-29-lifecycle-eval-scenario-design.md 中的合成场景方案

## 核心转变

RQ-001 原方案用 `importance >= 0.6 + len >= 5` 作为 formation ground truth，只能证明规则实现正确，无法测量系统真正的 formation/evolution 能力。本文档定义**从现有数据集结构化标注派生 lifecycle benchmark case** 的完整规则，标注缺失部分用 LLM-as-judge 补充并人工校验。

---

## 一、各数据集的 Lifecycle 信号映射

| 数据集 | Formation 信号 | Evolution 信号 | Lifecycle Chain |
|---|---|---|---|
| **LoCoMo** | session_summary + event_summary = 人工摘要的"值得记住什么"；observation = 用户画像更新 | 跨 session observation 差异 = 事实变化；event_summary 跨 session 可检测冲突 | **最高**：多 session + QA + evidence 引用可串全链路 |
| **LongMemEval** | answer_session_ids = 间接标注"哪些 session 含应记住的信息" | haystack_dates 提供时间轴；同一实体跨 session 陈述可能矛盾 | **中**：时间轴 + session 定位，无显式 evolution 标注 |
| **MemoryAgentBench** | Test_Time_Learning 多轮对话 = "哪些内容应被学习" | Conflict_Resolution 的候选答案 = 显式语义冲突 | **中**：Conflict_Resolution 最接近 evolution GT |
| **MemoryArena** | 每步选择结果 = 应被记住的决策 | 6 步 sequential task 中预算/兼容性约束随选择变化 = 状态演化 | **中高**：隐式但完整的 formation→evolution→retrieval |
| **AMA-Bench** | trajectory 中关键 action+observation = 应被记住的状态转移 | trajectory 推进中早期观察被后期状态替代 | **低中**：formation GT 需 LLM 补充标注 |

---

## 二、Formation 构造规则

### F1：LoCoMo Session Summary 派生法

**原理**：session_summary 和 event_summary 是人工摘要，= 人类判断的"这个 session 中值得记住什么"。

**构造步骤**：

1. 取 sample 的 session_N 对话原文（多轮 turn）
2. `should_write` = session_N_summary 按句拆分后的事实条目
3. `should_not_write` = session 中出现但 summary 未提及的内容（助手回复、寒暄、情绪、重复确认）
4. 对话原文作为输入，should_write / should_not_write 作为 ground truth
5. 评测：系统提取的记忆条目与 should_write 的 precision / recall

**GT 来源**：dataset_annotation（summary）+ llm_derived（should_not_write 的精确边界，见第六节 LLM 补充）

**case 规模**：10 samples × 10 sessions = ~100 个 formation case

### F2：LoCoMo Observation 派生法

**原理**：observation 字段记录"session 后对用户的新理解"（偏好、习惯、关系变化）。

**构造步骤**：

1. 取 session_N_observation 作为 should_write（session 级用户画像更新）
2. 取 session_N 对话中非 observation 内容作为 should_not_write 候选
3. 评测：系统是否提取出了 observation 级别的洞察

**与 F1 的关系**：F1 测"记住了什么事实"，F2 测"记住了什么推断"。互补使用。

**case 规模**：~100 个 case

### F3：LongMemEval Answer Session 派生法

**原理**：answer_session_ids 标注了答案在哪个 session。被标注 session 含应记住的信息，其余 session 是 haystack。

**构造步骤**：

1. 对每个 question，取 answer_session_ids 对应的 session 内容
2. 从 answer session 中提取与 answer 语义匹配的事实句 → should_write（需 LLM 补充）
3. 从 haystack session 随机采样同等数量的内容 → should_not_write
4. 评测：系统能否从 53+ session 中识别出哪些内容值得写入

**GT 来源**：dataset_annotation（session 定位）+ llm_derived（事实句提取）

**case 规模**：采样 50-100 个有单一 answer_session 的 case

### F4：MemoryArena 决策记忆派生法

**原理**：bundled_shopping 每步的 target_asin + attributes 是后续必须记住的信息。

**构造步骤**：

1. step_N 的 answer（选中产品 + 属性）→ should_write
2. step_N 的 question 中搜索过程描述 → should_not_write（过程信息）
3. 评测：系统是否只记住了决策而非搜索过程

**GT 来源**：dataset_annotation（answer 字段）

---

## 三、Evolution 构造规则

### E1：LoCoMo 跨 Session Observation 差异法

**原理**：session_1_observation ~ session_10_observation 记录用户画像随时间变化。相邻 session 的 observation 差异 = 事实演化。

**构造步骤**：

1. 对比 session_N_observation 与 session_M_observation（M > N）
2. 语义冲突（同一属性不同值）→ conflict_type = `replace`
3. 新增属性 → conflict_type = `new`
4. 消失的属性 → conflict_type = `forget` 候选
5. expected_state = 最新 session 的 observation

**GT 来源**：dataset_annotation（observation 文本）+ llm_derived（NLI 语义冲突检测）

**case 规模**：采样 50 个有明确差异的 observation pair

### E2：LoCoMo Event Summary 跨 Session 冲突检测

**原理**：events_session_1 ~ events_session_10 记录实际事件。同一实体/话题跨 session 事件可能矛盾。

**构造步骤**：

1. 收集所有 session 的 event_summary
2. 按实体/话题聚类（人名、地点、偏好项）
3. 同一实体不同 session 描述矛盾 → evolution case
4. expected_state = 最后 session 中的版本
5. 某事件只在早期出现且后续被替代 → forget case

### E3：MemoryAgentBench Conflict Resolution 直接复用

**原理**：Conflict_Resolution split 的 context 是编号事实列表，100 个候选答案存在语义冲突。**现有数据集中最接近 evolution GT 的数据**。

**构造步骤**：

1. context 中的事实列表 → 初始记忆
2. 100 个候选答案中相互矛盾的子集 → 冲突事件
3. query → 冲突解决后应回答的检索问题
4. 正确答案 = 冲突消解后应留存的事实

**GT 来源**：dataset_annotation（context + answer）

**case 规模**：8 个原始 case，每个可拆出多个冲突对

### E4：MemoryArena Sequential State 演化法

**原理**：bundled_shopping 6 步任务中预算和已选产品随步变化，后续正确答案依赖前序状态的正确更新。

**构造步骤**：

1. 初始状态 = step_1 的 global rules（总预算、兼容性要求）
2. 每个 step 的 answer 触发状态更新（剩余预算、已选列表）
3. expected_state_after_step_N = 累积前序选择后的状态
4. 评测：step_N 时系统是否正确维护了当前状态

**GT 来源**：dataset_annotation（answer + global rules 可计算推导）

---

## 四、Lifecycle Chain 构造规则

### L1：LoCoMo 全链路法（最完整）

LoCoMo 同时提供对话、摘要、观察、事件和 QA，支持完整 lifecycle chain：

```
Formation: session_1..session_K 对话 → 系统应提取 session_summary 中的事实
Evolution: session_K+1..session_N 引入新信息 → 系统应根据 observation 差异更新记忆
Retrieval: QA pair question → 系统应根据更新后的记忆回答
```

**构造步骤**：

1. 选取跨多 session 的 QA pair（evidence 引用 >= 2 个 session）
2. formation 阶段 = evidence 引用的最早 session 之前的所有 session
3. evolution 阶段 = evidence 引用的 session 之间的 observation 差异
4. retrieval 阶段 = QA question + answer
5. 构造 failure attribution 链：
   - formation_gt = 被引用 session 的 summary 中与 answer 相关的事实
   - evolution_gt = 跨 session 的 observation 变化
   - retrieval_gt = QA answer

**Failure Attribution 规则**：

| 最终表现 | formation 状态 | evolution 状态 | 归因 |
|---|---|---|---|
| QA 答错 | 缺失对应事实 | — | Formation 失败 |
| QA 答错 | 正确 | 未更新 | Evolution 失败 |
| QA 答错 | 正确 | 正确 | Retrieval 失败 |
| QA 答对 | 正确 | 正确 | 全链路通过 |

### L2：MemoryArena Step Chain 法

```
Formation: step_1 任务描述 + global rules → 系统应记住预算和约束
Evolution: step_2..step_6 选择 → 系统应更新剩余预算和已选列表
Retrieval: step_N 任务 → 需参考前序所有选择才能找到兼容产品
```

**Failure Attribution**：
- step_N 答错 + 未记录 global rules → Formation 失败
- step_N 答错 + 未更新前序选择 → Evolution 失败
- step_N 答错 + 状态正确但未匹配兼容产品 → Retrieval 失败

---

## 五、Benchmark Case 统一格式

路径：`ref/datasets/lifecycle-eval/`

```jsonl
{
  "id": "lifecycle-locomo-S01-chain-001",
  "source": "locomo",
  "lifecycle_type": "full_chain",

  "formation": {
    "input": "session 对话原文",
    "ground_truth": {
      "should_write": ["事实1: 用户住在上海", "事实2: 用户喜欢简洁回复"],
      "should_not_write": ["嗯", "好的", "助手程序性回复"]
    },
    "derivation": "session_3_summary 句级拆分",
    "derivation_type": "dataset_annotation"
  },

  "evolution": {
    "initial_state": {"m001": "用户住在北京"},
    "update_events": [
      {"session": 5, "type": "replace", "entity": "居住地",
       "old": "北京", "new": "上海"}
    ],
    "expected_state": {"m001": "用户住在上海"},
    "derivation": "session_3_observation vs session_5_observation",
    "derivation_type": "dataset_annotation + llm_derived"
  },

  "retrieval": {
    "query": "QA question",
    "expected_answer": "QA answer",
    "evidence_sessions": ["D3", "D5"],
    "depends_on_formation": true,
    "depends_on_evolution": true
  },

  "failure_attribution": {
    "if_formation_fails": "缺少 '用户住在上海' 导致无法回答居住地问题",
    "if_evolution_fails": "仍记录 '北京' 导致答案过时",
    "if_retrieval_fails": "记忆正确但未被召回"
  }
}
```

`lifecycle_type` 取值：
- `formation_only`：仅测 formation（F1-F4 规则产出）
- `evolution_only`：仅测 evolution（E1-E4 规则产出）
- `full_chain`：测完整 lifecycle（L1-L2 规则产出）

`derivation_type` 取值：
- `dataset_annotation`：GT 完全从数据集已有标注派生
- `llm_derived`：GT 由 LLM 标注，未经人工校验
- `llm_derived_human_verified`：GT 由 LLM 标注并经人工校验

---

## 六、LLM-as-Judge 补充策略

### 补充范围

数据集标注能覆盖的 GT 有明确边界，以下缺口需要 LLM-as-judge 补充：

| 缺口 | 涉及数据集 | 为什么标注不够 | LLM 补充方式 |
|---|---|---|---|
| Formation: should_not_write 精确边界 | LoCoMo | summary 只标注"应记住"，"不应记住"是推导的 | LLM 对每句话做 write/skip 分类，与 summary GT 交叉校验 |
| Formation: 事实句提取 | LongMemEval | answer_session_ids 只到 session 级，未标注哪句话含关键事实 | LLM 从 answer_session 提取与 answer 语义匹配的事实句 |
| Evolution: 语义冲突检测 | LoCoMo, LongMemEval | observation 差异可能是"新增"非"冲突"，需语义判断 | LLM 做 NLI，只保留 contradiction 作为 replace case |
| Evolution: 状态替代识别 | AMA-Bench | trajectory 100+ steps，哪些观察被后续替代需语义判断 | LLM 对相邻 observation 做变化检测 |
| Lifecycle: failure attribution 因果验证 | 所有 | failure_attribution 是推导的因果链，可能多因一果 | LLM 判断 retrieval 失败的主因 |

### 执行协议

**原则**：LLM 不生成 GT，只做分类/判断/提取；最终 GT 仍需人工校验。

1. **Prompt 模板化**：每种补充任务有固定 prompt，输入 = 数据集原文 + 结构化字段，输出 = 结构化 JSON
2. **双模型一致性**：两个模型独立标注，只保留一致结果
3. **人工校验采样**：随机抽样 20% 人工校验，一致率 < 85% 则回退该补充规则
4. **标注来源标记**：每个 GT 条目标注 derivation_type

### 示例 Prompt：Formation should_not_write 分类

```
你是一个记忆系统评测标注员。给定一段对话和这段对话的人工摘要，
请判断对话中的每句话是否应该被写入长期记忆。

## 输入
对话原文：{session_text}
人工摘要（= 值得记住的信息）：{session_summary}

## 输出格式
对每句话输出 JSON：
{"turn_idx": N, "text": "...", "label": "write" | "skip", "reason": "..."}

## 判断规则
- write: 内容与摘要某条事实语义匹配，或含摘要未提及但有长期价值的信息
- skip: 寒暄、确认、情绪表达、助手程序性回复、已被摘要更精确版本替代的原始表述
```

### 示例 Prompt：Evolution 跨 Session NLI

```
你是一个事实一致性判断员。给定同一用户在两个时间点的画像描述，
请判断它们的关系。

## 输入
时间点 A（session {N}）：{observation_N}
时间点 B（session {M}，M > N）：{observation_M}

## 输出格式
{
  "entity": "居住地",
  "statement_a": "住在北京",
  "statement_b": "住在上海",
  "relation": "contradiction" | "entailment" | "neutral" | "extension",
  "evolution_type": "replace" | "new" | "forget" | "unchanged"
}

## 判断规则
- contradiction → replace：B 直接否定 A 某属性值
- extension → new：B 新增 A 没提到的属性
- A 中有但 B 中消失 → forget 候选
- entailment → unchanged
```

### LLM 补充预期规模

| 补充任务 | 输入规模 | 预期产出 | 人工校验量 |
|---|---|---|---|
| LoCoMo should_not_write | 100 sessions × ~20 turns | ~2000 turn-level labels | ~400 条 |
| LongMemEval 事实句提取 | 50-100 questions × answer_session | ~200 事实句 | ~40 条 |
| 跨 session NLI | 50 observation pairs | ~100 实体级判断 | ~20 条 |
| AMA-Bench 状态变化 | 20 episodes × ~100 steps | ~400 step-level labels | ~80 条 |
| Failure attribution | 50 lifecycle chains | ~50 因果判断 | ~10 条 |

---

## 七、与现有工作的关系

### 替代关系

- 本文档替代 `2026-03-29-lifecycle-eval-scenario-design.md` 中的场景构造方案
- 该文档中的**指标定义**（formation_precision/recall、evolution_accuracy/forgetting_precision 等）仍然有效，本文档不重复定义指标，只定义 GT 的来源和构造方法

### 对 evaluation.py 的影响

- 现有 `build_formation_scenario()` / `build_evolution_scenario()` 的合成场景可保留为 smoke test
- 新增的 dataset-derived case 应通过独立入口加载（如 `load_lifecycle_cases()`），不混入现有 `load_benchmark_cases()`
- `compute_formation_metrics()` / `compute_evolution_metrics()` 的接口不变，只是 GT 来源从规则推导变为数据集派生

### 对 05-evaluation.md 的影响

本文档的构造规则如果落地实现，可以更新覆盖矩阵：

| Benchmark | Formation 质量 | Evolution 正确性 | Retrieval 忠实度 |
|---|---|---|---|
| LoCoMo | **可覆盖**（F1+F2 规则） | **可覆盖**（E1+E2 规则） | 覆盖 |
| LongMemEval | **可覆盖**（F3 规则 + LLM 补充） | 部分覆盖（LLM NLI） | 覆盖 |
| MemoryAgentBench | 部分覆盖 | **可覆盖**（E3 规则） | 覆盖 |
| MemoryArena | **可覆盖**（F4 规则） | **可覆盖**（E4 规则） | 覆盖 |
| AMA-Bench | 部分覆盖（LLM 补充） | 部分覆盖（LLM 补充） | 覆盖 |

---

## 边界声明

- 本文档定义构造规则，不包含实现代码。实现需进入 `docs/plans/` 的正式实验规格。
- LLM-as-judge 的标注质量取决于 prompt 设计和人工校验覆盖率，本文档给出的预期规模仅为估算。
- LoCoMo 全链路法（L1）是本方案的核心价值点，但其可行性取决于 LoCoMo 的 observation/event_summary 字段是否足够结构化以支撑自动化 diff。需要在实际数据上验证。
- 数据集 case 规模（~100 formation + ~50 evolution + ~50 lifecycle chain）足以验证框架可行性，但不足以作为正式 leaderboard。
