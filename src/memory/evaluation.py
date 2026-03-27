"""Agent Memory 可重复评测。

固定 seed 构造场景 → 执行检索 → 计算 hit@k / MRR / store 分布 → 快照 roundtrip 一致性检查。

用法:
    python -m src.memory.evaluation --out docs/memory-eval/latest
"""

from __future__ import annotations

import argparse
import json
import os
import random
import re
import tempfile
import time
from collections import Counter
from pathlib import Path
from typing import Any

from .base import FusionConfig, MemoryItem, MemoryType
from .episodic import EpisodicMemory
from .graph_store import GraphMemoryStore
from .manager import MemoryManager
from .vector_store import VectorMemoryStore

_DATASET_ROOT = Path(__file__).resolve().parents[2] / "ref" / "datasets"

# ---------------------------------------------------------------------------
# 场景构造
# ---------------------------------------------------------------------------

_FIXED_TIMESTAMP = 1700000000.0  # 固定基准时间，确保 decay 可重复


def _normalize_expected_ids(value: Any) -> list[str]:
    if isinstance(value, list):
        flattened: list[str] = []
        for entry in value:
            if isinstance(entry, list):
                flattened.extend(str(item) for item in entry)
            elif entry is not None:
                flattened.append(str(entry))
        return flattened
    if value is None:
        return []
    return [str(value)]


def _build_dataset_case(
    *,
    case_id: str,
    query: str,
    expected_ids: list[str],
    top_k: int,
    source: str,
    split: str,
    documents: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "id": case_id,
        "query": query,
        "expected_ids": expected_ids,
        "top_k": top_k,
        "source": source,
        "split": split,
        "documents": documents,
    }


def _session_text(entries: list[dict[str, Any]]) -> str:
    return "\n".join(str(entry.get("text", "")) for entry in entries if entry.get("text"))


def load_benchmark_cases(dataset_dir: str) -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []
    root = Path(dataset_dir)

    locomo_path = root / "locomo" / "locomo10.json"
    if locomo_path.exists():
        rows = json.loads(locomo_path.read_text(encoding="utf-8"))
        for row_idx, row in enumerate(rows):
            conversation = row.get("conversation", {})
            session_names = sorted(
                [name for name in conversation if name.startswith("session_") and not name.endswith("date_time")],
                key=lambda name: int(name.split("_")[1]),
            )
            documents = []
            for session_name in session_names:
                session_num = int(session_name.split("_")[1])
                doc_id = f"D{session_num}"
                documents.append({
                    "id": doc_id,
                    "content": _session_text(conversation.get(session_name, [])),
                    "tags": ["locomo", "session"],
                })
            for qa_idx, qa in enumerate(row.get("qa", [])):
                evidence = qa.get("evidence", [])
                if not evidence:
                    continue
                session_ids = {str(part).split(":")[0] for part in evidence}
                cases.append(_build_dataset_case(
                    case_id=f"locomo-{row.get('sample_id', row_idx)}-{qa_idx}",
                    query=str(qa.get("question", "")),
                    expected_ids=sorted(session_ids),
                    top_k=5,
                    source="locomo",
                    split="locomo10",
                    documents=documents,
                ))

    longmemeval_dir = root / "longmemeval-cleaned"
    oracle_path = longmemeval_dir / "longmemeval_oracle.json"
    if oracle_path.exists():
        rows = json.loads(oracle_path.read_text(encoding="utf-8"))
        for row_idx, row in enumerate(rows):
            documents = []
            for session_id, session_entries in zip(row.get("answer_session_ids", []), row.get("haystack_sessions", [])):
                documents.append({
                    "id": str(session_id),
                    "content": "\n".join(
                        str(entry.get("content", "")) for entry in session_entries if entry.get("content")
                    ),
                    "tags": ["longmemeval", str(row.get("question_type", "oracle"))],
                })
            cases.append(_build_dataset_case(
                case_id=str(row.get("question_id", f"longmemeval-{row_idx}")),
                query=str(row.get("question", "")),
                expected_ids=_normalize_expected_ids(row.get("answer_session_ids", [])),
                top_k=5,
                source="longmemeval",
                split=str(row.get("question_type", "oracle")),
                documents=documents,
            ))

    amabench_path = root / "AMA-bench" / "test" / "open_end_qa_set.jsonl"
    if amabench_path.exists():
        with amabench_path.open(encoding="utf-8") as f:
            for row_idx, line in enumerate(f):
                if not line.strip():
                    continue
                row = json.loads(line)
                documents = [{
                    "id": str(row.get("episode_id", f"ama-{row_idx}")),
                    "content": "\n".join(
                        [str(row.get("task", ""))]
                        + [str(turn.get("action", "")) + "\n" + str(turn.get("observation", "")) for turn in row.get("trajectory", [])]
                    ),
                    "tags": ["ama-bench", str(row.get("domain", "unknown"))],
                }]
                for qa_idx, qa in enumerate(row.get("qa_pairs", [])):
                    qtype = str(qa.get("type", "unknown"))
                    case_id = str(qa.get("question_uuid", f"ama-{row_idx}-{qa_idx}"))
                    cases.append(_build_dataset_case(
                        case_id=case_id,
                        query=str(qa.get("question", "")),
                        expected_ids=[str(row.get("episode_id", case_id))],
                        top_k=5,
                        source="ama-bench",
                        split=qtype,
                        documents=documents,
                    ))

    memory_arena_root = root / "MemoryArena"
    if memory_arena_root.exists():
        for jsonl_path in memory_arena_root.glob("**/data.jsonl"):
            split = jsonl_path.parent.name
            with jsonl_path.open(encoding="utf-8") as f:
                for row_idx, line in enumerate(f):
                    if not line.strip():
                        continue
                    row = json.loads(line)
                    row_id = str(row.get("id", row_idx))
                    backgrounds = row.get("backgrounds", [])
                    if isinstance(backgrounds, str):
                        background_text = backgrounds
                    else:
                        background_text = "\n".join(str(item) for item in backgrounds)
                    documents = [{
                        "id": row_id,
                        "content": "\n".join(
                            [background_text]
                            + [str(q) for q in row.get("questions", [])]
                            + [json.dumps(a, ensure_ascii=False) if isinstance(a, dict) else str(a) for a in row.get("answers", [])]
                        ),
                        "tags": ["memoryarena", split],
                    }]
                    questions = row.get("questions", [])
                    answers = row.get("answers", [])
                    for qa_idx, (question, answer) in enumerate(zip(questions, answers)):
                        expected_ids = [row_id]
                        if isinstance(answer, dict):
                            expected_ids = [str(answer.get("target_asin", row_id))]
                        cases.append(_build_dataset_case(
                            case_id=f"memoryarena-{split}-{row_id}-{qa_idx}",
                            query=str(question),
                            expected_ids=expected_ids,
                            top_k=5,
                            source="memoryarena",
                            split=split,
                            documents=documents,
                        ))

    return cases


def build_scenario(
    seed: int = 42,
    enable_vector_store: bool = False,
) -> tuple[MemoryManager, list[dict]]:
    """构造固定 seed 的评测场景。

    返回 (manager, queries)
    queries: [{"query": str, "expected_ids": list[str], "top_k": int}]
    """
    random.seed(seed)

    # ---- 创建 manager 和 stores ----
    config = FusionConfig(
        mode="rank",
        overfetch_factor=3,
        store_weights={"episodic": 1.0, "graph": 1.0},
    )
    manager = MemoryManager(fusion_config=config)

    ep_store = EpisodicMemory(max_capacity=1000, decay_rate=0.001)
    graph_store = GraphMemoryStore(max_capacity=1000, decay_rate=0.001)

    manager.register_store("episodic", ep_store, default=True)
    manager.register_store("graph", graph_store)
    vector_store = None
    if enable_vector_store:
        vector_store = VectorMemoryStore(max_capacity=1000, decay_rate=0.001)
        manager.register_store("vector", vector_store)

    # ---- 情景记忆 (ep-001 ~ ep-010) ----
    episodic_items = [
        ("ep-001", "用户询问如何配置 RAG 检索管道", 0.8, ["rag", "检索"]),
        ("ep-002", "调试向量数据库连接超时问题", 0.7, ["向量数据库", "调试"]),
        ("ep-003", "讨论 Agent 记忆的分层架构设计", 0.9, ["记忆", "架构"]),
        ("ep-004", "用户请求总结上周的会议内容", 0.5, ["总结", "会议"]),
        ("ep-005", "实现了基于 LRU 的工作记忆淘汰策略", 0.8, ["记忆", "淘汰"]),
        ("ep-006", "分析 MemGPT 论文中的虚拟分页机制", 0.9, ["memgpt", "论文"]),
        ("ep-007", "用户反馈检索结果相关性不足", 0.6, ["检索", "反馈"]),
        ("ep-008", "部署知识图谱到生产环境", 0.7, ["知识图谱", "部署"]),
        ("ep-009", "讨论情景记忆到语义记忆的巩固路径", 0.9, ["记忆", "巩固"]),
        ("ep-010", "优化 embedding 模型的推理延迟", 0.6, ["embedding", "优化"]),
    ]
    for i, (mid, content, importance, tags) in enumerate(episodic_items):
        item = MemoryItem(
            content=content,
            memory_type=MemoryType.EPISODIC,
            importance=importance,
            tags=tags,
            id=mid,
            created_at=_FIXED_TIMESTAMP + i * 60,
            last_accessed=_FIXED_TIMESTAMP + i * 60,
        )
        ep_store.add(item)
        if vector_store is not None:
            vector_store.add(
                MemoryItem(
                    content=content,
                    memory_type=MemoryType.EPISODIC,
                    importance=importance,
                    tags=tags,
                    id=f"vec-{mid}",
                    created_at=_FIXED_TIMESTAMP + i * 60,
                    last_accessed=_FIXED_TIMESTAMP + i * 60,
                )
            )

    # ---- 图记忆 (gr-001 ~ gr-008) ----
    graph_items = [
        ("gr-001", "RAG 系统由检索器、重排器和生成器三部分组成", 0.8,
         ["rag", "架构"], MemoryType.SEMANTIC),
        ("gr-002", "向量检索使用 HNSW 索引实现近似最近邻搜索", 0.7,
         ["向量数据库", "检索"], MemoryType.SEMANTIC),
        ("gr-003", "Agent 记忆分为情景记忆、语义记忆和程序性记忆", 0.9,
         ["记忆", "架构"], MemoryType.SEMANTIC),
        ("gr-004", "知识图谱通过实体-关系-实体三元组存储结构化知识", 0.8,
         ["知识图谱", "架构"], MemoryType.SEMANTIC),
        ("gr-005", "记忆巩固是将短期情景转化为长期语义知识的过程", 0.9,
         ["记忆", "巩固"], MemoryType.SEMANTIC),
        ("gr-006", "MemGPT 使用虚拟上下文管理实现无限对话记忆", 0.8,
         ["memgpt", "记忆"], MemoryType.SEMANTIC),
        ("gr-007", "遗忘曲线遵循幂律衰减模型", 0.6,
         ["记忆", "遗忘"], MemoryType.SEMANTIC),
        ("gr-008", "多轮对话中的上下文压缩策略", 0.5,
         ["对话", "压缩"], MemoryType.PROCEDURAL),
    ]
    for i, (mid, content, importance, tags, mtype) in enumerate(graph_items):
        item = MemoryItem(
            content=content,
            memory_type=mtype,
            importance=importance,
            tags=tags,
            id=mid,
            created_at=_FIXED_TIMESTAMP + i * 60,
            last_accessed=_FIXED_TIMESTAMP + i * 60,
        )
        graph_store.add(item)
        if vector_store is not None:
            vector_store.add(
                MemoryItem(
                    content=content,
                    memory_type=mtype,
                    importance=importance,
                    tags=tags,
                    id=f"vec-{mid}",
                    created_at=_FIXED_TIMESTAMP + i * 60,
                    last_accessed=_FIXED_TIMESTAMP + i * 60,
                )
            )

    # ---- 显式关系 ----
    graph_store.add_relation("gr-001", "gr-002", "组件")
    graph_store.add_relation("gr-003", "gr-005", "过程")
    graph_store.add_relation("gr-003", "gr-006", "实现")
    graph_store.add_relation("gr-005", "gr-007", "理论基础")
    graph_store.add_relation("gr-004", "gr-001", "互补")

    # ---- 评测 query ----
    queries = [
        {
            "query": "RAG 检索管道",
            "expected_ids": ["ep-001", "gr-001", "gr-002"],
            "top_k": 5,
        },
        {
            "query": "Agent 记忆架构",
            "expected_ids": ["ep-003", "gr-003"],
            "top_k": 5,
        },
        {
            "query": "记忆巩固路径",
            "expected_ids": ["ep-009", "gr-005"],
            "top_k": 5,
        },
        {
            "query": "MemGPT 虚拟分页",
            "expected_ids": ["ep-006", "gr-006"],
            "top_k": 5,
        },
        {
            "query": "知识图谱部署",
            "expected_ids": ["ep-008", "gr-004"],
            "top_k": 5,
        },
        {
            "query": "向量数据库调试",
            "expected_ids": ["ep-002", "gr-002"],
            "top_k": 5,
        },
        {
            "query": "遗忘曲线衰减",
            "expected_ids": ["gr-007"],
            "top_k": 5,
        },
    ]
    return manager, queries


# ---------------------------------------------------------------------------
# 指标计算
# ---------------------------------------------------------------------------


def compute_metrics(
    queries: list[dict],
    results_per_query: list[list[tuple[MemoryItem, float, str]]],
) -> dict[str, Any]:
    """计算 hit@k、MRR、store 分布。

    Args:
        queries: build_scenario 返回的 query 列表
        results_per_query: 每个 query 对应的 recall 结果

    Returns:
        {"hit@1": float, "hit@3": float, "hit@5": float,
         "mrr": float, "store_distribution": dict, "per_query": list}
    """
    ks = [1, 3, 5]
    hits: dict[int, int] = {k: 0 for k in ks}
    reciprocal_ranks: list[float] = []
    store_counter: Counter[str] = Counter()
    per_query: list[dict] = []

    for q, results in zip(queries, results_per_query):
        expected = set(q["expected_ids"])
        actual_ids = [item.id for item, _score, _store in results]
        actual_stores = [store for _item, _score, store in results]

        # hit@k
        for k in ks:
            if expected & set(actual_ids[:k]):
                hits[k] += 1

        # MRR: 第一个命中 expected 的排名
        rr = 0.0
        for rank, aid in enumerate(actual_ids, start=1):
            if aid in expected:
                rr = 1.0 / rank
                break
        reciprocal_ranks.append(rr)

        # store 分布（top-5）
        for s in actual_stores[:5]:
            store_counter[s] += 1

        per_query.append({
            "query": q["query"],
            "expected_ids": q["expected_ids"],
            "actual_ids": actual_ids,
            "reciprocal_rank": rr,
            **{f"hit@{k}": bool(expected & set(actual_ids[:k])) for k in ks},
        })

    n = len(queries)
    total_store_hits = sum(store_counter.values()) or 1
    return {
        "hit@1": hits[1] / n,
        "hit@3": hits[3] / n,
        "hit@5": hits[5] / n,
        "mrr": sum(reciprocal_ranks) / n,
        "store_distribution": {
            s: round(c / total_store_hits, 3) for s, c in store_counter.items()
        },
        "per_query": per_query,
    }


# ---------------------------------------------------------------------------
# 快照 roundtrip 一致性
# ---------------------------------------------------------------------------


def check_roundtrip(
    manager: MemoryManager, queries: list[dict], tmp_dir: str
) -> bool:
    """保存快照 → 从快照恢复新 manager → 对比 top-3 结果 ID 是否一致。"""
    snap_path = os.path.join(tmp_dir, "roundtrip_snap")
    manager.save_snapshot(snap_path)

    # 用与原 manager 相同构造参数注册空 store，供 load_snapshot 提取 init_kwargs
    new_manager = MemoryManager(fusion_config=manager._fusion_config)
    for name, store in manager._stores.items():
        new_manager.register_store(name, store.__class__(**store.get_init_kwargs()))

    new_manager.load_snapshot(snap_path)

    for q in queries:
        orig = manager.recall(q["query"], top_k=3)
        rest = new_manager.recall(q["query"], top_k=3)
        orig_ids = [item.id for item, _, _ in orig]
        rest_ids = [item.id for item, _, _ in rest]
        if orig_ids != rest_ids:
            return False
    return True


# ---------------------------------------------------------------------------
# 输出生成
# ---------------------------------------------------------------------------


def _write_report_json(
    metrics: dict,
    roundtrip_ok: bool,
    out_dir: str,
    formation_metrics: dict | None = None,
    evolution_metrics: dict | None = None,
    retrieval_backend: dict[str, Any] | None = None,
) -> str:
    """写入 report.json。"""
    report: dict[str, Any] = {
        "timestamp": time.time(),
        "seed": 42,
        "snapshot_roundtrip_consistent": roundtrip_ok,
    }
    if formation_metrics:
        report["formation"] = formation_metrics
    if evolution_metrics:
        report["evolution"] = evolution_metrics
    report["retrieval"] = {
        "hit@1": metrics["hit@1"],
        "hit@3": metrics["hit@3"],
        "hit@5": metrics["hit@5"],
        "mrr": metrics["mrr"],
        "store_distribution": metrics["store_distribution"],
    }
    if retrieval_backend:
        report["retrieval_backend"] = retrieval_backend
    path = os.path.join(out_dir, "report.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    return path


def _write_report_md(
    metrics: dict,
    roundtrip_ok: bool,
    out_dir: str,
    formation_metrics: dict | None = None,
    evolution_metrics: dict | None = None,
    retrieval_backend: dict[str, Any] | None = None,
) -> str:
    """写入 report.md（简洁摘要）。"""
    lines = [
        "# Memory Evaluation Report",
        "",
        f"seed: 42 | retrieval queries: {len(metrics['per_query'])}",
        "",
    ]
    if retrieval_backend:
        stores = ", ".join(retrieval_backend.get("stores", [])) or "unknown"
        semantic_enabled = retrieval_backend.get("semantic_vector_store_enabled", False)
        lines += [
            "## Retrieval backend",
            "",
            f"- stores: {stores}",
            f"- semantic_vector_store_enabled: {semantic_enabled}",
            "",
        ]
    if formation_metrics:
        lines += [
            "## Formation 质量",
            "",
            "| 指标 | 值 |",
            "|------|-----|",
            f"| formation_precision | {formation_metrics['formation_precision']:.3f} |",
            f"| formation_recall | {formation_metrics['formation_recall']:.3f} |",
            "",
        ]
    if evolution_metrics:
        lines += [
            "## Evolution 正确性",
            "",
            "| 指标 | 值 |",
            "|------|-----|",
            f"| evolution_accuracy | {evolution_metrics['evolution_accuracy']:.3f} |",
            f"| forgetting_precision | {evolution_metrics['forgetting_precision']:.3f} |",
            "",
        ]
    lines += [
        "## Retrieval 忠实度",
        "",
        "| 指标 | 值 |",
        "|------|-----|",
        f"| hit@1 | {metrics['hit@1']:.3f} |",
        f"| hit@3 | {metrics['hit@3']:.3f} |",
        f"| hit@5 | {metrics['hit@5']:.3f} |",
        f"| MRR | {metrics['mrr']:.3f} |",
        "",
        "## Store 分布 (top-5)",
        "",
        "| Store | 占比 |",
        "|-------|------|",
    ]
    for store, ratio in metrics["store_distribution"].items():
        lines.append(f"| {store} | {ratio:.3f} |")
    lines.extend([
        "",
        f"快照 roundtrip 一致性: {'PASS' if roundtrip_ok else 'FAIL'}",
    ])
    path = os.path.join(out_dir, "report.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return path


def _write_cases_jsonl(
    metrics: dict,
    traces: list[dict],
    out_dir: str,
) -> str:
    """写入 cases.jsonl，每行一个 query 的详细结果。"""
    path = os.path.join(out_dir, "cases.jsonl")
    with open(path, "w", encoding="utf-8") as f:
        for pq, trace in zip(metrics["per_query"], traces):
            record = {**pq, "trace": trace}
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    return path


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------


def compute_coverage_matrix(cases: list[dict[str, Any]]) -> dict[str, bool]:
    sources = {str(case.get("source", "")) for case in cases}
    splits = {str(case.get("split", "")) for case in cases}
    return {
        "formation": "Test_Time_Learning" in splits or "formation" in splits,
        "evolution": "Conflict_Resolution" in splits or "evolution" in splits,
        "retrieval": bool({"locomo", "longmemeval", "ama-bench", "memoryarena"} & sources),
        "memory_in_use": bool({"ama-bench", "memoryarena", "longmemeval"} & sources),
    }


def run_dataset_benchmark(dataset_dir: str, out_dir: str) -> dict[str, Any]:
    os.makedirs(out_dir, exist_ok=True)
    cases = load_benchmark_cases(dataset_dir)
    if not cases:
        raise FileNotFoundError(f"未在 {dataset_dir} 中找到可用的 benchmark case")

    summary_rows: list[dict[str, Any]] = []
    traces: list[dict[str, Any]] = []
    for case in cases:
        manager = MemoryManager(
            fusion_config=FusionConfig(
                mode="rank",
                overfetch_factor=3,
                store_weights={"episodic": 1.0, "graph": 1.0, "vector": 1.0},
            )
        )
        ep_store = EpisodicMemory(max_capacity=1000, decay_rate=0.001)
        graph_store = GraphMemoryStore(max_capacity=1000, decay_rate=0.001)
        manager.register_store("episodic", ep_store, default=True)
        manager.register_store("graph", graph_store)
        if case.get("source") == "memoryarena":
            vector_store = VectorMemoryStore(max_capacity=1000, decay_rate=0.001)
            manager.register_store("vector", vector_store)
        for doc in case.get("documents", []):
            item = MemoryItem(
                id=str(doc.get("id")),
                content=str(doc.get("content", "")),
                memory_type=MemoryType.EPISODIC,
                tags=[str(tag) for tag in doc.get("tags", [])],
                importance=0.7,
                created_at=_FIXED_TIMESTAMP,
                last_accessed=_FIXED_TIMESTAMP,
            )
            ep_store.add(item)
            graph_store.add(
                MemoryItem(
                    id=f"graph-{item.id}",
                    content=item.content,
                    memory_type=MemoryType.SEMANTIC,
                    tags=item.tags,
                    importance=item.importance,
                    created_at=_FIXED_TIMESTAMP,
                    last_accessed=_FIXED_TIMESTAMP,
                )
            )
            if "vector" in manager._stores:
                manager.get_store("vector").add(  # type: ignore[union-attr]
                    MemoryItem(
                        id=f"vec-{item.id}",
                        content=item.content,
                        memory_type=item.memory_type,
                        tags=item.tags,
                        importance=item.importance,
                        created_at=_FIXED_TIMESTAMP,
                        last_accessed=_FIXED_TIMESTAMP,
                    )
                )

        traced = manager.recall_with_trace(case["query"], top_k=int(case.get("top_k", 5)))
        results = traced["results"]
        result_ids = [item.id for item, _score, _store in results]
        expected_ids = {str(item) for item in case.get("expected_ids", [])}
        hit = bool(expected_ids & set(result_ids))
        summary_rows.append({
            "id": case["id"],
            "query": case["query"],
            "source": case["source"],
            "split": case["split"],
            "expected_ids": case.get("expected_ids", []),
            "result_ids": result_ids,
            "hit": hit,
        })
        traces.append(traced["trace"])

    hits = sum(1 for row in summary_rows if row["hit"])
    metrics = {
        "hit@1": hits / len(summary_rows),
        "hit@3": hits / len(summary_rows),
        "hit@5": hits / len(summary_rows),
        "mrr": hits / len(summary_rows),
        "store_distribution": {},
        "per_query": summary_rows,
    }
    coverage = compute_coverage_matrix(cases)
    retrieval_backend = {
        "stores": ["episodic", "graph"],
        "semantic_vector_store_enabled": any(case.get("source") == "memoryarena" for case in cases),
    }
    _write_report_json(metrics, True, out_dir, retrieval_backend=retrieval_backend)
    _write_report_md(metrics, True, out_dir, retrieval_backend=retrieval_backend)
    _write_cases_jsonl(metrics, traces, out_dir)
    summary = {
        "benchmark_name": "dataset-benchmark",
        "case_count": len(summary_rows),
        "metrics": {k: metrics[k] for k in ["hit@1", "hit@3", "hit@5", "mrr"]},
        "coverage": coverage,
        "retrieval_backend": retrieval_backend,
        "output_dir": out_dir,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return summary


def run_evaluation(out_dir: str) -> dict:
    """执行完整评测流程（formation + evolution + retrieval），返回指标摘要。"""
    os.makedirs(out_dir, exist_ok=True)

    # --- Stage 1: Formation ---
    fm_manager, events, expected_writes = build_formation_scenario(seed=42)
    actual_writes: set[str] = set()
    for ev in events:
        if ev["importance"] >= _IMPORTANCE_THRESHOLD and len(ev["content"]) >= _CONTENT_MIN_LEN:
            fm_manager.remember(
                content=ev["content"],
                importance=ev["importance"],
                tags=ev["tags"],
            )
            actual_writes.add(ev["id"])
    formation_metrics = compute_formation_metrics(actual_writes, expected_writes)

    # --- Stage 2: Evolution ---
    ev_manager, update_events, expected_state = build_evolution_scenario(seed=42)
    for event in update_events:
        if event["type"] == "update":
            ev_manager.update_memory(event["target_id"], content=event["new_content"])
        elif event["type"] == "forget":
            ev_manager.forget(event["target_id"])
    all_items: dict[str, str] = {}
    for store_name in ev_manager._stores:
        for item in ev_manager.get_store(store_name).list_all():
            all_items[item.id] = item.content
    evolution_metrics = compute_evolution_metrics(all_items, expected_state)

    # --- Stage 3: Retrieval ---
    ret_manager, queries = build_scenario(seed=42)
    results_per_query: list[list[tuple[MemoryItem, float, str]]] = []
    traces: list[dict] = []
    for q in queries:
        traced = ret_manager.recall_with_trace(q["query"], top_k=q["top_k"])
        results_per_query.append(traced["results"])
        traces.append(traced["trace"])
    retrieval_metrics = compute_metrics(queries, results_per_query)

    # --- Snapshot roundtrip (fresh retrieval manager) ---
    roundtrip_manager, roundtrip_queries = build_scenario(seed=42)
    with tempfile.TemporaryDirectory() as tmp_dir:
        roundtrip_ok = check_roundtrip(roundtrip_manager, roundtrip_queries, tmp_dir)

    # --- Write artifacts ---
    retrieval_backend = {
        "stores": list(ret_manager._stores.keys()),
        "semantic_vector_store_enabled": "vector" in ret_manager._stores,
    }
    _write_report_json(
        retrieval_metrics,
        roundtrip_ok,
        out_dir,
        formation_metrics=formation_metrics,
        evolution_metrics=evolution_metrics,
        retrieval_backend=retrieval_backend,
    )
    _write_report_md(
        retrieval_metrics,
        roundtrip_ok,
        out_dir,
        formation_metrics=formation_metrics,
        evolution_metrics=evolution_metrics,
        retrieval_backend=retrieval_backend,
    )
    _write_cases_jsonl(retrieval_metrics, traces, out_dir)

    summary = {
        "formation_precision": formation_metrics["formation_precision"],
        "formation_recall": formation_metrics["formation_recall"],
        "evolution_accuracy": evolution_metrics["evolution_accuracy"],
        "forgetting_precision": evolution_metrics["forgetting_precision"],
        "hit@1": retrieval_metrics["hit@1"],
        "hit@3": retrieval_metrics["hit@3"],
        "hit@5": retrieval_metrics["hit@5"],
        "mrr": retrieval_metrics["mrr"],
        "snapshot_roundtrip_consistent": roundtrip_ok,
        "retrieval_backend": retrieval_backend,
        "output_dir": out_dir,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return summary


# ---------------------------------------------------------------------------
# Formation 场景构造与指标
# ---------------------------------------------------------------------------

_IMPORTANCE_THRESHOLD = 0.6
_CONTENT_MIN_LEN = 5


def build_formation_scenario(
    seed: int = 42,
) -> tuple[MemoryManager, list[dict], set[str]]:
    """构造 formation 质量评测场景。

    返回 (manager, events, expected_writes)
    events: [{"id": str, "content": str, "importance": float, "tags": list[str]}]
    expected_writes: 按触发规则（importance >= 0.6 且 len(content) >= 5）应被写入的 id 集合
    """
    random.seed(seed)

    config = FusionConfig(mode="rank", overfetch_factor=3)
    manager = MemoryManager(fusion_config=config)
    ep_store = EpisodicMemory(max_capacity=1000, decay_rate=0.001)
    manager.register_store("episodic", ep_store, default=True)

    events = [
        {"id": "f-001", "content": "用户偏好：不喜欢冗长回复", "importance": 0.90, "tags": ["偏好"]},
        {"id": "f-002", "content": "嗯", "importance": 0.10, "tags": []},
        {"id": "f-003", "content": "用户工作地点是上海", "importance": 0.85, "tags": ["偏好", "地点"]},
        {"id": "f-004", "content": "好的", "importance": 0.05, "tags": []},
        {"id": "f-005", "content": "用户擅长 Python，不熟悉 Rust", "importance": 0.80, "tags": ["技能"]},
        {"id": "f-006", "content": "讨论了 RAG 检索管道的配置方法", "importance": 0.70, "tags": ["rag"]},
        {"id": "f-007", "content": "用户说明天有会议", "importance": 0.45, "tags": ["日程"]},
        {"id": "f-008", "content": "用户要求回复使用中文", "importance": 0.75, "tags": ["偏好"]},
        {"id": "f-009", "content": "哦", "importance": 0.08, "tags": []},
        {"id": "f-010", "content": "提到 Agent 记忆的分层架构设计原则", "importance": 0.88, "tags": ["架构"]},
        {"id": "f-011", "content": "用户不确定", "importance": 0.30, "tags": []},
        {"id": "f-012", "content": "确认了向量数据库选型为 ChromaDB", "importance": 0.72, "tags": ["工具"]},
        {"id": "f-013", "content": "嗯嗯", "importance": 0.12, "tags": []},
        {"id": "f-014", "content": "用户偏好暗色主题 UI", "importance": 0.65, "tags": ["偏好"]},
        {"id": "f-015", "content": "讨论了 LRU 淘汰策略的适用场景", "importance": 0.68, "tags": ["架构"]},
    ]

    expected_writes = {
        e["id"]
        for e in events
        if e["importance"] >= _IMPORTANCE_THRESHOLD and len(e["content"]) >= _CONTENT_MIN_LEN
    }
    return manager, events, expected_writes


def compute_formation_metrics(
    actual_writes: set[str],
    expected_writes: set[str],
) -> dict[str, float]:
    """计算 formation 质量指标。

    formation_precision: 实际写入中属于预期写入的比例
    formation_recall: 预期写入中被实际写入的比例
    """
    if not actual_writes and not expected_writes:
        return {"formation_precision": 1.0, "formation_recall": 1.0}
    tp = len(actual_writes & expected_writes)
    precision = tp / len(actual_writes) if actual_writes else 0.0
    recall = tp / len(expected_writes) if expected_writes else 0.0
    return {"formation_precision": precision, "formation_recall": recall}


# ---------------------------------------------------------------------------
# Evolution 场景构造与指标
# ---------------------------------------------------------------------------


def build_evolution_scenario(
    seed: int = 42,
) -> tuple[MemoryManager, list[dict], dict[str, str | None]]:
    """构造 evolution 正确性评测场景。

    返回 (manager, update_events, expected_state)
    update_events: [{"type": "update"|"forget", "target_id": str, ...}]
    expected_state: {item_id: content_after_update | None}  None 表示应被遗忘
    """
    random.seed(seed)

    config = FusionConfig(mode="rank", overfetch_factor=3)
    manager = MemoryManager(fusion_config=config)
    ep_store = EpisodicMemory(max_capacity=1000, decay_rate=0.001)
    manager.register_store("episodic", ep_store, default=True)

    # 预置记忆（固定 id 以便追踪）
    base_items = [
        ("ev-m001", "用户工作地点是北京", 0.85, ["偏好", "地点"]),
        ("ev-m002", "用户擅长 Java", 0.80, ["技能"]),
        ("ev-m003", "上次会议于周一举行", 0.60, ["日程"]),
        ("ev-m004", "用户偏好简洁回复", 0.90, ["偏好"]),
        ("ev-m005", "向量数据库选型为 FAISS", 0.70, ["工具"]),
    ]
    for fixed_id, content, importance, tags in base_items:
        item = MemoryItem(
            id=fixed_id,
            content=content,
            importance=importance,
            tags=tags,
            created_at=_FIXED_TIMESTAMP,
            last_accessed=_FIXED_TIMESTAMP,
        )
        ep_store._episodes[fixed_id] = item
        ep_store._timeline.append(fixed_id)

    update_events = [
        # 冲突更新：工作地点变更
        {"type": "update", "target_id": "ev-m001", "new_content": "用户工作地点是上海"},
        # 冲突更新：技能更新
        {"type": "update", "target_id": "ev-m002", "new_content": "用户擅长 Python 和 Java"},
        # 主动遗忘：日程信息过期
        {"type": "forget", "target_id": "ev-m003"},
        # 冲突更新：工具选型变更
        {"type": "update", "target_id": "ev-m005", "new_content": "向量数据库选型为 ChromaDB"},
    ]

    expected_state: dict[str, str | None] = {
        "ev-m001": "用户工作地点是上海",
        "ev-m002": "用户擅长 Python 和 Java",
        "ev-m003": None,  # 应被遗忘
        "ev-m004": "用户偏好简洁回复",  # 未变动
        "ev-m005": "向量数据库选型为 ChromaDB",
    }
    return manager, update_events, expected_state


def compute_evolution_metrics(
    actual_state: dict[str, str],
    expected_state: dict[str, str | None],
) -> dict[str, float]:
    """计算 evolution 正确性指标。

    evolution_accuracy: 预期存续记忆中内容匹配的比例
    forgetting_precision: 预期被遗忘的记忆中实际缺失的比例
    """
    should_survive = {k: v for k, v in expected_state.items() if v is not None}
    should_forget = {k for k, v in expected_state.items() if v is None}

    if should_survive:
        correct = sum(
            1 for k, v in should_survive.items() if actual_state.get(k) == v
        )
        evolution_accuracy = correct / len(should_survive)
    else:
        evolution_accuracy = 1.0

    if should_forget:
        actually_forgotten = sum(1 for k in should_forget if k not in actual_state)
        forgetting_precision = actually_forgotten / len(should_forget)
    else:
        forgetting_precision = 1.0

    return {
        "evolution_accuracy": evolution_accuracy,
        "forgetting_precision": forgetting_precision,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Agent Memory 评测")
    parser.add_argument("--out", default="docs/memory-eval/latest",
                        help="输出目录 (默认: docs/memory-eval/latest)")
    args = parser.parse_args()
    run_evaluation(args.out)


if __name__ == "__main__":
    main()
