# Architect Skill 设计文档

> v1.0.0 | 2026-03-26 | 状态：Accepted

## 背景

本项目是 Codex + Claude Code 双引擎研究项目，包含三类产物：代码原型（`src/memory/`）、研究综述（`docs/survey/`）、资料工具链（`src/references/`）。在 memory-core-v1 的开发中，Codex 产出的实施计划存在三处设计缺陷（FusionConfig 形式、graph 边多态序列化、评测 ground truth 缺失），这些问题本应在架构评审阶段被捕获。

借鉴 BMAD-METHOD 的架构师角色（Winston），为本项目创建一个轻量化的架构师 skill，在重大改动前提供结构化的架构评审。

## 设计决策

### Skill 定位

- 项目级 skill，仅服务于 AgentResearch 项目
- 用户通过 `/architect [主题]` 手动触发
- 在 fork 上下文中运行，不污染主对话
- 只做评审和决策，不写实现代码

### 4 步工作流

**Step 1: 上下文扫描**
- 自动读取 `AGENTS.md` 获取项目约定
- 用 Explore agent 扫描主题相关的代码/文档
- 输出影响面摘要（涉及文件列表 + 当前状态简述）

**Step 2: 架构决策**
- 按三个领域分别评估：
  - 代码原型（`src/memory/`, `src/references/`）：数据结构、接口设计、模块边界、依赖关系
  - 研究综述（`docs/survey/`）：章节组织、证据层级、引用规则一致性
  - 工具链（`src/references/`, 索引生成）：流程设计、输入输出契约
- 每个决策包含：决策内容、理由、替代方案、选择依据
- 决策分类：关键（阻塞实施）/ 重要（影响架构）/ 可延迟（MVP 后）
- 每个领域决策后暂停确认

**Step 3: 风险与依赖分析**
- 跨领域影响（如 memory 接口变更 → 评测脚本 → survey 描述）
- 技术风险（性能、依赖兼容性、数据迁移）
- 遗漏检查（对照 AGENTS.md 约定）

**Step 4: 输出架构决策文档**
- 写入 `docs/architecture/YYYY-MM-DD-<topic>.md`

### 交互模式

- 语调：冷静、务实，每个建议基于真实权衡
- 如果需求本身有问题，在 Step 2 前就提出挑战
- 评审完成后建议进入 Plan Mode，但不自动触发

### 输出文档结构

```markdown
# <主题> 架构决策

> 日期 | 状态：Proposed / Accepted / Superseded

## 背景
## 影响面
## 决策
### 关键决策
### 重要决策
### 可延迟决策
## 风险与依赖
### 跨领域影响
### 技术风险
## 替代方案
```

### 与现有流程的衔接

`/architect` → 架构决策文档 → Plan Mode → 实施计划 → 执行

## 替代方案

- **方案 B（2 步最小流程）**：未采用，因为缺少风险分析，容易漏掉跨领域影响
- **方案 C（6 步完整 BMAD）**：未采用，对研究项目的小改动来说太重

## 文件清单

- `.claude/skills/architect/SKILL.md` — skill 入口文件
