# BMAD-METHOD 与 Harness Engineering 差距清单

## 对照基准

本文基于 **OpenAI 于 2026-02-11 发布的《Harness engineering: leveraging Codex in an agent-first world》**，对当前 `BMAD-METHOD` 仓库进行对照分析。

判断口径不是“是否有 AI 工作流”，而是：该项目是否已经把 **仓库、运行环境、约束、验证、观测、评审、修复与交付** 组织成一个可供 agent 稳定执行的工程 harness。

结论先行：

- **BMAD 当前更像高结构化的 context engineering + workflow orchestration 框架。**
- **它已经吸收了部分 Harness Engineering 思想，但整体还不是完整的 Harness Engineering。**

---

## P0：核心方法论差距

### 1. 主轴仍是文档流，不是执行环境流

BMAD 的核心是：

- `PRD -> Architecture -> Story -> Dev/Review`
- 通过阶段化工件持续给后续 agent 提供上下文

这套设计非常强调“知道要做什么、为什么这样做”，但它的中心仍然是 **文档工件的流转**。Harness Engineering 的中心则更偏向 **可执行环境本身**：agent 如何在真实可运行、可调试、可验证、可回放的环境中工作。

仓库证据：

- `docs/reference/workflow-map.md` 明确将 BMM 定义为 `context engineering and planning`，并强调四阶段上下文构建。
- `docs/reference/workflow-map.md` 反复强调“每个文档成为下一个阶段的上下文”。

### 2. `project-context.md` 是软约束，不是硬约束

BMAD 提供了 `project-context.md`，并把它定位为项目的“constitution”，用于统一 agent 的实现规则和偏好。这是有价值的，但它本质上仍然是：

- 给 agent 阅读的规则文档
- 帮助 agent 减少自由发挥
- 提高跨工作流的一致性

Harness Engineering 更进一步，通常会把这些约束变成 **硬性、可执行、机械校验的规则**，例如：

- 依赖方向检查
- 模块边界检查
- 禁止调用某些层的 lint 规则
- 架构不变量测试
- 风格或 taste 约束的自动检查

当前 BMAD 主要还是“文字指导”，而不是“失败即阻断”的工程约束层。

仓库证据：

- `docs/explanation/project-context.md` 强调该文件用于记录模式、约束、偏好，并在工作流中自动加载。
- 但没有把这些规则系统性转成 structural lint / policy enforcement。

### 3. 缺少“环境即 harness”的一等建模

当前仓库没有把以下能力作为方法论核心来定义：

- 每个任务默认在隔离工作区或 worktree 中运行
- 本地应用必须可启动、可访问、可重现
- 浏览器/CDP 为 agent 默认可用
- 日志、指标、trace 默认可查
- 调试证据可自动收集并反馈给后续 agent

这意味着 BMAD 更像“告诉 agent 应该怎么做”，而不是“把环境改造成 agent 容易做对事的系统”。

---

## P1：自治执行与可观测性差距

### 4. Phase 4 仍不是完整自动化闭环

仓库文档在实现阶段仍写着：

- `Coming soon, full phase 4 automation!`

这本身就说明，BMAD 的实现阶段自动化还没有成为默认完成态。Harness Engineering 的重点恰恰是把实现、验证、修复、再验证这条链路尽量自动化，并将人类从频繁 checkpoint 中抽离出来。

仓库证据：

- `docs/reference/workflow-map.md` 对 Phase 4 的描述仍然保留“完整自动化尚未来到”的表述。

### 5. 人工 checkpoint 仍然较重

`Quick Dev` 已经在减少人工往返，但仍保留较强的人类关卡，例如：

- 意图澄清
- spec approval
- review 后多处 HALT
- 若有分歧则等待用户明确决策

这对质量是好的，但从 Harness Engineering 视角看，说明系统默认仍然是：

- 人类负责关键推进
- agent 负责局部执行与反馈

而不是：

- agent 自主完成构建、验证、审查、修复
- 只在不可判定的真实决策点升级给人

仓库证据：

- `docs/explanation/quick-dev.md` 明确把 `Spec approval` 和 `Review of the final product` 作为高价值人工时刻。
- `src/bmm-skills/4-implementation/bmad-quick-dev/step-02-plan.md` 要求在 checkpoint 处等待人工批准。
- `src/bmm-skills/4-implementation/bmad-code-review/steps/step-04-present.md` 在 patch/defer/decision 等环节多次 HALT 等待用户选择。

### 6. 缺少系统级“失败后自动再尝试”编排

BMAD 已经有很好的 review triage 思路，尤其是：

- `intent_gap`
- `bad_spec`
- `patch`
- `defer`
- `reject`

这说明它已经意识到“不要把所有失败都当成代码补丁问题”。但它还没有把以下能力变成默认工程机制：

- build 失败后自动定位并修复
- flaky test 自动重跑与隔离
- 前端问题自动抓取控制台、网络、截图后再修
- 集成测试失败后自动分析环境依赖
- CI 失败后自动回读日志并二次提交

也就是说，它有 **失败分层认知**，但还没有完整的 **失败闭环执行系统**。

### 7. 缺少运行时可观测性接入

仓库没有把以下内容作为 agent 默认工作界面的一部分：

- 应用日志
- 业务/系统指标
- 链路追踪
- 查询语言或统一检索入口
- 故障上下文自动采集

这使得 agent 的主要输入仍然偏向：

- 文档
- 代码
- diff
- 测试结果

而不是：

- 代码 + 运行时事实

Harness Engineering 里，后者是关键差异。

### 8. 缺少浏览器级调试 harness

当前仓库没有把前端或全栈调试的浏览器能力纳入核心工作流，例如：

- DOM snapshot
- console log
- network trace
- screenshot
- video recording
- 可脚本化浏览器交互

如果没有这类能力，agent 在 UI 与端到端问题上的自主修复能力会明显受限。

### 9. 缺少失败证据归档机制

BMAD 会把 review 结果回写进 story/spec，这是流程层的追踪。但缺少更接近工程 harness 的失败证据包，例如：

- 基线 commit
- 实际执行命令
- 失败输出
- 环境信息
- 截图/录像
- 关键日志片段
- trace ID 或可重放链接

这会影响：

- 二次分析
- 人工接手
- 多 agent 接力
- 审计与复盘

---

## P2：架构约束、协作与交付闭环差距

### 10. 架构 ADR 主要用于指导，不足以强制执行

BMAD 很强调架构在多 agent 实现中的共享上下文作用，这点是对的。它通过 ADR、标准与约定来降低 agent 冲突，例如：

- API 风格统一
- 命名统一
- 状态管理统一
- 测试模式统一

但这些内容仍主要停留在“文档指导层”。Harness Engineering 会进一步要求：

- 这些规则能够被自动检查
- 违反规则时 agent 被立即阻断
- 架构不是建议，而是约束系统的一部分

仓库证据：

- `docs/explanation/preventing-agent-conflicts.md` 清楚描述了架构文档如何防冲突。
- 但未形成系统化的自动 enforcement 机制。

### 11. “taste” 没有工程化

BMAD 有 conventions、patterns、project context，也有 code review，但还没有把“工程 taste”系统化成一组默认可执行工件，比如：

- golden examples
- forbidden patterns
- preferred abstractions
- structural snapshots
- review oracle

这意味着很多“风格与质量”的部分，仍然要靠：

- 文档描述
- agent 理解
- reviewer 主观判断

而不是规则引擎与样例驱动。

### 12. 对 repo-specific invariants 的自动抽取仍偏文档化

`bmad-generate-project-context` 能从架构或代码库中提炼约定，这很有价值。但目前它产出的重点仍然是：

- 为 agent 生成更好的上下文文件
- 帮助后续实现更贴合现有项目

它没有进一步把这些抽取结果直接转成：

- lint 配置
- 边界测试
- policy file
- CI gate

所以它更像上下文蒸馏器，而不是不变量编译器。

### 13. 没有把 worktree / branch isolation 作为默认作业模型

`Quick Dev` 会做 version control sanity check，也会基于 diff 进行 review，这说明它理解版本控制的重要性。但它没有明确把下面这套模式做成默认方法：

- 每个任务在隔离 worktree 中执行
- review 基于隔离 diff
- 回退只影响当前任务空间
- 多 agent 并行彼此不污染

这会限制并发安全性与可恢复性。

仓库证据：

- `src/bmm-skills/4-implementation/bmad-quick-dev/step-01-clarify-and-route.md` 包含工作树/分支合理性检查，但不是默认隔离执行模型。

### 14. 多 agent 协作更像讨论和评审，而不是生产流水线

BMAD 已经有：

- `party-mode` 进行多角色讨论
- `code-review` 做多 reviewer 并行评审
- `Quick Dev` 在某些环节支持 subagent

但还缺少明确的生产型 agent 拓扑与职责边界，例如：

- planner
- implementer
- verifier
- runtime debugger
- release/merge agent

也缺少这些角色之间的稳定交接协议。当前多 agent 更像“能力插件”，而不是完整工程流水线。

### 15. PR / merge / CI 不是方法主轴

仓库里当然提到 PR、code review、测试与交付建议，但它们更多像：

- 工作流的后继动作
- 用户可选的推进路径

而不是方法核心骨架。Harness Engineering 更倾向把以下过程视为主路径：

- 任务开始
- agent 实现
- 自动验证
- PR 生成
- review 修复
- 合并
- 部署验证

BMAD 目前还没有把这一整条链路变成主心骨。

### 16. 缺少“可部署系统”导向的默认检查

BMAD 很擅长把需求、架构、故事、实现组织起来，也要求测试与 review。但它没有默认纳入更接近线上系统的环节，例如：

- deployment smoke checks
- staging verification
- rollout checklist
- rollback awareness
- release gates

这让它更像开发方法，而不是完整交付 harness。

---

## 已经接近 Harness Engineering 的部分

尽管差距明显，BMAD 里已经有几块非常接近 Harness Engineering：

### 1. `Quick Dev` 的意图压缩与规格冻结

`Quick Dev` 明确要求：

- 先把用户意图压缩成单一、明确目标
- 生成 spec
- 经人类批准后冻结关键部分
- 再交给 agent 长时间执行

这与 Harness Engineering 中“工程师负责清晰表达意图与边界”的思想高度一致。

### 2. 无上下文 reviewer 设计

`Quick Dev` 和 `bmad-code-review` 都要求 reviewer subagent 尽量不带原始会话上下文，避免锚定偏差。这是很接近 Harness Engineering 的一项成熟做法。

### 3. review triage 按失败层级归因

`intent_gap / bad_spec / patch / defer / reject` 这一设计非常接近 Harness Engineering 的核心思想：

- 错不一定在代码层
- 失败必须回到真正出错的层级去修
- 不要用补丁掩盖规格问题或意图问题

### 4. story 驱动下的严格完成门槛

`dev-story` 工作流对完成定义、测试、回归、状态更新和 review follow-up 都有严格要求，这说明 BMAD 对“交付完整性”的要求是认真的，而不是只要代码能跑就算结束。

---

## 总结

一句话判断：

**BMAD 当前更像“高结构化的 context engineering 与工作流编排框架”，而不是“把环境、约束、观测、验证与交付统一组织起来的 Harness Engineering 系统”。**

它和 Harness Engineering 的关系不是“完全无关”，而是：

- 在意图压缩、规格冻结、分层纠错、agent review 方面，已经明显靠近
- 但在环境建模、可观测性、机械化约束、隔离执行、交付闭环方面，仍有系统性差距

如果要把 BMAD 进一步对齐 Harness Engineering，优先方向不会是再加更多 PRD 或角色流程，而会是：

- 把运行环境纳入方法核心
- 把 project context 编译成硬约束
- 把验证与失败修复做成默认闭环
- 把多 agent 协作升级为稳定生产流水线

---

## 参考

### 外部参考

- OpenAI, *Harness engineering: leveraging Codex in an agent-first world*  
  <https://openai.com/index/harness-engineering/>

### 仓库内关键文件

- `docs/reference/workflow-map.md`
- `docs/explanation/project-context.md`
- `docs/explanation/quick-dev.md`
- `docs/explanation/preventing-agent-conflicts.md`
- `src/bmm-skills/4-implementation/bmad-quick-dev/step-01-clarify-and-route.md`
- `src/bmm-skills/4-implementation/bmad-quick-dev/step-02-plan.md`
- `src/bmm-skills/4-implementation/bmad-quick-dev/step-04-review.md`
- `src/bmm-skills/4-implementation/bmad-code-review/steps/step-02-review.md`
- `src/bmm-skills/4-implementation/bmad-code-review/steps/step-03-triage.md`
- `src/bmm-skills/4-implementation/bmad-dev-story/workflow.md`
