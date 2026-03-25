# **跨越上下文窗口：下一代人工智能智能体的多模态记忆架构与空间推理研究报告**

## **智能体记忆的本体论转变与基础架构演进**

在2025年至2026年的前沿研究中，大语言模型（LLM）与人工智能智能体的核心发展轨迹发生了根本性的本体论转变。这一时期的大量文献表明，学术界与工业界已不再将记忆仅仅视为一种外部的检索工具，而是将其提升为智能体认知架构的“本体”（Memory-as-Ontology）1。传统的无状态文本生成器受限于固定长度的上下文窗口，在面对需要长期规划、多轮动态交互以及具身物理探索的复杂任务时，暴露出严重的上下文截断与灾难性遗忘问题2。因此，现代智能体必须具备跨越交互周期以持久化、组织并选择性提取信息的能力，这是将其转化为真正适应性智能体的关键前提2。

基于此，2025年12月发布的大型综述研究《AI智能体时代的记忆》首次系统性地统一了智能体记忆的分类法，将其划分为三个正交的维度：形式（包括Token级别、参数化与潜在空间）、功能（事实记忆、经验记忆、工作记忆）以及动态生命周期3。这一生命周期被形式化为“写入-管理-读取”（Write-Manage-Read）的闭环，亦被称为FER生命周期（形成Formation、演化Evolution、检索Retrieval），它不仅深度耦合了智能体的感知与行动，还定义了原始数据如何转化为结构化知识，以及知识如何随时间推移而自我更新2。

在这一本体论转变下，传统的检索增强生成（RAG）技术（即将其视为扁平的向量存储与相似度匹配）已显得捉襟见肘。研究表明，当纯文本的RAG被直接扩展应用于高维的多模态感知输入时，会导致严重的计算低效、跨模态语义错位以及极其脆弱的检索行为6。因此，2025至2026年的研究前沿不可逆转地转向了基于图结构（Graph-Based）的记忆系统与潜在记忆（Latent Memory）架构5。

### **基于图结构的记忆生命周期与多层次抽象**

图结构记忆因其在关系建模、层次化组织和因果依赖追踪方面的内在优势，成为解决多会话连贯性、个性化适应和复杂任务规划的基石7。在图记忆系统中，短期记忆充当一个极其活跃但容量受限的缓冲区，用于维护当前的对话上下文、活跃的推理轨迹以及瞬时状态变量5。随着事件的推进，记忆提取模块会将这些瞬时数据转化为持久化的节点和边，构建出包含明确属性和类型化关系的时间知识图谱（Temporal Knowledge Graphs）或超图（Hypergraphs）5。

诸如G-Memory和LiCoMemory等最新架构引入了层次化的图结构，将信息从句子级别的细粒度细节向上抽象为高层次的过程性见解8。这种细粒度到粗粒度的演化过程不仅极大地减少了记忆碎片，更重要的是，它为智能体的自我进化提供了底层支持8。当面临新任务时，图结构能够支持多跳推理（Multi-hop Reasoning），使得智能体能够顺着因果链条或时间线回溯，提取出最相关的历史经验，从而有效缓解大模型固有的参数化知识幻觉（Hallucination）问题7。

### **潜在空间记忆与逻辑导向的极化架构**

除了显式的图结构，针对大模型自回归生成带来的高昂计算成本，研究人员在2026年提出了一系列基于潜在空间（Latent Space）的记忆创新机制。在这个维度上，MemOCR架构展示了一种极具创造性的“非对称压缩”策略11。认识到深层网络能够将视觉线索编码为语言流，MemOCR并没有将所有交互历史转化为同等权重的文本Token，而是通过视觉布局模块将丰富的文本记忆（如标题、高亮段落）渲染为一幅高信息密度的“记忆图像”11。当智能体需要读取记忆时，它利用视觉通道对这张图像进行扫描，依据模态特有的冗余度和语义重要性，自适应地分配注意力，从而在极端的上下文预算下实现了长期逻辑推理能力的提升，并将浮点运算量（FLOPs）和键值缓存（KV-Cache）使用量降低了40%以上11。

更为前沿的突破体现在PolarMem（极化潜在图记忆）这一免训练架构上13。对于需要严格验证的跨模态任务，传统模型往往因为缺乏对“否定约束”的有效记忆而产生逻辑错误。PolarMem通过引入正交的抑制连接（Orthogonal Inhibitory Connections），在图拓扑结构中将“已验证的否定信息”作为一种主要的认知状态显式存储起来13。在推理阶段，PolarMem强制执行逻辑主导的检索范式，利用抑制信号直接阻断那些违反历史否定约束的幻觉模式生成。跨越八个冻结的视觉-语言模型（VLM）的评估证明，这种极化的潜在架构为构建可信、可验证的多模态智能体奠定了极为坚实的基础13。

| 记忆架构范式 | 核心技术机制 | 解决的主要痛点与应用优势 | 代表性研究与系统 |
| :---- | :---- | :---- | :---- |
| **传统RAG/向量记忆** | 扁平化的余弦相似度检索与文本块拼接 | 实现门槛低；适用于短时、基于特定关键词的浅层事实核查。 | Mem0, 早期检索系统 15 |
| **图结构记忆 (Graph-Based)** | 实体关系建模、层次化知识图谱与动态网络更新 | 解决多会话连贯性与复杂多跳推理；通过显式节点和边缓解事实幻觉。 | G-Memory, LiCoMemory, TeleMem 8 |
| **潜在/视觉压缩记忆** | 利用多模态通道进行不对称压缩（如将文本渲染为图像） | 极大地降低自回归推理的计算复杂度与KV缓存成本；提升信息密度。 | MemOCR, DARE 11 |
| **极化潜在拓扑网络** | 带有正交抑制连接的结构，显式存储“否定”逻辑约束 | 压制违背历史负面约束的幻觉；构建无需微调的可验证认知系统。 | PolarMem 13 |

## **多模态智能体的记忆机制：情景记忆与语义记忆的深度融合**

人类在物理世界中获取知识的过程并非仅仅依赖于被动的文本记录，而是通过不断整合视觉、听觉、语言等异构感知流，进而沉淀出对世界的深刻理解。2025至2026年的文献深刻指出，下一代基础智能体的核心挑战在于如何忠实地表征、对齐并抽象这些异构的感官输入，将其转化为连贯的内部状态6。在这个过程中，“情景记忆”（Episodic Memory）与“语义记忆”（Semantic Memory）的双轨制架构成为了多模态记忆领域的主导范式。

### **痕迹转换理论与M3-Agent的双轨记忆处理**

在认知心理学中，痕迹转换理论（Trace Transformation Theory）指出，事件的多种表征（从精确的、特定于情景的细节到核心的、图式化的语义表征）在编码时是同时形成的，并在检索过程中动态交互17。2025年发表于ICLR 2026的M3-Agent（见、听、记、推：具备长期记忆的多模态智能体）完美地在算法层面上复现了这一生物学过程18。

大多数早期的多模态智能体仅将原始对话文本或单帧截图塞入上下文窗口，这种方式不仅低效，而且容易导致严重的检索错误，被称为“上下文孤立”（Contextual Isolation）现象21。与之截然不同，M3-Agent的架构由两个并行进程组成：记忆化（Memorization）与控制（Control）18。在记忆化过程中，智能体以视频片段为单位实时处理输入的视听流，同时生成两种类型的长期记忆。情景记忆负责捕获原始视频中带有时间戳的视觉和听觉内容（例如：“Alice把空瓶子扔进了绿色的垃圾桶”）；而语义记忆则从这些具象的情景中提取出抽象的、可泛化的概念、实体身份、属性与因果关系（例如：“绿色的垃圾桶用于回收利用”）21。

这种双轨设计的深层逻辑在于，情景记忆充当了不可篡改的经验时间轴，支持精确的回溯；而语义记忆则打破了特定事件的束缚，构建了独立于底层模型参数更新的通用世界知识库21。因此，当M3-Agent面对复杂的长视频问答任务（如M3-Bench所评估的）时，它能够自发地进行多轮迭代推理，先通过语义记忆确定“绿色垃圾桶”的属性，再通过情景记忆定位“Alice”的动作，从而实现了零样本（Zero-shot）的跨模态推理18。

此外，在维持任意长跨度下的核心概念一致性方面，M3-Agent引入了极其精妙的潜在锚定机制。例如，当处理视频中未出现面部特征的说话者时，智能体直接利用音频编码提取出\<voice\_id\>作为锚点20。情景记忆会记录“\<voice\_0\> 说‘我喜欢苹果’”，而语义记忆则沉淀出“\<voice\_0\> 喜欢苹果”的属性节点20。所有的记忆项都被链接到这个隐式的实体身份上，彻底摆脱了传统视觉模型对“看脸”的绝对依赖，实现了真正的多模态实体追踪20。

### **克服上下文孤立：激活扩散与动态特征对齐**

尽管有了情景与语义的分离，基于余弦相似度的检索机制依然面临着“搜索假设”（Search Assumption）的桎梏：即系统盲目地认为，与当前查询向量距离最近的历史记录就是最相关的记忆22。然而在多轮的动态交互中，由于用户的偏好漂移和情境转移，语义上距离很远的记忆片段往往才是破局的关键6。

为了突破这一瓶颈，Synapse架构引入了受大脑神经生物学启发的“激活扩散”（Spreading Activation）机制22。Synapse并不依赖扁平的向量检索，而是构建了一个统一的情景-语义图（Unified Episodic-Semantic Graph），将原始的交互日志综合为抽象的概念节点22。当查询进入系统时，信号会在这个图网络中沿着具有强逻辑联系的边进行传播，激活那些在向量空间中看似遥远、但在因果逻辑上紧密相连的历史记忆。这种方法使得智能体在处理需要强逻辑连贯性的长上下文任务时，其准确率与召回鲁棒性获得了指数级的提升22。

在工业落地层面，TeleMem架构则通过融合微秒级的智能缓存与大模型语义聚类，重构了多模态记忆的管理路径15。当多模态数据（如长视频流）输入时，TeleMem自动启动包含帧提取、VLM（如Qwen3-Omni）密集标注和向量化存储的三阶段流水线。其核心创新在于废弃了Mem0框架中机械的向量去重，转而采用基于LLM的语义聚类（Semantic Deduplication）来合并相似的多模态记忆15。这不仅消除了多角色对话场景中的身份混淆现象（为每个角色创建独立的记忆画像），还有效控制了Token消耗，使得多模态智能体能够在成本可控的前提下，维持数天甚至数周的极长上下文推理能力15。

### **流式在线处理与长视频推理的计算优化**

对于持续在线的智能体而言，离线地处理整个长视频来生成记忆是不切实际的。因此，如何高效地在线构建片段级（Segment-Level）记忆成为了2025年的一大研究热点。LiveVLM等流式导向架构针对连续视频流提出了一种革命性的键值缓存（KV-Cache）管理策略26。

LiveVLM摒弃了在问答发生后才进行视频处理的被动模式，它实时生成并压缩视频的KV张量，在保留长期视觉微小细节的同时，积极剔除冗余的视觉Token26。当接收到用户查询时，LiveVLM的在线问答机制能够无缝地从压缩后的流式缓存中提取出短时与长时感知信息，最大限度地减少了无关上下文的干扰。实验数据表明，相较于早期的在线处理方法，在处理同样数量的帧输入时，这种流式记忆架构能够实现高达5倍的响应速度提升，不仅突破了设备显存的限制，更使得视觉-语言模型（VLM）在连续动态场景中的实时交互成为了可能26。

## **空间推理的演进：从被动2D感知到主动3D探索**

虽然多模态语义记忆赋予了智能体理解环境事件和人物关系的能力，但具身人工智能（Embodied AI）若要在这个世界上实际操作并完成物理任务，就必须深刻理解“空间”。空间推理（Spatial Reasoning）是指智能体理解、表征和操作物体、环境以及自身之间几何关系的能力，它是机器人导航、三维重建以及物理交互的基础27。

### **2D感知陷阱与执行层面的几何约束**

通过广泛梳理直至2025年的研究，一个普遍的结论是：现有的视觉-语言大模型（VLM）尽管在二维图像理解和视觉常识问答上表现优异，但它们仍然深陷于“2D感知陷阱”（2D Perceiver Trap）之中28。传统的VLM以帧为单位处理视觉输入，倾向于将空间属性（如绝对距离、坐标参考系、遮挡关系等）视为抽象的符号文本参数进行模式匹配，而缺乏对其物理实在性的深刻感知29。

例如，在地球观测（Earth Observation）以及基于多智能体的宏观空间任务中，基于大语言模型的智能体往往能够生成逻辑上极其合理的宏观规划，但却在具体的执行阶段遭遇灾难性失败。这种失败并非源于规划能力的不足，而是因为它们无法正确处理投影变换、空间重采样或是多视角的几何一致性29。这些早期且隐蔽的几何不匹配会在工作流中静默地传播，最终导致整个操作链条的崩溃。这促使研究焦点从“如何让智能体进行符号规划”转向了“如何在带有几何约束的物理环境中可靠地执行任务”29。在微观具身领域，如Web端网页遍历任务中，智能体同样面临严重的“空间迷失”现象。V-GEMS系统正是通过建立显式的记忆栈和视觉接地（Visual Grounding）机制，才解决了智能体在深层DOM结构导航中因为丢失空间坐标而陷入的无限循环错误31。

### **Think3D框架与具身“空间思维”链**

为了打破被动接受2D切片的局限，2026年一月发布的Think3D框架提出了一种极具破坏性创新的视角：将空间推理重构为一种主动的3D探索过程，即“利用3D空间进行思考”（Thinking with 3D Space）28。

人类并非通过静态的照片来理解房间，而是通过移动视角、建立物体间的遮挡和透视关系来建立一致的三维心理模型。受到这种认知过程的启发，Think3D赋予了VLM直接与重建的3D点云进行交互的能力28。该框架并没有依赖生成式视频模型来“幻觉”三维空间（这往往引入严重的物理谬误），而是通过集成一套可调用的3D操控工具集，让智能体能够主动控制相机的姿态、焦距与渲染参数28。

在Think3D的工作流中，智能体执行一个“观察 → 操控 → 反思”（Observe \-\> Manipulate \-\> Reflect）的迭代循环。它首先从全局顶视图（Global View）获取环境的拓扑概览，然后主动将视角切换到以自我为中心的微观视角（Ego-centric View），去观察特定的遮挡区域或物体细节30。每一帧由工具渲染出的新视角图像都会被追加到智能体的工作记忆中，从而在模型内部形成一条显式的“3D思维链”（3D Chain-of-Thought）30。这种方式彻底避免了传统2.5D工具（如简单的深度估计或裁剪）只能捕捉浅层空间线索的弊端。对于闭源的先进模型（如GPT-4o和Gemini-2.5-Pro），Think3D作为零样本（Zero-shot）插件，在BLINK、MindCube和VSI-Bench等多视角推理基准上，带来了高达7.8%的绝对性能提升，证明了基于工具增强的主动探索是释放多模态智能体类人三维推理能力的一条有效路径28。

### **强化学习在空间探索策略中的应用**

空间探索并非毫无代价，盲目的视角切换会导致严重的计算资源浪费和推理超时。虽然超大参数量的模型能够凭借其强大的零样本常识直觉地选择好的观察角度，但对于部署在边缘设备或机器人本体上的紧凑型模型（如3B至4B参数的视觉-语言-动作模型，VLA）而言，它们极度缺乏主动寻找信息量最丰富的视角的策略28。

针对这一痛点，Think3D-RL模块创新性地引入了强化学习（Reinforcement Learning）来优化空间探索的轨迹。通过采用无需显式价值函数的组相对策略优化（GRPO, Group Relative Policy Optimization）算法，模型通过最大化由多步视角操作所带来的信息增益和最终问答的准确率作为奖励信号进行微调28。

实证结果揭示了一个深刻的结论：在未进行强化学习干预前，Qwen3-VL-4B这种开源小模型在使用3D工具时仅能获得0.7%的边缘性能提升；而在经历RL微调后，它自主学会了系统性地扫描遮挡物死角，并智能地融合多视角的互补信息，其性能增益被剧烈放大至10.7%28。这表明，通过在记忆与动作之间闭环使用强化学习信号，我们能够使小参数量的模型展现出与超大参数模型高度对齐的复杂空间探索行为，从而彻底绕过了昂贵且难以获取的轨迹专家标注（Trajectory Annotations）数据28。

| 空间推理范式 | 环境表征基础 | 推理与探索机制 | 核心局限与突破 |
| :---- | :---- | :---- | :---- |
| **被动2D感知 (传统VLM)** | 离散的RGB快照 / 静态2D图像序列 | 依赖单一视角的帧级特征匹配，空间关系基于文本幻觉进行符号推断。 | 无法处理严重遮挡与深度信息；容易产生物理上不合理的空间规划。 |
| **2.5D工具增强** | 引入深度图、图像裁剪与目标检测框 | 使用外部视觉工具进行浅层的对象关系映射与相对位置判别。 | 无法进行跨视角的一致性对齐，难以理解复杂环境的三维几何拓扑。 |
| **主动3D探索 (Think3D)** | 3D重建点云 / 连续可渲染相机空间 | 闭环的“观察-操控-反思”链条，通过切换全局与第一人称视角累积几何记忆。 | 通过GRPO强化学习使得紧凑型模型（如4B）能够自动规划最优视线轨迹。 |
| **渲染即检索 (RenderMem)** | 完全几何建模的3D场景表征 | 将视线、遮挡和可见性判断卸载给图形渲染引擎，直接生成查询条件下的视觉证据。 | 消除了模型内部繁重的欧几里得几何计算负担，确保了推理的物理准确性。 |

## **具身人工智能的持久化空间记忆表示**

除了主动改变视角，对于在复杂物理世界中执行长周期（Long-Horizon）连续任务的具身机器人而言，如何“记住”它已经探索过的空间结构并加以利用，是另一个严峻的挑战。传统的具身问答（EQA）与具身多模态导航（EMN）任务大多局限于单次重置的场景，智能体在完成一个孤立目标后，其建立的地图和记忆即被清空34。一旦面对需要复用先前积累的空间信息、或者判断某项任务是否在当前环境中“不可行”（Infeasible Tasks）时，传统架构就会崩溃。

### **3D高斯泼溅作为持久化空间记忆 (GSMem)**

在2026年3月提出的GSMem（以3D高斯泼溅作为持久化空间记忆）框架中，研究人员直击了传统离散场景图和静态视图快照所存在的根本缺陷——缺乏“事后可重新观察性”（Post-hoc Re-observability）35。在传统范式下，如果机器人在巡逻时由于视角偏限没有注意到桌子底下的关键物体，那么这一信息的遗漏在后续的推理中是无法挽回的。

GSMem通过显式地将连续的几何结构和密集的视觉外观参数化为3D高斯泼溅（3D Gaussian Splatting, 3DGS），构建了一个致密的辐射场（Radiance Field）35。这一技术彻底赋予了智能体“空间回忆”（Spatial Recollection）的能力——即在脑海中进行时光旅行，从最佳的、甚至其物理实体从未占据过的新颖视角，重新渲染并审视之前探索过的高保真区域35。这极大模拟了人类在认知过程中，通过回忆某个房间的布局，在脑海中“环顾四周”以寻找被遗忘细节的高级心智能力。

为了让这种连续的三维记忆能够被大语言模型快速检索和理解，GSMem部署了极具创新性的多级检索渲染机制，它同时利用了并行的“对象级场景图”和“语义级语言场”35。当系统面对复杂的导航或视觉问答指令时，它首先在语言场中定位相关区域。传统的语义3DGS往往需要极其缓慢的迭代优化才能将语言嵌入与3D空间对齐，而GSMem采用了一种被称为“逆向聚合”（Reverse Aggregation）的免优化方法。它通过轻量级的超分辨率解码器，从2D关键帧中提取像素级的CLIP特征，然后利用在渲染过程中计算出的相同的Alpha混合权重（Alpha-blending weights），将这些高维语义特征直接反投影回3D高斯球上36。这一机制确保了3D语言场在没有任何额外训练周期的情况下，能够与视觉地图天然保持绝对的一致性36。

在定位到模糊的目标区域后，GSMem进一步“幻觉”出最佳的无遮挡视角，并渲染出高保真图像供视觉-语言大模型（VLM）进行最终的逻辑推理36。同时，其配备的混合探索策略巧妙地平衡了由VLM语义评分驱动的任务导向探索，与基于3DGS不确定性感知的几何覆盖率探索35。在严苛的GOAT-Bench等多模态终身导航基准上，GSMem达到了惊人的67.2%的成功率和46.9%的SPL（Success weighted by Path Length），全面超越了依赖于关键帧拼接的高层图结构方法，展示了密集几何记忆在长周期任务中的绝对统治力36。

### **RenderMem与3DSPMR：渲染与连续任务的统一界面**

延续了在连续介质中进行空间推理的思路，RenderMem（渲染即空间记忆检索）框架提出，具身推理本质上是高度依赖视角的。与其让计算资源受限于模型参数，不如直接将3D渲染引擎本身视为连接世界表征与大模型推理的核心接口38。当面对诸如“如果我站在门口，我能看到沙发后的盒子吗”这类涉及视线（Line-of-sight）、可见性和遮挡关系的复杂查询时，RenderMem并不要求模型去抽象计算三维向量，而是直接在维持的三维场景中，从查询所暗示的虚拟视角生成相应的视觉渲染证据，从而将艰涩的几何代数题降维成了一道直观的视觉问答题38。

在执行序列化的现实任务方面，3DSPMR（面向顺序具身MLLM推理的3D空间记忆）也贡献了独特的解决方案。针对连续目标的寻找与不可行任务的识别，该系统提取复杂环境的稀疏空间表征，形成文本化的场景图和几何地图34。在Geo-Reasoning（几何推理）模块的调度下，如果先前的任务已经在特定区域留下了物理足迹，智能体能够瞬间复用这些空间信息，避免了如同无头苍蝇般的重复探索；而当区域完全被遍历且语义核查均未能匹配目标时，它能够果断地判定任务的不可行性并停止执行，这标志着具身智能在决策鲁棒性和计算效率上迈出了重要一步34。

## **评测基准、动态策略与安全的信任边界**

随着智能体记忆在多模态理解与三维空间导航方面的能力呈指数级扩张，学术界与工业界用来评估和规范这些系统的基准也经历了天翻地覆的重构。过去那种依赖于静态QA文本库或单一模态记忆提取的评价标准已经完全过时。

### **多会话与连续依赖的动态基准测试**

2025至2026年间涌现的一系列基准测试（如MemBench, MemoryAgentBench, MemoryArena）彻底将评估的焦点从“信息回放”（Recall）转移到了“记忆与决策的紧密耦合”（Interleaved memory with decision-making）上2。这些基准要求智能体在不同的环境中切换，同时保持长期意图的一致性。

例如，TeleEgo被设计为首个覆盖多角色、多场景、多任务的“全能基准”（Omni-benchmark），它输入长达数小时甚至数天的第一人称（Egocentric）连续视频数据，迫使模型在极端的时间跨度下维持并执行跨记忆的复杂逻辑推理40。同样地，M3-Agent框架所附带的M3-Bench构建了大规模的机器人第一人称视角视频与多样化的网络视频集，专门测试智能体将零碎的片段提取为系统性通识（General Knowledge Extraction）的能力18。在空间智能评估方面，SAVVY-Bench更是开创性地将动态音频与3D场景深度融合，强制模型不仅要理解三维空间中的绝对距离与方向关系，还要能够执行细粒度的音视频时空接地（Spatio-temporal Grounding）41。研究揭示，即便是目前在常规测试中近乎饱和的最先进基础模型，在面对这些要求多模态和时空连续性的长周期任务时，其准确率也会发生断崖式的暴跌，这明确指示了未来的研发重点必须向底层的记忆管理策略倾斜2。

### **系统级具身效率与动作序列优化**

在具身机器人平台上的实际部署表明，传统大模型研究中所推崇的“效率”指标（如模型参数量、FLOPs、每秒Token解码数）与智能体在物理世界中的实际表现往往存在巨大的鸿沟43。研究发现，某些通过Token稀疏化或激进压缩动作序列来降低计算成本的方法，反而会导致末端执行器（如机械臂）的轨迹平滑度急剧下降，累积关节旋转冗余增加，从而推高了端到端的任务完成时间和运动能耗43。

因此，新一代的记忆和动作控制策略（如Agentic Memory通过分步GRPO对记忆操作进行RL强化2，或是基于环境反馈闭环微调的探索策略）更加强调对“系统级具身效率”的优化43。只有全面整合任务完成耗时、运动学指标与视觉语言推理的计算开销，才能为视觉-语言-动作模型（VLA）提供一个真实、公平、且具有实战指导意义的评估框架43。

### **持久化记忆的信任基础设施与安全挑战**

当智能体的记忆从临时的便签转变为持久化、跨会话的知识本体时，隐藏的巨大安全风险也随之浮出水面6。2026年的前沿研究反复发出警告：持久的用户和环境记忆极其容易受到恶意注入的攻击6。

长期的多模态记忆扩大了对抗性操纵（Adversarial Manipulation）和记忆投毒（Memory Poisoning）的攻击面。如果攻击者在视频帧或空间场景中注入微妙的对抗性扰动，不仅会误导智能体当下的决策，这些错误的感知更会被情景记忆所捕获，并在随后的图结构整合中，被系统提炼为某种错误但持久的“语义知识”或操作规则6。由于这种记忆演化过程是静默且累积的，它会在不触发现存安全防护围栏（Guardrails）的情况下，长期潜伏于智能体的底层行为逻辑中，导致灾难性的后果6。

为了应对这种结构性风险，建立安全且可审计的记忆模块（Auditable Memory Modules）成为了不可或缺的一环6。研究指出，可信赖的记忆基础设施必须包含细粒度的溯源追踪机制，同时提供受用户严密控制的接口，以支持对长效存储内容的审查、溯源、定点编辑乃至精确的权限撤销6。在设计用于开放世界的终身个性化基础智能体时，系统的鲁棒性、防御恶意写入的安全屏障，以及记忆机制的完全透明度，必须被提升至与多模态推理能力同等的首要目标地位6。

## **结语：迈向通用具身认知**

从2025年到2026年的这波技术爆发不仅重塑了AI智能体的内部工作机理，更为实现通用具身智能铺平了道路。通过将时间序列上的情景记忆与抽象可泛化的语义知识深度解耦并动态融合，多模态智能体成功地跨越了单次对话的上下文孤立。而在物理交互维度上，主动的3D空间探索链条与基于3D高斯泼溅的持久化辐射场记忆，彻底终结了模型对二维平面图像的被动依赖，赋予了机器真正意义上的“空间回忆”与视觉幻觉规避能力。

当底层的强化学习策略能够在毫秒级延迟内，调度这些庞大的跨模态时空图谱与渲染接口时，我们所见证的不再是简单的文本预测引擎，而是一个具备环境适应力、逻辑反思能力与长期进化潜能的完整认知实体。随着多智能体协同、流式处理效率以及安全审计基础设施的不断完善，这种深植于本体论变革中的记忆架构，必将在未来几年内深刻重塑机器人学、科学发现以及人类生活数字助手的演进格局。

#### **Works cited**

1. 1\. Introduction \- arXiv.org, accessed March 24, 2026, [https://arxiv.org/html/2603.04740v1](https://arxiv.org/html/2603.04740v1)  
2. Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers, accessed March 24, 2026, [https://arxiv.org/html/2603.07670v1](https://arxiv.org/html/2603.07670v1)  
3. \[2512.13564\] Memory in the Age of AI Agents \- arXiv, accessed March 24, 2026, [https://arxiv.org/abs/2512.13564](https://arxiv.org/abs/2512.13564)  
4. Memory in the Age of AI Agents (Dec 2025\) \- YouTube, accessed March 24, 2026, [https://www.youtube.com/watch?v=ZvaooFqZayc](https://www.youtube.com/watch?v=ZvaooFqZayc)  
5. Graph-based Agent Memory: Taxonomy, Techniques, and Applications \- Scribd, accessed March 24, 2026, [https://www.scribd.com/document/994695793/Graph-based-Agent-Memory-Taxonomy-Techniques-and-Applications](https://www.scribd.com/document/994695793/Graph-based-Agent-Memory-Taxonomy-Techniques-and-Applications)  
6. Rethinking Memory Mechanisms of Foundation Agents in the Second Half: A Survey, accessed March 24, 2026, [https://arxiv.org/html/2602.06052v2](https://arxiv.org/html/2602.06052v2)  
7. Graph-based Agent Memory: Taxonomy, Techniques, and Applications \- arXiv, accessed March 24, 2026, [https://arxiv.org/html/2602.05665](https://arxiv.org/html/2602.05665)  
8. TeleMem: Building Long-Term and Multimodal Memory for Agentic AI \- arXiv, accessed March 24, 2026, [https://arxiv.org/html/2601.06037v1](https://arxiv.org/html/2601.06037v1)  
9. Graph-based Agent Memory: Taxonomy, Techniques, and Applications \- arXiv, accessed March 24, 2026, [https://arxiv.org/html/2602.05665v1](https://arxiv.org/html/2602.05665v1)  
10. Graph-based Agent Memory: Taxonomy, Techniques, and Applications \- ResearchGate, accessed March 24, 2026, [https://www.researchgate.net/publication/400505993\_Graph-based\_Agent\_Memory\_Taxonomy\_Techniques\_and\_Applications](https://www.researchgate.net/publication/400505993_Graph-based_Agent_Memory_Taxonomy_Techniques_and_Applications)  
11. MemOCR: Layout-Aware Visual Memory for Efficient Long-Horizon Reasoning \- arXiv, accessed March 24, 2026, [https://arxiv.org/html/2601.21468v4](https://arxiv.org/html/2601.21468v4)  
12. Efficient Multimodal Spatial Reasoning via Dynamic and Asymmetric Routing \- OpenReview, accessed March 24, 2026, [https://openreview.net/forum?id=BQASoLmREU](https://openreview.net/forum?id=BQASoLmREU)  
13. PolarMem: A Training-Free Polarized Latent Graph Memory for Verifiable Multimodal Agents, accessed March 24, 2026, [https://www.researchgate.net/publication/400370819\_PolarMem\_A\_Training-Free\_Polarized\_Latent\_Graph\_Memory\_for\_Verifiable\_Multimodal\_Agents](https://www.researchgate.net/publication/400370819_PolarMem_A_Training-Free_Polarized_Latent_Graph_Memory_for_Verifiable_Multimodal_Agents)  
14. Zijie Zhou \- CatalyzeX, accessed March 24, 2026, [https://www.catalyzex.com/author/Zijie%20Zhou](https://www.catalyzex.com/author/Zijie%20Zhou)  
15. TeleAI-UAGI/telemem: TeleMem is a high-performance ... \- GitHub, accessed March 24, 2026, [https://github.com/TeleAI-UAGI/telemem](https://github.com/TeleAI-UAGI/telemem)  
16. Hindsight is 20/20: Building Agent Memory that Retains, Recalls, and Reflects \- arXiv, accessed March 24, 2026, [https://arxiv.org/html/2512.12818v1](https://arxiv.org/html/2512.12818v1)  
17. Adaptive episodic memory: how multiple memory representations drive behavior in humans and nonhumans | Physiological Reviews, accessed March 24, 2026, [https://journals.physiology.org/doi/10.1152/physrev.00005.2025](https://journals.physiology.org/doi/10.1152/physrev.00005.2025)  
18. Seeing, Listening, Remembering, and Reasoning: A Multimodal Agent with Long-Term Memory, accessed March 24, 2026, [https://m3-agent.github.io/](https://m3-agent.github.io/)  
19. Seeing, Listening, Remembering, and Reasoning: A Multimodal Agent with Long-Term Memory \- ResearchGate, accessed March 24, 2026, [https://www.researchgate.net/publication/394472801\_Seeing\_Listening\_Remembering\_and\_Reasoning\_A\_Multimodal\_Agent\_with\_Long-Term\_Memory](https://www.researchgate.net/publication/394472801_Seeing_Listening_Remembering_and_Reasoning_A_Multimodal_Agent_with_Long-Term_Memory)  
20. Seeing, Listening, Remembering, and Reasoning: A Multimodal Agent with Long-Term Memory | OpenReview, accessed March 24, 2026, [https://openreview.net/forum?id=PMz29A7Muq](https://openreview.net/forum?id=PMz29A7Muq)  
21. MemVerse: Multimodal Memory for Lifelong Learning Agents \- arXiv, accessed March 24, 2026, [https://arxiv.org/html/2512.03627v1](https://arxiv.org/html/2512.03627v1)  
22. Synapse: Empowering LLM Agents with Episodic-Semantic Memory via Spreading Activation \- arXiv, accessed March 24, 2026, [https://arxiv.org/html/2601.02744v2](https://arxiv.org/html/2601.02744v2)  
23. Seeing, Listening, Remembering, and Reasoning: A Multimodal Agent with Long-Term Memory \- arXiv.org, accessed March 24, 2026, [https://arxiv.org/html/2508.09736v1](https://arxiv.org/html/2508.09736v1)  
24. Seeing, Listening, Remembering, and Reasoning: A Multimodal Agent with Long-Term Memory \- arXiv, accessed March 24, 2026, [https://arxiv.org/html/2508.09736v2](https://arxiv.org/html/2508.09736v2)  
25. Agent Semantic Memory (AgentSM) \- Emergent Mind, accessed March 24, 2026, [https://www.emergentmind.com/topics/agent-semantic-memory-agentsm](https://www.emergentmind.com/topics/agent-semantic-memory-agentsm)  
26. LiveVLM: Efficient Online Video Understanding via Streaming-Oriented KV Cache and Retrieval \- ResearchGate, accessed March 24, 2026, [https://www.researchgate.net/publication/391954118\_LiveVLM\_Efficient\_Online\_Video\_Understanding\_via\_Streaming-Oriented\_KV\_Cache\_and\_Retrieval](https://www.researchgate.net/publication/391954118_LiveVLM_Efficient_Online_Video_Understanding_via_Streaming-Oriented_KV_Cache_and_Retrieval)  
27. ICLR 2026 Monday 04/27, accessed March 24, 2026, [https://iclr.cc/virtual/2026/day/4/27](https://iclr.cc/virtual/2026/day/4/27)  
28. Think3D: Thinking with Space for Spatial Reasoning \- arXiv, accessed March 24, 2026, [https://arxiv.org/html/2601.13029v3](https://arxiv.org/html/2601.13029v3)  
29. Experience-Driven Multi-Agent Systems Are Training-free Context-aware Earth Observers, accessed March 24, 2026, [https://arxiv.org/html/2602.02559v1](https://arxiv.org/html/2602.02559v1)  
30. Think3D: Thinking with Space for Spatial Reasoning \- arXiv, accessed March 24, 2026, [https://arxiv.org/html/2601.13029v1](https://arxiv.org/html/2601.13029v1)  
31. See and Remember: A Multimodal Agent for Web Traversal \- arXiv.org, accessed March 24, 2026, [https://arxiv.org/html/2603.02626v1](https://arxiv.org/html/2603.02626v1)  
32. Learning Unified Long-Term and Short-Term Memory Management for Large Language Model Agents \- arXiv, accessed March 24, 2026, [https://arxiv.org/pdf/2601.01885](https://arxiv.org/pdf/2601.01885)  
33. \[2601.13029\] Think3D: Thinking with Space for Spatial Reasoning \- arXiv, accessed March 24, 2026, [https://arxiv.org/abs/2601.13029](https://arxiv.org/abs/2601.13029)  
34. Vision to Geometry: 3D Spatial Memory for Sequential Embodied MLLM Reasoning and Exploration \- arXiv, accessed March 24, 2026, [https://arxiv.org/html/2512.02458v2](https://arxiv.org/html/2512.02458v2)  
35. GSMem: 3D Gaussian Splatting as Persistent Spatial Memory for Zero-Shot Embodied Exploration and Reasoning \- ResearchGate, accessed March 24, 2026, [https://www.researchgate.net/publication/402859807\_GSMem\_3D\_Gaussian\_Splatting\_as\_Persistent\_Spatial\_Memory\_for\_Zero-Shot\_Embodied\_Exploration\_and\_Reasoning](https://www.researchgate.net/publication/402859807_GSMem_3D_Gaussian_Splatting_as_Persistent_Spatial_Memory_for_Zero-Shot_Embodied_Exploration_and_Reasoning)  
36. GSMem: 3D Gaussian Splatting as Persistent Spatial Memory for Zero-Shot Embodied Exploration and Reasoning | alphaXiv, accessed March 24, 2026, [https://www.alphaxiv.org/overview/2603.19137v1](https://www.alphaxiv.org/overview/2603.19137v1)  
37. \[2603.19137\] GSMem: 3D Gaussian Splatting as Persistent Spatial Memory for Zero-Shot Embodied Exploration and Reasoning \- arXiv, accessed March 24, 2026, [https://arxiv.org/abs/2603.19137](https://arxiv.org/abs/2603.19137)  
38. RenderMem: Rendering as Spatial Memory Retrieval \- arXiv.org, accessed March 24, 2026, [https://arxiv.org/html/2603.14669v1](https://arxiv.org/html/2603.14669v1)  
39. 3D Spatial Memory for Sequential Embodied MLLM Reasoning and Exploration \- arXiv.org, accessed March 24, 2026, [https://arxiv.org/pdf/2512.02458](https://arxiv.org/pdf/2512.02458)  
40. Improve dataset card: Add task categories, HF paper link, GitHub link, correct project page, and sample usage · David0219/TeleEgo at 692cf38 \- Hugging Face, accessed March 24, 2026, [https://huggingface.co/datasets/David0219/TeleEgo/commit/692cf386e38d8e43e05462984249ca5a238876e5](https://huggingface.co/datasets/David0219/TeleEgo/commit/692cf386e38d8e43e05462984249ca5a238876e5)  
41. NeurIPS 2025 Orals, accessed March 24, 2026, [https://neurips.cc/virtual/2025/events/oral](https://neurips.cc/virtual/2025/events/oral)  
42. FindingDory: A Benchmark to Evaluate Memory in Embodied Agents | OpenReview, accessed March 24, 2026, [https://openreview.net/forum?id=cnn6KDy7YT](https://openreview.net/forum?id=cnn6KDy7YT)  
43. Robotics \- arXiv, accessed March 24, 2026, [https://arxiv.org/list/cs.RO/new](https://arxiv.org/list/cs.RO/new)