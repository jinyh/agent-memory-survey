"""记忆管理器。

统一调度不同类型的记忆存储，支持跨存储检索、
情景→语义的巩固路径、以及自适应遗忘策略。
"""

from __future__ import annotations

import logging
from typing import Any

from .base import MemoryItem, MemoryStore, MemoryType
from .episodic import EpisodicMemory

logger = logging.getLogger(__name__)


class MemoryManager:
    """Agent 记忆管理器。

    协调多个记忆存储后端（情景、语义、图等），
    提供统一的记忆读写接口和生命周期管理。

    灵感来源:
    - MemGPT/Letta: 分层记忆管理
    - AgeMem: 记忆操作作为 Agent 动作
    - LightMem: 离线巩固
    """

    def __init__(self):
        self._stores: dict[str, MemoryStore] = {}
        self._default_store: str | None = None
        self._consolidation_count = 0

    def register_store(
        self, name: str, store: MemoryStore, default: bool = False
    ) -> None:
        """注册一个记忆存储后端。"""
        self._stores[name] = store
        if default or not self._default_store:
            self._default_store = name

    def get_store(self, name: str) -> MemoryStore:
        """获取指定名称的存储后端。"""
        if name not in self._stores:
            raise KeyError(f"未注册的记忆存储: {name}")
        return self._stores[name]

    # ---- 核心操作 ----

    def remember(
        self,
        content: str,
        memory_type: MemoryType = MemoryType.SEMANTIC,
        store_name: str | None = None,
        importance: float = 0.5,
        tags: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> str:
        """存储一条新记忆。"""
        store_name = store_name or self._default_store
        if not store_name:
            raise RuntimeError("没有可用的记忆存储")

        item = MemoryItem(
            content=content,
            memory_type=memory_type,
            importance=importance,
            tags=tags or [],
            metadata=metadata or {},
        )
        store = self._stores[store_name]
        memory_id = store.add(item)
        logger.debug(f"记忆已存储: [{store_name}] {memory_id[:8]}...")
        return memory_id

    def recall(
        self,
        query: str,
        top_k: int = 5,
        store_names: list[str] | None = None,
        memory_type: MemoryType | None = None,
    ) -> list[tuple[MemoryItem, float, str]]:
        """从一个或多个存储中检索记忆。

        返回 (记忆, 分数, 存储名) 列表。
        """
        store_names = store_names or list(self._stores.keys())
        all_results: list[tuple[MemoryItem, float, str]] = []

        for name in store_names:
            if name not in self._stores:
                continue
            results = self._stores[name].query(
                query, top_k=top_k, memory_type=memory_type
            )
            for item, score in results:
                all_results.append((item, score, name))

        # 按分数排序，跨存储合并
        all_results.sort(key=lambda x: x[1], reverse=True)
        return all_results[:top_k]

    def forget(self, memory_id: str, store_name: str | None = None) -> bool:
        """删除指定记忆。"""
        if store_name:
            return self._stores[store_name].delete(memory_id)
        # 在所有存储中尝试删除
        for store in self._stores.values():
            if store.delete(memory_id):
                return True
        return False

    def update_memory(
        self, memory_id: str, store_name: str | None = None, **kwargs: Any
    ) -> bool:
        """更新指定记忆。"""
        if store_name:
            return self._stores[store_name].update(memory_id, **kwargs)
        for store in self._stores.values():
            if store.update(memory_id, **kwargs):
                return True
        return False

    # ---- 巩固与生命周期管理 ----

    def consolidate_all(self) -> dict[str, int]:
        """对所有存储执行巩固操作。"""
        results = {}
        for name, store in self._stores.items():
            count = store.consolidate()
            results[name] = count
        self._consolidation_count += 1
        logger.info(f"巩固完成 (第{self._consolidation_count}次): {results}")
        return results

    def consolidate_episodic_to_semantic(
        self,
        episodic_store_name: str,
        semantic_store_name: str,
        min_frequency: int = 3,
    ) -> list[str]:
        """将情景记忆中的重复模式巩固为语义记忆。

        这实现了认知科学中 "情景→语义" 的巩固路径。
        """
        episodic = self._stores.get(episodic_store_name)
        semantic = self._stores.get(semantic_store_name)

        if not isinstance(episodic, EpisodicMemory) or semantic is None:
            return []

        patterns = episodic.extract_patterns(min_frequency=min_frequency)
        new_semantic_ids = []

        for pattern in patterns:
            # 收集相关情景记忆的内容
            related_items = []
            for sample_id in pattern["sample_ids"]:
                items = [
                    item
                    for item in episodic.list_all()
                    if item.id == sample_id
                ]
                related_items.extend(items)

            if not related_items:
                continue

            # 生成语义摘要（简化版：拼接关键内容）
            summary_parts = [item.content for item in related_items[:3]]
            summary = f"[巩固自{pattern['frequency']}次情景] " + " | ".join(
                summary_parts
            )

            semantic_item = MemoryItem(
                content=summary,
                memory_type=MemoryType.SEMANTIC,
                importance=pattern["avg_importance"],
                tags=[pattern["tag"], "consolidated"],
                metadata={
                    "source": "episodic_consolidation",
                    "episode_count": pattern["frequency"],
                    "source_ids": pattern["sample_ids"],
                },
            )
            mid = semantic.add(semantic_item)
            new_semantic_ids.append(mid)
            logger.debug(
                f"巩固: '{pattern['tag']}' ({pattern['frequency']}次) → 语义记忆 {mid[:8]}"
            )

        return new_semantic_ids

    # ---- 状态查询 ----

    def stats(self) -> dict[str, Any]:
        """返回所有存储的统计信息。"""
        return {
            name: {
                "size": store.size(),
                "type": type(store).__name__,
            }
            for name, store in self._stores.items()
        }

    def total_memories(self) -> int:
        """返回所有存储的记忆总数。"""
        return sum(store.size() for store in self._stores.values())
