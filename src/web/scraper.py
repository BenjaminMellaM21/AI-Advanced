"""Extrae texto limpio de una URL (para alimentar la memoria del asistente)."""
import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0 (JARVIS-Auto learning bot)"}


def fetch_clean_text(url: str, max_chars: int = 3000) -> str:
    """Descarga una página y devuelve su texto principal, sin scripts/estilos."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=8)
        resp.raise_for_status()
    except requests.RequestException as e:
        return f"[No se pudo acceder a {url}: {e}]"

    soup = BeautifulSoup(resp.text, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
        tag.decompose()

    text = " ".join(soup.get_text(separator=" ").split())
    return text[:max_chars]
