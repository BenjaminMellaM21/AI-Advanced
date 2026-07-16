"""El 'cerebro' del asistente: decide qué sabe, qué necesita investigar, y responde."""
from src.config import settings
from src.core.llm_client import ask_claude
from src.memory.vector_store import vector_store
from src.memory.learning import research_topic, extract_and_store_facts

SYSTEM_PROMPT = """Eres JARVIS-Auto, un asistente conversacional con memoria propia que
va aprendiendo con el tiempo. Responde de forma clara y natural en español.
Si te doy contexto de 'memoria' o 'resultados de investigación', úsalo para responder
con precisión, y menciona brevemente de dónde sacaste el dato si es relevante."""

# Saludos y mensajes cortos que nunca deberían disparar una búsqueda en internet
_GREETING_WORDS = {
    "hola", "buenas", "buenos", "hey", "hi", "hello", "que", "qué", "tal",
    "gracias", "adios", "adiós", "chao", "ok", "vale",
}


def _looks_like_greeting_or_smalltalk(message: str) -> bool:
    words = [w.strip("¿?¡!.,").lower() for w in message.split()]
    if len(words) <= 4 and any(w in _GREETING_WORDS for w in words):
        return True
    return False


def _build_context_block(memories: list[dict]) -> str:
    if not memories:
        return "(sin recuerdos relevantes todavía)"
    lines = [f"- {m['text']} (fuente: {m['metadata'].get('source', 'desconocida')})" for m in memories]
    return "\n".join(lines)


def chat(user_message: str) -> dict:
    """Punto de entrada principal: recibe un mensaje y devuelve la respuesta + metadata."""
    memories = vector_store.query_knowledge(user_message, n_results=5)

    best_distance = min((m["distance"] for m in memories), default=1.0)
    needs_research = (
        best_distance > (1 - settings.memory_confidence_threshold)
        and not _looks_like_greeting_or_smalltalk(user_message)
    )

    researched_facts: list[str] = []
    if needs_research:
        try:
            researched_facts = research_topic(user_message)
            # Volvemos a consultar la memoria ya enriquecida con lo recién aprendido
            memories = vector_store.query_knowledge(user_message, n_results=5)
        except Exception as e:
            # Si la investigación falla (ej. rate limit de búsqueda), seguimos
            # respondiendo con lo que ya sabemos en vez de tumbar la app.
            print(f"[assistant] La investigación falló, respondo sin ella: {e}")

    context_block = _build_context_block(memories)
    prompt = f"""Memoria relevante:
{context_block}

Pregunta del usuario: {user_message}"""

    answer = ask_claude(SYSTEM_PROMPT, prompt)

    # Auto-aprendizaje: la propia conversación también deja hechos nuevos.
    # Si esto falla (ej. el LLM tarda o da un formato raro), no debe romper
    # la respuesta que ya tenemos lista para el usuario.
    try:
        extract_and_store_facts(
            f"Pregunta: {user_message}\nRespuesta: {answer}",
            source="conversacion",
        )
        vector_store.log_conversation(user_message, answer)
    except Exception as e:
        print(f"[assistant] No se pudo guardar el aprendizaje de esta conversación: {e}")

    return {
        "answer": answer,
        "researched": needs_research,
        "new_facts_learned": researched_facts,
        "memory_size": vector_store.count_knowledge(),
    }
