# Architecture

## High-level

```
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ Telegram bot │  │ Messenger    │  │ PWA          │
│ (this repo)  │  │ (this repo)  │  │ (srokwork-web)│
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │                 │                 │
       └─────────────────┼─────────────────┘
                         │ HTTP / webhook
                  ┌──────▼──────┐
                  │   FastAPI   │
                  │  (this repo)│
                  └──────┬──────┘
              ┌──────────┼──────────┐
              │          │          │
      ┌───────▼──┐ ┌─────▼─────┐ ┌──▼────┐
      │  Agents  │ │  Services │ │  arq  │
      │(PydanticAI)│ │           │ │worker│
      └───────┬──┘ └─────┬─────┘ └──┬────┘
              │          │          │
              └──────┬───┴──────────┘
                     │
              ┌──────▼──────────────┐
              │ PostgreSQL+pgvector │
              │ Redis               │
              └─────────────────────┘
                     │
              ┌──────▼──────┐
              │   LLM API   │
              │ (DeepSeek)  │
              └─────────────┘
```

## Why these choices

### Python over Node

The product is an agent. Khmer NLP libraries, embedding models, and the
Pydantic AI / LangChain / LlamaIndex ecosystem are Python-first. Cambodian
student devs (RUPP, CADT) learn Python. Node would be a second-class citizen
for the AI work and a tax for every future AI feature.

### Pydantic AI over LangChain

LangChain is a kitchen sink. Pydantic AI is typed, small, model-agnostic, and
uses the same Pydantic primitives FastAPI uses. New contributors read the code
once and understand it. No magic.

### PostgreSQL + pgvector, no separate vector DB

One database, one connection pool, one backup. pgvector handles tens of
thousands of embeddings on commodity hardware — far beyond our v1.0 scale.
Pinecone, Weaviate, and Qdrant are unnecessary cost and ops complexity for
this size.

### Single Postgres for everything (no microservices)

v0.1–v1.0 fits in one process and one DB. We split only when something
breaks. Premature service splitting kills small projects.

### Telegram first, Messenger and PWA later

Telegram is dominant in Cambodia, has the lowest dev friction (single token,
free webhook, no Business Verification), and gives us a working product in
weeks. Messenger requires Meta business verification — a real blocker for an
unfunded project. PWA waits until the API contract is stable.

### MIT license

A pure community-good positioning. Anyone can fork it for another country.
If/when a hosted Pro version exists, it lives in a separate proprietary repo
with the value-add features (enterprise SSO, multi-tenant admin, audit logs).

## Module boundaries

| Module | Responsibility |
|---|---|
| `srokwork.api` | HTTP routes, webhooks, request validation |
| `srokwork.agents` | All LLM-facing code. Each agent is one file. Pure functions of `(input) -> typed_output` |
| `srokwork.bots.telegram` | Telegram-specific handlers, keyboards, message formatting |
| `srokwork.bots.messenger` | (v0.2) Messenger handlers |
| `srokwork.services` | Business logic that doesn't belong to a single channel: user lookup, matching, ratings |
| `srokwork.db` | SQLAlchemy models + Alembic migrations. The schema is the contract. |
| `srokwork.i18n` | Khmer + English message catalogs |
| `srokwork.core` | Config, logging, cross-cutting concerns |

A channel handler (Telegram, Messenger, future Web) should:
- Parse channel-specific input
- Call agents and services
- Format channel-specific output

It should NOT contain business logic. That goes in `services/`.

## Data flow: candidate CV deposit

1. Candidate sends text/photo/PDF to Telegram bot
2. `bots/telegram/bot.py::on_text` (or future `on_document`) extracts raw text
3. `agents/cv_extraction.py::extract_cv(raw)` returns `ExtractedCV` (typed)
4. `services/profiles.py::save_candidate_profile()` writes to DB + computes embedding
5. Bot replies with extracted summary in user's language; asks to confirm

## Data flow: employer search

1. Employer sends NL query to bot
2. `agents/query_parsing.py::parse_query(raw)` returns `ParsedQuery` (typed)
3. `services/matching.py::find_candidates(parsed)` does hybrid search:
   - Filter by structured criteria (location, salary, experience)
   - Rank by cosine similarity to the query embedding
   - Boost by `rating_avg`
4. Bot formats top N results with inline "contact" buttons

## Data flow: saved alert

1. After a search, employer taps "Save as alert"
2. `services/alerts.py::save_alert(search_id)` flips `is_alert = True`
3. arq worker runs every 15 min, sweeps active alerts, runs the same hybrid search
4. For each new match since `last_run_at`, push a Telegram/Messenger message

## Adding a new channel

To add WhatsApp, Viber, or anything else:

1. Create `bots/<channel>/bot.py` that handles channel-specific I/O
2. Reuse `agents/` and `services/` unchanged
3. Add a webhook route in `api/main.py`
4. Add a `<channel>_id` column to `users` and update `services/users.py`

The agents and DB don't know which channel a user came from. That's the point.
