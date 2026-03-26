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
import tempfile
import time
from collections import Counter
from typing import Any

from .base import FusionConfig, MemoryItem, MemoryType
from .episodic import EpisodicMemory
from .graph_store import GraphMemoryStore
from .manager import MemoryManager

# ---------------------------------------------------------------------------
# 场景构造
# ---------------------------------------------------------------------------

_FIXED_TIMESTAMP = 1700000000.0  # 固定基准时间，确保 decay 可重复


def build_scenario(seed: int = 42) -> tuple[MemoryManager, list[dict]]:
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
    # 保存
    snap_path = os.path.join(tmp_dir, "roundtrip_snap")
    manager.save_snapshot(snap_path)

    # 读取快照 JSON
    with open(os.path.join(snap_path, "snapshot.json"), "r", encoding="utf-8") as f:
        snapshot = json.load(f)

    # 重建 manager（手动恢复，避免 load_snapshot 签名问题）
    config = FusionConfig(
        mode="rank",
        overfetch_factor=3,
        store_weights={"episodic": 1.0, "graph": 1.0},
    )
    new_manager = MemoryManager(fusion_config=config)

    stores_data = snapshot.get("stores", {})
    if "episodic" in stores_data:
        ep = EpisodicMemory.from_snapshot_dict(
            stores_data["episodic"]["data"],
            max_capacity=1000,
            decay_rate=0.001,
        )
        new_manager.register_store("episodic", ep)
    if "graph" in stores_data:
        gs = GraphMemoryStore.from_snapshot_dict(
            stores_data["graph"]["data"],
            max_capacity=1000,
            decay_rate=0.001,
        )
        new_manager.register_store("graph", gs)

    # 对比
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


def _write_report_json(metrics: dict, roundtrip_ok: bool, out_dir: str) -> str:
    """写入 report.json。"""
    report = {
        "timestamp": time.time(),
        "seed": 42,
        "hit@1": metrics["hit@1"],
        "hit@3": metrics["hit@3"],
        "hit@5": metrics["hit@5"],
        "mrr": metrics["mrr"],
        "store_distribution": metrics["store_distribution"],
        "snapshot_roundtrip_consistent": roundtrip_ok,
    }
    path = os.path.join(out_dir, "report.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    return path


def _write_report_md(metrics: dict, roundtrip_ok: bool, out_dir: str) -> str:
    """写入 report.md（简洁摘要）。"""
    lines = [
        "# Memory Evaluation Report",
        "",
        f"seed: 42 | queries: {len(metrics['per_query'])}",
        "",
        "## 指标",
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


def run_evaluation(out_dir: str) -> dict:
    """执行完整评测流程，返回指标摘要。"""
    os.makedirs(out_dir, exist_ok=True)

    # 1. 构造场景
    manager, queries = build_scenario(seed=42)

    # 2. 执行检索（带 trace）
    results_per_query: list[list[tuple[MemoryItem, float, str]]] = []
    traces: list[dict] = []
    for q in queries:
        traced = manager.recall_with_trace(q["query"], top_k=q["top_k"])
        results_per_query.append(traced["results"])
        # trace 中的 raw 数据序列化
        traces.append(traced["trace"])

    # 3. 计算指标
    metrics = compute_metrics(queries, results_per_query)

    # 4. 快照 roundtrip
    with tempfile.TemporaryDirectory() as tmp_dir:
        roundtrip_ok = check_roundtrip(manager, queries, tmp_dir)

    # 5. 写入产物
    _write_report_json(metrics, roundtrip_ok, out_dir)
    _write_report_md(metrics, roundtrip_ok, out_dir)
    _write_cases_jsonl(metrics, traces, out_dir)

    summary = {
        "hit@1": metrics["hit@1"],
        "hit@3": metrics["hit@3"],
        "hit@5": metrics["hit@5"],
        "mrr": metrics["mrr"],
        "snapshot_roundtrip_consistent": roundtrip_ok,
        "output_dir": out_dir,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Agent Memory 评测")
    parser.add_argument("--out", default="docs/memory-eval/latest",
                        help="输出目录 (默认: docs/memory-eval/latest)")
    args = parser.parse_args()
    run_evaluation(args.out)


if __name__ == "__main__":
    main()
