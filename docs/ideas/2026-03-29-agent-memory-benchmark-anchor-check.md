# Agent Memory Benchmark Anchor Check

## 背景
当前 `05-evaluation.md` 已经把 Agent Memory 评测拆成 retrieval hit、memory-in-use、长期管理能力与治理/成本四层。
这份笔记用于确认三个近年的 benchmark 是否应该继续作为章节主锚点，还是只保留为补充证据：
- MemoryAgentBench
- MemoryArena
- AMA-Bench

## 核心判断
### MemoryAgentBench
- 角色：主证据
- 最强借鉴点：把评测从长文档 recall 推进到 `test-time learning / selective forgetting / long-range understanding`
- 适合支撑的论点：
  - benchmark 必须拆层看
  - retrieval 不能代表 memory 全貌
  - evolution 至少需要行为侧信号
- 不能支撑的论点：
  - formation 已被独立测量
  - evolution 中间状态已被白盒测量
- 建议：继续作为 `05-evaluation` 主锚点，同时作为 `03-evolution` 的弱旁证

### MemoryArena
- 角色：主证据
- 最强借鉴点：`interdependent multi-session agentic tasks`
- 适合支撑的论点：
  - memory-in-use 不是单轮 QA
  - 评测对象应包含多 session 的持续约束
- 不能支撑的论点：
  - 写入质量可被独立归因
  - 删除 / 审计 / 权限治理已覆盖
- 建议：继续作为 `05-evaluation` 的 multi-session 主锚点

### AMA-Bench
- 角色：主证据
- 最强借鉴点：`agent trajectory + tool use`
- 适合支撑的论点：
  - 真实 agentic task 里的 memory 不是静态回忆
  - 轨迹长度和工具使用会暴露记忆系统的因果缺口
- 不能支撑的论点：
  - lifecycle 全链路已覆盖
  - systems / governance 问题已经解决
- 建议：继续作为 `05-evaluation` 的 trajectory 主锚点

## 结论
- 这三篇都应保留在 `05-evaluation.md` 里。
- 其中 `MemoryAgentBench` 可以作为 evolution 的行为侧旁证，但不升级为 evolution 主证据。
- 这组 benchmark 的共同作用，是把“评测什么”从 retrieval hit 推向 memory policy / memory-in-use / agent trajectory。
