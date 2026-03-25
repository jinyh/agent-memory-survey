# AgentOrchestra: Orchestrating Multi-Agent Intelligence with TEA Protocol

> arXiv:2506.12508v5 | Skywork AI & NTU | 2026

## 核心贡献

1. **TEA Protocol**: 统一 Tool-Environment-Agent 的协议抽象，支持生命周期管理和版本控制
2. **AgentOrchestra**: 基于 TEA 的层次化多智能体框架，中央规划 Agent + 专业子 Agent
3. **自进化模块**: TextGrad + Self-reflection 闭环优化 Agent 组件

## 记忆相关设计

### Memory Manager（六大基础管理器之一）
- Session-based 持久化：记录执行轨迹和可复用洞察
- 并发控制：多 Agent 同时访问记忆时的一致性保证

### Version Manager
- 维护所有组件（prompt/tool/agent/environment/memory code）的演化历史
- 优化后的组件自动注册为新版本

### Self-Evolution Module
- 将 Agent 组件包装为可进化变量
- TextGrad: 基于梯度的文本优化
- Self-reflection: 符号化的自我评估和策略调整

### Agent 设计原则中的记忆
- 六核心组件: Agent, Environment, Model, **Memory**, Observation, Action
- 感知-解释-行动循环: 感知观察 → 从**记忆**检索上下文 → 通过模型推理 → 执行行动 → 结果记录回**记忆**

## 协议转换与记忆
- A2T (Agent→Tool): Agent 的能力和推理封装为工具接口
- T2A (Tool→Agent): 工具映射为 Agent 的目标驱动动作
- 六种转换支持组件间动态角色切换

## 实验结果
- GAIA: 89.04% (SOTA)
- SimpleQA: 95.3%
- HLE: 37.46%

## 与记忆研究的关联
- **系统层面**: TEA 提供了记忆管理的协议标准化框架
- **版本追踪**: 记忆演化的可追溯性
- **多 Agent 记忆**: 通过 ACP 和 session 管理实现 Agent 间上下文共享
