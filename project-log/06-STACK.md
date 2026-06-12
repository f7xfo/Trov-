# 06 — STACK (Architecture & environment)

> The technical map. Update only when the stack actually changes (and log it in
> 05-DECISIONS). Lets Claude Code act without guessing your setup.
>
> ⚠️ This file is a LIGHT pointer layer. The authoritative technical docs live in `docs/`
> and are NOT duplicated here — follow the pointers below.

## 📎 Authoritative docs (read these for detail — do not re-copy them here)
- **Full architecture:** `docs/ARCHITECTURE.md`
- **Developer specification (47K, the source of truth for build):** `docs/DEVELOPER_SPEC.md`
  — §1 Architecture · §4 Rating System · §6 DB Schema · §7 API Endpoints · §8 n8n · §9 Kill-Criteria · §10 Deployment
- **Local setup:** `docs/SETUP.md`
- **Production deployment:** `docs/DEPLOY.md`
- **Audit baseline (7/10, 2026-05-23):** `docs/AUDIT_2026-05-23.md`

## Stack (summary — detail in docs/)
- **Bot:** Grammy.js (Node/TS) — note: current code uses python-telegram-bot in `src/trov/bots/telegram/`
- **Backend:** FastAPI (Python 3.12)
- **Database:** PostgreSQL 16 + pgvector (one DB, no separate vector store); Redis (cache/sessions)
- **AI / models:** DeepSeek V3 (chat) + text-embedding-3-small (OpenAI-compatible, swappable)
- **Orchestration:** n8n (self-hosted) — alert sweep, embedding sync, kill-criteria monitoring
- **Container:** Docker Compose (local + prod); CI in `.github/`

## Repo structure (top level)
```
/src/trov     agents · api · services · db · i18n · bots · core
/docs         ARCHITECTURE · DEVELOPER_SPEC · PITCH_DECK · PROJECT_DOSSIER · ROADMAP · SETUP · DEPLOY · AUDIT
/investor-kit Master_Plan · PWA_Prototype.html · exec_summary · oracle_simulation · README · CONTRIBUTING
/demo         HTML/CSS design (by Alex)
/tests
/project-log  ← these tracking files
docker-compose.yml · Dockerfile · alembic.ini · pyproject.toml
```

## How to run locally
```bash
# (from docs/SETUP.md / README — authoritative version there)
cp .env.example .env          # set TELEGRAM_BOT_TOKEN, LLM_API_KEY
docker compose up -d postgres redis
pip install -e ".[dev]"
alembic upgrade head
python -m trov                # Telegram bot in polling mode; send /start
```

## External services & accounts
- Telegram bot (Bot API, polling in Phase 0)
- DeepSeek API (NLP + embeddings)
- PostgreSQL 16 + pgvector · Redis · n8n (self-hosted)
- Target prod VPS: Phnom Penh / Bangkok (~$25-45/mo)

## Secrets policy
- Secrets live in `.env` (git-ignored — `.gitignore` already covers `.env`, `.env.local`).
  Only `.env.example` is committed. NEVER paste, print, or commit secrets.
- Reference by name only, e.g. `TELEGRAM_BOT_TOKEN`, `LLM_API_KEY`.
