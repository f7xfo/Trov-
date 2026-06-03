# Local setup

This walks a new contributor from zero to "the Telegram bot is talking to me on my laptop" in about 15 minutes.

## 1. Prerequisites

- Docker + Docker Compose
- Python 3.12 or newer
- A Telegram account
- An LLM API key. We default to **DeepSeek** (~$0.10 / million tokens, cheapest production-grade for bilingual NLP). Get one at https://platform.deepseek.com — $5 in credits will last weeks of dev.

Alternatives: any OpenAI-compatible endpoint (OpenAI, Together, Groq) or a local [Ollama](https://ollama.com/) running `qwen2.5:7b` or similar.

## 2. Get a Telegram bot token

1. Open Telegram, search for `@BotFather`
2. Send `/newbot`
3. Follow prompts (pick a name and a unique username ending in `_bot`)
4. BotFather replies with a token like `123456:ABC-DEF...`
5. Save it — it goes in `.env`

## 3. Clone and configure

```bash
git clone https://github.com/YOUR-ORG/srokwork-core.git
cd srokwork-core
cp .env.example .env
```

Edit `.env`:

```
TELEGRAM_BOT_TOKEN=<the token from BotFather>
LLM_API_KEY=<your DeepSeek key>
```

Leave the rest as defaults for local dev.

## 4. Start the stack

```bash
docker compose up -d postgres redis
```

Wait ~5 seconds for them to be healthy.

## 5. Install Python deps and run migrations

```bash
# uv is fastest (https://docs.astral.sh/uv/)
pip install uv
uv pip install --system -e ".[dev]"

alembic upgrade head
```

You should see two tables created and the `vector` extension enabled.

## 6. Run the API + bot

```bash
python -m srokwork
```

In `APP_ENV=development`, the bot starts in **polling mode** — no public URL needed. You'll see:

```
telegram_polling_started
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## 7. Test it

Open Telegram, find your bot by username, and send `/start`. You should see the bilingual onboarding prompt. Pick a role and try messages like:

- `I need a cook in Siem Reap under $400`
- `ខ្ញុំធ្លាប់ធ្វើជាបាគងនៅភ្នំពេញ ៥ ឆ្នាំ ស្វែងរកការងារនៅសៀមរាប`

The agent will parse / extract and reply.

## 8. Run the tests

```bash
pytest
ruff check .
mypy src/
```

## Troubleshooting

**`vector` extension missing** — make sure you're using the `pgvector/pgvector:pg16` image, not stock Postgres. The provided `docker-compose.yml` uses the right one.

**Bot doesn't respond** — check that `TELEGRAM_BOT_TOKEN` is set and `APP_ENV=development` (for polling). For production webhooks, see `docs/DEPLOY.md`.

**LLM errors** — confirm `LLM_BASE_URL` matches the provider. For Ollama: `http://host.docker.internal:11434/v1` and `LLM_API_KEY=ollama`.

**Khmer characters look broken in terminal** — your terminal font doesn't have Khmer glyphs. Try a different font like Noto Sans Khmer. The bot output to Telegram is unaffected.

## Next steps

- Read [`docs/ARCHITECTURE.md`](ARCHITECTURE.md)
- Read [`CONTRIBUTING.md`](../CONTRIBUTING.md)
- Pick a [`good first issue`](https://github.com/YOUR-ORG/srokwork-core/labels/good%20first%20issue)
