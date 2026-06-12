# 05 — DECISIONS (Decision log)

> Why we chose what we chose. Stops you (and Claude) from re-debating settled
> questions 3 weeks later. One entry per real decision. Newest at top.
> Source: `docs/PROJECT_DOSSIER.md`, `docs/DEVELOPER_SPEC.md §11`, git history.

---
### DEC-007 — Adopt richer local docs (re-instate RULE_27 + WorkingNA positioning) — 2026-06-xx
- **Decision:** Adopt the richer local DEVELOPER_SPEC / PITCH_DECK / PROJECT_DOSSIER copies;
  RULE_27 kill-criteria and WorkingNA positioning are **ACTIVE** in the public docs (HEAD `ea46b23`).
- **Why:** The local pre-rename copies were more complete; kill-criteria and competitive
  positioning belong in the public dossier/pitch for legitimacy and discipline.
- **Alternatives rejected:** Keeping them stack-internal only — earlier commits `01ea0f6`
  ("Remove kill-criteria — stack-internal only") and `344dde5` ("Remove WorkingNA positioning")
  did this, then were reversed by `ea46b23`.
- **Status:** active

### DEC-006 — Open-source + non-profit, free forever, MIT — 2026-05-23
- **Decision:** Trov is a public good housed in a (future) Cambodian non-profit; MIT-licensed,
  self-hostable, free for all users forever, no data selling, no ads.
- **Why:** A recruitment platform has a structural trust problem; only a free, open, non-profit
  model can credibly promise "we won't sell your data or start charging". Free is also required
  for the rating-volume critical mass.
- **Alternatives rejected:** VC-backed for-profit (business model contradicts the trust promises).
- **Status:** active

### DEC-005 — Rating system is immutable & structured-only — 2026-05-23
- **Decision:** Ratings = star + binary categories, NO free text. Ratings can NEVER be modified
  or deleted except via a 2/3 maintainer governance vote (publicly logged). No deletion API,
  no admin override; enforced at the DB permission level (REVOKE UPDATE/DELETE).
- **Why:** Trust is the moat → ratings must be tamper-proof. Structured-only avoids defamation
  risk under Cambodian law. Immutability makes ratings a portable work history for workers.
- **Alternatives rejected:** Free-text reviews (defamation + abuse); soft-deletable ratings (gameable).
- **Status:** active

### DEC-004 — Phase 0 stack: DeepSeek V3 + pgvector + Grammy.js + n8n, monolith-first — 2026-05-23
- **Decision:** DeepSeek V3 (+ text-embedding-3-small) for bilingual NLP; PostgreSQL 16 + pgvector
  (one DB, no separate vector store); Grammy.js for the bot; n8n for orchestration; single
  process + single DB until something breaks.
- **Why:** Cheapest production-grade bilingual LLM (~$0.10/M tok, OpenAI-compatible/swappable);
  pgvector avoids a second datastore; n8n lets non-engineers inspect alert/kill-criteria flows;
  monolith keeps Phase 0 operable at <$50/mo.
- **Alternatives rejected:** Separate vector DB; arq for alerts (replaced by n8n); microservices (premature).
- **Status:** active

### DEC-003 — Not competing with WorkingNA (serve the other 95%) — 2026-05-23
- **Decision:** Position Trov as serving the blue-collar / micro-SME base, explicitly NOT competing
  with WorkingNA ($89/mo, white-collar top of the pyramid).
- **Why:** Different segment, different price point ($0 vs $89/mo), Ministry mandate sits at the base.
- **Status:** active (re-instated, see DEC-007)

### DEC-002 — Rename SrokWork → Trov — 2026-05
- **Decision:** Rename the project/namespace from `srokwork` to `Trov` (ទ្រូវ).
- **Why:** Short (4 letters), evocative ("trouver"/"trove"), language-neutral (KH/EN/FR), domain-friendly.
- **Alternatives rejected:** Keeping "SrokWork" (longer, less domain-flexible). Migration is 100%
  complete — audit confirms zero imports to the old `srokwork` namespace.
- **Status:** active

### DEC-001 — Telegram-first (Phase 0), then Messenger then PWA — 2026-05-23
- **Decision:** Launch on Telegram first; Messenger (Phase 1) and PWA (Phase 2) come later.
- **Why:** It's where Cambodian informal workers already are; fastest path to rating density.
- **Alternatives rejected:** Web/PWA-first (workers aren't there yet; slower critical mass).
- **Status:** active
---
