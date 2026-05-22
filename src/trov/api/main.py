"""FastAPI application.

Combines:
- HTTP API (health check, future PWA endpoints)
- Telegram webhook receiver
- Bot lifecycle: in production, registers a webhook; in dev, runs polling.

Why one process: simplicity for v0.1. Splitting into separate services
(api + bot + worker) is a deploy-time choice via docker-compose, not a
code-time choice.
"""

from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI, HTTPException, Request, status
from telegram import Update

from trov.bots.telegram.bot import build_application
from trov.api.routes import router as api_router
from trov.core.config import settings
from trov.core.logging import log, setup_logging

setup_logging()

_tg_app = None


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    """Initialize the Telegram bot on startup, stop it on shutdown."""
    global _tg_app

    if not settings.telegram_bot_token:
        log.warning("telegram_disabled", reason="TELEGRAM_BOT_TOKEN not set")
        yield
        return

    _tg_app = build_application()
    await _tg_app.initialize()
    await _tg_app.start()

    if settings.is_dev:
        # Polling for local dev — no public URL needed
        log.info("telegram_polling_started")
        await _tg_app.updater.start_polling()
    elif settings.telegram_webhook_url:
        webhook_url = f"{settings.telegram_webhook_url.rstrip('/')}/telegram/webhook"
        await _tg_app.bot.set_webhook(
            url=webhook_url,
            secret_token=settings.telegram_webhook_secret,
            drop_pending_updates=True,
        )
        log.info("telegram_webhook_set", url=webhook_url)
    else:
        log.warning("telegram_webhook_skipped", reason="TELEGRAM_WEBHOOK_URL not set")

    yield

    if _tg_app:
        if settings.is_dev and _tg_app.updater:
            await _tg_app.updater.stop()
        await _tg_app.stop()
        await _tg_app.shutdown()


app = FastAPI(
    title="Trov",
    description="Open-source, free recruitment platform for Cambodia's informal workforce",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(api_router)


@app.get("/")
async def root() -> dict[str, str]:
    return {"service": "trov", "version": "0.1.0", "status": "ok"}


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "trov"}


@app.post("/telegram/webhook")
async def telegram_webhook(request: Request) -> dict[str, str]:
    """Production Telegram webhook receiver. Verifies the secret header."""
    if not _tg_app:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "Bot not initialized")

    secret = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
    if secret != settings.telegram_webhook_secret:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Invalid secret")

    data = await request.json()
    update = Update.de_json(data, _tg_app.bot)
    await _tg_app.process_update(update)
    return {"ok": "true"}
