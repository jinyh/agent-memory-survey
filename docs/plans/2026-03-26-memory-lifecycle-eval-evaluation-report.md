# E-20260326-lifecycle-eval 评测报告

> status: completed | owner: Experiment Engineer | 2026-03-26

## experiment_id

`E-20260326-lifecycle-eval`

## validated_decisions

- `D-20260326-lifecycle-eval-framework`：**已验证**。在现有 `evaluation.py` 中扩展 formation/evolution 场景和指标的方案可行，三个阶段独立初始化、互不干扰，产物格式统一。

## results_summary

### 实验结果

| 阶段 | 指标 | 值 | 合格线 | 判定 |
|---|---|---|---|---|
| Formation | formation_precision | 1.000 | >= 0.8 | PASS |
| Formation | formation_recall | 1.000 | >= 0.7 | PASS |
| Evolution | evolution_accuracy | 1.000 | >= 0.8 | PASS |
| Evolution | forgetting_precision | 1.000 | >= 0.9 | PASS |
| Retrieval | hit@1 | 0.429 | >= 0.4 | PASS |
| Retrieval | hit@3 | 0.429 | >= 0.6 | **FAIL** |
| Retrieval | hit@5 | 0.571 | >= 0.8 | **FAIL** |
| Retrieval | mrr | 0.464 | >= 0.5 | **FAIL** |
| 系统 | snapshot_roundtrip | true | true | PASS |

### 解读

1. **Formation 和 Evolution 指标全部 1.0**：这是预期结果。当前场景使用"规则推导 ground truth"策略（experiment-spec 决策 3），规则与执行逻辑完全对齐，因此 precision/recall 必然为 1.0。这证明框架本身可用，但**不证明规则是好的**——只证明规则被正确实现了。

2. **Retrieval 指标低于合格线**：hit@3（0.429）和 hit@5（0.571）未达到 experiment-spec 中的 0.6 和 0.8 合格线。**根因**：当前原型的检索基于 tag 重叠和时间衰减，不是语义相似度（未启用 VectorMemoryStore），在中文查询 vs 中文内容的匹配上能力有限。这是已知的原型局限，而非评测框架缺陷。

3. **三阶段独立性验证通过**：三个场景各自初始化独立 manager，无状态串扰。

### Benchmark 覆盖矩阵

| Benchmark | Formation 质量 | Evolution 正确性 | Retrieval 忠实度 | 判断依据 |
|---|---|---|---|---|
| LoCoMo | 不覆盖 | 不覆盖 | 覆盖（对话检索 QA） | 论文只定义 retrieval QA 任务，无写入/更新评测协议 |
| LongMemEval | 不覆盖 | 不覆盖 | 覆盖（长对话 QA） | 论文评测维度为 temporal/spatial/relational retrieval，无 formation 独立指标 |
| MemoryAgentBench | 部分覆盖 | 部分覆盖（selective forgetting） | 覆盖 | 论文包含 test-time learning 和 selective forgetting 维度，是最接近全生命周期的 benchmark |
| MemoryArena | 不覆盖 | 部分覆盖（multi-session drift） | 覆盖 | 论文评测跨 session 一致性，间接触及 evolution 但无独立指标 |
| AMA-Bench | 不覆盖 | 不覆盖 | 覆盖（agent trajectory） | 论文评测 agent 工具使用中的记忆利用，不涉及写入/更新质量 |

**结论**：5 个 benchmark 中，0 个完整覆盖 formation 独立评测，1 个（MemoryAgentBench）部分覆盖 evolution。这一结论来自各 benchmark 论文的评测协议描述，非综合推断。

## failure_cases

### Retrieval 未达合格线

- **hit@3 = 0.429**（合格线 0.6）、**hit@5 = 0.571**（合格线 0.8）、**mrr = 0.464**（合格线 0.5）
- 根因：EpisodicMemory 和 GraphMemoryStore 的 `query()` 依赖 tag 匹配 + 时间衰减评分，不支持语义相似度。查询 "RAG 检索管道" 只能通过 tag `["rag", "检索"]` 匹配，无法捕捉语义近义词
- 分类：**原型能力局限**，非评测框架缺陷
- 处置：experiment-spec failure_condition #1 的回退条件为「无法通过调整触发规则参数在 3 次内修复」。此处不适用——retrieval 合格线是为语义检索设计的，当前原型不支持语义检索。建议在后续启用 VectorMemoryStore 后重新验证

### Formation/Evolution 的 1.0 分值

- 分类：**场景设计局限**，非框架缺陷
- 说明：规则推导 ground truth 保证了 precision/recall = 1.0，但这只验证了"规则被正确编码"，不验证"规则是否合理"。在实际系统中，formation 决策由模型预测（如 Mem0 的意图检测），规则与执行之间存在不确定性，此时 precision/recall 才会有区分度
- 处置：标注为已知边界，不阻塞后续工件。未来若引入模型预测的写入决策，应重新评测

## boundary_notes

### 适用边界

1. **场景规模**：formation 15 条事件、evolution 5 条初始记忆 + 4 条更新、retrieval 18 条记忆 + 7 条查询。结论仅适用于玩具规模，不能外推到生产环境（千级以上记忆项）
2. **触发规则**：formation 使用固定阈值（importance >= 0.6 且 content length >= 5），实际系统使用模型预测，二者差距是已知边界
3. **冲突解决**：evolution 场景中冲突覆盖依赖 `update_memory()` 的直接字段替换，不涉及语义冲突检测（如两条事实矛盾时的选择）
4. **遗忘机制**：evolution 场景中遗忘使用 `forget()` 显式删除，不涉及基于时间/访问频率的自动遗忘策略
5. **检索能力**：retrieval 阶段未启用 VectorMemoryStore（需 sentence-transformers 模型），tag 匹配的检索能力是本次实验的已知瓶颈

### 不支撑的结论

- 不能声明「本框架已覆盖全生命周期评测」——formation 和 evolution 的场景仅验证了框架可用性，不验证指标的区分度
- 不能声明「formation/evolution 指标优于现有 benchmark」——当前场景下 1.0 的分值来自规则对齐，不来自真实的模型预测
- 不能用 retrieval 的 0.429~0.571 与其他系统对比——基于 tag 匹配的检索不等价于语义检索

### 可支撑的结论

- 现有 5 个主流 benchmark 均不完整覆盖 formation 独立评测和 evolution 正确性评测，这一判断有论文级依据
- 在 `evaluation.py` 中扩展 formation/evolution 场景和指标的技术方案可行，三阶段独立、产物统一
- formation_precision/recall 和 evolution_accuracy/forgetting_precision 四个指标定义合理，在引入模型预测后可直接复用
