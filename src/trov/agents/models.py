"""LLM model factory — single point of truth for which model agents use.

Pydantic AI is model-agnostic; we use the OpenAI-compatible interface for
DeepSeek (default), OpenAI, and Ollama. Anthropic uses its own provider.
"""

import httpx

from pydantic_ai.models import Model
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

from trov.core.config import settings


def get_model() -> Model:
    """Return the configured LLM. Easy to swap per agent later if needed."""
    if settings.llm_provider == "anthropic":
        from pydantic_ai.models.anthropic import AnthropicModel
        return AnthropicModel(settings.llm_model, api_key=settings.llm_api_key)

    # deepseek, openai, ollama all use OpenAI-compatible API
    provider = OpenAIProvider(
        base_url=settings.llm_base_url,
        api_key=settings.llm_api_key or "ollama",  # ollama doesn't need a real key
    )
    return OpenAIModel(settings.llm_model, provider=provider)


async def get_embedding(text: str) -> list[float]:
    """Generate embedding vector for search indexing.
    
    Uses OpenAI-compatible embeddings API.
    Default model: text-embedding-3-small (1536 dimensions).
    """
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{settings.llm_base_url}/embeddings",
            headers={"Authorization": f"Bearer {settings.llm_api_key or 'ollama'}"},
            json={"model": settings.llm_embedding_model, "input": text},
            timeout=30.0,
        )
        resp.raise_for_status()
        data = resp.json()
        return data["data"][0]["embedding"]
