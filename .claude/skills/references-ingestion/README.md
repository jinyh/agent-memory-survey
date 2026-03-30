# references-ingestion

项目级 skill，用于把新材料正确接入 AgentResearch 的 references 流水线，而不是只做内容摘要。

## 适用场景

当你想让 Claude 回答下面这类问题时，应该触发这个 skill：

- 这份新材料该进 `ref/paper/`、`ref/blog/` 还是 `ref/DeepResearch/`？
- 它应当算主证据、工程补充、工程参照、评测参照，还是线索？
- 它要不要进入 `docs/references/`？
- 是否应该只先记到 `docs/ideas/`，而不是直接写进 survey？
- 新增或修改这份材料后，要不要运行 `uv run --active python -m src.references`？

## 默认工作方式

这个 skill 默认只做**分析**，不改文件。

默认输出四部分：

1. `快速判断`
2. `摄取判断`
3. `边界`
4. `建议动作`

只有当用户明确要求时，才进入**分析 + 最小落笔**模式，去更新仓库中的材料层或索引层。

## 项目绑定的 references 流水线

它围绕这个仓库的三层 references 结构工作：

- `ref/`：原始材料层
  - `ref/paper/`
  - `ref/blog/`
  - `ref/DeepResearch/`
- `docs/references/`：结构化索引层
- `docs/ideas/` / `docs/survey/*.md`：当材料升级为稳定判断后才进入

## 使用边界

这个 skill 不适合：

- 单篇论文的深度纳入判断（优先用 `survey-evidence-mapper`）
- 重大跨层设计评审（优先用 `architect`）
- 正式研究工件链路推进（优先用 `research-workflow`）
- 与 references 摄取无关的实现任务

## 示例提示词

- `这篇 blog 要不要纳入 references？应该进 ref/blog 还是只记到 ideas？`
- `这个 GitHub project 在仓库里应该算工程参照还是暂不纳入？`
- `我刚往 ref/DeepResearch 加了一份报告，帮我判断要不要重建 references 索引。`
- `先判断这份材料的正确落点；如果值得纳入，再最小化更新对应索引。`

## 相关文件

- Skill 定义：`SKILL.md`
