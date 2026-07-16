"""Wrapper de ChromaDB: guarda y recupera 'recuerdos' (conocimiento aprendido)."""
from datetime import datetime, timezone
import uuid

import chromadb

from src.config import settings


class VectorStore:
    """Memoria a largo plazo del asistente, respaldada por ChromaDB."""

    def __init__(self):
        self.client = chromadb.PersistentClient(path=settings.chroma_persist_dir)
        # Colección con la función de embeddings por defecto de Chroma
        # (all-MiniLM-L6-v2 vía onnxruntime, corre local, sin API key).
        self.knowledge = self.client.get_or_create_collection(
            name="knowledge",
            metadata={"description": "Hechos aprendidos de conversaciones y de internet"},
        )
        self.conversations = self.client.get_or_create_collection(
            name="conversations",
            metadata={"description": "Historial crudo de intercambios usuario/asistente"},
        )

    def add_knowledge(self, text: str, source: str, topic: str = "") -> str:
        """Guarda un hecho/nuevo conocimiento con metadata de trazabilidad."""
        doc_id = str(uuid.uuid4())
        self.knowledge.add(
            ids=[doc_id],
            documents=[text],
            metadatas=[{
                "source": source,
                "topic": topic,
                "learned_at": datetime.now(timezone.utc).isoformat(),
            }],
        )
        return doc_id

    def query_knowledge(self, query: str, n_results: int = 5):
        """Devuelve los recuerdos más relevantes junto con su distancia (menor = más similar)."""
        results = self.knowledge.query(query_texts=[query], n_results=n_results)
        items = []
        docs = results.get("documents", [[]])[0]
        metas = results.get("metadatas", [[]])[0]
        dists = results.get("distances", [[]])[0]
        for doc, meta, dist in zip(docs, metas, dists):
            items.append({"text": doc, "metadata": meta, "distance": dist})
        return items

    def log_conversation(self, user_message: str, assistant_response: str):
        doc_id = str(uuid.uuid4())
        self.conversations.add(
            ids=[doc_id],
            documents=[f"Usuario: {user_message}\nAsistente: {assistant_response}"],
            metadatas=[{"timestamp": datetime.now(timezone.utc).isoformat()}],
        )

    def count_knowledge(self) -> int:
        return self.knowledge.count()


vector_store = VectorStore()
