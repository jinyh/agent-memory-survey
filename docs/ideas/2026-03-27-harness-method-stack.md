# Harness engineering 与研究方法栈

## 背景

刚才讨论了 `ref/blog/` 里关于 harness engineering 和 agentic thinking 的新内容，并对照了本项目现有的研究版 BMAD 方法层、gates、traceability 和 workflow。

## 核心想法

本项目可以借鉴 harness engineering，但只借 **约束与反馈**，不借 **自治与重自动化**。

### 可以借鉴的部分

- 把 `research-brief -> evidence-map -> architecture-decision -> experiment-spec -> evaluation-report -> survey-update-note` 继续作为主链路
- 在实验与评测中强化可复现性
- 为关键工件增加轻量追踪字段
- 为失败场景建立统一证据包
- 让 Gate A / B / C 更像明确的验证门，而不是形式检查

### 不建议直接搬来的部分

- 自治执行流
- 默认多 agent / worktree 编排
- 浏览器 / CDP / UI 调试 harness
- 把方法层做成工程交付流水线

## 结论

对 AgentResearch 来说，harness engineering 更适合做 **实验与验证增强层**，而不是主框架。

## 后续动作

如果后面要继续推进，优先考虑：

1. 给 `experiment-spec` 和 `evaluation-report` 补最小运行契约
2. 给 `traceability` 增加轻量机械检查
3. 为评测产物定义统一 failure evidence bundle
