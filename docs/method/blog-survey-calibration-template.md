# 非论文外部材料 ↔ Survey 对照分析模板

> v1.1.0 | 2026-03-29

这份模板用于处理一种特定任务：**输入一份非论文外部材料，输出它与当前 survey 主框架的对齐、边界、风险和推荐落点。**

适用于：技术 Blog、项目介绍页、vendor engineering post、X thread、工程经验总结页、release note、GitHub project / open-source implementation、benchmark / eval repo。
不适用于：论文 PDF / arXiv / 正式 paper（优先走 `survey-evidence-mapper`）、泛化 literature review、实现规划或仅做内容摘要的场景。

## 最小分类规则

非论文外部输入默认先收敛为以下几类角色，再决定是否写入正式文档：

- `工程补充证据`：如 blog、engineering post、release note，用于补充工程实践、产品化取舍、benchmark 争议与运维经验。
- `工程参照`：如 GitHub project、open-source implementation，用于 `systems baseline`、`implementation inspiration`、`evaluation reference`。
- `评测参照`：如 benchmark、eval repo、leaderboard implementation，用于补 benchmark 口径、case 组织和评测基线。
- `线索 / 候选`：如 DeepResearch 派生线索、尚未确认价值的外部材料，只保留为待摄取候选。
- `暂不纳入`：相关度不足、风险偏高或尚无稳定落点的材料。

默认规则：

- `paper` 仍是主研究证据，不由本模板提升替代。
- GitHub project 默认归为 `工程参照`，不直接替代 `paper` 成为主研究证据。
- 所有非论文外部输入都必须先回答两件事：它属于哪一类；它应该落到哪一层。

## 使用原则

1. **先守住 survey 主框架**
   - 先按当前 survey 的 lifecycle / chapter 组织问题，不能先跟着外部材料自身的分类走。

2. **非论文外部输入默认降级处理**
   - 除非有非常明确的理由，否则这类材料不应被提升为主证据；其中 Blog 默认只做工程补充。

3. **必须先定边界，再写优点**
   - 任何分析都必须明确：它支撑什么、只弱补强什么、不支撑什么。

4. **不能让非论文外部输入改写主论点**
   - 这类材料可以帮助解释、补充、启发，但不能直接替代 survey 现有的 anchor judgment；其中 Blog 仍默认按工程补充处理。

5. **优先判断落点，再判断是否写入**
   - 先决定它更适合进 `docs/ideas/`、survey 某章的工程补充位、`blogs-index`，还是暂不纳入。

## 固定输出模板

### 1. 快速判断

- **是否值得借鉴**：是 / 否 / 暂缓
- **推荐角色**：`systems baseline` / `engineering supplement` / `implementation inspiration` / `defer`
- **推荐落点（可多选，但需标主次）**：`docs/ideas/` / `docs/survey/*.md` 工程补充位 / `docs/references/blogs-index.md` / 暂不纳入

### 2. 与 Survey 的对齐

- **主要对应章节**：`01-framework` / `02-formation` / `03-evolution` / `04-retrieval` / `05-evaluation` / `06-systems-and-engineering` / `07-frontiers`
- **主要对应 lifecycle**：`formation` / `evolution` / `retrieval` / `evaluation` / `systems` / `frontiers`
- **它补强的现有判断**：
- **它是否只是解释已有判断**：是 / 否
- **如果有张力，优先保留的主框架**：

### 3. 边界

- **支撑**：
- **补强但不主导**：
- **不支撑**：

这一节是必填项，且应先于“可借鉴点”填写。

### 4. 可借鉴点

只保留 2-4 条结构性启发，优先写：

- systems / control plane 启发
- representation / object boundary 启发
- evaluation / benchmark 口径启发
- engineering implementation 启发

避免写成泛摘要。

### 5. 防带偏提醒

按以下最小格式写：

- **风险类型**：`marketing bias` / `benchmark bias` / `product framing risk` / `retrieval-centric overreach` / `demo → general conclusion`
- **触发证据**：
- **影响范围**：

如果不存在明显风险，也应写“未见强风险，但仍按工程补充处理”。

### 6. 建议动作

从以下动作中选择，并标主次：

1. 记入 `docs/ideas/`
2. 最小补充到 survey 某章工程补充段
3. 只补 `blogs-index` 或索引层
4. 暂缓，不写入正式文档
## 角色判定表

| 角色 | 含义 | 何时使用 |
| --- | --- | --- |
| `systems baseline` | 代表某类工程起步形态或最小实现范式 | 非论文外部输入更适合说明工程直觉、baseline 或 MVP 结构，但不足以承担主论点 |
| `engineering supplement` | 对现有 survey 判断提供工程补充说明 | 这类材料能帮助解释已有判断的工程意义，但不改变主框架 |
| `implementation inspiration` | 对代码/原型/接口设计有局部启发 | 这类材料对实现细节或接口组织有参考价值，但研究支撑弱 |
| `defer` | 暂不纳入 | 相关度不够，或风险高于收益 |

快速区分规则：
- 更偏“说明第一代工程起步形态” → `systems baseline`
- 更偏“补一句工程含义，但主判断已在 survey 中成立” → `engineering supplement`
- 更偏“对原型/接口/实现有局部启发” → `implementation inspiration`
- 如果很难稳定归类，优先降级处理，而不是抬高证据定位 |

## 误用速查

- **把非论文外部输入当主证据**：直接把这类材料的结论上升成 chapter 主判断，或用它替代 paper / 稳定 anchor
- **把产品叙事写成一般性规律**：把 demo / vendor post 误写成普遍趋势，未说明适用范围
- **只写优点，不写边界**：只有“可借鉴点”，没有“不支撑什么”与风险提醒
- **被 retrieval-centric 叙事带偏**：把 memory 收缩成 retrieval / vector store / recall loop，忽略 formation、evolution、evaluation、governance

## 最小示例

```md
## 快速判断
- 是否值得借鉴：是
- 推荐角色：systems baseline
- 推荐落点（主）：docs/survey/06-systems-and-engineering.md 工程补充位
- 推荐落点（次）：docs/ideas/

## 与 Survey 的对齐
- 主要对应章节：06-systems-and-engineering
- 主要对应 lifecycle：retrieval / systems
- 它补强的现有判断：第一代工程系统常把 memory 理解为 retrieval-enhanced persistence
- 它是否只是解释已有判断：是
- 如果有张力，优先保留的主框架：survey 的 lifecycle 主线

## 边界
- 支撑：工程起步形态、MVP 结构、最小 baseline
- 补强但不主导：systems 章节中的工程补充判断
- 不支撑：memory lifecycle 全貌、governance 成熟度、主证据地位

## 可借鉴点
1. 可用来解释 retrieval-centric MVP 为什么对工程团队有吸引力
2. 可作为 systems baseline，而不是成熟 architecture

## 防带偏提醒
- 风险类型：retrieval-centric overreach
- 触发证据：全文将 memory loop 压缩为 recall/write 闭环
- 影响范围：容易弱化 formation、evolution、evaluation 的独立地位

## 建议动作
1. （主）最小补充到 systems 章节工程补充位
2. （次）写入 docs/ideas
```

## 反例示例（应 defer）

```md
## 快速判断
- 是否值得借鉴：暂缓
- 推荐角色：defer
- 推荐落点（主）：暂不纳入

## 与 Survey 的对齐
- 主要对应章节：无稳定主落点
- 主要对应 lifecycle：无
- 它补强的现有判断：较弱
- 它是否只是解释已有判断：否
- 如果有张力，优先保留的主框架：survey 现有章节锚点

## 边界
- 支撑：局部产品经验
- 补强但不主导：很弱
- 不支撑：一般性研究趋势、通用 memory 结论、评测口径判断

## 可借鉴点
1. 可作为后续线索，但不宜直接写入正式文档

## 防带偏提醒
- 风险类型：product framing risk
- 触发证据：核心结论建立在单一产品叙事上
- 影响范围：容易把场景特化经验误写成普遍规律

## 建议动作
1. （主）暂缓，不写入正式文档
2. （次）如确有需要，仅在 blogs-index 保留索引
```

## 相关规则

使用这份模板时，仍需遵守：`docs/method/README.md`、`docs/method/gates.md`、`docs/method/roles.md`、`docs/method/traceability.md`、`docs/survey/README.md`。
