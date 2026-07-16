"""Búsqueda en internet sin necesidad de API key (DuckDuckGo)."""
from duckduckgo_search import DDGS

from src.config import settings


def web_search(query: str) -> list[dict]:
    """Devuelve una lista de {title, href, body} con los resultados más relevantes."""
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=settings.web_search_max_results))
    return results
