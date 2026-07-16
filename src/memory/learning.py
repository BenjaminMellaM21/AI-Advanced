"""Lógica de 'aprendizaje': convierte texto crudo en hechos atómicos y los guarda."""
from src.core.llm_client import ask_claude
from src.memory.vector_store import vector_store
from src.web.search import web_search
from src.web.scraper import fetch_clean_text

EXTRACT_FACTS_PROMPT = """Eres un extractor de conocimiento. A partir del siguiente texto,
devuelve entre 1 y 5 hechos concretos, cortos y autocontenidos (una oración cada uno),
uno por línea, sin numeración ni texto extra. Si no hay hechos útiles, responde "NADA"."""


def extract_and_store_facts(text: str, source: str, topic: str = "") -> list[str]:
    """Pide al LLM que resuma el texto en hechos atómicos y los guarda en la memoria."""
    raw = ask_claude(EXTRACT_FACTS_PROMPT, text, max_tokens=400)
    if raw.strip().upper() == "NADA":
        return []

    facts = [line.strip("- ").strip() for line in raw.splitlines() if line.strip()]
    for fact in facts:
        vector_store.add_knowledge(fact, source=source, topic=topic)
    return facts


def research_topic(topic: str) -> list[str]:
    """Busca un tema en internet, scrapea las páginas top y aprende de ellas."""
    results = web_search(topic)
    all_facts = []
    for r in results:
        url = r.get("href", "")
        if not url:
            continue
        content = fetch_clean_text(url)
        if content.startswith("[No se pudo"):
            continue
        facts = extract_and_store_facts(content, source=url, topic=topic)
        all_facts.extend(facts)
    return all_facts
