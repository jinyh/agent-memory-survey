"""记忆管理器。

统一调度不同类型的记忆存储，支持跨存储检索、
情景→语义的巩固路径、以及自适应遗忘策略。
"""

from __future__ import annotations

import json
import logging
import os
import time
from typing import Any

from .base import FusionConfig, MemoryItem, MemoryStore, MemoryType
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

    def __init__(self, fusion_config: FusionConfig | None = None):
        self._stores: dict[str, MemoryStore] = {}
        self._default_store: str | None = None
        self._consolidation_count = 0
        self._fusion_config = fusion_config or FusionConfig()

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
        """从一个或多个存储中检索记忆（rank 归一化融合）。

        1. 对每个 store 预取 top_k * overfetch_factor 条结果
        2. 按 rank 归一化: normalized_score = 1.0 / rank
        3. 乘以 store 权重: fused_score = weight * normalized_score
        4. 跨 store 合并，按 fused_score 降序取 top_k

        返回 (记忆, fused_score, 存储名) 列表。
        """
        store_names = store_names or list(self._stores.keys())
        overfetch_k = top_k * self._fusion_config.overfetch_factor

        # item_id → (MemoryItem, fused_score, store_name)
        # 同一条记忆可能出现在多个 store，取最高 fused_score
        merged: dict[str, tuple[MemoryItem, float, str]] = {}

        for name in store_names:
            if name not in self._stores:
                continue
            weight = self._fusion_config.get_weight(name)
            results = self._stores[name].query(
                query, top_k=overfetch_k, memory_type=memory_type
            )
            for rank, (item, _raw_score) in enumerate(results, start=1):
                normalized_score = 1.0 / rank
                fused_score = weight * normalized_score
                existing = merged.get(item.id)
                if existing is None or fused_score > existing[1]:
                    merged[item.id] = (item, fused_score, name)

        all_results = list(merged.values())
        all_results.sort(key=lambda x: x[1], reverse=True)
        return all_results[:top_k]

    def recall_with_trace(
        self,
        query: str,
        top_k: int = 5,
        store_names: list[str] | None = None,
        memory_type: MemoryType | None = None,
    ) -> dict:
        """带调试追踪的检索，返回融合结果和每个 store 的评分明细。

        返回:
            {
                "results": [(MemoryItem, fused_score, store_name), ...],
                "trace": {
                    store_name: [
                        {"item_id": str, "raw_score": float, "rank": int,
                         "normalized_score": float, "fused_score": float}
                    ]
                }
            }
        """
        store_names = store_names or list(self._stores.keys())
        overfetch_k = top_k * self._fusion_config.overfetch_factor

        trace: dict[str, list[dict]] = {}
        merged: dict[str, tuple[MemoryItem, float, str]] = {}

        for name in store_names:
            if name not in self._stores:
                continue
            weight = self._fusion_config.get_weight(name)
            results = self._stores[name].query(
                query, top_k=overfetch_k, memory_type=memory_type
            )
            store_trace: list[dict] = []
            for rank, (item, raw_score) in enumerate(results, start=1):
                normalized_score = 1.0 / rank
                fused_score = weight * normalized_score
                store_trace.append({
                    "item_id": item.id,
                    "raw_score": raw_score,
                    "rank": rank,
                    "normalized_score": normalized_score,
                    "fused_score": fused_score,
                })
                existing = merged.get(item.id)
                if existing is None or fused_score > existing[1]:
                    merged[item.id] = (item, fused_score, name)
            trace[name] = store_trace

        all_results = list(merged.values())
        all_results.sort(key=lambda x: x[1], reverse=True)
        return {
            "results": all_results[:top_k],
            "trace": trace,
        }

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

    # ---- 快照持久化 ----

    def save_snapshot(self, path: str) -> dict:
        """将当前所有 store 状态序列化为 JSON 快照。

        Args:
            path: 快照目录路径，快照文件写入 {path}/snapshot.json

        Returns:
            manifest 摘要，包含路径、总记忆数、各 store 大小、创建时间
        """
        os.makedirs(path, exist_ok=True)

        created_at = time.time()
        stores_data: dict[str, Any] = {}
        stores_sizes: dict[str, int] = {}

        for name, store in self._stores.items():
            stores_data[name] = {
                "type": type(store).__name__,
                "data": store.to_snapshot_dict(),
            }
            stores_sizes[name] = store.size()

        snapshot = {
            "schema_version": "1.0",
            "created_at": created_at,
            "manager": {
                "consolidation_count": self._consolidation_count,
                "default_store": self._default_store,
                "fusion_config": {
                    "mode": self._fusion_config.mode,
                    "overfetch_factor": self._fusion_config.overfetch_factor,
                    "store_weights": self._fusion_config.store_weights,
                },
            },
            "stores": stores_data,
        }

        snapshot_path = os.path.join(path, "snapshot.json")
        with open(snapshot_path, "w", encoding="utf-8") as f:
            json.dump(snapshot, f, ensure_ascii=False, indent=2)

        total = sum(stores_sizes.values())
        logger.info(f"快照已保存: {snapshot_path} ({total} 条记忆)")
        return {
            "path": snapshot_path,
            "total_memories": total,
            "stores": stores_sizes,
            "created_at": created_at,
        }

    def load_snapshot(
        self, path: str, strict: bool = True, clear_before_load: bool = True
    ) -> dict:
        """从 JSON 快照恢复所有 store 状态。

        Args:
            path: 快照目录路径，读取 {path}/snapshot.json
            strict: 严格模式下校验 schema_version、ID 唯一性、图边端点完整性
            clear_before_load: 加载前是否清空已有 store 数据

        Returns:
            manifest 摘要

        Raises:
            ValueError: strict 模式下校验失败
            FileNotFoundError: 快照文件不存在
        """
        snapshot_path = os.path.join(path, "snapshot.json")
        with open(snapshot_path, "r", encoding="utf-8") as f:
            snapshot = json.load(f)

        # ---- strict 校验 ----
        if strict:
            self._validate_snapshot(snapshot)

        # ---- 恢复 manager 状态 ----
        mgr_state = snapshot.get("manager", {})
        self._consolidation_count = mgr_state.get(
            "consolidation_count", self._consolidation_count
        )
        self._default_store = mgr_state.get("default_store", self._default_store)
        fc = mgr_state.get("fusion_config", {})
        self._fusion_config = FusionConfig(
            mode=fc.get("mode", "rank"),
            overfetch_factor=fc.get("overfetch_factor", 3),
            store_weights=fc.get("store_weights", {}),
        )

        # ---- store 类型 → 类的映射 ----
        store_class_map = self._build_store_class_map()

        # ---- 恢复各 store ----
        stores_sizes: dict[str, int] = {}
        for name, store_snapshot in snapshot.get("stores", {}).items():
            store_type_name = store_snapshot["type"]
            store_data = store_snapshot["data"]

            if name not in self._stores:
                logger.warning(f"快照中的 store '{name}' 未注册，跳过")
                continue

            existing_store = self._stores[name]
            cls = store_class_map.get(store_type_name)
            if cls is None:
                logger.warning(
                    f"未知 store 类型 '{store_type_name}'，跳过 '{name}'"
                )
                continue

            # 清空已有数据
            if clear_before_load:
                for item in existing_store.list_all():
                    existing_store.delete(item.id)

            # 用已注册 store 实例的参数重建
            restored = cls.from_snapshot_dict(store_data, existing_store)
            self._stores[name] = restored
            stores_sizes[name] = restored.size()

        total = sum(stores_sizes.values())
        logger.info(f"快照已加载: {snapshot_path} ({total} 条记忆)")
        return {
            "path": snapshot_path,
            "total_memories": total,
            "stores": stores_sizes,
            "created_at": snapshot.get("created_at", 0),
        }

    @staticmethod
    def _build_store_class_map() -> dict[str, type]:
        """构建 store 类型名 → 类的映射。"""
        from .episodic import EpisodicMemory
        from .graph_store import GraphMemoryStore
        from .vector_store import VectorMemoryStore

        return {
            "EpisodicMemory": EpisodicMemory,
            "GraphMemoryStore": GraphMemoryStore,
            "VectorMemoryStore": VectorMemoryStore,
        }

    @staticmethod
    def _validate_snapshot(snapshot: dict) -> None:
        """严格模式下校验快照完整性。"""
        # schema_version 校验
        version = snapshot.get("schema_version")
        if version != "1.0":
            raise ValueError(
                f"不支持的快照版本: {version!r}，当前仅支持 '1.0'"
            )

        for store_name, store_snapshot in snapshot.get("stores", {}).items():
            data = store_snapshot.get("data", {})
            items = data.get("items", [])

            # ID 唯一性校验
            seen_ids: set[str] = set()
            for item_dict in items:
                item_id = item_dict.get("id", "")
                if item_id in seen_ids:
                    raise ValueError(
                        f"store '{store_name}' 中存在重复 ID: {item_id}"
                    )
                seen_ids.add(item_id)

            # GraphMemoryStore 边端点校验
            if store_snapshot.get("type") == "GraphMemoryStore":
                edges = data.get("edges", [])
                for edge in edges:
                    src = edge.get("source", "")
                    tgt = edge.get("target", "")
                    if src not in seen_ids:
                        raise ValueError(
                            f"store '{store_name}' 的边引用了不存在的源节点: {src}"
                        )
                    if tgt not in seen_ids:
                        raise ValueError(
                            f"store '{store_name}' 的边引用了不存在的目标节点: {tgt}"
                        )

