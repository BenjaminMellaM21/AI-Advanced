"""Wrapper delgado sobre la API de Anthropic."""
from anthropic import Anthropic

from src.config import settings

_client = Anthropic(api_key=settings.anthropic_api_key)


def ask_claude(system_prompt: str, user_prompt: str, max_tokens: int = 1000) -> str:
    response = _client.messages.create(
        model=settings.claude_model,
        max_tokens=max_tokens,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )
    parts = [block.text for block in response.content if block.type == "text"]
    return "\n".join(parts)
