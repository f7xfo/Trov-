# 02 — TODO

> The plan. Organized around a sprint with a binary GO/KILL test.
> Source: `docs/ROADMAP.md` (v0.1 unchecked items) + `docs/AUDIT_2026-05-23.md` (action items).

## Current sprint
- **Dates:** ⚠️ VALIDATE (set start → +14 days)
- **Sprint goal (one sentence):** Close the 3 deploy-blocking gaps so the Phase 0 Telegram bot can go live.
- **GO/KILL test at the end:** Can a candidate complete CV→extract→review→publish and an
  employer run an authenticated search end-to-end on the live bot? (yes/no)

### This sprint (do now)
- [ ] (P1) A1 — Auth middleware: Telegram header → user UUID (replaces hardcoded placeholders) — _~2h_
- [ ] (P1) A2 — `ConversationHandler` for the multi-step Telegram flow — _~3h_
- [ ] (P1) A3 — `conversations.py` message-relay service — _~2h_
- [ ] (P2) B1 — Trigger embedding after `publish_profile()` (else profiles never vectorized) — _~1h_
- [ ] (P2) B2 — n8n workflows JSON (alert sweep + embedding sync + kill-criteria monitoring) — _~2h_
- [ ] (P3) B3 — Log the silent embedding fallback (`except Exception: pass` at `routes.py:145`) — _~10min_
- [ ] (P3) C1 — Unit tests on ratings / matching / search (currently 4 smoke tests only) — _~3h_

## Backlog (NOT now — parked on purpose)
> From `docs/ROADMAP.md` v0.2–v0.5. Don't pull mid-sprint.
- v0.1 finish: persist profile + compute embedding; PDF/image CV (OCR); confirm/correct flow before publish.
- v0.2: real hybrid matching UI, "save as alert" flow, arq/n8n alert sweep, reciprocal rating after conversation, Redis conversation state.
- v0.3: Messenger bot (Meta Cloud API), cross-channel relay, LPDP audit log.
- v0.4: ≥500 Khmer query test set, eval harness (DeepSeek vs Claude vs Qwen), embedding fine-tune, offline Ollama.
- v0.5: `srokwork-web` PWA (Next.js 14), mobile-first, web push.

## Done (this sprint) ✅
- [x] Migration to standard project-tracking format (project-log/ + CLAUDE.md) — 2026-06-13
