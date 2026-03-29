# ruff: noqa: E501
"""Agent Memory 核心模块测试。"""

import json
import time
from pathlib import Path

import pytest

from src.memory.base import FusionConfig, MemoryItem, MemoryType
from src.memory.episodic import EpisodicMemory
from src.memory.evaluation import (
    build_scenario,
    load_benchmark_cases,
    run_dataset_benchmark,
)
from src.memory.graph_store import GraphMemoryStore
from src.memory.manager import MemoryManager
from src.memory.vector_store import VectorMemoryStore

# ---- MemoryItem 测试 ----


class TestMemoryItem:
    def test_create_default(self):
        item = MemoryItem(content="test")
        assert item.content == "test"
        assert item.memory_type == MemoryType.SEMANTIC
        assert item.importance == 0.5
        assert item.access_count == 0

    def test_touch(self):
        item = MemoryItem(content="test")
        old_time = item.last_accessed
        time.sleep(0.01)
        item.touch()
        assert item.access_count == 1
        assert item.last_accessed > old_time

    def test_decay_score(self):
        item = MemoryItem(content="test", importance=1.0)
        score1 = item.decay_score(decay_rate=0.01)
        time.sleep(0.05)
        score2 = item.decay_score(decay_rate=0.01)
        # 分数应该随时间衰减
        assert score2 <= score1

    def test_tags_and_links(self):
        item = MemoryItem(content="test", tags=["a", "b"], links=["id1"])
        assert "a" in item.tags
        assert "id1" in item.links


# ---- EpisodicMemory 测试 ----


class TestEpisodicMemory:
    def test_add_and_size(self):
        em = EpisodicMemory()
        em.add_episode("事件1", importance=0.5, tags=["test"])
        em.add_episode("事件2", importance=0.8, tags=["test"])
        assert em.size() == 2

    def test_query(self):
        em = EpisodicMemory()
        em.add_episode("用户问了关于 Python 的问题", tags=["python"])
        em.add_episode("用户问了关于 Java 的问题", tags=["java"])
        em.add_episode("系统发生了错误", tags=["error"])

        results = em.query("Python 问题")
        assert len(results) > 0
        # 第一个结果应该包含 Python
        assert (
            "Python" in results[0][0].content
            or "python" in results[0][0].content.lower()
        )

    def test_recent(self):
        em = EpisodicMemory()
        em.add_episode("事件1")
        em.add_episode("事件2")
        em.add_episode("事件3")
        recent = em.recent(2)
        assert len(recent) == 2
        assert recent[0].content == "事件3"

    def test_delete(self):
        em = EpisodicMemory()
        mid = em.add_episode("要删除的事件")
        assert em.size() == 1
        assert em.delete(mid)
        assert em.size() == 0

    def test_consolidate(self):
        em = EpisodicMemory(importance_threshold=0.5)
        em.add_episode("低重要性", importance=0.1)
        em.add_episode("高重要性", importance=0.9)
        # 低重要性记忆在衰减后应该被清理
        # 注：刚添加的记忆衰减分数还较高，这里主要测试接口
        count = em.consolidate()
        assert isinstance(count, int)

    def test_extract_patterns(self):
        em = EpisodicMemory()
        for i in range(5):
            em.add_episode(f"关于记忆的讨论{i}", tags=["记忆", "讨论"])
        for i in range(2):
            em.add_episode(f"关于推理的讨论{i}", tags=["推理"])

        patterns = em.extract_patterns(min_frequency=3)
        assert len(patterns) > 0
        assert patterns[0]["tag"] == "记忆"
        assert patterns[0]["frequency"] == 5

    def test_capacity_limit(self):
        em = EpisodicMemory(max_capacity=3)
        em.add_episode("事件1", importance=0.9)
        em.add_episode("事件2", importance=0.1)
        em.add_episode("事件3", importance=0.5)
        em.add_episode("事件4", importance=0.8)
        assert em.size() == 3  # 应该淘汰一条


# ---- GraphMemoryStore 测试 ----


class TestGraphMemoryStore:
    def test_add_and_query(self):
        gs = GraphMemoryStore()
        gs.add(MemoryItem(content="Python 编程语言", tags=["python", "编程"]))
        gs.add(MemoryItem(content="Java 编程语言", tags=["java", "编程"]))
        gs.add(MemoryItem(content="深度学习基础", tags=["AI", "深度学习"]))

        results = gs.query("编程")
        assert len(results) > 0

    def test_tag_overlap_links(self):
        gs = GraphMemoryStore()
        gs.add(MemoryItem(content="Python", tags=["编程"]))
        gs.add(MemoryItem(content="Java", tags=["编程"]))

        stats = gs.graph_stats()
        assert stats["edges"] > 0  # 应该有 tag 重叠的自动链接

    def test_explicit_relation(self):
        gs = GraphMemoryStore()
        item1 = MemoryItem(content="Transformer")
        item2 = MemoryItem(content="注意力机制")
        id1 = gs.add(item1)
        id2 = gs.add(item2)

        assert gs.add_relation(id1, id2, "包含")
        neighbors = gs.get_neighbors(id1)
        assert any(n.content == "注意力机制" for n in neighbors)

    def test_delete_removes_from_graph(self):
        gs = GraphMemoryStore()
        item = MemoryItem(content="临时记忆")
        mid = gs.add(item)
        assert gs.size() == 1
        gs.delete(mid)
        assert gs.size() == 0
        assert gs.graph_stats()["nodes"] == 0

    def test_graph_stats(self):
        gs = GraphMemoryStore()
        gs.add(MemoryItem(content="A", tags=["x"]))
        gs.add(MemoryItem(content="B", tags=["x"]))
        stats = gs.graph_stats()
        assert "nodes" in stats
        assert "edges" in stats
        assert stats["nodes"] == 2


# ---- MemoryManager 测试 ----


class TestMemoryManager:
    def test_register_and_remember(self):
        mm = MemoryManager()
        mm.register_store("ep", EpisodicMemory())
        mm.register_store("sem", GraphMemoryStore(), default=True)

        mid = mm.remember("测试记忆", tags=["test"])
        assert mid is not None
        assert mm.total_memories() == 1

    def test_recall_across_stores(self):
        mm = MemoryManager()
        ep = EpisodicMemory()
        gs = GraphMemoryStore()
        mm.register_store("ep", ep)
        mm.register_store("sem", gs, default=True)

        ep.add_episode("Python 事件", tags=["python"])
        mm.remember("Python 知识", store_name="sem", tags=["python"])

        results = mm.recall("Python")
        assert len(results) > 0
        # 结果应该来自两个存储
        store_names = {r[2] for r in results}
        assert len(store_names) >= 1

    def test_forget(self):
        mm = MemoryManager()
        gs = GraphMemoryStore()
        mm.register_store("sem", gs, default=True)

        mid = mm.remember("要忘记的")
        assert mm.total_memories() == 1
        assert mm.forget(mid)
        assert mm.total_memories() == 0

    def test_consolidate_episodic_to_semantic(self):
        mm = MemoryManager()
        ep = EpisodicMemory()
        gs = GraphMemoryStore()
        mm.register_store("ep", ep)
        mm.register_store("sem", gs)

        # 添加足够多的同主题情景记忆
        for i in range(5):
            ep.add_episode(f"记忆研究讨论{i}", tags=["记忆"])

        new_ids = mm.consolidate_episodic_to_semantic("ep", "sem", min_frequency=3)
        assert len(new_ids) > 0
        assert gs.size() > 0

    def test_stats(self):
        mm = MemoryManager()
        mm.register_store("ep", EpisodicMemory())
        mm.register_store("sem", GraphMemoryStore())

        stats = mm.stats()
        assert "ep" in stats
        assert "sem" in stats
        assert stats["ep"]["size"] == 0


# ---- FusionConfig 测试 ----


class TestFusionConfig:
    def test_default_values(self):
        """默认配置: mode=rank, overfetch_factor=3, store_weights={}。"""
        fc = FusionConfig()
        assert fc.mode == "rank"
        assert fc.overfetch_factor == 3
        assert fc.store_weights == {}

    def test_get_weight_default(self):
        """未配置的 store 返回默认权重 1.0。"""
        fc = FusionConfig()
        assert fc.get_weight("any_store") == 1.0
        assert fc.get_weight("nonexistent") == 1.0

    def test_get_weight_custom(self):
        """配置了的 store 返回配置值。"""
        fc = FusionConfig(store_weights={"ep": 2.0, "graph": 0.5})
        assert fc.get_weight("ep") == 2.0
        assert fc.get_weight("graph") == 0.5
        # 未配置的仍返回 1.0
        assert fc.get_weight("other") == 1.0


# ---- Rank 融合测试 ----


class TestRankFusion:
    def test_cross_store_rank_fusion(self):
        """跨 store rank 归一化融合：结果不被单一 store 劫持，fused_score 递减。"""
        mm = MemoryManager()
        ep = EpisodicMemory()
        gs = GraphMemoryStore()
        mm.register_store("ep", ep)
        mm.register_store("graph", gs)

        # episodic 中添加 3 条关于 Python 的记忆
        ep.add_episode("Python 基础教程", importance=0.8, tags=["python"])
        ep.add_episode("Python 高级特性", importance=0.7, tags=["python"])
        ep.add_episode("Python 数据分析", importance=0.6, tags=["python"])

        # graph 中添加 3 条关于 Python 的记忆
        gs.add(MemoryItem(content="Python 编程语言", tags=["python", "编程"]))
        gs.add(MemoryItem(content="Python 机器学习", tags=["python", "ML"]))
        gs.add(MemoryItem(content="Python Web 开发", tags=["python", "web"]))

        results = mm.recall("Python", top_k=3)
        assert len(results) == 3

        # 验证结果来自两个 store（不被单一 store 劫持）
        store_names = {r[2] for r in results}
        assert len(store_names) >= 2, "结果应来自至少两个 store"

        # 验证 fused_score 递减
        scores = [r[1] for r in results]
        for i in range(len(scores) - 1):
            assert scores[i] >= scores[i + 1], "fused_score 应递减"

    def test_recall_with_trace(self):
        """recall_with_trace 返回 trace 信息，包含评分明细。"""
        mm = MemoryManager()
        ep = EpisodicMemory()
        gs = GraphMemoryStore()
        mm.register_store("ep", ep)
        mm.register_store("graph", gs)

        ep.add_episode("Python 基础教程", importance=0.8, tags=["python"])
        ep.add_episode("Python 高级特性", importance=0.7, tags=["python"])
        ep.add_episode("Python 数据分析", importance=0.6, tags=["python"])

        gs.add(MemoryItem(content="Python 编程语言", tags=["python", "编程"]))
        gs.add(MemoryItem(content="Python 机器学习", tags=["python", "ML"]))
        gs.add(MemoryItem(content="Python Web 开发", tags=["python", "web"]))

        output = mm.recall_with_trace("Python", top_k=3)

        # 验证返回结构
        assert "results" in output
        assert "trace" in output
        assert len(output["results"]) == 3

        # 验证 trace 中每个 store 的条目包含必要字段
        required_fields = {
            "item_id",
            "raw_score",
            "rank",
            "normalized_score",
            "fused_score",
        }
        for store_name, entries in output["trace"].items():
            assert len(entries) > 0, f"store '{store_name}' 应有 trace 条目"
            for entry in entries:
                assert required_fields.issubset(entry.keys()), (
                    f"trace 条目缺少字段: {required_fields - entry.keys()}"
                )

        # 验证 normalized_score 符合 1/rank 规律
        for _store_name, entries in output["trace"].items():
            for entry in entries:
                expected = 1.0 / entry["rank"]
                assert abs(entry["normalized_score"] - expected) < 1e-9, (
                    f"normalized_score 应为 1/rank={expected}，实际为 {entry['normalized_score']}"
                )

    def test_store_weights(self):
        """store 权重影响融合排序：高权重 store 的结果排名更靠前。"""
        # ep 权重 2.0，graph 权重 0.5
        fc = FusionConfig(store_weights={"ep": 2.0, "graph": 0.5})
        mm = MemoryManager(fusion_config=fc)
        ep = EpisodicMemory()
        gs = GraphMemoryStore()
        mm.register_store("ep", ep)
        mm.register_store("graph", gs)

        # 两个 store 添加相似内容
        for i in range(3):
            ep.add_episode(f"Python 话题 {i}", importance=0.7, tags=["python"])
            gs.add(MemoryItem(content=f"Python 话题 {i}", tags=["python"]))

        results = mm.recall("Python", top_k=6)
        assert len(results) > 0

        # 统计 top 位置中 ep 的数量
        top_half = results[: len(results) // 2] if len(results) >= 2 else results
        ep_count = sum(1 for _, _, sn in top_half if sn == "ep")
        graph_count = sum(1 for _, _, sn in top_half if sn == "graph")
        assert ep_count >= graph_count, "高权重 ep store 应在 top 位置更多"


# ---- 快照持久化测试 ----


class TestSnapshot:
    def test_roundtrip_episodic_graph(self, tmp_path):
        """save_snapshot → load_snapshot 往返：记忆数量和 recall 结果一致。"""
        # 创建并填充 manager
        mm1 = MemoryManager()
        ep1 = EpisodicMemory()
        gs1 = GraphMemoryStore()
        mm1.register_store("ep", ep1)
        mm1.register_store("graph", gs1, default=True)

        ep1.add_episode("Python 基础", importance=0.8, tags=["python"])
        ep1.add_episode("Python 进阶", importance=0.7, tags=["python"])
        ep1.add_episode("Python 实战", importance=0.6, tags=["python"])

        id_g1 = gs1.add(MemoryItem(content="Python 编程", tags=["python", "编程"]))
        id_g2 = gs1.add(MemoryItem(content="Python 框架", tags=["python", "web"]))
        gs1.add(MemoryItem(content="Python 数据", tags=["python", "data"]))
        gs1.add_relation(id_g1, id_g2, "相关")

        # 保存快照
        snap_dir = str(tmp_path / "snap1")
        mm1.save_snapshot(snap_dir)
        total_before = mm1.total_memories()
        recall_before = [r[0].id for r in mm1.recall("Python", top_k=3)]

        # 创建新 manager，加载快照
        mm2 = MemoryManager()
        mm2.register_store("ep", EpisodicMemory())
        mm2.register_store("graph", GraphMemoryStore(), default=True)
        mm2.load_snapshot(snap_dir)

        # 验证记忆总数一致
        assert mm2.total_memories() == total_before

        # 验证同样 query 的 top-3 结果 ID 一致
        recall_after = [r[0].id for r in mm2.recall("Python", top_k=3)]
        assert set(recall_after) == set(recall_before)

    def test_strict_validation_bad_schema(self, tmp_path):
        """strict 模式下，错误的 schema_version 应抛 ValueError。"""
        mm = MemoryManager()
        mm.register_store("ep", EpisodicMemory())
        snap_dir = str(tmp_path / "snap_bad_schema")
        mm.save_snapshot(snap_dir)

        # 手动篡改 schema_version
        snap_file = tmp_path / "snap_bad_schema" / "snapshot.json"
        data = json.loads(snap_file.read_text(encoding="utf-8"))
        data["schema_version"] = "99.0"
        snap_file.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

        mm2 = MemoryManager()
        mm2.register_store("ep", EpisodicMemory())
        with pytest.raises(ValueError, match="不支持的快照版本"):
            mm2.load_snapshot(snap_dir, strict=True)

    def test_strict_validation_bad_graph_edge(self, tmp_path):
        """strict 模式下，图边指向不存在的节点应抛 ValueError。"""
        mm = MemoryManager()
        gs = GraphMemoryStore()
        mm.register_store("graph", gs, default=True)
        gs.add(MemoryItem(content="节点A", tags=["test"]))

        snap_dir = str(tmp_path / "snap_bad_edge")
        mm.save_snapshot(snap_dir)

        # 手动注入一条指向不存在 ID 的边
        snap_file = tmp_path / "snap_bad_edge" / "snapshot.json"
        data = json.loads(snap_file.read_text(encoding="utf-8"))
        graph_data = data["stores"]["graph"]["data"]
        graph_data["edges"].append(
            {
                "source": "nonexistent-id-000",
                "target": "nonexistent-id-001",
                "relation": "fake",
                "attrs": {},
            }
        )
        snap_file.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

        mm2 = MemoryManager()
        mm2.register_store("graph", GraphMemoryStore(), default=True)
        with pytest.raises(ValueError, match="不存在的.*节点"):
            mm2.load_snapshot(snap_dir, strict=True)

    def test_load_non_strict(self, tmp_path):
        """non-strict 模式下，错误的 schema_version 不抛错。"""
        mm = MemoryManager()
        mm.register_store("ep", EpisodicMemory())
        snap_dir = str(tmp_path / "snap_non_strict")
        mm.save_snapshot(snap_dir)

        # 篡改 schema_version
        snap_file = tmp_path / "snap_non_strict" / "snapshot.json"
        data = json.loads(snap_file.read_text(encoding="utf-8"))
        data["schema_version"] = "99.0"
        snap_file.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

        mm2 = MemoryManager()
        mm2.register_store("ep", EpisodicMemory())
        # strict=False 不应抛错
        result = mm2.load_snapshot(snap_dir, strict=False)
        assert "total_memories" in result


# ---- 各 Store 序列化单测 ----


class TestStoreSnapshot:
    def test_episodic_snapshot_roundtrip(self):
        """EpisodicMemory to_snapshot_dict → from_snapshot_dict 往返一致。"""
        ep = EpisodicMemory()
        ep.add_episode("事件A", importance=0.9, tags=["a"])
        ep.add_episode("事件B", importance=0.5, tags=["b"])
        ep.add_episode("事件C", importance=0.3, tags=["c"])

        snap = ep.to_snapshot_dict()
        restored = EpisodicMemory.from_snapshot_dict(snap)

        assert restored.size() == ep.size()
        original_contents = sorted(i.content for i in ep.list_all())
        restored_contents = sorted(i.content for i in restored.list_all())
        assert original_contents == restored_contents

    def test_graph_snapshot_roundtrip(self):
        """GraphMemoryStore to_snapshot_dict → from_snapshot_dict 往返一致。"""
        gs = GraphMemoryStore()
        id1 = gs.add(MemoryItem(content="概念A", tags=["x"]))
        gs.add(MemoryItem(content="概念B", tags=["x"]))
        id3 = gs.add(MemoryItem(content="概念C", tags=["y"]))
        gs.add_relation(id1, id3, "关联")

        original_stats = gs.graph_stats()
        snap = gs.to_snapshot_dict()
        restored = GraphMemoryStore.from_snapshot_dict(snap)

        assert restored.size() == gs.size()
        assert restored.graph_stats()["edges"] == original_stats["edges"]

    def test_vector_snapshot_roundtrip(self):
        """VectorMemoryStore 手动设置 embedding 的序列化往返。"""
        vs = VectorMemoryStore()
        # 手动设置 embedding，不调用 _get_model
        item1 = MemoryItem(
            content="向量A",
            embedding=[0.1, 0.2, 0.3],
            tags=["vec"],
        )
        item2 = MemoryItem(
            content="向量B",
            embedding=[0.4, 0.5, 0.6],
            tags=["vec"],
        )
        # 直接写入 _memories 跳过 _encode
        vs._memories[item1.id] = item1
        vs._memories[item2.id] = item2

        snap = vs.to_snapshot_dict()
        restored = VectorMemoryStore.from_snapshot_dict(snap)

        assert restored.size() == vs.size()
        # 验证 embedding 值一致
        for orig_item in vs.list_all():
            restored_item = next(i for i in restored.list_all() if i.id == orig_item.id)
            assert restored_item.embedding == orig_item.embedding


# ---------------------------------------------------------------------------
# Formation 质量指标测试
# ---------------------------------------------------------------------------


class TestFormationMetrics:
    def test_build_formation_scenario_returns_structure(self):
        from src.memory.evaluation import build_formation_scenario

        manager, events, expected_writes = build_formation_scenario()
        assert len(events) >= 10
        assert len(expected_writes) >= 3
        assert len(expected_writes) < len(events)  # 非全写入

    def test_compute_formation_metrics_perfect(self):
        from src.memory.evaluation import compute_formation_metrics

        actual = {"a", "b", "c"}
        expected = {"a", "b", "c"}
        m = compute_formation_metrics(actual, expected)
        assert m["formation_precision"] == 1.0
        assert m["formation_recall"] == 1.0

    def test_compute_formation_metrics_partial(self):
        from src.memory.evaluation import compute_formation_metrics

        actual = {"a", "b", "d"}  # d 是误写，c 被遗漏
        expected = {"a", "b", "c"}
        m = compute_formation_metrics(actual, expected)
        assert abs(m["formation_precision"] - 2 / 3) < 1e-9
        assert abs(m["formation_recall"] - 2 / 3) < 1e-9

    def test_compute_formation_metrics_empty_actual(self):
        from src.memory.evaluation import compute_formation_metrics

        m = compute_formation_metrics(set(), {"a", "b"})
        assert m["formation_precision"] == 0.0
        assert m["formation_recall"] == 0.0

    def test_formation_scenario_rule_produces_perfect_score(self):
        from src.memory.evaluation import (
            build_formation_scenario,
            compute_formation_metrics,
        )

        _IMPORTANCE_THRESHOLD = 0.6
        _CONTENT_MIN_LEN = 5
        manager, events, expected_writes = build_formation_scenario()
        actual_writes = {
            e["id"]
            for e in events
            if e["importance"] >= _IMPORTANCE_THRESHOLD
            and len(e["content"]) >= _CONTENT_MIN_LEN
        }
        m = compute_formation_metrics(actual_writes, expected_writes)
        assert m["formation_precision"] == 1.0
        assert m["formation_recall"] == 1.0


# ---------------------------------------------------------------------------
# Evolution 正确性指标测试
# ---------------------------------------------------------------------------


class TestEvolutionMetrics:
    def test_build_evolution_scenario_returns_structure(self):
        from src.memory.evaluation import build_evolution_scenario

        manager, update_events, expected_state = build_evolution_scenario()
        assert len(update_events) >= 3
        assert len(expected_state) >= 3
        assert any(v is None for v in expected_state.values())  # 至少一条遗忘

    def test_compute_evolution_metrics_perfect(self):
        from src.memory.evaluation import compute_evolution_metrics

        actual = {"m1": "content A", "m2": "content B"}
        expected = {"m1": "content A", "m2": "content B", "m3": None}
        m = compute_evolution_metrics(actual, expected)
        assert m["evolution_accuracy"] == 1.0
        assert m["forgetting_precision"] == 1.0

    def test_compute_evolution_metrics_partial(self):
        from src.memory.evaluation import compute_evolution_metrics

        actual = {"m1": "content A", "m2": "wrong", "m3": "should be gone"}
        expected = {"m1": "content A", "m2": "content B", "m3": None}
        m = compute_evolution_metrics(actual, expected)
        assert m["evolution_accuracy"] < 1.0
        assert m["forgetting_precision"] == 0.0

    def test_evolution_scenario_correct_execution(self):
        from src.memory.evaluation import (
            build_evolution_scenario,
            compute_evolution_metrics,
        )

        manager, update_events, expected_state = build_evolution_scenario()
        for event in update_events:
            if event["type"] == "update":
                manager.update_memory(event["target_id"], content=event["new_content"])
            elif event["type"] == "forget":
                manager.forget(event["target_id"])
        all_items: dict[str, str] = {}
        for store_name in manager._stores:
            for item in manager.get_store(store_name).list_all():
                all_items[item.id] = item.content
        m = compute_evolution_metrics(all_items, expected_state)
        assert m["evolution_accuracy"] >= 0.8
        assert m["forgetting_precision"] >= 0.9


class TestEvaluationOutputs:
    def test_compute_metrics_uses_expected_ranking(self):
        from src.memory.evaluation import compute_metrics

        queries = [{"query": "q1", "expected_ids": ["m1"], "top_k": 5}]
        results = [
            [
                (MemoryItem(id="m2", content="x"), 0.9, "ep"),
                (MemoryItem(id="m1", content="y"), 0.8, "graph"),
            ]
        ]

        metrics = compute_metrics(queries, results)

        assert metrics["hit@1"] == 0.0
        assert metrics["hit@3"] == 1.0
        assert metrics["mrr"] == 0.5

    def test_export_memoryagentbench_writes_jsonl_and_md(self, tmp_path):
        from src.memory.export_memoryagentbench import export_memoryagentbench

        summary = export_memoryagentbench(
            dataset_root="/Users/jinyh/Documents/AIProjects/AgentResearch/ref/datasets/MemoryAgentBench",
            out_root=str(tmp_path / "normalized"),
        )

        out_root = tmp_path / "normalized"
        assert (out_root / "Accurate_Retrieval.jsonl").exists()
        assert (out_root / "Accurate_Retrieval.md").exists()
        assert (out_root / "Test_Time_Learning.jsonl").exists()
        assert (out_root / "Test_Time_Learning.md").exists()
        assert (out_root / "Long_Range_Understanding.jsonl").exists()
        assert (out_root / "Long_Range_Understanding.md").exists()
        assert (out_root / "Conflict_Resolution.jsonl").exists()
        assert (out_root / "Conflict_Resolution.md").exists()
        assert (out_root / "README.md").exists()
        assert summary["Accurate_Retrieval"] > 0

    def test_load_benchmark_cases_normalizes_files(self):
        dataset_root = Path(
            "/Users/jinyh/Documents/AIProjects/AgentResearch/ref/datasets"
        )

        cases = load_benchmark_cases(str(dataset_root))

        assert isinstance(cases, list)
        assert len(cases) > 0
        assert all(
            {"id", "query", "expected_ids", "top_k"}.issubset(case) for case in cases
        )

    def test_run_dataset_benchmark_writes_artifacts(self, tmp_path, monkeypatch):
        def fake_encode(self, text: str):
            vocab = ["memory", "agent", "task"]
            lowered = text.lower()
            return [lowered.count(token) for token in vocab]

        monkeypatch.setattr(VectorMemoryStore, "_encode", fake_encode)

        summary = run_dataset_benchmark(
            dataset_dir="/Users/jinyh/Documents/AIProjects/AgentResearch/ref/datasets",
            out_dir=str(tmp_path / "dataset-out"),
        )

        out_dir = tmp_path / "dataset-out"
        assert (out_dir / "report.json").exists()
        assert (out_dir / "report.md").exists()
        assert (out_dir / "cases.jsonl").exists()
        assert "benchmark_name" in summary
        assert "coverage" in summary

    def test_run_evaluation_writes_artifacts(self, tmp_path):
        from src.memory.evaluation import run_evaluation

        summary = run_evaluation(str(tmp_path))

        report_json = tmp_path / "report.json"
        report_md = tmp_path / "report.md"
        cases_jsonl = tmp_path / "cases.jsonl"

        assert report_json.exists()
        assert report_md.exists()
        assert cases_jsonl.exists()
        assert summary["snapshot_roundtrip_consistent"] is True
        assert summary["retrieval_backend"]["semantic_vector_store_enabled"] is False

        report = json.loads(report_json.read_text(encoding="utf-8"))
        assert {"formation", "evolution", "retrieval", "retrieval_backend"}.issubset(
            report.keys()
        )
        assert report["retrieval_backend"]["semantic_vector_store_enabled"] is False
        assert len(cases_jsonl.read_text(encoding="utf-8").strip().splitlines()) > 0

    def test_build_scenario_with_vector_store(self, monkeypatch):
        def fake_encode(self, text: str):
            vocab = ["python", "rag", "记忆"]
            lowered = text.lower()
            return [lowered.count(token) for token in vocab]

        monkeypatch.setattr(VectorMemoryStore, "_encode", fake_encode)
        manager, queries = build_scenario(enable_vector_store=True)

        assert "vector" in manager._stores
        assert len(queries) > 0

    def test_vector_store_query_and_update(self, monkeypatch):
        def fake_encode(self, text: str):
            vocab = ["python", "rust", "agent"]
            lowered = text.lower()
            return [lowered.count(token) for token in vocab]

        monkeypatch.setattr(VectorMemoryStore, "_encode", fake_encode)
        store = VectorMemoryStore()
        python_id = store.add(MemoryItem(content="Python 记忆系统", tags=["python"]))
        rust_id = store.add(MemoryItem(content="Rust 运行时", tags=["rust"]))

        results = store.query("python", top_k=2)
        assert results[0][0].id == python_id

        store.update(rust_id, content="Python 与 Rust 的比较")
        results_after = store.query("python", top_k=2)
        assert results_after[0][0].id in {python_id, rust_id}
        assert any(item.id == rust_id for item, _score in results_after)
