# Ideas

这个目录用于记录与 Claude 交互过程中产生的想法、临时洞察、候选映射和尚未进入正式研究链路的局部启发。

## 命名规则

- 使用 Markdown 文件
- 文件名格式：`YYYY-MM-DD-<short-slug>.md`
- `short-slug` 使用小写 `kebab-case`
- 同一天多条记录时，用不同 slug 或序号区分

## 写作建议

每个文件尽量包含：

- 标题
- 想法背景
- 核心内容
- 可能的下一步
- 待确认事项

## 当前记录

### 2026-04-04：知识库工作流观察

- [2026-04-04-llm-kb-workflow-note.md](2026-04-04-llm-kb-workflow-note.md) — LLM 编译式知识库 workflow 的角色边界与可借鉴点

### 2026-03-29：本轮改动与整理

- [2026-03-29-agentresearch-change-summary.md](2026-03-29-agentresearch-change-summary.md) — 本轮仓库改动摘要与目录观察
- [2026-03-29-agent-memory-benchmark-anchor-check.md](2026-03-29-agent-memory-benchmark-anchor-check.md) — 评估 `05-evaluation.md` 的 benchmark 主锚点
- [2026-03-29-evermemos-systems-note.md](2026-03-29-evermemos-systems-note.md) — EverMemOS 系统观察
- [2026-03-29-magma-mirix-systems-note.md](2026-03-29-magma-mirix-systems-note.md) — Magma / Mirix 系统观察
- [2026-03-29-worldmm-frontiers-note.md](2026-03-29-worldmm-frontiers-note.md) — WorldMM 与前沿方向观察

### 2026-03-28：方向映射与闭环笔记

- [2026-03-28-agent-memory-rag-idea-mapping.md](2026-03-28-agent-memory-rag-idea-mapping.md) — Agentic Memory 与 Vectorless RAG 的可借鉴点映射
- [2026-03-28-frontiers-external-materials-evaluation.md](2026-03-28-frontiers-external-materials-evaluation.md) — 前沿外部材料的筛选与判断

### 2026-03-27：问题排序与方法栈

- [2026-03-27-harness-method-stack.md](2026-03-27-harness-method-stack.md) — harness 与方法栈的对应关系
- [2026-03-27-memory-lifecycle-rq-ranking.md](2026-03-27-memory-lifecycle-rq-ranking.md) — Agent Memory 研究问题排序与关系

## 升级路径

`docs/ideas/` 不是正式研究结论层，而是前置孵化层。默认先轻量记录，再按成熟度升级：

1. 如果已经形成明确研究问题、范围、非目标和 success criteria，升级到 `docs/plans/` 下的 `research-brief`。
2. 如果已经整理出支持/反对证据、代表引用、争议点与缺口，升级到 `docs/plans/` 下的 `evidence-map`。
3. 如果已经形成需要落到 `src/`、工具链或评测逻辑的稳定判断，升级到 `docs/architecture/` 或对应 `experiment-spec`。
4. 如果只是对 survey 与实现关系的候选映射、待确认论点或局部工程启发，先保留在 `docs/ideas/`，确认后再写入 `docs/survey/survey-map.md` 或正式研究工件。

## 使用边界

- 不要把 `docs/ideas/` 当作长期的正式结论仓库。
- 如果内容已经形成明确研究问题、证据地图、实验规格或可稳定复用的判断，应升级到 `docs/plans/` 或 `docs/architecture/`，而不是继续停留在 ideas。
- “最小实现是否支撑 survey” 的稳定映射，优先回写到 `docs/survey/survey-map.md`。
- blog / 外部材料的纳入边界判断，优先遵循 `docs/method/blog-survey-calibration-template.md`。
- 方法层自我设计、skill 设计或支线 case 若暂未进入正式研究链路，也优先放在 `docs/ideas/` 或后续归档，而不是直接进入 `docs/plans/`。
