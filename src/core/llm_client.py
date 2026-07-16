"""Wrapper delgado sobre el LLM. Funciona con CUALQUIER endpoint compatible con
la API de OpenAI: Ollama (local, 100% tuyo), Groq (gratis en la nube), o incluso
Anthropic/OpenAI directamente. Se controla todo desde .env, sin tocar código."""
from openai import OpenAI

from src.config import settings

_client = OpenAI(
    api_key=settings.llm_api_key,
    base_url=settings.llm_base_url,
)


def ask_claude(system_prompt: str, user_prompt: str, max_tokens: int = 1000) -> str:
    """El nombre se mantiene por compatibilidad con el resto del código."""
    response = _client.chat.completions.create(
        model=settings.llm_model,
        max_tokens=max_tokens,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    return response.choices[0].message.content
