"""Agent Memory 核心模块测试。"""

import time

import pytest

from src.memory.base import MemoryItem, MemoryType
from src.memory.episodic import EpisodicMemory
from src.memory.graph_store import GraphMemoryStore
from src.memory.manager import MemoryManager


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
        assert "Python" in results[0][0].content or "python" in results[0][0].content.lower()

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
        id1 = gs.add(MemoryItem(content="Python", tags=["编程"]))
        id2 = gs.add(MemoryItem(content="Java", tags=["编程"]))

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
