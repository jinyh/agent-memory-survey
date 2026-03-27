# RQ-001 补齐更新

## 背景

在确认 `RQ-001 完成度表` 之后，继续补齐未完成内容，并把 survey、评测实现和测试闭环收口到更稳定的状态。

## 核心内容

### 已完成的补齐

- `docs/survey/05-evaluation.md`：将 benchmark 覆盖边界改写为论文级稳定结论，避免把本项目实验结果写成 survey 结论。
- `docs/survey/survey-map.md`：把 benchmark 覆盖映射收紧为“主要覆盖 retrieval，MemoryAgentBench 仅部分触及 evolution”。
- `src/memory/evaluation.py`：
  - 新增 `VectorMemoryStore` 的可选接入；
  - 增加 `retrieval_backend` 输出说明；
  - 修正 roundtrip 检查，避免使用已污染状态进行自检。
- `tests/test_memory.py`：
  - 增加 evaluation 产物测试；
  - 增加 `VectorMemoryStore` 的 query/update/snapshot 测试；
  - 增加 formation/evolution 场景与指标的确定性测试。

### 验证结果

- `uv run --active --extra dev pytest tests/test_memory.py -q`
- 结果：`46 passed`

## 结论

RQ-001 目前已经从“原型验证 + 草案收敛”推进到更完整的闭环状态，但 formation / evolution 的区分度仍然应被表述为原型级验证，而不是成熟结论。

## 可能的下一步

- 把这次变更整理成更正式的收口说明
- 如果后续继续推进 RQ-001，再考虑将语义检索作为默认 retrieval 场景的一部分
