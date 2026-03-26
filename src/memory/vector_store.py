"""基于向量嵌入的语义记忆后端。

使用 sentence-transformers 生成嵌入向量，
支持余弦相似度检索。轻量实现，不依赖外部向量数据库。
"""

from __future__ import annotations

from typing import Any

import numpy as np

from .base import MemoryItem, MemoryStore, MemoryType


def _cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """计算两个向量的余弦相似度。"""
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(np.dot(a, b) / (norm_a * norm_b))


class VectorMemoryStore(MemoryStore):
    """基于向量嵌入的语义记忆存储。

    使用 sentence-transformers 编码文本为向量，
    通过余弦相似度进行语义检索。
    """

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
        max_capacity: int = 10000,
        decay_rate: float = 0.01,
    ):
        self._memories: dict[str, MemoryItem] = {}
        self._max_capacity = max_capacity
        self._decay_rate = decay_rate
        self._model_name = model_name
        self._model = None  # lazy load

    def _get_model(self):
        """延迟加载 embedding 模型。"""
        if self._model is None:
            try:
                from sentence_transformers import SentenceTransformer

                self._model = SentenceTransformer(self._model_name)
            except ImportError:
                raise ImportError(
                    "需要安装 sentence-transformers: "
                    "uv pip install sentence-transformers"
                )
        return self._model

    def _encode(self, text: str) -> list[float]:
        """将文本编码为嵌入向量。"""
        model = self._get_model()
        embedding = model.encode(text, convert_to_numpy=True)
        return embedding.tolist()

    def add(self, item: MemoryItem) -> str:
        if item.embedding is None:
            item.embedding = self._encode(item.content)
        self._memories[item.id] = item
        # 容量管理：超过上限时清理低分记忆
        if len(self._memories) > self._max_capacity:
            self._evict_lowest()
        return item.id

    def query(
        self,
        query: str,
        top_k: int = 5,
        memory_type: MemoryType | None = None,
        min_score: float = 0.0,
    ) -> list[tuple[MemoryItem, float]]:
        if not self._memories:
            return []

        query_embedding = np.array(self._encode(query))
        results: list[tuple[MemoryItem, float]] = []

        for item in self._memories.values():
            if memory_type and item.memory_type != memory_type:
                continue
            if item.embedding is None:
                continue

            # 语义相似度 * 时间衰减加权
            sim = _cosine_similarity(query_embedding, np.array(item.embedding))
            decay = item.decay_score(self._decay_rate)
            score = 0.7 * sim + 0.3 * decay  # 加权组合

            if score >= min_score:
                results.append((item, score))

        results.sort(key=lambda x: x[1], reverse=True)

        # 更新访问记录
        for item, _ in results[:top_k]:
            item.touch()

        return results[:top_k]

    def update(self, memory_id: str, **kwargs) -> bool:
        if memory_id not in self._memories:
            return False
        item = self._memories[memory_id]
        for key, value in kwargs.items():
            if hasattr(item, key):
                setattr(item, key, value)
        # 如果内容更新了，重新编码
        if "content" in kwargs:
            item.embedding = self._encode(item.content)
        return True

    def delete(self, memory_id: str) -> bool:
        if memory_id not in self._memories:
            return False
        del self._memories[memory_id]
        return True

    def consolidate(self) -> int:
        """清理低分记忆。"""
        threshold = 0.1
        to_remove = [
            mid
            for mid, item in self._memories.items()
            if item.decay_score(self._decay_rate) < threshold
        ]
        for mid in to_remove:
            del self._memories[mid]
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

    # ── 序列化 / 反序列化 ──────────────────────────────

    def get_init_kwargs(self) -> dict:
        return {
            "model_name": self._model_name,
            "max_capacity": self._max_capacity,
            "decay_rate": self._decay_rate,
        }

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
        return {"init_kwargs": self.get_init_kwargs(), "items": items}

    @classmethod
    def from_snapshot_dict(cls, data: dict, **kwargs: Any) -> VectorMemoryStore:
        """从 dict 恢复 store 状态（不重新编码 embedding），kwargs 优先，缺省回退到 data['init_kwargs']。"""
        init = {**data.get("init_kwargs", {}), **kwargs}
        store = cls(
            model_name=init.get("model_name", "all-MiniLM-L6-v2"),
            max_capacity=init.get("max_capacity", 10000),
            decay_rate=init.get("decay_rate", 0.01),
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
            # 直接写入 _memories，跳过 add() 避免触发重新编码
            store._memories[item.id] = item
        return store

    def _evict_lowest(self) -> None:
        """淘汰衰减分数最低的记忆。"""
        if not self._memories:
            return
        lowest_id = min(
            self._memories,
            key=lambda mid: self._memories[mid].decay_score(self._decay_rate),
        )
        del self._memories[lowest_id]
