"""Application configuration loaded from environment variables."""

from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # App
    app_env: Literal["development", "production"] = "development"
    log_level: str = "INFO"
    secret_key: str = "changeme"

    # Database
    database_url: str = "postgresql+asyncpg://trov:trov@localhost:5432/trov"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # LLM
    llm_provider: Literal["deepseek", "openai", "anthropic", "ollama"] = "deepseek"
    llm_api_key: str = ""
    llm_base_url: str = "https://api.deepseek.com/v1"
    llm_model: str = "deepseek-chat"
    llm_embedding_model: str = "text-embedding-3-small"  # 1536 dimensions
    llm_embedding_model: str = "text-embedding-3-small"

    # Telegram
    telegram_bot_token: str = ""
    telegram_webhook_url: str = ""
    telegram_webhook_secret: str = "changeme"

    # Messenger (Phase 2)
    messenger_page_access_token: str = ""
    messenger_verify_token: str = ""

    @property
    def is_dev(self) -> bool:
        return self.app_env == "development"


settings = Settings()
