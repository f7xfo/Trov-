# Trov — ទ្រូវ

**Open-source, free recruitment platform for Cambodia's informal workforce.**
*ស្រុកការងារ — Work for everyone.*

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/)
[![Status: Phase 0](https://img.shields.io/badge/status-phase%200-orange.svg)]()

Trov structures the blue-collar / SME hiring already happening in chaos across Cambodia's Telegram channels — adding intelligent natural-language matching and a verifiable trust layer (reciprocal rating system). Built for the workers who don't have LinkedIn.

> **Free to find work. Always.** No data selling. No ads. Open-source under MIT.

---

## What it does

- 🇰🇭 **Natural language search** — describe who you need in Khmer or English: *"ខ្ញុំត្រូវការអ្នកធ្វើម្ហូបនៅសៀមរាប"* or *"I need a cook in Siem Reap under $400"*
- 📋 **Smart CV intake** — candidates describe their experience; AI extracts a structured profile
- ⭐ **Reciprocal rating system** — structured, verified, immutable. Trust as infrastructure.
- 🔔 **Saved alerts** — employers get notified when a matching candidate appears
- 📱 **Telegram bot** (Phase 0) — where Cambodian workers already are

---

## Quick Start

```bash
git clone git@github.com:f7xfo/Trov-.git
cd Trov-
cp .env.example .env
# Edit .env: set TELEGRAM_BOT_TOKEN, LLM_API_KEY
docker compose up -d postgres redis
pip install -e ".[dev]"
alembic upgrade head
python -m trov
```

The Telegram bot is now live in polling mode. Send `/start` to test.

---

## Architecture

```
Telegram Bot (Grammy.js Phase 0) → FastAPI Backend (Python) → DeepSeek + PostgreSQL/pgvector + Redis
                                                              n8n (orchestration)
```

| Layer | Stack |
|---|---|
| Bot | Grammy.js (Node.js/TypeScript) or python-telegram-bot |
| API | FastAPI (Python 3.12) |
| AI | DeepSeek V3 + text-embedding-3-small |
| DB | PostgreSQL 16 + pgvector |
| Cache | Redis |
| Orchestration | n8n (self-hosted) |

---

## Project Structure

```
├── src/trov/
│   ├── agents/       # Pydantic AI agents (CV extraction, query parsing)
│   ├── api/          # FastAPI routes
│   ├── services/     # Business logic (matching, ratings, alerts, search)
│   ├── db/           # SQLAlchemy models + Alembic migrations
│   ├── i18n/         # Khmer + English message catalogs
│   ├── bots/         # Telegram bot handlers
│   └── core/         # Config, logging
├── tests/
├── docs/             # Spec, pitch deck, project dossier
├── docker-compose.yml
└── Dockerfile
```

---

## The Rating System (Core Differentiator)

Trov's rating system is **structured, verified, bidirectional, and immutable**:

- ⭐ Star score + predefined categories (e.g., "paid on time: yes/no")
- 🔗 Only participants in a verified on-platform conversation can rate
- 🔄 Candidates rate employers on payment/conditions; employers rate candidates on reliability
- 🔒 Ratings cannot be deleted — enforced at the database permission level

[Full design →](docs/DEVELOPER_SPEC.md#4-rating-system-design)

---

## Kill-Criteria (RULE_27)

Trov is declared dead at Day 60 if **any** of:
- Fewer than 50 candidates created a profile
- Fewer than 5 employers ran repeat searches
- Khmer query parsing fails on >40% of real queries

Auto-checked daily via n8n and reported cold.

---

## Roadmap

| Phase | Timeline | Focus |
|---|---|---|
| **Phase 0** | 60 days | Telegram bot + matching + rating system |
| **Phase 1** | Months 3-12 | Messenger bot, cross-channel relay, Khmer NLP fine-tuning |
| **Phase 2** | Months 13-18 | PWA, voice CV, local LLM, multi-country |

---

## Positioning

Trov targets the **95% of Cambodian workers** not served by corporate job boards — blue-collar, micro-SME, informal hiring. It is a **public good**, intended for non-profit housing with eventual MoLVT/NEA partnership. It does not compete with WorkingNA.

---

## Contributing

MIT licensed. We especially need help with:
- 🇰🇭 Khmer NLP — query datasets, parsing accuracy
- 🎨 UI/UX — mobile-first for low-bandwidth
- 🌏 Localization — Khmer review
- 🧪 Testing — bot flows, edge cases

---

*Built in Phnom Penh. Open to the world.*
