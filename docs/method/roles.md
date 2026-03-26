# 研究角色

> v1.0.0 | 2026-03-26

本项目的方法层不沿用产品开发里的 PM、Dev、QA 角色，而是按研究闭环重新定义职责。

每个角色都用三段式描述：

- 输入工件
- 输出工件
- 不负责什么

## Research Lead

输入工件：

- 研究主题
- 现有 survey 或历史计划

输出工件：

- `research-brief`
- 阶段推进决定

不负责什么：

- 不直接代替证据分析
- 不跳过架构决策直接下实现结论

## Evidence Analyst

输入工件：

- `research-brief`
- `ref/` 中的 paper/blog/DeepResearch
- `docs/references*`

输出工件：

- `evidence-map`
- 代表引用与证据边界说明

不负责什么：

- 不把工程叙事包装成论文证据
- 不直接定义原型架构

## Architect

输入工件：

- `research-brief`
- `evidence-map`
- 相关 survey 判断

输出工件：

- `architecture-decision`
- 风险与替代方案

不负责什么：

- 不直接写实现代码
- 不在证据不足时强行冻结设计

## Experiment Engineer

输入工件：

- `architecture-decision`
- 相关原型代码和测试约束

输出工件：

- `experiment-spec`
- `evaluation-report`
- 相关实现与测试产物

不负责什么：

- 不替代架构评审
- 不把一次实验结果上升为通用研究结论

## Reviewer

输入工件：

- 全部关键工件
- 相关 survey/architecture/plan 文档

输出工件：

- 一致性审查意见
- 缺口、冲突和风险清单

不负责什么：

- 不替代作者重写全部文档
- 不在没有证据的情况下给出“通过”判断

## Writer

输入工件：

- `evidence-map`
- `evaluation-report`
- survey 相关章节

输出工件：

- `survey-update-note`
- 更新后的研究叙述

不负责什么：

- 不新增未经审查的研究判断
- 不省略边界和适用条件

## 默认交接关系

- `Research Lead -> Evidence Analyst`
- `Evidence Analyst -> Architect`
- `Architect -> Experiment Engineer`
- `Experiment Engineer -> Writer`
- `Reviewer` 可以在 Gate A / B / C 插入审查
