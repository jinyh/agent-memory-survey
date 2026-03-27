# RQ-001 状态收口

> v1.0.0 | 2026-03-27
>
> status: completed
> owner: Research Lead

## 背景

这份记录用于收口当前 RQ-001 相关工作，明确哪些内容已经完成、哪些任务适合暂停、以及后续如果继续推进应优先做什么。

## 当前完成情况

### 已完成

- RQ-001 的研究问题、证据地图、实验规格、评测报告已经形成闭环。
- `src/memory/evaluation.py` 已补齐 formation / evolution / retrieval 三阶段评测，并增加 retrieval backend 说明。
- `tests/test_memory.py` 已补齐 evaluation 产物、语义检索后端和场景确定性测试。
- `docs/survey/05-evaluation.md` 与 `docs/survey/survey-map.md` 已收紧 benchmark 覆盖边界，并记录版本号。
- `docs/plans/README.md` 与 `docs/ideas/README.md` 已整理为各自入口索引。
- `RQ-001` 相关补齐内容已提交并推送到 `origin/main`。

### 已完成的任务

- Task #1：补齐 RQ-001 未完成内容
- Task #2：定位 RQ-001 关键文件
- Task #3：评估测试与文档组织
- Task #4：梳理 memory 评测相关模式
- Task #5：整理 plans 与 survey 版本

## 暂停的任务

以下任务目前不建议继续推进，适合作为下一轮研究整理工作：

- Task #6：Map memory evaluation implementations
- Task #7：Identify RQ-001 usage patterns
- Task #8：Assess reuse and redundancy

## 后续优先级

如果后续继续推进，建议顺序为：

1. Task #6：先补实现映射，确认评测实现与文档之间的对应关系。
2. Task #7：再梳理 RQ-001 的使用模式，沉淀可复用套路。
3. Task #8：最后评估复用与冗余，做进一步减法。

## 结论

当前这轮工作已经完成到“研究闭环 + 文档收口 + 提交推送”的状态，可以先停下来；后续任务更适合下一轮继续。
