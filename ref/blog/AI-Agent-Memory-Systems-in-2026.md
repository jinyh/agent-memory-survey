## Stop Duct-Taping RAG to Your Agent and Call It Memory — A 2026 Builder’s Guide

[

![Yogesh Yadav](https://miro.medium.com/v2/resize:fill:64:64/1*e1zFbz7gICE2P4TwU8EYsw.png)



](https://yogeshyadav.medium.com/?source=post_page---byline--96e35b818da8---------------------------------------)

12 min read

4 days ago

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:1400/1*zoIh12sK1eFMBEVQfIUrWQ.png)

I’ve been building with LLMs long enough to remember when “memory” meant stuffing the last five messages into the system prompt and calling it a day. We’ve come a long way since then — but also, frankly, not far enough.

The problem hasn’t changed. Your agent finishes a conversation, the context window closes, and everything that just happened — every user preference, every decision, every piece of nuance — evaporates. Next session, you’re a stranger again. For a chatbot demo, you can live with that. For anything production agents are supposed to _actually do_ — support, tutoring, sales, coding assistance, healthcare — it’s a silent killer that quietly destroys trust and retention before you’ve even noticed.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:1400/1*iGMw48MuR7ynaKPdkZd6Mw.png)

This article is an attempt to map every serious memory solution that exists right now, explain what they actually do under the hood, benchmark them honestly against each other, and tell you where the sharp edges are. I’ll also cover why a surprising number of experienced agent builders have started quietly moving away from the most popular options.

## First, Why “Just Use a Bigger Context Window” Is a Trap

Every time a new model drops with a larger context window — 128k, 200k, now a million tokens — someone inevitably posts “memory problem solved.” It isn’t.

There are two reasons this argument falls apart in production. First, conversations with real users don’t stay neatly scoped to a single topic. A user might tell you they’re vegetarian at the start of a chat about recipes, spend an hour asking you to debug their Python code, then come back three days later asking for dinner ideas. A full-context model would need to reason through all that noise to find one relevant dietary fact. That’s expensive, slow, and often unreliable — attention mechanisms genuinely degrade over very long contexts.

Second, even Gemini’s 10-million-token window doesn’t help you when the conversation happened six weeks ago in a different session. Context windows only hold what’s _in front of them right now_. They don’t persist across time. That’s the entire problem, and a bigger window just delays the cliff you eventually fall off.

What you actually need is a system that selectively captures what matters, stores it durably, evolves it as things change, and retrieves only the relevant pieces when needed. That’s a fundamentally different problem — and that’s what the memory layer space is trying to solve.

## The Landscape: Every Serious Option Right Now

Let me break these down honestly across categories, from the production-grade players to the research frontier.

## 🏆 The First Generation: Vector Store + Extraction

This is where most builders started. The architecture is conceptually simple: extract important facts from conversations using an LLM, embed them, store them in a vector database, retrieve the top-k most relevant ones at query time. Clean, understandable, deployable.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:1400/1*-VWuI20P-Z8WwG-QLhTk3A.png)

**Mem0 (**[**mem0.ai**](http://mem0.ai/)**)**

Mem0 is probably the most widely known memory library in the agentic space right now — 41,000 GitHub stars, 14 million downloads, and AWS chose it as the exclusive memory provider for their Agent SDK. It’s earned its reputation.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:1400/1*V8N0PqYG3XkRCMHH2O7dmA.png)

The architecture is genuinely clever. Instead of storing raw conversation chunks, Mem0 runs an extraction phase that identifies salient facts from every message pair and distills them into compact natural language memories. When you add a memory, it doesn’t just dump it into a vector DB — it compares the new fact against existing memories and chooses one of four operations: ADD, UPDATE, DELETE, or NOOP. This means if a user says they moved from Mumbai to Bangalore, Mem0 will actually _delete_ the old city fact and add the new one. Most RAG systems wouldn’t handle that at all.

The Mem0 research paper (published April 2025 on ArXiv) benchmarks this rigorously against six baseline categories on the LOCOMO dataset. The headline numbers: Mem0 achieves a 67.13% LLM-as-a-Judge score on LOCOMO, with a p95 search latency of just 0.200 seconds, using only ~1,764 tokens per conversation versus 26,031 for full-context. That’s a 91% latency reduction and 90%+ token savings.

Their graph-enhanced variant, Mem0g, stores memories as directed labeled graphs (entities as nodes, relationships as edges) and particularly shines on temporal reasoning tasks — scoring 58.13% versus OpenAI’s 21.71% on time-sensitive questions. The reason OpenAI performed so poorly? It consistently failed to attach timestamps to stored memories, making chronological questions nearly impossible.

_Where it struggles:_ Real-world teams at scale have reported indexing reliability issues — memories not being added consistently, context recall failures under load, and limited native support for ingestion pipelines beyond chat. The library is a memory store, not a full memory platform. When you need connectors, pipelines, and smarter recall logic, you’re building that yourself.

**Zep (**[**getzep.com**](http://getzep.com/)**)**

Zep takes a different structural bet. Rather than flat vector storage, it builds a **temporal knowledge graph** using their open-source Graphiti library. Every memory is stored with time anchoring — Zep knows not just _what_ you said but _when_ you said it and how it relates to what came before and after.

This design makes Zep particularly strong on open-domain and temporally complex queries. The Zep team also published a rebuttal to Mem0’s paper arguing their system was misconfigured in the benchmark, claiming a corrected Zep score of 75.14% on LOCOMO — significantly above the 65.99% Mem0 reported for them.

The practical trade-off: Zep’s graph construction is thorough but expensive. The Mem0 paper found Zep’s memory footprint exceeds 600,000 tokens per conversation (versus 1,764 for Mem0), and their team’s testing found that immediate post-ingestion retrieval often failed — correct answers only appeared hours later after background graph processing completed. For real-time applications, that’s a serious constraint.

[**LangMem**](https://langchain-ai.github.io/langmem/) **by LangChain**

If your stack is already LangGraph, LangMem is the path of least resistance. It integrates natively as the long-term memory layer, supports semantic, episodic, and procedural memory types, and handles both fact extraction and behavior-level memory (i.e., it can remember _how_ an agent should act, not just _what_ it knows).

The benchmark numbers are honest and middling — 58.10% overall on LOCOMO, with a brutal p95 search latency of 59.82 seconds that makes it genuinely impractical for interactive real-time agents. It’s a great fit for offline or batch-mode agents where latency isn’t a concern. For anything conversational and live, you’ll hit walls.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:1400/1*bnKCh6roxV8zQrfvw8rKJA.png)

**Letta / MemGPT (**[**letta.com**](http://letta.com/)**)**

MemGPT, now rebranded as Letta, introduced an idea that felt ahead of its time when it launched: treat the LLM like an operating system managing its own memory. There’s a “main context” (RAM — what’s in the prompt right now), a “recall store” (recent conversation history), and an “archival store” (external long-term storage). The model itself decides when to page information in and out through function calls.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:1400/1*KKN2lHOl5qzD--ehOclyFQ.png)

The philosophical appeal is real — making memory management _transparent_ to the model, not hidden from it. Developers can inspect and edit individual memory blocks directly. The practical limitation is that the OS-paging metaphor adds complexity and latency that doesn’t always pay off on standard benchmarks, and the agentic loop overhead can make simple tasks surprisingly expensive.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:1400/1*KXoGCIlQ5nGh7dvvEbaOpw.png)

## 🔬 The Specialists

**Cognee (**[**cognee.ai**](http://cognee.ai/)**)** — Focuses on building a full knowledge graph from your data before any queries happen, combining graph structure with RAG. Backed by OpenAI and Facebook AI Research founders. Best for document-heavy use cases where you need structured entity relationships.

[**MemoryBank**](https://github.com/zhongwanjun/MemoryBank-SiliconFriend) — Research-origin system with a “forgetting mechanism” where memories decay over time if not reinforced, similar to human memory consolidation. Genuinely interesting concept; benchmark performance on LOCOMO is weak (5–9 points), which limits practical adoption.

[**A-Mem**](https://github.com/agiresearch/A-mem) — Zettelkasten-style linked memory notes where each note evolves when new related information arrives. The interconnected structure enables surprisingly good multi-hop reasoning. Accepted for LOCOMO benchmarking and actively cited in the Mem0 paper.

[**usecortex.ai**](http://usecortex.ai/) — A commercial-only memory layer positioning itself on the harder LongMemEval benchmark rather than LOCOMO. Claims 90.23% accuracy on LongMemEval-s, which if independently verified would make it the accuracy leader in the space. Built for production personalization use cases: voice agents, CS agents, coding agents. Latency and token efficiency numbers aren’t yet publicly published.

## The LOCOMO vs. LongMemEval Benchmark Wars

Before going further, you need to understand that the benchmark wars in this space are real.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:1400/1*CJ0Yw4SFB3Lo44O0VKcQYA.png)

[**LOCOMO**](https://github.com/snap-research/locomo) (used by Mem0’s paper) consists of 10 extended conversations, each ~600 dialogues and ~26,000 tokens. It’s well-controlled and widely used.

[**LongMemEval**](https://github.com/xiaowu0162/LongMemEval) (preferred by Zep, Cortex, Hindsight) tests conversations up to 1.5 million tokens across 500 questions, with five distinct temporal complexity levels. It’s broadly considered the harder, more realistic test.

The fact that different vendors benchmark on different datasets makes direct comparison nearly impossible and lets everyone claim leadership simultaneously. When a vendor only publishes numbers on one benchmark, it’s worth asking why.

## The Second Wave: Why Builders Are Moving On

Here’s the uncomfortable conversation that’s been happening in private Discords and engineering team retros for the past several months.

Mem0 and Supermemory (and to a lesser extent, the other first-gen tools) all share a fundamental architectural assumption: **memory is retrieval.** You store facts, you retrieve them. Smart storage, smart retrieval, done.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:1400/1*VwmcyL2PKsmUwqCPyZcKxg.png)

The problem is that this model breaks down in a few specific but common scenarios:

**Belief contradiction.** When a user corrects something — they changed jobs, moved cities, changed their opinion on something — first-gen systems either append the new fact alongside the old one (now you have contradictory memories), or silently overwrite with no audit trail. Neither is great.

**Long-horizon reasoning.** Answering “how has this user’s relationship with X changed over the past three months?” requires reasoning across time, not just retrieving the most semantically similar fact.

**Explainability.** When an agent makes a decision or gives a recommendation, builders increasingly need to justify _why_ — which specific memories led to that response. A vector similarity score doesn’t give you that.

**Supermemory specifically** had an additional practical problem: it worked as a proxy layer, meaning _every single LLM request_ went through their servers first. This added latency on every call, burned tokens faster, and gave developers no control over what context got injected.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:1400/1*RXAQpq-_Ipa5lP7l2AfTPw.png)

## The New Wave: Three Bets on What Comes Next

### 1\. [Hindsight](https://github.com/vectorize-io/hindsight) — Memory as Structured Belief

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:1400/1*hR3ABTkM08Ikoovx3C2u0Q.png)

Hindsight is the most architecturally ambitious system in this list. Instead of one undifferentiated memory store, it maintains **four distinct memory networks**:

-   **World Network** — objective external facts (“Paris is the capital of France”)
-   **Experience Network** — the agent’s own first-person action history (“I recommended X to this user on March 3rd”)
-   **Opinion Network** — subjective beliefs with confidence scores that update as evidence accumulates
-   **Entity/Observation Network** — synthesized profiles of people, companies, topics the agent has interacted with

The separation between _evidence_ and _inference_ is the key insight. When an agent says “I think this user prefers concise answers,” that belief lives in the Opinion Network with a confidence score — not mixed in with the factual memory “user’s name is Priya.” The belief can be updated, challenged, and explained.

The benchmark numbers back it up. On LongMemEval, Hindsight hits 91.4% overall accuracy. More telling are the per-category numbers: multi-session questions jump from 21.1% to 79.7%. Temporal reasoning from 31.6% to 79.7%. With an open-source 20B backbone, it outperforms full-context GPT-4o on the same benchmark.

It’s fully open-source, ships with an MCP server, deploys via Docker.

### 2\. [Memvid](https://github.com/memvid/memvid) — No Infrastructure, Period

Memvid takes a completely different philosophical stance: what if memory didn’t require a database at all?

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:1400/1*PPjvfluYD8N8RnceOu7bmw.png)

It packages everything — data, embeddings, search index, metadata — into a single `.mv2` file. The inspiration comes from video encoding: memories are stored as "Smart Frames" in an append-only, immutable sequence. Every frame has a content hash, timestamp, and metadata. The whole thing is a rewindable timeline in a portable file.

The performance claims are aggressive: 0.025ms P50 retrieval latency, 1,372× higher throughput than standard RAG. The LoCoMo score claim is +35% over industry average.

Why builders are interested: for agents that need to work offline, on edge devices, for individual users with portable memory, or in environments where running database infrastructure is overkill — Memvid just _works_. One file, no server, no connection strings, no ops burden.

The real limitation is worth being clear about: no concurrent writes, no ACID transactions, no fine-grained deletions. If you need to update or delete a specific memory, you’re rebuilding the file. It’s a read-mostly, append-and-search tool. For static or slow-changing memory profiles, it’s elegant. For highly dynamic memory at enterprise scale, it’s the wrong tool.

### 3\. Memobase — Two Products, One Name

There are actually two distinct projects using this name, and you’ll want to know which is which.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:1400/1*NHQMy9pvHBeFm6f2IslG5g.png)

[**memobase.ai**](http://memobase.ai/) is a cross-tool memory passport. The idea is that your Claude conversations, your Cursor sessions, and your other MCP-compatible agents all share the same persistent memory layer. You connect it once via MCP config, and memory flows across everything. It stores 1536-dimension embeddings, retrieves by semantic meaning, and uses PostgreSQL Row-Level Security for data isolation per user. Useful if you care about memory continuity across tools in your personal workflow.

[**memobase.io**](http://memobase.io/) (open source) is architecturally more interesting for app builders. Rather than storing individual memory facts, it builds a **structured evolving user profile**. Every few interactions, it enriches the profile with new information rather than appending raw memories. The design caps LLM calls per run at exactly 3, which it claims reduces token costs 40–50% versus naive memory implementations. The LOCOMO claim is SOTA, though independent verification is limited at this point.

## The Decision Framework

After all of this, here’s how I’d actually think about the choice depending on what you’re building:

**You’re building a production SaaS product and need reliable memory today:** Mem0 is still the pragmatic choice. The ecosystem integrations (CrewAI, LangGraph, Flowise) are unmatched, the SDK is mature, and the team ships fast. Accept the reliability caveats and build monitoring around them.

**You need deep temporal or relational reasoning:** Zep is the better fit. The knowledge graph structure earns its overhead when your queries involve “what did this user’s goals look like in Q1 versus now” or multi-hop entity relationships.

**You care most about accuracy and have tolerance for a newer system:** Hindsight is worth taking seriously. The benchmark numbers are the strongest in the field and the 4-network architecture addresses real failure modes. It’s newer, but it’s open source.

**You’re building offline, edge, or single-user applications:** Memvid’s zero-infrastructure model is genuinely appealing. Don’t let the unconventional architecture put you off — for the right use case, it’s the cleanest solution.

**You need cross-tool memory sharing for your own workflow:** memobase.ai solves this cleanly.

**Your stack is entirely LangGraph:** LangMem. Stop reading, just use it.

## The Meta-Point Nobody Wants to Say Out Loud

The memory layer space right now feels a lot like the vector database space felt in 2022 — a cluster of solutions each solving part of the problem, active benchmark wars, real production pain, and a consolidation wave clearly approaching.

The benchmark dispute between Mem0 and Zep, the emergence of Hindsight with a genuinely better architecture, the “no infra” bet from Memvid — all of these suggest we haven’t found the canonical answer yet.

What’s becoming clear is that the correct framing isn’t “memory as storage” but **“memory as a cognitive substrate.”** The systems that will win long-term are the ones that maintain the distinction between facts and beliefs, track how knowledge changes over time, can explain their reasoning, and stay cheap enough to actually run in production.

That description fits Hindsight better than anything else available today. Whether it, Memvid, Memobase, or something that hasn’t shipped yet ends up being the Rails of agent memory — that’s the actual question worth watching.

## Quick Reference: The Full Comparison Table

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:1400/1*TyBM3oUNHPkhWKNJ3j15hw.png)

\*Zep’s self-reported corrected score; Mem0’s paper reported 65.99%