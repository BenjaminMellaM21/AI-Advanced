"""Configuración centralizada, cargada desde variables de entorno."""
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
    claude_model: str = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-5-20250929")
    chroma_persist_dir: str = os.getenv("CHROMA_PERSIST_DIR", "./data/chroma")
    web_search_max_results: int = int(os.getenv("WEB_SEARCH_MAX_RESULTS", "5"))
    memory_confidence_threshold: float = float(
        os.getenv("MEMORY_CONFIDENCE_THRESHOLD", "0.35")
    )


settings = Settings()
