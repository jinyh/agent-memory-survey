# 用样本卡片看 `src/memory` 为什么已具备 formation → evolution → retrieval → evaluation 的最小闭环

## 这篇笔记在回答什么

这不是一篇“数据集综述”，也不是 `docs/survey/05-evaluation.md` 的缩写版。

它真正想回答的是两个更具体的问题：

1. 为什么很多 memory benchmark 看起来在测“长期记忆”，但单靠它们并不足以证明一个系统已经覆盖完整 lifecycle。
2. 为什么把这些 benchmark 样本和 `src/memory` 里的内部原型放在一起看时，当前项目可以更稳妥地说：它已经具备 `formation -> evolution -> retrieval -> evaluation` 的**最小闭环**。

> benchmark 能提供的是分阶段压力和外部行为证据；真正把 lifecycle 补成闭环的，还需要系统内部对白盒 formation / evolution 的原型化验证。

## 先把边界说清楚

这里有三个层次，不能混在一起：

- `src/memory/evaluation.py` 里的 `load_benchmark_cases()`：负责把外部数据集归一化成统一 benchmark case。
- `src/memory/manager.py`：提供真正串 lifecycle 的记忆操作接口。
- `src/memory/evaluation.py` 里的 formation / evolution / retrieval / roundtrip 原型评测：负责补上外部 benchmark 很难直接覆盖的白盒环节。

所以这些外部样本的作用，是帮助我们看清 retrieval、memory-in-use、formation 信号、evolution 信号分别长什么样；**不是说这些 benchmark 单独就构成了完整 lifecycle benchmark**。

## 闭环骨架

| 生命周期阶段 | 关键接口 | 作用 |
| --- | --- | --- |
| formation | `MemoryManager.remember()` | 决定什么信息被写入 store |
| evolution | `update_memory()` / `forget()` / `consolidate_episodic_to_semantic()` | 更新、删除、巩固已有记忆 |
| retrieval | `recall()` / `recall_with_trace()` | 从多个 store 检索并融合结果 |
| evaluation | `run_evaluation()` / `run_dataset_benchmark()` / `check_roundtrip()` | 用原型场景和 datasets case 检查行为 |

补一句实现细节：`recall()` 用的是 **rank 融合**，不是 raw score 直排；要解释为什么某条被召回，优先看 `recall_with_trace()`。

---

## 一、这些 benchmark 最稳的是 retrieval / evaluation 证据

先看最容易成立的一组：它们最擅长证明“已有历史能不能被正确找回来”，以及“在检索评测口径下系统表现如何”。

### 样本卡片 1：LoCoMo 基础检索样本

#### 样本内容（中文重述）
- 来源：`ref/datasets/locomo/locomo10.json`
- `sample_id`：`conv-26`
- 问题：**Caroline 是什么时候去 LGBTQ 支持小组的？**
- 答案：**2023 年 5 月 7 日**
- 证据位置：`D1:3`

证据附近对话可译为：
- Caroline：**我昨天去参加了一个 LGBTQ 支持小组，感觉特别有力量。**
- Melanie：**太棒了，发生了什么？有没有听到很受鼓舞的故事？**
- Caroline：**那些跨性别者的故事特别打动我，我真的很感激能得到这样的支持。**

#### 它对应闭环的哪一段
- 主要对应：**retrieval → evaluation**

#### 为什么它能说明问题
这张卡片最适合解释 benchmark case 是怎么进入系统的：
- `question` 会变成统一 case 的 `query`
- `evidence` 会被转成 `expected_ids`
- 对话 session 会被整理成 `documents`

换句话说，这条样本说明：`src/memory/evaluation.py` 已经能把真实对话历史归一化成可检索对象，然后再用 hit@k / MRR 去评测系统有没有把正确证据找回来。

#### 它不能说明什么
它不能说明 formation，也不能说明 evolution。因为这里默认“历史已经存在”，问题只是在问：**已有历史能不能被找回来。**

---

### 样本卡片 2：LoCoMo 高难度多证据样本

#### 样本内容（中文重述）
- 来源：`ref/datasets/locomo/locomo10.json`
- `sample_id`：`conv-26`
- 问题：**Caroline 以后可能会选择什么学习或职业方向？**
- 答案：**心理学、咨询相关认证**
- 证据位置：`D1:9`、`D1:11`

关键证据可译为：
- `D1:9`：Melanie：**Caroline，你在考虑哪类工作？有没有特别想走的方向？**
- `D1:11`：Melanie：**你一定会成为很好的咨询师，你的同理心和理解力会帮到很多人。**

#### 它对应闭环的哪一段
- 主要对应：**retrieval → evaluation**
- 比卡片 1 更强，因为它需要**多证据合并**

#### 为什么它能说明问题
这条样本比单证据 QA 更“硬”，因为答案不是一句原文直接抄出来，而是要把多个位置的线索合在一起：
- 一条在问未来方向
- 另一条在暗示咨询、同理心、帮助他人

这说明 retrieval 不是只会命中一条句子就够了，而是要把**多个相关片段一起捞出来**，后续回答才可能成立。

这和 `MemoryManager.recall()` 的多 store 检索逻辑是对齐的：系统真正需要的不是“命中一条最像的话”，而是“把足够支撑回答的记忆集合找回来”。

#### 它不能说明什么
它仍然主要是 retrieval 样本。它要求的是“从历史里综合线索”，不是“判断哪些线索应该被写入”或“冲突线索如何被更新”。

---

### 样本卡片 3：LongMemEval 跨 session 时序样本

#### 样本内容（中文重述）
- 来源：`ref/datasets/longmemeval-cleaned/longmemeval_oracle.json`
- `question_id`：`gpt4_2655b836`
- 类型：`temporal-reasoning`
- 问题：**我的新车第一次保养之后，最先出现的问题是什么？**
- 答案：**GPS 系统失灵**
- 相关 session：3 个

关键上下文可译为：
- 早期 session：**我 2 月 10 日买了一辆新的银色 Honda Civic，我想多用用车上的 GPS 功能。**
- 后续 session：**我 3 月 22 日发现 GPS 出问题了，只好把车开回经销商那里修，他们后来把整套系统都换掉了。**
- 还有一段 session：围绕 car detailing、wax、保养周期展开，造成干扰信息很多。

#### 它对应闭环的哪一段
- 主要对应：**retrieval → evaluation**
- 但比普通 QA 更强调**跨 session + 时序推理**

#### 为什么它能说明问题
这条样本硬在两点：
1. 关键事实分散在多个 session 里
2. 问题问的不是“有没有 GPS 问题”，而是“第一次保养之后最先出现的问题是什么”

也就是说，系统必须：
- 读回多段相关历史
- 建立时间顺序
- 排除无关噪音

这非常像真实 memory 系统的读取场景：不是当前对话就给你答案，而是得从多段历史中恢复事件链。

#### 它不能说明什么
它依旧主要是 retrieval 压力测试。它不能直接说明：系统当初为什么决定把“GPS 出问题”写入长期记忆，也不能说明后来如果又来了新信息，系统会不会正确更新。

### 这一组样本合起来说明什么
这三张卡片共同说明：外部 benchmark 在 **retrieval / evaluation** 上最稳，因为它们天然擅长给出：
- 明确 query
- 对应 evidence
- 可比较的 hit@k / MRR / 命中结果

但它们共同的前提也是：**历史已经在那里了。**

所以这组证据可以很强地说明“读出来没有”，却不能单独回答“当初该不该写进去”以及“后来该不该更新掉”。

---

## 二、再往前一步，它们开始触到 memory-in-use

第二组样本已经不只是“找证据回答问题”，而是开始逼系统在持续任务中把历史真的用起来。

### 样本卡片 4：AMA-Bench 轨迹回退样本

#### 样本内容（中文重述）
- 来源：`ref/datasets/AMA-bench/test/open_end_qa_set.jsonl`
- `episode_id`：`0`
- 任务：类似 Baba Is You 的规则操纵谜题
- 问题：**第 8 步之后的观察结果和第 6 步一样。是什么动作因果关系造成了这种“状态回退”？这说明 agent 的进展如何？**
- 标准答案要点：**后续动作抵消了前一步动作，导致状态回到之前的位置，说明这两步没有净进展。**

核对后的关键步骤：
- 第 6 步动作：向左
- 第 7 步动作：向左
- 第 8 步动作：向下
- 第 9 步动作：向上
- 第 9 步观察重新回到第 6 步附近的状态

#### 它对应闭环的哪一段
- 主要对应：**retrieval → evaluation**
- 更具体地说，是 **memory-in-use**

#### 为什么它能说明问题
这里的“历史”已经不是聊天记录，而是 agent 自己的轨迹：
- 做了什么动作
- 看到了什么 observation
- 环境状态是否真的推进

这说明 memory 的作用不只是“回答问题时引用旧句子”，而是让系统在任务执行中判断：
- 我是不是在原地打转？
- 这两步是不是互相抵消了？
- 下一步应该换策略吗？

这就是 memory-in-use 的典型形态。

#### 它不能说明什么
这条样本仍然不能单独证明 formation 或 evolution。它只是很强地说明：**如果系统没有把过去轨迹记住并在当前推理里用出来，就根本看不出自己是在回退。**

---

### 样本卡片 5：MemoryArena 多约束 itinerary 样本

#### 样本内容（中文重述）
- 来源：`ref/datasets/MemoryArena/group_travel_planner/data.jsonl`
- `id`：`1`
- 用户约束可译为：
  - **第 2 天早餐，希望是甜点 / 烘焙类，人均价格在指定区间。**
  - **第 2 天晚餐，希望是墨西哥餐，价格在指定区间。**
  - **第 3 天午餐，希望价格在指定区间，评分也落在给定区间。**
  - **第 3 天晚餐，希望是甜点 + 法餐组合，价格也受限。**

样本中给出的候选 itinerary 片段包括：
- 第 2 天早餐：`Mr. Confectioner - Pride Plaza Hotel, Rockford`
- 第 2 天晚餐：`New Bhappe Di Hatti, Rockford`
- 第 3 天午餐：`Coco Bambu, Rockford`
- 第 3 天晚餐：`U Like, Rockford`

以及另一组候选：
- 第 2 天早餐：`Dial A Cake, Rockford`
- 第 2 天晚餐：`Cafe Southall, Rockford`
- 第 3 天午餐：`Gajalee Sea Food, Rockford`
- 第 3 天晚餐：`Nutri Punch, Rockford`

#### 它对应闭环的哪一段
- 主要对应：**memory-in-use**
- 如果中途改约束，也会自然碰到 evolution

#### 为什么它能说明问题
这个样本比普通 QA 强很多，因为它不是回答一个孤立问题，而是在一个多日、多约束、互相关联的任务里持续保持一致：
- 第 2 天和第 3 天约束不同
- 早午晚餐的 cuisine / price / rating 约束不同
- 结果必须在整个 itinerary 里一起成立

这就是 `docs/survey/05-evaluation.md` 里说的 `multi-session memory-agent-environment loop`：记忆不是为了一次问答，而是为了支撑持续决策。

如果映射到 `src/memory`：
- formation：预算、菜系、时间偏好要被写入
- evolution：如果用户中途改预算、改口味、改同行人，旧约束要被覆盖或更新
- retrieval：生成 itinerary 时，系统必须重新拿出相关约束
- evaluation：最终 itinerary 是否同时满足多天多槽位约束，就是外部行为检查

#### 它不能说明什么
它更像 memory-in-use 主证据，而不是白盒 formation / evolution 证据。它能说明“系统行为像不像在利用记忆”，但不能直接告诉我们内部哪条记忆是怎么写进去、怎么被更新的。

### 这一组样本合起来说明什么
这组样本把 benchmark 往前推了一步：它们不再只测“找得到”，而开始测“用得上”。

但它们仍然主要是**外部行为证据**，很难白盒回答：
- 哪个约束当初该不该写
- 新约束来了旧约束如何被覆盖
- 哪类历史该被遗忘、压缩、巩固

---

## 三、再往前一步，benchmark 开始出现 formation / evolution 的间接信号

第三组样本开始逼近 lifecycle 更前面的环节，但仍然主要是**行为侧证据**，还不是系统内部状态的直接验证。

### 样本卡片 6：MemoryAgentBench 冲突解析样本

#### 样本内容（中文重述）
- 来源：`ref/datasets/MemoryAgentBench/normalized/Conflict_Resolution.md`
- `id`：`Conflict_Resolution-00000`
- 问题：**《我们共同的朋友》的作者的配偶，其国籍是什么？**
- 上下文：给出一长串事实列表，要求系统顺着事实关系链推出最终答案。

#### 它对应闭环的哪一段
- 主要对应：**evolution 信号**

#### 为什么它能说明问题
这条样本的重点不在“搜到一条事实”，而在“处理事实之间的冲突、覆盖与关系约束”。

当前项目在 `src/memory/evaluation.py` 中，已经把：
- `Test_Time_Learning` 视为 formation 信号之一
- `Conflict_Resolution` 视为 evolution 信号之一

这正好说明：系统已经意识到某些 benchmark split 开始部分触碰 lifecycle，而不只是 retrieval。

如果映射到 `src/memory/manager.py`，这里最相关的就是：
- `update_memory()`
- `forget()`
- `consolidate_episodic_to_semantic()`

一句话概括：**没有 evolution，系统只是记得多；有了 evolution，系统才开始处理“旧信息如何被新信息修正”。**

#### 它不能说明什么
它仍然不能替代白盒 evolution 评测。它更多是通过外部行为间接反映“系统像不像正确地处理了冲突”，而不是直接展示内部状态是怎么变的。

---

### 样本卡片 7：MemoryAgentBench 的 Test-Time Learning 样本

#### 样本内容（中文重述）
- 来源：`ref/datasets/MemoryAgentBench/normalized/Test_Time_Learning.md`
- `id`：`Test_Time_Learning-00000`
- query 里的关键对话可译为：
  - 用户：**你最喜欢的电影是什么？**
  - 系统：**《谋杀绿脚趾》**
  - 用户：**这片子真好笑。你看过《阿呆与阿瓜》或者《金牌流浪汉》吗？它们也是很搞笑的喜剧。**
  - 系统：**看过。你还能想到别的吗？**
- context 里的另一段对话可译为：
  - 用户：**我很喜欢恐怖片。**
  - 系统：**那你可能会喜欢《杀出个黎明》《僵尸之地》这类片子。**

#### 它对应闭环的哪一段
- 主要对应：**formation 信号**

#### 为什么它能说明问题
这条样本问的不是“旧知识有没有找到”，而是：

> 用户刚刚在交互中透露的新偏好，系统有没有把它学进去，并在后续推荐里体现出来？

这非常贴近 formation 的真实难点：
- 不是所有话都值得写入
- 但用户新暴露出的偏好、口味、约束，往往值得写入
- 写入之后，下一轮行为要看得出“我学到了”

如果映射到 `src/memory`：
- formation：`remember()` 决定是否把用户偏好写进去
- retrieval：下一轮推荐时 `recall()` 要能把新偏好捞回来
- evaluation：最终行为要体现“系统不是蒙对，而是真的用了刚形成的记忆”

#### 它不能说明什么
它仍然不能像 `build_formation_scenario()` 那样，白盒地告诉你“哪些该写、哪些不该写”。它只是通过外部交互行为间接反映 formation 是否发生。

### 这一组样本合起来说明什么
这组 benchmark 已经开始碰到 lifecycle 更前端的问题，但方式仍然是**间接的**：
- 通过冲突处理结果，侧面看 evolution 有没有发生
- 通过 test-time learning 行为，侧面看 formation 有没有发生

它们说明 benchmark 不再只测 retrieval，但仍然主要回答“系统行为像不像形成了 / 更新了记忆”，而不直接回答“系统内部到底写入了什么、修改了什么、删掉了什么”。

---

## 四、真正把闭环补齐的，是项目内部的白盒原型

前面三组样本已经足够说明：外部 benchmark 提供了从 retrieval 到 memory-in-use，再到 formation / evolution 间接信号的连续压力。

但如果要让“最小闭环”这个说法真正站住，还差最后一步：**对白盒 formation / evolution 的显式验证。**

这一步不是外部 benchmark 自动给的，而是项目自己补上的。

### 样本卡片 8：内部 formation 原型样本

#### 样本内容（中文）
来源：`src/memory/evaluation.py` 的 `build_formation_scenario()`

写入规则：
- `importance >= 0.6`
- `len(content) >= 5`

高价值样本：
- `f-001`：**用户偏好：不喜欢冗长回复**
- `f-003`：**用户工作地点是上海**
- `f-005`：**用户擅长 Python，不熟悉 Rust**
- `f-008`：**用户要求回复使用中文**

低价值样本：
- `f-002`：**嗯**
- `f-004`：**好的**
- `f-009`：**哦**

#### 它对应闭环的哪一段
- 直接对应：**formation**

#### 为什么它能说明问题
外部 datasets 往往只能间接反映 formation；而这组内部样本是白盒的：
- 什么该写
- 什么不该写
- 规则是什么
都被直接写出来了。

这说明 `src/memory` 不是“来什么都存”，而是已经有最小写入策略。

#### 它不能说明什么
它是原型级 formation 规则，还不是完整生产级写入策略。但它已经足够说明：formation 在项目里不是空白概念。

---

### 样本卡片 9：内部 evolution 原型样本

#### 样本内容（中文）
来源：`src/memory/evaluation.py` 的 `build_evolution_scenario()`

初始记忆：
- `ev-m001`：**用户工作地点是北京**
- `ev-m002`：**用户擅长 Java**
- `ev-m003`：**上次会议于周一举行**
- `ev-m004`：**用户偏好简洁回复**
- `ev-m005`：**向量数据库选型为 FAISS**

更新事件：
- `ev-m001` → **用户工作地点是上海**
- `ev-m002` → **用户擅长 Python 和 Java**
- `ev-m003` → **遗忘**
- `ev-m005` → **向量数据库选型为 ChromaDB**

#### 它对应闭环的哪一段
- 直接对应：**evolution**

#### 为什么它能说明问题
这已经是非常白盒的 evolution 卡片：
- 原来是什么
- 现在应该变成什么
- 哪条应该被遗忘
全部明确给出。

它正好对应 `MemoryManager` 里的：
- `update_memory()`
- `forget()`
- `consolidate_episodic_to_semantic()`

这说明 evolution 在当前项目里不是模糊口号，而是已经被做成可重复验证的原型场景。

#### 它不能说明什么
它还是原型级 evolution，不等于生产环境的完整 belief revision / governance 方案；但它已经足够把闭环中的 evolution 段补齐。

### 这一组样本合起来说明什么
这是全文最关键的一步。

如果没有这两组内部原型，前面的外部 benchmark 最多只能支持这样的说法：我们有 retrieval benchmark、memory-in-use benchmark，以及一些 formation / evolution 的行为信号。

但有了这两组白盒原型之后，系统就不再只是“看起来像有记忆”，而是已经能明确验证：
- 哪类信息应该被形成
- 哪类旧信息应该被更新、遗忘、巩固

也正因为如此，`formation -> evolution -> retrieval -> evaluation` 在这个项目里才不是一句口号，而是一个最小但可检验的闭环。

---

## 总表：样本 ↔ 生命周期阶段 ↔ 证据边界

| 样本 | 主要阶段 | 为什么是强样本 | 能说明什么 | 不能说明什么 |
| --- | --- | --- | --- | --- |
| LoCoMo 基础检索样本 | Retrieval / Evaluation | 单条问题 + 明确 evidence，最适合展示 case 如何归一化进入系统 | `load_benchmark_cases()` 能把真实对话整理成 `query / documents / expected_ids`，系统可据此评测 hit@k / MRR | 不能证明 formation，也不能证明 evolution |
| LoCoMo 高难多证据样本 | Retrieval / Evaluation | 需要把多个 evidence 合起来才能回答，不是单句抄写 | retrieval 不只是找一条最像的话，而是要找回足够支撑回答的记忆集合 | 仍然主要是 retrieval 样本，不能回答“该不该写入”或“如何更新” |
| LongMemEval 跨 session 时序样本 | Retrieval / Evaluation | 关键事实分散在多个 session，且问题要求恢复事件顺序 | 系统需要跨 session 读取历史、做时序恢复、排除噪音 | 不能直接说明写入策略，也不能直接验证冲突更新 |
| AMA-Bench 轨迹回退样本 | Retrieval / Memory-in-use | 历史对象变成 action + observation + 状态，不再只是对话文本 | memory 应服务任务判断，帮助系统识别“是否原地打转” | 不能单独证明 formation 或 evolution，只强烈说明 memory-in-use |
| MemoryArena 多约束 itinerary 样本 | Memory-in-use（并部分触及 evolution） | 多天、多槽位、多约束持续生效，比单问答更接近真实 agent | 说明记忆真正难点是让历史约束在持续任务中持续起作用 | 不能直接展示内部哪条记忆是如何写入或被更新的 |
| MemoryAgentBench 冲突解析样本 | Evolution 信号 | 不只是命中事实，还要处理事实间冲突、覆盖与关系链 | 说明 memory layer 需要 update / forget 等操作，不然无法处理新旧信息修正 | 不能替代白盒 evolution 评测，更多是外部行为侧证据 |
| MemoryAgentBench Test-Time-Learning 样本 | Formation 信号 | 关注刚刚暴露的新偏好能否被学进去并用于下一轮行为 | formation 不只是存事实，而是把新偏好、新约束写成可复用记忆 | 不能像内部 formation 场景那样给出完整“该写/不该写”标准 |
| 内部 formation 原型样本 | Formation | 明确给出高价值/低价值事件与写入阈值，是白盒样本 | 证明项目内部已显式定义最小写入策略，而非“来什么都存” | 仍是原型级 formation，不等于生产级写入策略 |
| 内部 evolution 原型样本 | Evolution | 明确给出初始状态、更新事件、遗忘事件和目标状态 | 证明项目内部已对白盒 evolution 做了可重复场景化建模 | 仍是原型级 evolution，不等于完整 belief revision / governance |

## 结论：benchmark 不够，但闭环已经有了最小版本

如果把这篇笔记压成一句话，最稳妥的说法是：

> 外部 benchmark 已经足够告诉我们 memory 不只是 retrieval，但它们单独仍不足以证明完整 lifecycle；当前项目之所以能说自己具备最小闭环，是因为外部样本提供了分阶段压力，而内部白盒 formation / evolution 原型把缺的两段补上了。

把它拆开说，就是四点：

1. 外部 datasets 已经能提供多种不同压力下的具体样本：
   - LoCoMo：长对话证据定位
   - LongMemEval：跨 session 时序恢复
   - AMA-Bench：轨迹回退与 memory-in-use
   - MemoryArena：多约束持续决策
   - MemoryAgentBench：formation / evolution 的间接行为信号
2. 这些样本共同说明：`src/memory` 需要的不只是普通 QA 检索，而是能够处理长历史、跨 session 历史、agent 轨迹、冲突信息、新形成偏好和持续任务约束的 memory layer。
3. 但如果只靠这些外部样本，仍不足以单独证明 formation 和白盒 evolution；它们主要提供的是 retrieval、memory-in-use，以及 formation / evolution 的外部行为侧证据。
4. `src/memory/evaluation.py` 里的 `build_formation_scenario()`、`build_evolution_scenario()`、`run_evaluation()` 正好补上这块空白，因此整个项目已经形成了 `formation -> evolution -> retrieval -> evaluation` 的最小闭环。

## 这篇 ideas note 适合怎么用

- **对内回看**：提醒自己不要把 benchmark 命中率误当成完整 memory lifecycle 证据。
- **对外解释项目**：快速说明 `src/memory` 为什么不是一个 retrieval demo，而是已经有最小 lifecycle 骨架。
- **后续并入 survey**：更适合拆回 `05-evaluation.md` 和 `survey-map.md` 的主线判断，而不是整篇原样搬运。

## 可能的下一步

1. 把这 9 张样本卡片再压缩成一页表格，方便同步到 `docs/survey/05-evaluation.md`。
2. 再补一篇短 note，专门解释如何结合 `recall_with_trace()` 阅读 retrieval 结果。
3. 如果想继续工程化，可把每张卡片进一步映射到 `tests/test_memory.py` 中的具体测试点。