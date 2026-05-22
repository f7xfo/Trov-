"""Entrypoint: `python -m trov` runs the API + Telegram bot together for local dev."""

import asyncio

import uvicorn

from trov.core.config import settings
from trov.core.logging import setup_logging


def main() -> None:
    setup_logging()
    config = uvicorn.Config(
        "trov.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.app_env == "development",
        log_level=settings.log_level.lower(),
    )
    server = uvicorn.Server(config)
    asyncio.run(server.serve())


if __name__ == "__main__":
    main()
