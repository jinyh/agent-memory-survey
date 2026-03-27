Title: Yohei on X: "The state of AI memory systems: benchmarks, architectures, and what actually works" / X

URL Source: https://x.com/yoheinakajima/status/2037201711937577319

Published Time: Fri, 27 Mar 2026 08:03:19 GMT

Markdown Content:
## Article

## Conversation

[![Image 1: Image](https://pbs.twimg.com/media/HEWX-_ZbYAESJgL?format=jpg&name=small)](https://x.com/yoheinakajima/article/2037201711937577319/media/2037201514880786433)

The state of AI memory systems: benchmarks, architectures, and what actually works

> This research was compiled by Claude Opus 4.6 Research. Full prompt: Research the top memory benchmarks for AI systems, look at the top performing memory systems, and to the extent you can look at how they approach memory (looking at code if they are open source), note similarities and differences, and infer what you can learn about the various approaches and their strengths and weaknesses.

The single most important finding in AI memory research is that architecture matters more than model size. A 20B-parameter model with Hindsight's multi-strategy memory achieves 83.6% on LongMemEval, dramatically outperforming full-context GPT-4o at 60.2%.

Across every major benchmark, systems combining graph-based knowledge structures with multi-strategy retrieval consistently dominate, while pure vector-store approaches plateau around 50%. The field has matured rapidly from 2024-2026, with at least seven major benchmarks, a dozen serious open-source frameworks, and a clear architectural consensus emerging: hybrid storage (vector + graph), temporal awareness, and active memory consolidation are the three pillars of high-performing memory systems.

The proliferation of memory benchmarks in 2024-2026 reflects both the field's importance and dissatisfaction with earlier evaluation approaches. Each benchmark addresses a different failure mode.

LongMemEval has emerged as the gold standard. Published by Wu et al.

and accepted at ICLR 2025, it tests five core abilities — information extraction, multi-session reasoning, temporal reasoning, knowledge updates,

and abstention — across 500 manually curated questions

embedded in conversations scaling from ~115K tokens (LongMemEval_S) to

1.5 million tokens (LongMemEval_M).

Its three-stage framework (Indexing → Retrieval → Reading) with LLM-as-judge scoring provides the most rigorous evaluation available.

Commercial chat assistants show a 30-60% accuracy drop on sustained interactions,

and even full-context GPT-4o achieves only 60-64%.

LoCoMo (ACL 2024, Snap Research/UNC Chapel Hill) tests long-term conversational memory across 10 conversations of ~300 turns each,

evaluating single-hop QA, multi-hop reasoning, temporal reasoning, and adversarial questions.

Despite wide adoption, LoCoMo has significant limitations: relatively short conversations (~9K tokens),

data quality concerns, and fierce vendor disputes about proper implementation

— Mem0 and Zep have publicly contradicted each other's reported scores,

making LoCoMo rankings unreliable for cross-vendor comparison.

MemBench (ACL 2025 Findings) uniquely distinguishes factual memory (explicitly stated information) from reflective memory (implicitly derived information) across participation and observation scenarios.

MemoryBench (Tsinghua, 2025) pioneers evaluation of continual learning from user feedback

across

11 datasets, 3 domains, and 2 languages.

MemoryAgentBench (ICLR 2026) tests four competencies — accurate retrieval, test-time learning, long-range understanding, and conflict resolution

— revealing that no existing method excels at all four simultaneously.

EverMemBench (February 2026) uniquely targets multi-party group conversations,

and the Letta Leaderboard evaluates how effectively LLMs manage their own memory through autonomous tool calls.

The cross-benchmark consensus: temporal reasoning is consistently the hardest capability, showing the largest performance gaps between systems and humans (up to 73% gap on LoCoMo).

Systems that don't model time explicitly score poorly across all benchmarks.

Hindsight (Vectorize, December 2025) holds the current state of the art: 91.4% on LongMemEval

with Gemini-3 Pro, and 89.61% on LoCoMo.

Even its smaller open-source variants score impressively — 83.6% with a 20B model and 89.0% with a 120B model.

These numbers dwarf every other system on the most challenging benchmark.

The architecture separates memory into four logical networks: world facts, agent experiences, entity observations, and evolving opinions/beliefs.

This epistemic separation — structurally distinguishing evidence from inference — is a key innovation. Rather than treating all memories uniformly, Hindsight routes different types of information to different stores with different retrieval characteristics.

Retrieval runs four concurrent strategies: cosine semantic similarity, BM25 keyword matching, graph traversal across the shared memory graph, and temporal reasoning. Results from all four are fused via cross-encoder reranking.

This multi-strategy approach is the single biggest performance differentiator — on temporal queries specifically, Hindsight improved from a 31.6% baseline to

91.0%, a nearly 60-point gain.

The system also stores dual timestamps (occurrence time and mention time), enabling both "what happened when" and "what did I learn when" queries.

It is open source under the MIT license.

Zep's core engine, Graphiti (Apache 2.0,

24K+ GitHub stars), builds a formally defined graph G = (N, E, ϕ) organized into three hierarchical tiers. The episode subgraph stores raw conversation turns as non-lossy data. The semantic entity subgraph extracts entities and their relationships as persistent facts. The community subgraph uses label propagation to cluster strongly connected entities with high-level summaries

— mirroring the psychological distinction between episodic and semantic memory.

Graphiti's most important innovation is its bi-temporal data model. Every entity edge tracks four timestamps: valid_at (when the fact became true in the world), invalid_at (when it was superseded), created_at (when Graphiti ingested it), and expired_at (when the record was logically replaced).

This enables point-in-time queries ("What did we know about X on date Y?"), historical reasoning about fact evolution, and full audit trails — critical for enterprise compliance.

Contradicting facts are invalidated rather than deleted, preserving the complete temporal record.

The retrieval pipeline f(α) = χ(ρ(φ(α))) runs three concurrent search strategies: cosine similarity on embeddings, BM25 full-text search, and breadth-first graph traversal from seed nodes.

Critically, no LLM calls occur during retrieval — everything is pre-computed via vector, BM25, and graph indexes,

achieving sub-200ms to sub-second latency

(P95 ~300ms in Zep Cloud). Reranking options include reciprocal rank fusion, maximal marginal relevance, cross-encoder scoring, node distance, and episode-mentions frequency.

On benchmarks, Zep achieves 71.2% on LongMemEval (GPT-4o)

and claims 75.14% ± 0.17 on LoCoMo after correcting what it calls implementation errors in Mem0's evaluation.

On MemGPT's own Deep Memory Retrieval benchmark, Zep scored 94.8-

98.2%, outperforming MemGPT itself.

The main tradeoff: Graphiti's thorough graph construction is expensive in compute and time — ingestion for large corpora can take hours due to multiple LLM calls for entity extraction, resolution, and relationship inference.

Entity extraction uses a reflection technique (inspired by Reflexion) to minimize hallucinations during LLM-based extraction.

Entity resolution operates in two phases: first computing 1024D embedding similarity plus full-text search to find candidates, then using an LLM to determine if candidates are true duplicates.

Edge deduplication is constrained to edges between the same entity pairs, significantly reducing computational complexity.

Graphiti supports four pluggable graph database backends: Neo4j (primary), FalkorDB, Kuzu (embedded), and Amazon Neptune.

MemGPT (UC Berkeley, ICML 2024) introduced the most conceptually distinctive approach: the LLM manages its own memory, analogous to an operating system managing virtual memory. The context window is "physical RAM," external databases are "disk," and the agent pages data in and out through function calls.

This was productionized as Letta (Apache 2.0,

~20.9K GitHub stars), backed by the original Berkeley researchers.

The memory hierarchy has three tiers. Core memory (analogous to RAM) consists of size-limited, read-write text blocks

— typically a "human" block storing user facts and a "persona" block containing the agent's self-concept,

each capped at ~2K characters.

Recall memory stores the complete, uncompressed history of all messages as a searchable database. Archival memory provides general-purpose long-term storage

backed by PostgreSQL with pgvector, supporting semantic search with HNSW indexing.

The defining feature is self-directed memory operations. The agent decides when, what, and where to store or retrieve through explicit function calls:

core_memory_append, core_memory_replace,

memory_rethink (complete block rewrite), archival_memory_search, and archival_memory_insert. Even sending a message to the user is a function call — there is no native chat mode.

Memory pressure warnings at ~70% context capacity give the agent a chance to save critical information before forced eviction at ~100%, when a recursive summary compresses evicted messages.

Sleep-time compute (April 2025 paper) addressed MemGPT's main weakness — memory management consuming user-facing latency.

Background "sleep-time agents" process information during idle periods using stronger/slower models, producing refined "learned context" written to shared memory blocks.

This separates memory management from conversation, achieving both better memory quality and lower response latency.

On benchmarks, MemGPT showed dramatic improvements over baselines: GPT-4 Turbo jumped from 35.3% to 93.4% on Deep Memory Retrieval when augmented with MemGPT's memory system.

A striking finding: Letta demonstrated that a simple filesystem approach (agent + file tools) achieved 74.0% on LoCoMo with GPT-4o-mini, outperforming Mem0's best score of 68.5% — suggesting that agent capability matters more than specialized memory infrastructure.

The system uses PostgreSQL with 42+ database tables and Alembic for migrations,

with the complete agent state serializable to an open Agent File (.af) format.

Mem0 (Y Combinator, $24M raised October 2025, ~48K GitHub stars)

takes the most pragmatic approach: a two-phase extraction-update pipeline that converts conversations into discrete natural-language facts stored in a vector database, with optional graph enhancement.

The extraction phase combines three context sources — conversation summary, last 10 messages, and the new message pair — and uses an LLM to extract candidate memory facts.

The update phase retrieves the top 10 semantically similar existing memories for each new fact and presents them to the LLM, which decides one of four operations via function calling: ADD (new memory), UPDATE (augment existing), DELETE (remove contradicted), or NOOP.

This conflict resolution is entirely LLM-delegated — there is no product-level orchestration layer,

making it flexible but opaque.

The optional graph variant (Mem0ᵍ) stores entities and relationships in a directed labeled graph G=(V,E,L),

using dual retrieval: entity-centric search (identify entities → traverse neighbors) and semantic triplet search (embed full query → match against relationship encodings).

Vector and graph operations run in parallel via concurrent.futures.ThreadPoolExecutor.

Storage supports 24+ vector stores (default: Qdrant), 5+ graph stores (default: Neo4j),

with every operation logged to SQLite for audit trails.

Mem0 achieves 66.9-68.5% on LoCoMo (base and graph variants respectively) with excellent latency — 1.40s p95 versus 17.12s for full-context

and 60s for LangMem.

However, it scores only ~49% on LongMemEval, revealing that its single/dual-strategy semantic retrieval struggles with diverse query types at scale.

The graph variant adds ~3 points on temporal reasoning

but doesn't close the gap with graph-native systems. Key weaknesses: no bi-temporal modeling, no fact/opinion separation, no BM25/keyword search in the base variant, no confidence scores, and no built-in forgetting/decay mechanism.

Cognee (Topoteretes, Berlin, $7.5M seed

February 2026, ~12K GitHub stars) builds the richest knowledge representation through its three-store architecture

— graph (Kuzu), vector (LanceDB), and relational (SQLite) — all file-based by default for zero-infrastructure local development, swappable to production databases (Neo4j, Qdrant, PostgreSQL) for scale.

The core abstraction is the DataPoint, a Pydantic model that carries content and metadata. Every entity, chunk, summary, and relationship is a DataPoint with configurable embedding fields.

The cognify() pipeline runs six stages: classify documents → check permissions → extract chunks → extract graph (using Instructor for structured LLM output) → summarize text → embed and persist.

The optional ontology validation layer uses RDF/OWL ontologies to canonicalize extracted entities — fuzzy matching via difflib.get_close_matches() resolves "car manufacturer," "automobile maker," and "vehicle producer" to a single canonical node, dramatically reducing graph fragmentation.

Cognee's most distinctive feature is its 14 retrieval modes, from basic RAG to graph-completion with chain-of-thought reasoning, natural language to Cypher translation, temporal search, and a "feeling lucky" mode where the LLM auto-selects the best strategy. The default GRAPH_COMPLETION mode uses vector search as a hint to find relevant graph triplets, then traverses the graph for structured context — fundamentally different from returning top-k chunks by cosine similarity.

The memify() post-processing pipeline is inspired by cognitive science: it prunes stale nodes, strengthens frequent connections, adds derived facts, and optimizes embeddings.

An internal Dreamify engine tunes hyperparameters (chunking strategy, extraction approach, retrieval mode, prompting) for optimal performance.

On HotPotQA, chain-of-thought graph traversal improved exact match scores by 1,618% over the base configuration,

and Cognee outperformed LightRAG, Graphiti, and Mem0 across all metrics in their evaluations.

However, Cognee's benchmarks are primarily self-reported; independent third-party validation is still limited.

Several additional systems contribute important ideas. HippoRAG (NeurIPS 2024, OSU-NLP) maps the hippocampal indexing theory onto LLMs + knowledge graphs + Personalized PageRank, achieving up to 20% improvement on multi-hop QA while being 10-30x cheaper than iterative retrieval. A-MEM uses a Zettelkasten-inspired approach where memories self-organize through dynamic indexing and linking without predefined schemas.

RAPTOR (Stanford, ICLR 2024) recursively clusters and summarizes text bottom-up into hierarchical trees, achieving 20% improvement on QuALITY.

MemoRAG implements a dual-system architecture with a lightweight long-range LLM for global memory generating retrieval "clues."

MemOS treats memory as a manageable system resource with three memory types (plaintext, activation/KV-cache, and parameter/LoRA weights),

claiming 159% improvement in temporal reasoning on LoCoMo.

LightRAG offers a lightweight graph+vector alternative that's much cheaper than full GraphRAG while maintaining quality.

Analyzing performance across all major benchmarks reveals clear correlations between architectural choices and results.

Pattern 1: Multi-strategy retrieval is the single biggest differentiator. Hindsight's four parallel strategies (semantic, BM25, graph traversal, temporal) with cross-encoder reranking produce 91.4% on LongMemEval.

Zep's three strategies (cosine, BM25, BFS) achieve 71.2%.

Mem0's one-to-two strategies (vector similarity, optional graph) score 49%.

The correlation is nearly linear: more diverse retrieval strategies yield better results, because different query types demand different retrieval approaches.

BM25 catches exact mentions that embedding search misses; graph traversal finds multi-hop connections invisible to flat similarity; temporal filtering prevents returning outdated facts.

Pattern 2: Graph structure is essential for complex reasoning but vector search remains important for breadth. The 22-point gap between Zep (71.2%, graph-native) and Mem0 (49.0%, vector-primary) on LongMemEval directly reflects the limitation of pure vector approaches for multi-hop, temporal, and relational queries.

However, graph-only retrieval misses semantically similar content that lacks explicit edges. Every top system uses hybrid storage.

The specific graph implementation matters less than having one — Neo4j, FalkorDB, and custom in-memory graphs all appear in high-performing systems.

Pattern 3: Temporal modeling correlates with the largest performance gains. Temporal reasoning shows the biggest gaps between systems and humans across every benchmark

(73% gap on LoCoMo).

Systems with explicit temporal modeling — Hindsight's dual timestamps, Zep's bi-temporal model,

Cognee's temporal search mode — consistently score 20-60 points higher on temporal queries than systems treating time as metadata. Mem0's basic timestamping and LangMem's minimal temporal awareness (23.4% on LoCoMo temporal questions)

illustrate the cost of ignoring time.

Pattern 4: Active memory consolidation prevents performance degradation at scale. Systems that merely accumulate memories without consolidation suffer from noise as memory grows. Hindsight's reflect operation updates beliefs based on new evidence.

Zep invalidates contradicted facts rather than deleting them

(preserving history while preventing retrieval of outdated information).

Cognee's memify pipeline prunes stale nodes and strengthens frequent connections.

Letta's sleep-time compute enables background memory refinement.

Mem0's LLM-driven ADD/UPDATE/DELETE/NOOP decisions provide consolidation but with less structural sophistication.

Pattern 5: Agent-controlled memory can outperform specialized infrastructure. Letta's demonstration that a simple filesystem approach (agent + file tools) achieves 74.0% on LoCoMo — outperforming Mem0's specialized memory infrastructure at 68.5%

— is a striking result. It suggests that giving an LLM the ability to iteratively search, read, and organize its own memory can matter more than the sophistication of the underlying storage system. However, this approach consumes tokens for memory operations and depends heavily on the underlying model's instruction-following capability.

Three tensions define the design space. Richness vs. latency: Zep's thorough graph construction produces the richest representations but takes hours for large corpora;

Mem0's lighter extraction is near-instant but misses relational structure. Autonomy vs. determinism: MemGPT/Letta's agent-controlled memory is maximally flexible but non-deterministic and model-dependent; Zep's pre-computed retrieval is fast and predictable but less adaptive. Completeness vs. compression: Zep preserves raw episodes alongside extracted knowledge (non-lossy but storage-intensive);

Mem0 extracts only "important" facts

(efficient but risks losing nuanced information).

The benchmark data strongly suggests that the field is converging on a specific architectural template: hybrid vector+graph storage, multi-strategy retrieval with reranking, explicit temporal modeling, and active memory consolidation. Hindsight's 91.4% demonstrates this template at its best.

The remaining open question is not what architecture to use, but how to make it economically practical — Hindsight's four parallel retrieval strategies with cross-encoder reranking are expensive, and Zep's graph construction requires significant LLM calls during ingestion.

The next breakthrough will likely come from making these rich architectures cheaper and faster, not from fundamentally different approaches. ******************************************************** Mentioned in article:

/ Hindsight (

)

/ Graphiti (

)

/ MemGPT (

)

(

)

(

)

/ HippoRAG (

)
