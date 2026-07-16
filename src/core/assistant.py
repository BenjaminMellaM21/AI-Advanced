"""El 'cerebro' del asistente: decide qué sabe, qué necesita investigar, y responde."""
from src.config import settings
from src.core.llm_client import ask_claude
from src.memory.vector_store import vector_store
from src.memory.learning import research_topic, extract_and_store_facts

SYSTEM_PROMPT = """Eres JARVIS-Auto, un asistente conversacional con memoria propia que
va aprendiendo con el tiempo. Responde de forma clara y natural en español.
Si te doy contexto de 'memoria' o 'resultados de investigación', úsalo para responder
con precisión, y menciona brevemente de dónde sacaste el dato si es relevante."""


def _build_context_block(memories: list[dict]) -> str:
    if not memories:
        return "(sin recuerdos relevantes todavía)"
    lines = [f"- {m['text']} (fuente: {m['metadata'].get('source', 'desconocida')})" for m in memories]
    return "\n".join(lines)


def chat(user_message: str) -> dict:
    """Punto de entrada principal: recibe un mensaje y devuelve la respuesta + metadata."""
    memories = vector_store.query_knowledge(user_message, n_results=5)

    best_distance = min((m["distance"] for m in memories), default=1.0)
    needs_research = best_distance > (1 - settings.memory_confidence_threshold)

    researched_facts: list[str] = []
    if needs_research:
        researched_facts = research_topic(user_message)
        # Volvemos a consultar la memoria ya enriquecida con lo recién aprendido
        memories = vector_store.query_knowledge(user_message, n_results=5)

    context_block = _build_context_block(memories)
    prompt = f"""Memoria relevante:
{context_block}

Pregunta del usuario: {user_message}"""

    answer = ask_claude(SYSTEM_PROMPT, prompt)

    # Auto-aprendizaje: la propia conversación también deja hechos nuevos
    extract_and_store_facts(
        f"Pregunta: {user_message}\nRespuesta: {answer}",
        source="conversacion",
    )
    vector_store.log_conversation(user_message, answer)

    return {
        "answer": answer,
        "researched": needs_research,
        "new_facts_learned": researched_facts,
        "memory_size": vector_store.count_knowledge(),
    }
