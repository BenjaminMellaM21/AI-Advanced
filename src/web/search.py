"""Búsqueda en internet vía Tavily: API gratuita (1000 créditos/mes, sin
tarjeta), pensada para agentes de IA. Devuelve contenido ya extraído,
así que no necesitamos un scraper aparte."""
from tavily import TavilyClient

from src.config import settings

_client = TavilyClient(api_key=settings.tavily_api_key)


def web_search(query: str) -> list[dict]:
    """Devuelve una lista de {title, href, body} (body = contenido ya extraído)."""
    try:
        response = _client.search(
            query=query,
            max_results=settings.web_search_max_results,
        )
        return [
            {
                "title": r.get("title", ""),
                "href": r.get("url", ""),
                "body": r.get("content", ""),
            }
            for r in response.get("results", [])
        ]
    except Exception as e:
        print(f"[web_search] Tavily no disponible ahora mismo ({e}). Sigo sin resultados web.")
        return []
