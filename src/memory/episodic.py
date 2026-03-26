"""情景记忆实现。

按时间索引存储具体事件/交互，支持时间衰减权重和重要性评分。
灵感来自 AriGraph 和 "Episodic Memory is the Missing Piece" 论文。
"""

from __future__ import annotations

from typing import Any

from .base import MemoryItem, MemoryStore, MemoryType


class EpisodicMemory(MemoryStore):
    """情景记忆存储。

    特点:
    - 按时间顺序索引
    - 支持时间衰减（旧记忆逐渐被遗忘）
    - 重要性评分（关键事件保留更久）
    - 支持巩固：将频繁出现的模式提取为语义记忆
    """

    def __init__(
        self,
        max_capacity: int = 5000,
        decay_rate: float = 0.02,
        importance_threshold: float = 0.3,
    ):
        self._episodes: dict[str, MemoryItem] = {}
        self._timeline: list[str] = []  # 按时间排序的 ID 列表
        self._max_capacity = max_capacity
        self._decay_rate = decay_rate
        self._importance_threshold = importance_threshold

    def add(self, item: MemoryItem) -> str:
        item.memory_type = MemoryType.EPISODIC
        self._episodes[item.id] = item
        self._timeline.append(item.id)
        if len(self._episodes) > self._max_capacity:
            self._evict_oldest_unimportant()
        return item.id

    def add_episode(
        self,
        content: str,
        importance: float = 0.5,
        tags: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> str:
        """添加一条情景记忆的便捷方法。"""
        item = MemoryItem(
            content=content,
            memory_type=MemoryType.EPISODIC,
            importance=importance,
            tags=tags or [],
            metadata=metadata or {},
        )
        return self.add(item)

    def query(
        self,
        query: str,
        top_k: int = 5,
        memory_type: MemoryType | None = None,
        min_score: float = 0.0,
    ) -> list[tuple[MemoryItem, float]]:
        """基于关键词匹配 + 时间衰减 + 重要性的检索。"""
        query_lower = query.lower()
        query_terms = set(query_lower.split())

        scored: list[tuple[MemoryItem, float]] = []
        for item in self._episodes.values():
            # 文本匹配
            content_lower = item.content.lower()
            term_hits = sum(1 for t in query_terms if t in content_lower)
            text_score = term_hits / max(len(query_terms), 1)

            # 时间衰减
            decay = item.decay_score(self._decay_rate)

            # 综合分数
            score = 0.5 * text_score + 0.3 * decay + 0.2 * item.importance

            if score >= min_score:
                scored.append((item, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        for item, _ in scored[:top_k]:
            item.touch()
        return scored[:top_k]

    def query_by_time(
        self,
        start_time: float | None = None,
        end_time: float | None = None,
        limit: int = 20,
    ) -> list[MemoryItem]:
        """按时间范围检索情景记忆。"""
        results = []
        for mid in reversed(self._timeline):
            if mid not in self._episodes:
                continue
            item = self._episodes[mid]
            if start_time and item.created_at < start_time:
                continue
            if end_time and item.created_at > end_time:
                continue
            results.append(item)
            if len(results) >= limit:
                break
        return results

    def recent(self, n: int = 10) -> list[MemoryItem]:
        """获取最近 n 条情景记忆。"""
        result = []
        for mid in reversed(self._timeline):
            if mid in self._episodes:
                result.append(self._episodes[mid])
                if len(result) >= n:
                    break
        return result

    def update(self, memory_id: str, **kwargs) -> bool:
        if memory_id not in self._episodes:
            return False
        item = self._episodes[memory_id]
        for key, value in kwargs.items():
            if hasattr(item, key):
                setattr(item, key, value)
        return True

    def delete(self, memory_id: str) -> bool:
        if memory_id not in self._episodes:
            return False
        del self._episodes[memory_id]
        # 不从 timeline 移除（惰性清理）
        return True

    def consolidate(self) -> int:
        """巩固情景记忆：清理低重要性的过期记忆。

        返回被清理的记忆数量。
        真正的巩固（提取模式→语义记忆）由 MemoryManager 协调。
        """
        to_remove = []
        for mid, item in self._episodes.items():
            score = item.decay_score(self._decay_rate)
            if score < self._importance_threshold and item.importance < 0.7:
                to_remove.append(mid)

        for mid in to_remove:
            del self._episodes[mid]

        # 清理 timeline 中的无效引用
        self._timeline = [
            mid for mid in self._timeline if mid in self._episodes
        ]
        return len(to_remove)

    def extract_patterns(self, min_frequency: int = 3) -> list[dict[str, Any]]:
        """从情景记忆中提取重复出现的模式/主题。

        这些模式可以被 MemoryManager 转化为语义记忆（巩固路径）。
        """
        from collections import Counter

        tag_counter: Counter[str] = Counter()
        for item in self._episodes.values():
            for tag in item.tags:
                tag_counter[tag] += 1

        patterns = []
        for tag, count in tag_counter.items():
            if count >= min_frequency:
                related = [
                    item
                    for item in self._episodes.values()
                    if tag in item.tags
                ]
                avg_importance = sum(i.importance for i in related) / len(related)
                patterns.append(
                    {
                        "tag": tag,
                        "frequency": count,
                        "avg_importance": avg_importance,
                        "sample_ids": [i.id for i in related[:3]],
                    }
                )
        return sorted(patterns, key=lambda x: x["frequency"], reverse=True)

    def list_all(
        self, memory_type: MemoryType | None = None
    ) -> list[MemoryItem]:
        return sorted(
            self._episodes.values(),
            key=lambda x: x.created_at,
            reverse=True,
        )

    def size(self) -> int:
        return len(self._episodes)

    # ── 序列化 / 反序列化 ──────────────────────────────

    def get_init_kwargs(self) -> dict:
        return {
            "max_capacity": self._max_capacity,
            "decay_rate": self._decay_rate,
            "importance_threshold": self._importance_threshold,
        }

    def to_snapshot_dict(self) -> dict:
        """将全部状态导出为可 JSON 序列化的 dict。"""
        items = []
        for item in self._episodes.values():
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
        return {
            "init_kwargs": self.get_init_kwargs(),
            "items": items,
            "timeline": list(self._timeline),
        }

    @classmethod
    def from_snapshot_dict(cls, data: dict, **kwargs: Any) -> EpisodicMemory:
        """从 dict 恢复 store 状态，kwargs 优先，缺省回退到 data['init_kwargs']。"""
        init = {**data.get("init_kwargs", {}), **kwargs}
        store = cls(
            max_capacity=init.get("max_capacity", 5000),
            decay_rate=init.get("decay_rate", 0.02),
            importance_threshold=init.get("importance_threshold", 0.3),
        )
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
            store._episodes[item.id] = item
        store._timeline = list(data.get("timeline", []))
        return store

    def _evict_oldest_unimportant(self) -> None:
        """淘汰最旧且最不重要的记忆。"""
        candidates = sorted(
            self._episodes.items(),
            key=lambda x: x[1].decay_score(self._decay_rate),
        )
        if candidates:
            self.delete(candidates[0][0])
