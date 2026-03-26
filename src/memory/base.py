"""统一记忆接口定义。

定义 MemoryItem 数据结构和 MemoryStore 抽象基类，
所有记忆后端（向量、图、情景等）都实现此接口。
"""

from __future__ import annotations

import time
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class MemoryType(Enum):
    """记忆类型，对应认知科学分类。"""

    EPISODIC = "episodic"  # 情景记忆：具体事件
    SEMANTIC = "semantic"  # 语义记忆：抽象知识
    PROCEDURAL = "procedural"  # 程序性记忆：操作步骤
    WORKING = "working"  # 工作记忆：即时上下文


@dataclass
class FusionConfig:
    """跨 store 检索融合配置。

    mode: 融合策略，当前仅支持 "rank"（rank 归一化融合）
    overfetch_factor: 每个 store 预取倍数，实际取 top_k * overfetch_factor
    store_weights: 各 store 的权重，key 为 store 名称，缺省权重为 1.0
    """

    mode: str = "rank"
    overfetch_factor: int = 3
    store_weights: dict[str, float] = field(default_factory=dict)

    def get_weight(self, store_name: str) -> float:
        """获取指定 store 的权重，缺省返回 1.0。"""
        return self.store_weights.get(store_name, 1.0)


@dataclass
class MemoryItem:
    """单条记忆条目。"""

    content: str
    memory_type: MemoryType = MemoryType.SEMANTIC
    metadata: dict[str, Any] = field(default_factory=dict)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: float = field(default_factory=time.time)
    last_accessed: float = field(default_factory=time.time)
    access_count: int = 0
    importance: float = 0.5  # 0.0 ~ 1.0
    embedding: list[float] | None = None
    tags: list[str] = field(default_factory=list)
    links: list[str] = field(default_factory=list)  # 关联记忆 ID

    def touch(self) -> None:
        """标记为已访问，更新访问时间和计数。"""
        self.last_accessed = time.time()
        self.access_count += 1

    def decay_score(self, decay_rate: float = 0.01) -> float:
        """计算考虑时间衰减的相关性分数。

        使用幂律衰减（更符合人类记忆曲线）:
        score = importance * (1 + elapsed)^(-decay_rate)
        """
        elapsed = time.time() - self.last_accessed
        return self.importance * (1 + elapsed) ** (-decay_rate)


class MemoryStore(ABC):
    """记忆存储的抽象基类。

    所有记忆后端都必须实现这五个核心操作:
    add, query, update, delete, consolidate
    """

    @abstractmethod
    def add(self, item: MemoryItem) -> str:
        """添加一条记忆，返回记忆 ID。"""

    @abstractmethod
    def query(
        self,
        query: str,
        top_k: int = 5,
        memory_type: MemoryType | None = None,
        min_score: float = 0.0,
    ) -> list[tuple[MemoryItem, float]]:
        """检索记忆，返回 (记忆, 相关性分数) 列表。"""

    @abstractmethod
    def update(self, memory_id: str, **kwargs: Any) -> bool:
        """更新指定记忆的字段，返回是否成功。"""

    @abstractmethod
    def delete(self, memory_id: str) -> bool:
        """删除指定记忆，返回是否成功。"""

    @abstractmethod
    def consolidate(self) -> int:
        """执行记忆巩固（压缩、合并、清理过期记忆等）。

        返回被巩固/清理的记忆数量。
        """

    @abstractmethod
    def list_all(
        self, memory_type: MemoryType | None = None
    ) -> list[MemoryItem]:
        """列出所有记忆（可按类型过滤）。"""

    @abstractmethod
    def size(self) -> int:
        """返回当前记忆总数。"""

    @abstractmethod
    def get_init_kwargs(self) -> dict:
        """返回重建本 store 所需的构造参数 dict。"""

    @abstractmethod
    def to_snapshot_dict(self) -> dict:
        """导出全部状态（含 init_kwargs）为可 JSON 序列化的 dict。"""

    @classmethod
    @abstractmethod
    def from_snapshot_dict(cls, data: dict, **kwargs: Any) -> "MemoryStore":
        """从 dict 恢复 store 状态，kwargs 为构造参数（缺省回退到 data['init_kwargs']）。"""
