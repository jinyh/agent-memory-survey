# RQ-001 Survey 更新说明

> status: active | owner: Writer | 2026-03-26

## experiment_id

`E-20260326-lifecycle-eval`

## affected_survey_sections

- `docs/survey/05-evaluation.md`：主要更新目标
- `docs/survey/survey-map.md`：补充评测覆盖维度到按问题映射

## updated_claims

### 可回写的结论（有论文级依据）

1. **「当前 benchmark 覆盖边界」**：5 个主流 benchmark（LoCoMo、LongMemEval、MemoryAgentBench、MemoryArena、AMA-Bench）均不完整覆盖 formation 质量和 evolution 正确性的独立评测。MemoryAgentBench 通过 selective forgetting 维度部分触及 evolution，是已知最接近全生命周期评测的 benchmark。
   - 证据类型：论文证据（各 benchmark 论文的评测协议描述）
   - 建议写入位置：`05-evaluation.md` 新增 `### 当前 benchmark 未覆盖的评测维度` 小节

2. **「评测什么 vs 没评什么」的细化**：现有 benchmark 的共同模式是以端到端 retrieval QA 准确率为代理指标，无法区分「写入错误」和「检索错误」，也无法区分「记忆被检索到但被 agent 错误使用」与「记忆未被检索到」。
   - 证据类型：综合推断（基于 5 个 benchmark 评测协议的交叉对比）
   - 建议写入位置：`05-evaluation.md` 现有 `评测什么` 节的补充段落，需标注为综合推断

### 不可回写的结论（边界外）

- ~~formation/evolution 指标优于现有 benchmark~~ — 当前实验中 1.0 分值来自规则对齐，不来自模型预测，无区分度证据
- ~~本项目原型的 retrieval 能力弱于 benchmark 报告的其他系统~~ — tag 匹配 vs 语义检索不可比
- ~~三阶段联合评测框架已成熟~~ — 仅验证了技术可行性，指标区分度未经实证

## evidence_scope

| 结论 | 证据类型 | 来源 |
|---|---|---|
| 5 个 benchmark 均不完整覆盖 formation/evolution | 论文证据 | 各 benchmark 论文评测协议 |
| MemoryAgentBench 最接近全生命周期评测 | 论文证据 | arXiv:2507.05257 selective forgetting 维度 |
| 端到端 QA 无法归因写入错误 vs 检索错误 | 综合推断 | 5 个 benchmark 评测协议交叉对比 |
| formation/evolution 指标定义可行 | 实验证据（本项目） | E-20260326-lifecycle-eval evaluation-report |

## open_questions

1. formation 场景引入模型预测写入决策后，precision/recall 的实际区分度是多少？（需后续实验）
2. evolution 中的语义冲突检测（两条矛盾事实的自动识别与选择）是否应作为独立评测维度纳入？
3. 是否需要在 `05-evaluation.md` 中增加「评测框架演进路线图」小节，还是留给后续 RQ？

## 回写草案

### `05-evaluation.md` 新增内容（建议位置：现有章节末尾）

```markdown
### 当前 benchmark 未覆盖的评测维度

现有 5 个主流 benchmark 的评测覆盖范围如下：

| Benchmark | Formation 质量 | Evolution 正确性 | Retrieval 忠实度 |
|---|---|---|---|
| LoCoMo | 不覆盖 | 不覆盖 | 覆盖 |
| LongMemEval | 不覆盖 | 不覆盖 | 覆盖 |
| MemoryAgentBench | 部分覆盖 | 部分覆盖 | 覆盖 |
| MemoryArena | 不覆盖 | 部分覆盖 | 覆盖 |
| AMA-Bench | 不覆盖 | 不覆盖 | 覆盖 |

其中，MemoryAgentBench（arXiv:2507.05257）通过 selective forgetting 维度最接近 evolution 正确性评测，但仍依赖最终 retrieval 结果间接判断，未直接测量 evolution 中间状态。

这一覆盖空白意味着：现有 benchmark 能检测「agent 是否能从历史中找到正确答案」，但无法单独归因「写入选择是否正确」或「冲突更新是否准确」。当系统在 demo 和基准上表现良好但在长期部署中出现记忆污染和冲突事实时，现有评测缺乏定位根因的能力。
```

### `survey-map.md` 补充（建议位置：按问题映射表）

在「当前 benchmark 到底在测什么」行追加说明：现有 benchmark 集中覆盖 retrieval，formation 和 evolution 的独立评测仍为空白。
