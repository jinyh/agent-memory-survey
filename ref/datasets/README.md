# ref/datasets

本目录存放 agent memory 相关 benchmark 的评测数据文件。

## 已下载数据集

| 数据集 | 来源论文 | arXiv | 内容 | 路径 |
|---|---|---|---|---|
| **LoCoMo** | Evaluating Very Long-Term Conversational Memory of LLM Agents | 2402.17753 | 长对话 recall + 时间问题 | `locomo/` |
| **LongMemEval** | LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory | 2410.10813 | 超长会话/跨会话压力测试 | `longmemeval-cleaned/` |
| **MemoryAgentBench** | MemoryAgentBench: Evaluating Memory in LLM Agents via Incremental Multi-Turn Interactions | 2507.05257 | 多轮增量交互，含 episodic/working 子集 | `MemoryAgentBench/` |
| **MemoryArena** | MemoryArena: Benchmarking Agent Memory in Interdependent Multi-Session Agentic Tasks | 2602.16313 | 跨 session 相互依赖任务 | `MemoryArena/` |
| **AMA-Bench** | AMA-Bench: Evaluating Long-Horizon Memory for Agentic Applications | 2602.22769 | long-horizon agentic memory + tool use | `AMA-bench/` |
| **M3-Bench** | M3-Agent: Seeing, Listening, Remembering, and Reasoning | 2508.09736 | 多模态 QA：robot.json（100视频）+ web.json（920视频） | `M3-Bench/` |

## 数据集链接与未发布状态

| 数据集 | 状态 | 备注 |
|---|---|---|
| SEER-Bench | **未公开** | Vision to Geometry（arXiv:2512.02458）配套 benchmark，截至 2026-04-27 作者未发布数据集链接 |
| DMR（Deep Memory Retrieval） | **非独立数据集** | Zep（arXiv:2501.13956）引用的 MemGPT 内部评测指标，非可下载数据集；LongMemEval 已有 |
| Think3D benchmark data | **依赖外部 benchmark** | spagent repo（zhangzaibin/spagent）的 dataset/ 目录仅含生成脚本，实际评测使用 BLINK Multi-view / MindCube / VSI-Bench 等已有外部 benchmark |

## 注意事项

- M3-Bench 的原始视频文件（1020 个）通过 `web.json` 中的 `video_url` 字段外链，未本地下载。
- 预计算的 memory graph（`.pkl` 格式）在 HuggingFace `ByteDance-Seed/M3-Bench`，体积较大，未下载。
- 新增 benchmark 时，只取 JSON/annotation 格式的评测数据文件，跳过模型权重和原始媒体文件。
