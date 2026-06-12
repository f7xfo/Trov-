# 01 — STATE (Where we are right now)

> Single source of truth. If it's not here, it's not "done".
> **Last updated: 2026-06-13**

## In one paragraph
Trov is a Phase 0 Telegram MVP for Cambodian informal-workforce recruitment. The Engineer
audit (2026-05-23, commit `344dde5`) scored it **7/10 — PASS, ~60-65% delivered**: the
backbone is solid (DB schema + migrations, CV-extraction + query-parsing agents, hybrid
search, the rating system "moat", bilingual KM/EN i18n, Docker Compose + CI). Three
deployment-blocking gaps remain (auth, ConversationHandler, message-relay service). Latest
work was documentation consolidation — DEVELOPER_SPEC / PITCH_DECK / PROJECT_DOSSIER rescued
from pre-rename `srokwork` copies and adopted (HEAD `ea46b23`). Not yet deployable.

## Done ✅
<!-- "Done" = actually run/tested. These come from the audit (code review PASS) — runtime
deployment NOT yet verified, so deploy-level items stay in "In progress". -->
- [2026-05-23] Database schema + 2 Alembic migrations (users, candidates, employers,
  searches, ratings, conversations) — _verified by: audit, schema integrity 10/10, REVOKE UPDATE/DELETE_
- [2026-05-23] Rating system (the moat): 4 `can_rate()` checks, decay-weighted, structured
  categories, DB-immutable — _verified by: audit, rating system 10/10_
- [2026-05-23] CV-extraction + query-parsing agents (Pydantic AI, DeepSeek) — _verified by: audit, agent completeness 10/10_
- [2026-05-23] Hybrid search (SQL filters + pgvector cosine, 60/25/15 ranking, graceful
  degradation) — _verified by: audit_
- [2026-05-23] Telegram bot `/start` + role pick + free-text routing, bilingual KM/EN i18n — _verified by: audit (flows 6/10, see A2)_
- [2026-05-23] 10/10 API endpoints present; Docker Compose (local+prod) + CI — _verified by: audit_
- [2026-06-xx] Docs consolidation: DEVELOPER_SPEC/PITCH/DOSSIER adopted (HEAD `ea46b23`) — _verified by: git log_

## In progress 🔨
- Deployment readiness — _status: ~60-65%, blocked on the 3 critical gaps (A1/A2/A3 in `04-BUGS.md`)_

## Next up ⏭️
- A1 — Auth middleware (Telegram header → user UUID); `rater_user_id`/`employer_id` are hardcoded placeholders.
- A2 — Telegram `ConversationHandler` to orchestrate CV→extract→review→publish.
- A3 — `conversations.py` service (message relay between employer/candidate).

## Known risks ⚠️
- **Low adoption** — <50 candidates in 60 days = KILL (KC-1). Mitigation: concentrate on 3 verticals (hospitality/retail/services), Phnom Penh first.
- **Khmer NLP quality** — parsing fails >40% = KILL (KC-3). Mitigation: ≥20-query test suite, prompt iteration, structured-form fallback.
- **Silent embedding fallback** (B3, `routes.py:145`) could hide failures — new profiles never vectorized (B1).

## Environment quick facts
- Runs on: Docker Compose (local + prod target VPS Phnom Penh/Bangkok, ~$25-45/mo)
- Live URL(s): none yet (Phase 0 = Telegram polling); public target `srokwork.org` at v1.0
- Repo: `git@github.com:f7xfo/Trov-.git` (branch `main`)
- Key external services: Telegram Bot API, DeepSeek V3 + embeddings, PostgreSQL 16 + pgvector, Redis, n8n
