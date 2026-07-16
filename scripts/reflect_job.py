"""Job periódico de 'reflexión': el sistema revisa su memoria, detecta hechos
duplicados o muy similares, y los consolida en uno solo más completo.

Ejecutar manualmente:  python scripts/reflect_job.py
Programar con cron:    0 3 * * * cd /ruta/al/proyecto && venv/bin/python scripts/reflect_job.py
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.core.llm_client import ask_claude
from src.memory.vector_store import vector_store

DEDUP_DISTANCE_THRESHOLD = 0.15  # más bajo = más estricto

CONSOLIDATE_PROMPT = """Estos son varios hechos casi duplicados guardados por un asistente
con auto-aprendizaje. Combínalos en un solo hecho, más completo y sin redundancia,
en una sola oración. Responde solo con el hecho final."""


def reflect():
    all_docs = vector_store.knowledge.get(include=["documents", "metadatas", "embeddings"])
    ids = all_docs["ids"]
    docs = all_docs["documents"]

    if len(ids) < 2:
        print("Memoria demasiado pequeña para reflexionar todavía.")
        return

    print(f"Revisando {len(ids)} hechos guardados...")
    seen = set()
    merged_count = 0

    for i, doc in enumerate(docs):
        if ids[i] in seen:
            continue
        similar = vector_store.query_knowledge(doc, n_results=3)
        near_duplicates = [
            s for s in similar
            if s["distance"] < DEDUP_DISTANCE_THRESHOLD and s["text"] != doc
        ]
        if near_duplicates:
            combined_text = doc + "\n" + "\n".join(d["text"] for d in near_duplicates)
            consolidated = ask_claude(CONSOLIDATE_PROMPT, combined_text, max_tokens=150)
            vector_store.add_knowledge(consolidated, source="reflexion", topic="consolidado")
            merged_count += 1
            seen.add(ids[i])

    print(f"Reflexión completa. {merged_count} grupos de hechos consolidados.")


if __name__ == "__main__":
    reflect()
