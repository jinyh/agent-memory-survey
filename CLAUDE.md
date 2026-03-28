# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository overview

AgentResearch is a research-oriented repository for agent memory. It combines:

- `docs/`: survey, method, plans, architecture decisions, and reference indexes
- `ref/`: raw source materials (`paper`, `blog`, `DeepResearch`, datasets)
- `src/`: minimal prototype implementations and reference indexing tools

The project workflow is documented in `docs/method/README.md` and `docs/method/workflow.md`. Use those as the source of truth when deciding where new work belongs.

## Common commands

### Environment setup

```bash
uv venv "$HOME/.venvs/agentresearch"
source "$HOME/.venvs/agentresearch/bin/activate"
uv sync --active --extra dev
```

### Tests

```bash
uv run --active --extra dev pytest tests/
uv run --active --extra dev pytest tests/test_memory.py -q
uv run --active --extra dev pytest tests/test_memory.py -q -k recall
```

`tests/test_memory.py -q` is the most common regression check for the memory layer.

### Run prototypes and indexing

```bash
uv run --active python -m src.memory.agent
uv run --active python -m src.memory.evaluation --out docs/memory-eval/latest
uv run --active python -m src.references
```

Use `python -m src.references` after adding new files under `ref/paper/` or `ref/blog/`, or when citations in `ref/DeepResearch/` change.

### Lint

```bash
uv run --active --extra dev ruff check .
```

## Architecture

### 1. Research workflow layer (`docs/`)

This repository is organized around a document-driven research loop rather than code-first development:

1. external inputs are collected and classified
2. evidence is organized into formal research artifacts
3. stable judgments are turned into architecture / experiment decisions
4. prototype code and evaluation results are written back into the survey

Key locations:

- `docs/method/`: workflow, artifacts, gates, traceability, and input classification rules
- `docs/survey/`: the main survey text
- `docs/survey/survey-map.md`: the long-lived survey ↔ code ↔ gap index; it is an index layer, not the body text
- `docs/plans/`: `research-brief`, `evidence-map`, `experiment-spec`, `evaluation-report`, `survey-update-note`
- `docs/architecture/`: architecture decisions that connect research judgment to implementation
- `docs/references/`: generated indexes and quality metadata for source materials

When editing survey chapters, usually sync both `docs/survey/README.md` and `docs/survey/survey-map.md`.

### 2. Memory prototype layer (`src/memory/`)

The memory prototype is intentionally a minimal multi-store memory system. The important big-picture structure is:

- `base.py`: shared types such as `MemoryItem`, `MemoryType`, and `FusionConfig`
- `episodic.py`: episodic memory store and consolidation primitives
- `graph_store.py`: graph-style semantic store
- `vector_store.py`: vector retrieval store
- `manager.py`: the orchestrator that registers stores, performs cross-store recall, updates/deletes memories, and handles consolidation
- `agent.py`: minimal agent loop using the memory system
- `evaluation.py`: repeatable evaluation harness and dataset adapters for `ref/datasets`

Important implementation detail: `MemoryManager.recall()` uses rank-based fusion, not raw score sorting. When debugging retrieval behavior, inspect `recall_with_trace()` first.

### 3. Evaluation and datasets

`src/memory/evaluation.py` normalizes datasets from `ref/datasets` into benchmark cases. Keep the distinction clear:

- dataset adapters in `evaluation.py` are for converting raw datasets into comparable cases
- retrieval-heavy datasets should not be described as full lifecycle benchmarks

The evaluation harness covers scenario construction, dataset normalization, retrieval metrics, and snapshot roundtrip checks.

### 4. Reference ingestion layer (`src/references/`)

`src/references/__main__.py` is the entrypoint for rebuilding the references layer. It:

- extracts entries from the DeepResearch report
- downloads open-access papers referenced there
- scans the repository reference library
- writes updated indexes into `docs/references/`

This is the bridge from raw materials in `ref/` to structured indexes used by the survey and research workflow.

## Repository-specific rules

- Non-paper external inputs are classified via `docs/method/blog-survey-calibration-template.md` before they enter formal artifacts.
- GitHub projects and open-source implementations are treated as engineering references by default, not as primary research evidence.
- `docs/survey/survey-map.md` should remain an index layer; do not turn it into a replacement for survey prose.
- If you are deciding whether to create or update a Claude guidance file, first check for existing files with:
  `find . -name "CLAUDE.md" -o -name ".claude.local.md"`
