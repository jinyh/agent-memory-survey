"""Agent 集成示例。

展示如何在简单的对话 Agent 中使用记忆系统，
包括记忆的存储、检索和巩固。
"""

from __future__ import annotations

import logging

from .base import MemoryType
from .episodic import EpisodicMemory
from .graph_store import GraphMemoryStore
from .manager import MemoryManager

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


class SimpleMemoryAgent:
    """带记忆系统的简单 Agent 演示。

    展示 Agent 如何:
    1. 将交互存储为情景记忆
    2. 将知识存储为图结构语义记忆
    3. 检索相关记忆辅助决策
    4. 定期巩固情景→语义记忆
    """

    def __init__(self):
        self.manager = MemoryManager()

        # 注册情景记忆（对话历史、事件）
        self.episodic = EpisodicMemory(max_capacity=1000, decay_rate=0.02)
        self.manager.register_store("episodic", self.episodic)

        # 注册图结构语义记忆（知识、事实）
        self.semantic = GraphMemoryStore(max_capacity=5000, decay_rate=0.005)
        self.manager.register_store("semantic", self.semantic, default=True)

        self._interaction_count = 0

    def observe(self, observation: str, importance: float = 0.5, tags: list[str] | None = None) -> str:
        """Agent 观察到新信息，存储为情景记忆。"""
        self._interaction_count += 1
        memory_id = self.episodic.add_episode(
            content=observation,
            importance=importance,
            tags=tags or [],
            metadata={"interaction": self._interaction_count},
        )
        logger.info(f"[观察] 存储情景记忆: {observation[:50]}...")

        # 每 10 次交互执行一次巩固
        if self._interaction_count % 10 == 0:
            self._auto_consolidate()

        return memory_id

    def learn(self, fact: str, tags: list[str] | None = None, importance: float = 0.7) -> str:
        """Agent 学习新知识，存储为语义记忆。"""
        memory_id = self.manager.remember(
            content=fact,
            memory_type=MemoryType.SEMANTIC,
            store_name="semantic",
            importance=importance,
            tags=tags or [],
        )
        logger.info(f"[学习] 存储语义记忆: {fact[:50]}...")
        return memory_id

    def think(self, query: str, top_k: int = 5) -> list[str]:
        """Agent 检索相关记忆进行思考。"""
        results = self.manager.recall(query, top_k=top_k)
        memories = []
        for item, score, store_name in results:
            memories.append(f"[{store_name}|{score:.2f}] {item.content}")
        logger.info(f"[思考] 查询 '{query[:30]}' → 找到 {len(memories)} 条相关记忆")
        return memories

    def _auto_consolidate(self) -> None:
        """自动巩固：将情景中的重复模式提取为语义记忆。"""
        new_ids = self.manager.consolidate_episodic_to_semantic(
            "episodic", "semantic", min_frequency=2
        )
        if new_ids:
            logger.info(f"[巩固] 从情景记忆中提取了 {len(new_ids)} 条语义记忆")

        # 清理过期记忆
        cleanup = self.manager.consolidate_all()
        total_cleaned = sum(cleanup.values())
        if total_cleaned:
            logger.info(f"[清理] 清理了 {total_cleaned} 条过期记忆")

    def status(self) -> dict:
        """返回 Agent 记忆状态。"""
        stats = self.manager.stats()
        stats["total_interactions"] = self._interaction_count
        stats["total_memories"] = self.manager.total_memories()
        return stats


def demo():
    """运行一个简单的演示。"""
    agent = SimpleMemoryAgent()

    print("=" * 60)
    print("Agent Memory 概念原型演示")
    print("=" * 60)

    # 1. Agent 学习一些知识
    print("\n--- 阶段 1: 学习知识 ---")
    agent.learn("Python 是一种解释型编程语言", tags=["python", "编程"])
    agent.learn("Transformer 是深度学习中的核心架构", tags=["transformer", "深度学习"])
    agent.learn("RAG 是检索增强生成的缩写", tags=["RAG", "记忆"])
    agent.learn("MSA 使用稀疏注意力实现 100M token 记忆", tags=["MSA", "记忆", "注意力"])

    # 2. Agent 经历一些事件
    print("\n--- 阶段 2: 记录事件 ---")
    for i in range(12):
        event = f"用户询问了关于 Agent 记忆的问题（第{i+1}次）"
        tags = ["用户交互", "记忆"]
        if i % 3 == 0:
            tags.append("重要")
        agent.observe(event, importance=0.3 + (i % 3) * 0.2, tags=tags)

    # 3. Agent 检索记忆
    print("\n--- 阶段 3: 检索记忆 ---")
    results = agent.think("记忆系统的实现方式")
    for r in results:
        print(f"  {r}")

    print("\n--- 阶段 4: 检索 Transformer 相关 ---")
    results = agent.think("Transformer 架构")
    for r in results:
        print(f"  {r}")

    # 4. 查看状态
    print("\n--- Agent 记忆状态 ---")
    status = agent.status()
    for key, value in status.items():
        print(f"  {key}: {value}")

    print("\n" + "=" * 60)
    print("演示完成")


if __name__ == "__main__":
    demo()
