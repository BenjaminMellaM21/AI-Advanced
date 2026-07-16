"""Tests básicos de la memoria vectorial. Corre: pytest tests/"""
import shutil
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import pytest

TEST_CHROMA_DIR = "./data/test_chroma"


@pytest.fixture
def store(monkeypatch):
    monkeypatch.setenv("CHROMA_PERSIST_DIR", TEST_CHROMA_DIR)
    from src.memory.vector_store import VectorStore
    vs = VectorStore()
    yield vs
    shutil.rmtree(TEST_CHROMA_DIR, ignore_errors=True)


def test_add_and_query_knowledge(store):
    store.add_knowledge("Dead by Daylight es un juego de terror asimétrico 4v1.", source="test")
    results = store.query_knowledge("¿Qué es Dead by Daylight?", n_results=1)
    assert len(results) == 1
    assert "asimétrico" in results[0]["text"]


def test_count_knowledge_increases(store):
    initial = store.count_knowledge()
    store.add_knowledge("Minecraft tiene modo supervivencia y creativo.", source="test")
    assert store.count_knowledge() == initial + 1
