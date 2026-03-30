# research-workflow

项目级 skill，用于把研究主题推进到 AgentResearch 的正式工件链路中，而不是只给泛泛流程建议。

## 适用场景

当你想让 Claude 回答下面这类问题时，应该触发这个 skill：

- 这个主题现在该写 `research-brief`、`evidence-map`、`architecture-decision`、`experiment-spec`、`evaluation-report` 还是 `survey-update-note`？
- 这个主题当前处在哪个阶段？
- 现在是否满足 Gate A、Gate B、Gate C？
- 如果还不能进入下一步，应该回退到哪一阶段？
- 如何把已有 `docs/ideas/`、survey judgment 或 prototype work 升级为正式工件？

## 默认工作方式

这个 skill 默认只做**流程判断**，不改文件。

默认输出五部分：

1. `当前阶段判断`
2. `Gate 检查`
3. `推荐下一步`
4. `边界`
5. `建议动作`

只有当用户明确要求时，才进入**流程判断 + 最小落笔**模式，去补当前最关键的正式工件。

## 项目绑定的正式链路

它围绕这个仓库的标准工件链工作：

- `research-brief`
- `evidence-map`
- `architecture-decision`
- `experiment-spec`
- `evaluation-report`
- `survey-update-note`

对应的核心方法层真源：

- `docs/method/workflow.md`
- `docs/method/gates.md`
- `docs/method/artifacts.md`

## 使用边界

这个 skill 不适合：

- 单篇论文纳入判断（优先用 `survey-evidence-mapper`）
- 非论文材料摄取与索引判断（优先用 `references-ingestion`）
- 重大架构专项评审（优先用 `architect`）
- 纯实现任务或局部 bug fix

## 示例提示词

- `把 memory lifecycle eval 这个主题推进成正式 research brief。`
- `这个 topic 现在是否已经能进入 experiment-spec？`
- `帮我检查这个主题是否过了 Gate A，如果没过应该回退到哪一步？`
- `先判断当前阶段和缺口；如果明确，再最小化补齐下一份正式工件。`

## 相关文件

- Skill 定义：`SKILL.md`
