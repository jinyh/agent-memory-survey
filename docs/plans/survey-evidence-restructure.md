# Survey 证据重构计划

> 记录时间：2026-03-26
>
> 用途：供后续 session 直接执行，解决 survey 中关键概念缺引用、2026 重要进展缺失、主次证据层级混乱的问题。

## Summary

本轮不是简单“补引用”，而是重构 survey 的证据层级，解决三个根问题：

1. 关键概念没有显式代表引用，导致正文提到不等于真正纳入主线。
2. 2026 年几项非常重要的新进展没有进入主线，尤其是评测与记忆表示两条线。
3. 现有部分内容权重过高，混淆了 `paper 主证据` 与 `engineering/frontier 补充`。

实现目标是把 survey 改成三层证据结构：

- `主证据`：定义关键概念、支撑章节主判断
- `次级证据`：补充工程实现、系统取舍或边界讨论
- `线索/前沿`：提示方向，但不承担主判断

## Key Changes

### 1. 规范层：把“关键概念必须有主证据”写成硬规则

更新 `AGENTS.md`：

- `docs/survey/` 中关键概念、方法范式、系统路线、评测对象、组织性判断，必须绑定明确代表引用。
- 代表引用优先 `paper`；`blog` 只能做工程补充；`DeepResearch` 只能做线索。
- 如果正文出现缩写或系统名并承担论证功能，首次必须写出明确作品名，不允许只用泛称或缩写承担主判断。
- 更新共享写作规则时，必须同步检查 `CLAUDE.md`。

同步更新 `CLAUDE.md`：

- 保持入口文档定位。
- 增加一句硬约束：编辑 survey 时必须遵守 `AGENTS.md` 的关键概念引用规则。
- 不复制细则，只保留同步提醒和单一真源声明。

### 2. Survey 结构层：每章补“关键概念与代表引用”

在 `01-07` 各章统一新增：

- `## 关键概念与代表引用`

每条概念统一包含：

- 概念名
- 本文使用语义
- 主代表引用
- 证据类型：`主证据 / 工程补充 / 前沿线索`
- 一句边界说明：该引用支撑什么，不支撑什么

这部分放在研究矩阵之后、正文主体之前，用来先定义概念，再进入论证。

### 3. 2026 重要进展纳入主线

以下条目必须升格为主线，不再只是可选补充：

- `Recursive Language Models`
  - 位置：`01-framework`、`04-retrieval`、`06-systems-and-engineering`
  - 作用：定义 `程序化 working memory / recursive retrieval`
  - 要求：不再只写 `RLM` 缩写，也不再和 `MSA` 混成一个概念桶
- `MemoryAgentBench`
  - 位置：`05-evaluation`
  - 作用：支撑评测维度从 retrieval hit 扩展到 `test-time learning / long-range understanding / selective forgetting`
- `MemoryArena`
  - 位置：`05-evaluation`
  - 作用：支撑 `multi-session agent-environment loop` 是比长对话 QA 更强的记忆评测对象
- `AMA-Bench`
  - 位置：`05-evaluation`
  - 作用：支撑 memory benchmark 从“对话历史问答”走向“agent trajectory + tool use”
- `Memora`
  - 位置：`02-formation`、`03-evolution`、`04-retrieval`
  - 作用：支撑“abstraction 与 specificity 平衡”这一条独立表示路线
- `MemSkill`
  - 位置：`02-formation` 或 `03-evolution`
  - 作用：补足 memory operation 可学习化，而非只有规则工程
- `BMAM`
  - 位置：`06-systems-and-engineering`
  - 作用：作为 brain-inspired memory architecture 的次级证据，不升为最核心主线

### 4. 现有内容降权与重排

以下内容保留，但从主证据降为次级证据或补充：

- `AgentOrchestra`
  - 从 `03-evolution` 主证据降为补充，避免把多 agent 协议误当作记忆演化主线
- `Elastic memory architecture`
  - 收缩到 `06-systems-and-engineering` 为主，在 `01/02/04` 中只作为工程补充，不再承担范式定义角色
- `Synapse`
  - 保留，但从 evolution 主锚点降为 episodic-semantic activation 的补充案例
- `TeleMem / MemOCR / M3-Agent / Think3D / GSMem / RenderMem`
  - 在 `07-frontiers` 中只保留 2 到 3 个主锚点，其余改成补充线索
  - 推荐主锚点：`TeleMem`、`Think3D`、`RenderMem`
- 泛称式表述
  - `工程治理材料`、`benchmark 比较文章`、`Letta 的 stateful agents 叙事` 这类泛称，不再作为主证据表述
  - 必须替换为具体作品名，或明确降级成背景说明

### 5. 各章节的具体重构方向

- `01-framework`
  - 新增关键概念锚点：生命周期框架、retrieval-centric、memory management、belief vs evidence、programmatic working memory
  - 提升 `Recursive Language Models`
  - 下调 `Elastic`
- `02-formation`
  - 新增关键概念锚点：extractive formation、active state、provenance、abstraction vs specificity
  - 引入 `Memora`，可选补 `MemSkill`
- `03-evolution`
  - 新增关键概念锚点：consolidation、version semantics、belief-aware update、forgetting
  - 主证据以 `Hindsight` 为核心，`Memora/MemSkill` 辅助
  - 下调 `AgentOrchestra`、`Synapse`
- `04-retrieval`
  - 新增关键概念锚点：hybrid retrieval、graph retrieval、agentic retrieval、recursive retrieval、sparse latent retrieval
  - 明确拆开 `RLM` 与 `MSA`
  - 引入 `Memora`
- `05-evaluation`
  - 新增关键概念锚点：retrieval hit、memory-in-use、multi-session loop、trajectory-based evaluation、selective forgetting
  - 主证据改为 `LoCoMo + LongMemEval + MemoryAgentBench + MemoryArena + AMA-Bench`
- `06-systems-and-engineering`
  - 新增关键概念锚点：memory service、memory OS、belief-aware architecture、programmatic working memory、native long-memory mechanism、control plane
  - 主线拆为：`Mem0/LangMem`、`Letta/MemGPT`、`Hindsight`、`RLM`、`MSA`
  - `BMAM` 作为补充
- `07-frontiers`
  - 新增关键概念锚点：multimodal memory、spatial memory、world state、auditability/deletion
  - 收缩前沿案例数量，避免“论文堆叠”
  - 只保留少数主锚点，其余作为延伸线索

### 6. README 联动

更新 `docs/survey/README.md`：

- 明确“研究矩阵”负责横向比较
- 明确“关键概念与代表引用”负责定义与追溯
- 在“按系统读”里把 `Recursive Language Models` 单独点出，不再只作为 `RLM / MSA`
- 在“使用方式”里增加一句：先看研究矩阵，再看关键概念与代表引用，再读正文论证

## Test Plan

更新 `tests/test_survey_docs.py`，增加以下约束：

- 每章必须包含 `## 关键概念与代表引用`
- 每章该区段必须出现至少一个 `主证据` 或至少一个 `paper`
- `AGENTS.md` 必须包含关键概念引用规则
- `CLAUDE.md` 必须包含同步提醒
- `01-framework`、`04-retrieval`、`06-systems-and-engineering` 中必须出现 `Recursive Language Models`
- `05-evaluation` 中必须出现 `MemoryAgentBench`、`MemoryArena`、`AMA-Bench`
- `02/03/04` 至少一章必须出现 `Memora`
- `03-evolution` 中 `AgentOrchestra` 不再作为核心证据区段的唯一或首要引用
- `07-frontiers` 中前沿主锚点数量受控，避免继续无限堆叠案例

执行验证：

- `uv run --active --extra dev pytest tests/test_survey_docs.py -q`
- `uv run --active --extra dev pytest tests/ -q`

## Assumptions

- 默认不引入脚注式参考文献系统，继续使用 markdown 内显式概念锚点。
- 默认不新建独立“概念总表”页，主结构仍采用章节内强绑定。
- 默认优先使用现有本地索引和本地资料；若仓库缺少 `MemoryAgentBench / MemoryArena / AMA-Bench / Memora / MemSkill / BMAM` 的本地索引条目，实施时应先补资料索引，再写入主文。
- 默认以“提升主证据、下调次级证据”为主，不做全文重写，不改当前生命周期章节结构。
