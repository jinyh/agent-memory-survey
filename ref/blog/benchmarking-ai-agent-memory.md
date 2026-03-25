Title: Benchmarking AI Agent Memory: Is a Filesystem All You Need?  | Letta

URL Source: https://www.letta.com/blog/benchmarking-ai-agent-memory

Published Time: Mon, 23 Mar 2026 20:02:47 GMT

Markdown Content:
# Benchmarking AI Agent Memory: Is a Filesystem All You Need? | Letta

[](https://www.letta.com/)[Research ![Image 1](https://cdn.prod.website-files.com/66b5f39db6c9510dc8cbe834/68ecd074ce970e73cb212219_giphy3-ezgif.com-crop.gif)](https://www.letta.com/research)

![Image 2](https://cdn.prod.website-files.com/66b5f39db6c9510dc8cbe834/68ecd074ce970e73cb212219_giphy3-ezgif.com-crop.gif)

Product

[Letta Code Run agents locally inside your terminal](https://www.letta.com/)[Letta API Build agents into your apps with our API](https://app.letta.com/)![Image 3](https://cdn.prod.website-files.com/66b5f39db6c9510dc8cbe834/68ecd074ce970e73cb212219_giphy3-ezgif.com-crop.gif)

![Image 4](https://cdn.prod.website-files.com/66b5f39db6c9510dc8cbe834/68ecd074ce970e73cb212219_giphy3-ezgif.com-crop.gif)

Resources

[Blog Learn about product and research updates](https://www.letta.com/blog)[Customer Stories Read about Letta in production](https://www.letta.com/case-studies)[Demos See Letta in action](https://www.letta.com/demos)[Model Leaderboard Understand which LLMs work best](https://leaderboard.letta.com/)[Developer Community Join the Letta community on Discord](https://discord.gg/letta)![Image 5](https://cdn.prod.website-files.com/66b5f39db6c9510dc8cbe834/68ecd074ce970e73cb212219_giphy3-ezgif.com-crop.gif)

![Image 6](https://cdn.prod.website-files.com/66b5f39db6c9510dc8cbe834/68ecd074ce970e73cb212219_giphy3-ezgif.com-crop.gif)

Company

[About us Learn about our mission and team](https://www.letta.com/about-us)[Careers Join our team to work on open AI](https://jobs.ashbyhq.com/letta)[Contact us Get in touch](https://www.letta.com/cdn-cgi/l/email-protection#eb8884859f8a889fab878e9f9f8ac5888486d4989e89818e889fd6a884859f8a889fced9dba78e9f9f8a)![Image 7](https://cdn.prod.website-files.com/66b5f39db6c9510dc8cbe834/68ecd074ce970e73cb212219_giphy3-ezgif.com-crop.gif)

[Pricing ![Image 8](https://cdn.prod.website-files.com/66b5f39db6c9510dc8cbe834/68ecd074ce970e73cb212219_giphy3-ezgif.com-crop.gif)](https://www.letta.com/pricing)

[Letta Developer Platform](https://app.letta.com/)
Use the Letta API to build agents that can actually remember and learn about your users over time. Open source, production ready, and fully model-agnostic.

[Letta Code](https://docs.letta.com/letta-code)
Letta Code is a memory-first coding harness, built on top of the Letta API. Instead of working in independent sessions, you work with a persisted agent that learns over time and is portable across models.

Light

Dark

[11.3K](https://github.com/cpacker/MemGPT)

Menu

Close

[19K](https://github.com/letta-ai/letta-code)[Docs](https://docs.letta.com/)[Sign In](https://app.letta.com/)

Light

Dark

Research

# Benchmarking AI Agent Memory: Is a Filesystem All You Need?

August 12, 2025

![Image 9](https://cdn.prod.website-files.com/66bb3d1f468f0f3848a20a84/689ad5b144245a7bee0bb80a_evaluation%402x.png)

**_Summary_**_: Letta agents running on `gpt-4o-mini` achieve 74.0% accuracy on LoCoMo by simply storing conversation histories in files, rather than using specialized memory or retrieval tools. This suggests that: 1) current memory benchmarks may not be very meaningful, and 2) memory is more about how agents manage context than the exact retrieval mechanism used._

## Memory for AI Agents

Since the dawn of GPT-4, LLMs have been their limited context length. Without long-term memory, LLMs and agents face significant limitations: they forget information, cannot learn and improve over time, and lose track of their objectives during long-running, complex tasks (a phenomenon often referred to as “derailment”).

[MemGPT](https://arxiv.org/abs/2310.08560) introduced [memory management for agents](https://www.letta.com/blog/agent-memory) by creating a memory hierarchy inspired by a traditional operating system (OS). Agents actively manage what remains in their immediate context (core memory) versus what gets stored in external layers (conversational memory, archival memory, and external files) that can be retrieved as needed. This approach allows agents to maintain unlimited memory capacity within fixed context windows. Many agentic systems today, including Letta, implement MemGPT’s design to enable long-term memory in LLM agents.

Additionally, various memory-specific tools have emerged to offer "memory" as a pluggable service, providing agents with tools to store and retrieve information, often using specialized knowledge graphs or vector database solutions.

## Attempts at Benchmarking Memory Tools (e.g., Mem0, LangMem, Zep)

Evaluating the effectiveness of these memory tools in isolation is extremely challenging. The quality of an agent's memory often depends more on the underlying agentic system's ability to manage context and call tools than on the memory tools themselves. For example, even if a search tool is theoretically more performant, it won't work well for memory if the agent cannot use it effectively (due to poor prompting or lack of examples in training data).

As a result, evaluation of memory tools has primarily focused on retrieval benchmarks like LoCoMo, rather than agentic memory itself. [LoCoMo](https://snap-research.github.io/locomo/) is a question-answering benchmark focusing on retrieval from long conversations. Each sample contains two fictional speakers and a list of AI-generated, timestamped conversations. The task involves answering questions about the speakers or facts presented in their conversations.

One memory tool creator, Mem0, published [controversial results](https://www.reddit.com/r/LangChain/comments/1kash7b/i_benchmarked_openai_memory_vs_langmem_vs_letta/) claiming to have run MemGPT on LoCoMo. The results were puzzling, since our research team (the same team behind MemGPT) was unable to determine a way to backfill LoCoMo data into MemGPT/Letta without significant refactoring of the codebase. Mem0 [did not respond](https://github.com/mem0ai/mem0/issues/3004) to requests for clarification on how the benchmarking numbers were computed, or provide any modified MemGPT implementation that supports meaningful backfill of LoCoMo data.

## Benchmarking Letta Filesystem with LoCoMo

Although Letta does not have a native way to ingest conversational histories like those in LoCoMo, we recently added support for connecting files to Letta agents (including MemGPT agents) - called [Letta Filesystem](http://www.letta.com/blog/letta-filesystem). We were curious to see how Letta would perform by simply placing the LoCoMo conversational history into a file, without any specialized memory tools.

When files are attached to a Letta agent, the agent gains access to a set of file operation tools:

*   `grep`
*   `search_files`
*   `open`
*   `close`

The conversational data is placed into a file, which is uploaded and attached to the agent. Files in Letta are automatically parsed and embedded to enable semantic (vector) search over their contents. The agent is given tools for semantic search (search_files), text matching (grep), and answering questions (answer_question).

We used GPT-4o mini for the agent to match the original experiment that was said to have been run with MemGPT. Since GPT-4o mini is a weaker model, we made the agent only partially autonomous by defining tool rules to limit the agent's tool-calling patterns. The agent must start by calling search_files and continue searching through files until it decides to call answer_question and terminate. What it searches for and how many times it calls tools is up to the agent.

This simple agent achieves **74.0%** on LoCoMo with GPT-4o mini and minimal prompt tuning, significantly above Mem0's reported 68.5% score for their top-performing graph variant.

## Why Does a Filesystem Beat Specialized Memory Tools?

Agents today are highly effective at using tools, especially those likely to have been in their training data (such as filesystem operations). As a result, specialized memory tools that may have originally been designed for single-hop retrieval are less effective than simply allowing the agent to autonomously search through data with iterative querying.

Agents can generate their own queries rather than simply searching the original questions (e.g., transforming "How does Calvin stay motivated when faced with setbacks?" into "Calvin motivation setbacks"), and they can continue searching until the right data is found.

## Memory for Agents: Agent Capabilities Matter More Than the Tools

Whether an agent "remembers" something depends on whether it successfully retrieves the right information when needed. Therefore, it's much more important to consider whether an agent will be able to effectively use a retrieval tool (knowing when and how to call it) rather than focusing on the exact retrieval mechanisms (e.g. knowledge graphs vs vector databases).

Agents today are extremely effective at using filesystem tools, largely due to post-training optimization for agentic coding tasks. In general, simpler tools are more likely to be in the training data of an agent and therefore more likely to be used effectively. While more complex solutions like knowledge graphs may help in specific domains, they may also come at the cost of being more difficult for the LLM (agent) to understand.

## How to Properly Evaluate Agent Memory

An agent's memory depends on the agent architecture, its tools, and the underlying model. Comparing agent frameworks and agent memory tools is like comparing apples to oranges, as you can always mix and match frameworks and tools (and, of course, models).

The [Letta Memory Benchmark](https://www.letta.com/blog/letta-leaderboard) (Letta Leaderboard) provides an apples-to-apples comparison evaluating different models' capabilities in terms of memory management, keeping the framework (currently just Letta) and tools constant. The benchmark creates memory interactions on-the-fly to evaluate memory in a dynamic context, rather than just retrieval (as with LoCoMo).

Another approach to evaluating memory is to assess the agent's holistic performance on specific tasks that require memory. One example is [Terminal-Bench](https://www.tbench.ai/), which evaluates how well agents can solve complex, long-running tasks. Because tasks are long-running and require processing far more state than what fits into context, agents can leverage their memory to keep track of their task state and progress. Letta's OSS terminal-use agent is currently [#4 overall (#1 for OSS)](https://www.letta.com/blog/terminal-bench) on the Terminal-Bench coding benchmark.

## Conclusion

With a well-designed agent, even simple filesystem tools are sufficient to perform well on retrieval benchmarks such as LoCoMo. More complex memory tools can be plugged into agent frameworks like Letta via MCP or custom tools.

For more resources, see:

*   [Letta Memory Benchmark](https://www.letta.com/blog/letta-leaderboard) for evaluating model capabilities for agentic memory
*   [Code](https://github.com/letta-ai/letta-leaderboard/blob/main/leaderboard/locomo/locomo_benchmark.py#L784) for running the LoCoMo benchmark

You can get started with Letta agents on [Letta Platform](https://app.letta.com/).

[Back](https://www.letta.com/trash/old-blog)

[Twitter/X](https://www.letta.com/blog/benchmarking-ai-agent-memory#)[LinkedIn](https://www.letta.com/blog/benchmarking-ai-agent-memory#)

[## Company Company announcements, partnerships](https://www.letta.com/blog-categories/company)

[](https://www.letta.com/blog/our-next-phase)

![Image 10](https://cdn.prod.website-files.com/66bb3d1f468f0f3848a20a84/69b888444f1a4fb5ed73a178_benchmarking%20experiments%402x%20copy.png)

Mar 16, 2026

Letta's next phase

Letta builds agents that learn. Agents with persistent memory, real computer access, and the infrastructure to improve from their own lived experience and work. Letta Code is the runtime that brings these together: git-backed memory, skills, subagents, and deployment that works across every model provider.

[](https://www.letta.com/blog/agent-memory)

![Image 11](https://cdn.prod.website-files.com/66bb3d1f468f0f3848a20a84/686b5e988ad87717a55fca3f_letta_graphs_2x.webp)

Jul 7, 2025

Agent Memory: How to Build Agents that Learn and Remember

Traditional LLMs operate in a stateless paradigm—each interaction exists in isolation, with no knowledge carried forward from previous conversations. Agent memory solves this problem.

[](https://www.letta.com/blog/guide-to-context-engineering)

![Image 12](https://cdn.prod.website-files.com/66bb3d1f468f0f3848a20a84/6866c72419989f4527ad72d4_letta_CPU.OS%402x.png)

Jul 3, 2025

Anatomy of a Context Window: A Guide to Context Engineering

As AI agents become more sophisticated, understanding how to design and manage their context windows (via context engineering) has become crucial for developers.

[](https://www.letta.com/blog/memory-blocks)

![Image 13](https://cdn.prod.website-files.com/66bb3d1f468f0f3848a20a84/6824ff9e8b9b8cfa0b38d37d_memory-h-l4.png)

May 14, 2025

Memory Blocks: The Key to Agentic Context Management

Memory blocks offer an elegant abstraction for context window management. By structuring the context into discrete, functional units, we can give LLM agents more consistent, usable memory.

[](https://www.letta.com/blog/rag-vs-agent-memory)

![Image 14](https://cdn.prod.website-files.com/66bb3d1f468f0f3848a20a84/67aafd6c88a6c68cca350b59_letta_books%402x.webp)

Feb 13, 2025

RAG is not Agent Memory

Although RAG provides a way to connect LLMs and agents to more data than what can fit into context, traditional RAG is insufficient for building agent memory.

[](https://www.letta.com/blog/stateful-agents)

![Image 15](https://cdn.prod.website-files.com/66bb3d1f468f0f3848a20a84/67a44735ae8c2311297490c9_letta_memory_2x.webp)

Feb 6, 2025

Stateful Agents: The Missing Link in LLM Intelligence

Introducing “stateful agents”: AI systems that maintain persistent memory and actually learn during deployment, not just during training.

[](https://www.letta.com/blog/ai-agents-stack)

![Image 16](https://cdn.prod.website-files.com/66bb3d1f468f0f3848a20a84/6735971c9bed4dbe4fd98d55_BlogPost_01.webp)

Nov 14, 2024

The AI agents stack

Understanding the AI agents stack landscape.

[](https://www.letta.com/blog/deeplearning-ai-llms-as-operating-systems-agent-memory)

![Image 17](https://cdn.prod.website-files.com/66bb3d1f468f0f3848a20a84/6732732bb6386c6228ad1ae9_letta_dlai_grey.webp)

Nov 7, 2024

New course on Letta with DeepLearning.AI

DeepLearning.AI has released a new course on agent memory in collaboration with Letta.

[](https://www.letta.com/blog/announcing-letta)

![Image 18](https://cdn.prod.website-files.com/66bb3d1f468f0f3848a20a84/67314733cc0d8719cd76879f_letta_intro.webp)

Sep 23, 2024

Announcing Letta

We are excited to publicly announce Letta.

[](https://www.letta.com/blog/memgpt-and-letta)

![Image 19](https://cdn.prod.website-files.com/66bb3d1f468f0f3848a20a84/67314a470f07af58bc65b179_letta_memgpt.webp)

Sep 23, 2024

MemGPT is now part of Letta

The MemGPT open source project is now part of Letta.

[## Product Release notes, feature announcements](https://www.letta.com/blog-categories/product)

[](https://www.letta.com/blog/remote-environments-for-letta-code)

![Image 20](https://cdn.prod.website-files.com/66bb3d1f468f0f3848a20a84/69a8d1c01ac29115443782de_remote-envs.png)

Mar 4, 2026

Remote Environments for Letta Code

Using remote environments, you can message an agent working on your laptop from your phone.

[](https://www.letta.com/blog/conversations)

![Image 21](https://cdn.prod.website-files.com/66bb3d1f468f0f3848a20a84/69712b4b2e0b7a130e8915aa_data%20streams%402x.png)

Jan 21, 2026

Conversations: Shared Agent Memory across Concurrent Experiences

The Conversations API allows you to build agents that can maintain shared memory across parallel experiences with users

[](https://www.letta.com/blog/letta-code)

![Image 22](https://cdn.prod.website-files.com/66bb3d1f468f0f3848a20a84/69419caea50a5208e60e88d9_letta-code-blog-thumb.png)

Dec 16, 2025

Letta Code: A Memory-First Coding Agent

Introducing Letta Code, a memory-first coding agent. Letta Code is the #1 model-agnostic open source agent on the leading AI coding benchmark Terminal-Bench.

[](https://www.letta.com/blog/programmatic-tool-calling-with-any-llm)

![Image 23](https://cdn.prod.website-files.com/66bb3d1f468f0f3848a20a84/692dff0f8c7ecba7ca2db3fe_scale%20growing%402x.png)

Dec 1, 2025

Programmatic Tool Calling with any LLM

The Letta API now supports programmatic tool calling for any LLM model, enabling agents to generate their own workflows.

[](https://www.letta.com/blog/letta-evals)

![Image 24](https://cdn.prod.website-files.com/66bb3d1f468f0f3848a20a84/68f9cce19e13b738da57f275_evals2x.png)

Oct 23, 2025

Letta Evals: Evaluating Agents that Learn

Introducing Letta Evals: an open-source evaluation framework for systematically testing stateful agents.

[](https://www.letta.com/blog/letta-v1-agent)

![Image 25](https://cdn.prod.website-files.com/66bb3d1f468f0f3848a20a84/68edb440587079f73297d6f0_agentic-loop.webp)

Oct 14, 2025

Rearchitecting Letta’s Agent Loop: Lessons from ReAct, MemGPT, & Claude Code

Introducing Letta's new agent architecture, optimized for frontier reasoning models.

[](https://www.letta.com/blog/introducing-sonnet-4-5-and-the-memory-omni-tool-in-letta)

![Image 26](https://cdn.prod.website-files.com/66bb3d1f468f0f3848a20a84/68dc3e4f0f4b902c1443470f_tool_usage.webp)

Sep 30, 2025

Introducing Claude Sonnet 4.5 and the memory omni-tool in Letta

Letta agents can now take full advantage of Sonnet 4.5’s advanced memory tool capabilities to dynamically manage their own memory blocks.

[](https://www.letta.com/blog/letta-filesystem)

![Image 27](https://cdn.prod.website-files.com/66bb3d1f468f0f3848a20a84/6881a27d66b2ac405309303b_image.png)

Jul 24, 2025

Introducing Letta Filesystem

Today we're announcing Letta Filesystem, which provides an interface for agents to organize and reference content from documents like PDFs, transcripts, documentation, and more.

[](https://www.letta.com/blog/announcing-our-sdks)

![Image 28](https://cdn.prod.website-files.com/66bb3d1f468f0f3848a20a84/68012229d2774402e0e526ae_letta_fern_2x.webp)

Apr 17, 2025

Announcing Letta Client SDKs for Python and TypeScript

We've releasing new client SDKs (support for TypeScript and Python) and upgraded developer documentation

[](https://www.letta.com/blog/agent-file)

![Image 29](https://cdn.prod.website-files.com/66bb3d1f468f0f3848a20a84/67ed897786b9e1a53bd585e1_agentfile_blog_small.webp)

Apr 2, 2025

Agent File

Introducing Agent File (.af): An open file format for serializing stateful agents with persistent memory and behavior.

[](https://www.letta.com/blog/introducing-the-agent-development-environment)

![Image 30](https://cdn.prod.website-files.com/66bb3d1f468f0f3848a20a84/678685ffc445fbad06362394_ade_thumbnail.webp)

Jan 15, 2025

Introducing the Agent Development Environment

Introducing the Letta Agent Development Environment (ADE): Agents as Context + Tools

[](https://www.letta.com/blog/letta-v0-6-4-release)

![Image 31](https://cdn.prod.website-files.com/66bb3d1f468f0f3848a20a84/675ca410bbe509b8e72e2140_letta_064_release.webp)

Dec 13, 2024

Letta v0.6.4 release

Letta v0.6.4 adds Python 3.13 support and an official TypeScript SDK.

[](https://www.letta.com/blog/letta-v0-5-2-release)

![Image 32](https://cdn.prod.website-files.com/66bb3d1f468f0f3848a20a84/6731407133e684213a75bcfe_letta_v052.webp)

Nov 6, 2024

Letta v0.5.2 release

Letta v0.5.2 adds tool rules, which allows you to constrain the behavior of your Letta agents similar to graphs.

[](https://www.letta.com/blog/letta-v0-5-1-release)

![Image 33](https://cdn.prod.website-files.com/66bb3d1f468f0f3848a20a84/67313f239f7f093166906290_letta_v051.webp)

Oct 23, 2024

Letta v0.5.1 release

Letta v0.5.1 adds support for auto-loading entire external tool libraries into your Letta server.

[](https://www.letta.com/blog/letta-v0-5-release)

![Image 34](https://cdn.prod.website-files.com/66bb3d1f468f0f3848a20a84/67313cb6ab1b61326e745837_letta_v05.webp)

Oct 14, 2024

Letta v0.5 release

Letta v0.5 adds dynamic model (LLM) listings across multiple providers.

[](https://www.letta.com/blog/letta-v0-4-1-release)

![Image 35](https://cdn.prod.website-files.com/66bb3d1f468f0f3848a20a84/67313680e8dcc90d962a4439_letta_v041.webp)

Oct 3, 2024

Letta v0.4.1 release

Letta v0.4.1 adds support for Composio, LangChain, and CrewAI tools.

[## Research Sleep-time compute, anatomy of a context window](https://www.letta.com/blog-categories/research)

[](https://www.letta.com/blog/context-repositories)

![Image 36](https://cdn.prod.website-files.com/66bb3d1f468f0f3848a20a84/698e42db9ca2d206d0e588bb_image%20(5).png)

Feb 12, 2026

Introducing Context Repositories: Git-based Memory for Coding Agents

We're introducing Context Repositories, a rebuild of how memory works in Letta Code based on programmatic context management and git-based versioning.

[](https://www.letta.com/blog/continual-learning)

![Image 37](https://cdn.prod.website-files.com/66bb3d1f468f0f3848a20a84/6939e1df2872ece8e8298a83_sound_waves%402x.png)

Dec 11, 2025

Continual Learning in Token Space

At Letta, we believe that learning in token space is the key to building AI agents that truly improve over time. Our interest in this problem is driven by a simple observation: agents that can carry their memories across model generations will outlast any single foundation model.

[](https://www.letta.com/blog/skill-learning)

![Image 38](https://cdn.prod.website-files.com/66bb3d1f468f0f3848a20a84/692f4687c4226272753e94b9_speed%402x.png)

Dec 2, 2025

Skill Learning: Bringing Continual Learning to CLI Agents

Today we’re releasing Skill Learning, a way to dynamically learn skills through experience. With Skill Learning, agents can use their past experience to actually improve, rather than degrade, over time.

[](https://www.letta.com/blog/context-bench-skills)

![Image 39](https://cdn.prod.website-files.com/66bb3d1f468f0f3848a20a84/690e3f466f9e5a266a7823d7_tracing%20and%20understanding%402x.png)

Nov 7, 2025

Can Any Model Use Skills? Adding Skills to Context-Bench

Today we're releasing Skill Use, a new evaluation suite inside of Context-Bench that measures how well models discover and load relevant skills from a library to complete tasks.

[](https://www.letta.com/blog/context-bench)

![Image 40](https://cdn.prod.website-files.com/66bb3d1f468f0f3848a20a84/6903098c91ecf5051a3ba64a_tokens%20words%402x.png)

Oct 30, 2025

Context-Bench: Benchmarking LLMs on Agentic Context Engineering

We are open-sourcing Context-Bench, which evaluates how well language models can chain file operations, trace entity relationships, and manage multi-step information retrieval in long-horizon tasks.

[](https://www.letta.com/blog/recovery-bench)

![Image 41](https://cdn.prod.website-files.com/66bb3d1f468f0f3848a20a84/68edd9502e6ba397447c9ee3_recovery.webp)

Aug 27, 2025

Introducing Recovery-Bench: Evaluating LLMs' Ability to Recover from Mistakes

We're excited to announce Recovery-Bench, a benchmark and evaluation method for measuring how well agents can recover from errors and corrupted states.

[](https://www.letta.com/blog/terminal-bench)

![Image 42](https://cdn.prod.website-files.com/66bb3d1f468f0f3848a20a84/68924a831b743fff4eaadc89_terminalbench-thumb.png)

Aug 5, 2025

Building the #1 open source terminal-use agent using Letta

We built the #1 open-source agent for terminal use, achieving 42.5% overall score on Terminal-Bench ranking 4th overall and 2nd among agents using Claude 4 Sonnet.

[](https://www.letta.com/blog/letta-leaderboard)

![Image 43](https://cdn.prod.website-files.com/66bb3d1f468f0f3848a20a84/6838bc001f142182a0d48fbb_letta-leaderboard-thumb.webp)

May 29, 2025

Letta Leaderboard: Benchmarking LLMs on Agentic Memory

We're excited to announce the Letta Leaderboard, a comprehensive benchmark suite that evaluates how effectively LLMs manage agentic memory.

[](https://www.letta.com/blog/sleep-time-compute)

![Image 44](https://cdn.prod.website-files.com/66bb3d1f468f0f3848a20a84/68065943b27ea6238e9d427e_sleeptime_header_wide.webp)

Apr 21, 2025

Sleep-time Compute

Sleep-time compute is a new way to scale AI capabilities: letting models "think" during downtime. Instead of sitting idle between tasks, AI agents can now use their "sleep" time to process information and form new connections by rewriting their memory state.

in this article

[This is some text inside of a div block.](https://www.letta.com/blog/benchmarking-ai-agent-memory#)

[](https://www.letta.com/)

### Product

[What is Letta](https://www.letta.com/#product)

[Customers](https://www.letta.com/case-studies)[Research](https://www.letta.com/research)[News](https://www.letta.com/blog)

### DEVELOPERS

[GitHub 11.9K](https://github.com/letta-ai/letta-code)[Documentation](http://docs.letta.com/)[Community](https://discord.com/invite/letta)[Demos](https://www.letta.com/demos)

### Company

[About us](https://www.letta.com/about-us)[Open positions](https://www.letta.com/about-us#joinus)[Privacy policy](https://www.letta.com/privacy-policy)[Terms of service](https://www.letta.com/terms-of-service)

### Newsletter

Thank you, you are subscribed

Oops! Something went wrong while submitting the form.

Follow Letta

Follow Letta

Follow Letta

Follow Letta

Follow Letta

Follow Letta

[GitHub](https://github.com/letta-ai/letta)[Discord](https://discord.gg/letta)[Twitter/X](https://x.com/letta_ai)[Bluesky](https://bsky.app/profile/letta.com)[Instagram](https://www.letta.com/blog/benchmarking-ai-agent-memory#)[YouTube](https://www.youtube.com/@letta-ai)[LinkedIn](https://www.linkedin.com/company/letta-ai)
