"""基于知识图谱的结构化记忆后端。

使用 NetworkX 实现轻量知识图谱，支持实体-关系-实体三元组存储，
以及基于图遍历的检索。灵感来自 Zep/Graphiti 的时序知识图谱。
"""

from __future__ import annotations

import time
from typing import Any

try:
    import networkx as nx
except ImportError:
    nx = None

from .base import MemoryItem, MemoryStore, MemoryType


class GraphMemoryStore(MemoryStore):
    """基于知识图谱的记忆存储。

    每条记忆存储为图中的节点，记忆间的关系存储为边。
    支持通过图遍历发现关联记忆。
    """

    def __init__(self, max_capacity: int = 10000, decay_rate: float = 0.01):
        if nx is None:
            raise ImportError(
                "需要安装 networkx: uv pip install networkx"
            )
        self._graph = nx.DiGraph()
        self._memories: dict[str, MemoryItem] = {}
        self._max_capacity = max_capacity
        self._decay_rate = decay_rate

    def add(self, item: MemoryItem) -> str:
        self._memories[item.id] = item
        self._graph.add_node(
            item.id,
            content=item.content,
            memory_type=item.memory_type.value,
            created_at=item.created_at,
            importance=item.importance,
            tags=item.tags,
        )
        # 建立与已有记忆的链接
        for link_id in item.links:
            if link_id in self._memories:
                self._graph.add_edge(
                    item.id, link_id, relation="linked", created_at=time.time()
                )
                self._graph.add_edge(
                    link_id, item.id, relation="linked", created_at=time.time()
                )
        # 基于 tag 重叠自动建立弱链接
        for other_id, other in self._memories.items():
            if other_id == item.id:
                continue
            shared_tags = set(item.tags) & set(other.tags)
            if shared_tags and not self._graph.has_edge(item.id, other_id):
                self._graph.add_edge(
                    item.id,
                    other_id,
                    relation="tag_overlap",
                    shared_tags=list(shared_tags),
                    created_at=time.time(),
                )
        return item.id

    def add_relation(
        self, source_id: str, target_id: str, relation: str, **attrs: Any
    ) -> bool:
        """显式添加两条记忆之间的关系。"""
        if source_id not in self._memories or target_id not in self._memories:
            return False
        self._graph.add_edge(
            source_id,
            target_id,
            relation=relation,
            created_at=time.time(),
            **attrs,
        )
        return True

    def query(
        self,
        query: str,
        top_k: int = 5,
        memory_type: MemoryType | None = None,
        min_score: float = 0.0,
    ) -> list[tuple[MemoryItem, float]]:
        """基于关键词匹配 + 图邻居扩展的检索。"""
        query_lower = query.lower()
        query_terms = set(query_lower.split())

        scored: list[tuple[MemoryItem, float]] = []
        for item in self._memories.values():
            if memory_type and item.memory_type != memory_type:
                continue

            # 文本匹配分数
            content_lower = item.content.lower()
            term_hits = sum(1 for t in query_terms if t in content_lower)
            text_score = term_hits / max(len(query_terms), 1)

            # tag 匹配分数
            tag_hits = sum(
                1 for t in query_terms if any(t in tag.lower() for tag in item.tags)
            )
            tag_score = tag_hits / max(len(query_terms), 1)

            # 图中心性加权
            try:
                degree = self._graph.degree(item.id)
                centrality_bonus = min(degree / 10.0, 0.3)
            except nx.NetworkXError:
                centrality_bonus = 0.0

            # 时间衰减
            decay = item.decay_score(self._decay_rate)

            score = 0.4 * text_score + 0.2 * tag_score + 0.1 * centrality_bonus + 0.3 * decay

            if score >= min_score:
                scored.append((item, score))

        scored.sort(key=lambda x: x[1], reverse=True)

        # 对 top 结果进行图邻居扩展
        seen_ids = {item.id for item, _ in scored[:top_k]}
        expanded: list[tuple[MemoryItem, float]] = list(scored[:top_k])

        for item, score in scored[:top_k]:
            item.touch()
            for neighbor_id in self._graph.neighbors(item.id):
                if neighbor_id not in seen_ids and neighbor_id in self._memories:
                    neighbor = self._memories[neighbor_id]
                    if memory_type and neighbor.memory_type != memory_type:
                        continue
                    neighbor_score = score * 0.5  # 邻居得分衰减
                    expanded.append((neighbor, neighbor_score))
                    seen_ids.add(neighbor_id)

        expanded.sort(key=lambda x: x[1], reverse=True)
        return expanded[:top_k]

    def get_neighbors(self, memory_id: str, depth: int = 1) -> list[MemoryItem]:
        """获取指定记忆的图邻居（BFS 到指定深度）。"""
        if memory_id not in self._graph:
            return []
        visited: set[str] = set()
        current_level = {memory_id}
        for _ in range(depth):
            next_level: set[str] = set()
            for node in current_level:
                for neighbor in self._graph.neighbors(node):
                    if neighbor not in visited and neighbor != memory_id:
                        next_level.add(neighbor)
                        visited.add(neighbor)
            current_level = next_level
        return [self._memories[nid] for nid in visited if nid in self._memories]

    def update(self, memory_id: str, **kwargs) -> bool:
        if memory_id not in self._memories:
            return False
        item = self._memories[memory_id]
        for key, value in kwargs.items():
            if hasattr(item, key):
                setattr(item, key, value)
        # 同步更新图节点属性
        if memory_id in self._graph:
            self._graph.nodes[memory_id].update(
                {k: v for k, v in kwargs.items() if k in ("content", "importance", "tags")}
            )
        return True

    def delete(self, memory_id: str) -> bool:
        if memory_id not in self._memories:
            return False
        del self._memories[memory_id]
        if memory_id in self._graph:
            self._graph.remove_node(memory_id)
        return True

    def consolidate(self) -> int:
        """清理低分记忆和孤立节点。"""
        threshold = 0.1
        to_remove = []
        for mid, item in self._memories.items():
            score = item.decay_score(self._decay_rate)
            degree = self._graph.degree(mid) if mid in self._graph else 0
            # 低分且孤立的记忆优先清理
            if score < threshold and degree <= 1:
                to_remove.append(mid)
        for mid in to_remove:
            self.delete(mid)
        return len(to_remove)

    def list_all(
        self, memory_type: MemoryType | None = None
    ) -> list[MemoryItem]:
        items = list(self._memories.values())
        if memory_type:
            items = [i for i in items if i.memory_type == memory_type]
        return sorted(items, key=lambda x: x.created_at, reverse=True)

    def size(self) -> int:
        return len(self._memories)

    def graph_stats(self) -> dict[str, Any]:
        """返回图的统计信息。"""
        return {
            "nodes": self._graph.number_of_nodes(),
            "edges": self._graph.number_of_edges(),
            "density": nx.density(self._graph) if self._graph.number_of_nodes() > 1 else 0,
            "components": nx.number_weakly_connected_components(self._graph),
        }

    # ── 序列化 / 反序列化 ──────────────────────────────

    def to_snapshot_dict(self) -> dict:
        """将全部状态导出为可 JSON 序列化的 dict。"""
        items = []
        for item in self._memories.values():
            items.append({
                "content": item.content,
                "memory_type": item.memory_type.value,
                "metadata": item.metadata,
                "id": item.id,
                "created_at": item.created_at,
                "last_accessed": item.last_accessed,
                "access_count": item.access_count,
                "importance": item.importance,
                "embedding": item.embedding,
                "tags": item.tags,
                "links": item.links,
            })
        edges = []
        for source, target, edge_data in self._graph.edges(data=True):
            relation = edge_data.get("relation", "")
            attrs = {k: v for k, v in edge_data.items() if k != "relation"}
            edges.append({
                "source": source,
                "target": target,
                "relation": relation,
                "attrs": attrs,
            })
        return {
            "items": items,
            "edges": edges,
        }

    @classmethod
    def from_snapshot_dict(
        cls,
        data: dict,
        max_capacity: int = 10000,
        decay_rate: float = 0.01,
    ) -> GraphMemoryStore:
        """从 dict 恢复 store 状态。"""
        store = cls(max_capacity=max_capacity, decay_rate=decay_rate)
        for d in data.get("items", []):
            item = MemoryItem(
                content=d["content"],
                memory_type=MemoryType(d["memory_type"]),
                metadata=d.get("metadata", {}),
                id=d["id"],
                created_at=d["created_at"],
                last_accessed=d["last_accessed"],
                access_count=d.get("access_count", 0),
                importance=d.get("importance", 0.5),
                embedding=d.get("embedding"),
                tags=d.get("tags", []),
                links=d.get("links", []),
            )
            store._memories[item.id] = item
            # 恢复图节点（与 add() 中的属性保持一致）
            store._graph.add_node(
                item.id,
                content=item.content,
                memory_type=item.memory_type.value,
                created_at=item.created_at,
                importance=item.importance,
                tags=item.tags,
            )
        # 恢复图边
        for edge in data.get("edges", []):
            store._graph.add_edge(
                edge["source"],
                edge["target"],
                relation=edge["relation"],
                **edge.get("attrs", {}),
            )
        return store
