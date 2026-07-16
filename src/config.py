"""Configuración centralizada, cargada desde variables de entorno."""
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    llm_api_key: str = os.getenv("LLM_API_KEY", "ollama")  # Ollama ignora este valor
    llm_model: str = os.getenv("LLM_MODEL", "llama3.1")
    llm_base_url: str = os.getenv("LLM_BASE_URL", "http://localhost:11434/v1")
    tavily_api_key: str = os.getenv("TAVILY_API_KEY", "")
    chroma_persist_dir: str = os.getenv("CHROMA_PERSIST_DIR", "./data/chroma")
    web_search_max_results: int = int(os.getenv("WEB_SEARCH_MAX_RESULTS", "5"))
    memory_confidence_threshold: float = float(
        os.getenv("MEMORY_CONFIDENCE_THRESHOLD", "0.35")
    )


settings = Settings()
