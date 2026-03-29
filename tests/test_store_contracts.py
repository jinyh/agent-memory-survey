from __future__ import annotations

from src.memory.base import MemoryItem, MemoryStore, MemoryType
from src.memory.episodic import EpisodicMemory
from src.memory.graph_store import GraphMemoryStore
from src.memory.vector_store import VectorMemoryStore


STORE_FACTORIES = [
    lambda: EpisodicMemory(),
    lambda: GraphMemoryStore(),
    lambda: VectorMemoryStore(),
]


def _exercise_store(store: MemoryStore, monkeypatch) -> None:
    if isinstance(store, VectorMemoryStore):
        monkeypatch.setattr(
            VectorMemoryStore,
            "_encode",
            lambda self, text: [float(len(text))],
        )

    item = MemoryItem(content="contract item", memory_type=MemoryType.SEMANTIC)
    memory_id = store.add(item)

    assert store.size() == 1
    assert store.list_all()
    assert store.query("contract", top_k=1)
    assert store.update(memory_id, content="updated contract item")
    assert store.delete(memory_id)
    assert store.size() == 0
    assert store.consolidate() >= 0
    assert store.get_init_kwargs()
    snapshot = store.to_snapshot_dict()
    restored = store.__class__.from_snapshot_dict(snapshot)
    assert restored.size() == store.size()


def test_memory_store_contracts(monkeypatch):
    for factory in STORE_FACTORIES:
        _exercise_store(factory(), monkeypatch)
