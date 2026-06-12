# 00 — BOUSSOLE (Compass)

> The North Star. When in doubt, this file wins. Changes rarely.
> Last reviewed: 2026-06-13
>
> ⚠️ **DRAFT — TO BE VALIDATED BY ALEX.** The vision / north star / kill-criteria
> below were pre-filled by extraction from `docs/PROJECT_DOSSIER.md` + `docs/PITCH_DECK.md`
> so Alex has a starting point. **Alex owns this file** — review, correct, and confirm
> every field marked `⚠️ VALIDATE`.

## Why this project exists
- **Problem:** Cambodia's informal workforce (~85% of the labour market — cooks, drivers,
  cleaners, guards, retail, construction) finds jobs through chaotic Telegram/Facebook
  groups with no search, no profiles, no reputation, no protection against scams.
- **User:** Blue-collar / micro-SME workers and employers — the 95% that WorkingNA
  ($89/mo, white-collar) does not serve. Built "for the workers who don't have LinkedIn".
- **Value:** Structured natural-language matching (Khmer/EN) + a **verifiable trust layer**
  (the reciprocal rating system) delivered in the messaging apps workers already use.

## The ONE governing milestone
⚠️ VALIDATE — **Phase 0 Telegram MVP live + Day-60 kill-gate passed.** Everything is
measured against the Day-60 GO/KILL test below.

## North star (1 yr / 3 yr) — long-horizon vision
⚠️ VALIDATE (comes from Alex's head, not the code):
- **~1 year (Phase 1):** Messenger + cross-channel relay, ≥1,000 published profiles,
  MoLVT/NEA partnership formalized, registered Cambodian non-profit (សមាគម).
- **~3 years (Phase 2+):** PWA + voice CV + Khmer NLP fine-tuning, ≥10,000 profiles,
  ≥5,000 verified ratings, replication template for Laos / Myanmar / Vietnam.

## Current focus (the single most important thing right now)
Close the 3 deployment-blocking gaps (auth middleware, ConversationHandler,
`conversations.py`) so the Phase 0 Telegram bot can actually go live. See `01-STATE.md`.

## Critical path
**On the critical path (do these):**
- Auth middleware (Telegram header → user UUID) — A1.
- Telegram `ConversationHandler` for the multi-step CV→extract→review→publish flow — A2.
- `conversations.py` message-relay service — A3.
- Embedding trigger after `publish_profile()` so profiles are searchable — B1.

**NOT on the critical path (resist the temptation):**
- PWA, voice CV, Messenger bot, Khmer fine-tuning — all Phase 1/2 (see `07-IDEAS.md`).
- Polishing docs / investor-kit — already rich enough for Phase 0.

## Red lines (never, regardless of progress)
- **Ratings are immutable.** No deletion/modification API. No admin override. Removal only
  via 2/3 maintainer governance vote, logged publicly. Enforced at DB level (REVOKE).
- **Structured ratings only** — star + binary categories, NEVER free text (defamation risk
  under Cambodian law).
- **Free forever. No data selling. No ads.** MIT-licensed, self-hostable public good.
- **Parsing agent returns `null` if a field is missing — never guesses.**

## Definition of done / kill
**Day-60 kill-gate (RULE_27)** — Trov is declared dead if, 60 days after the bot goes live,
**any** of these is true (auto-checked daily by n8n, reported cold at Day 60):
- **GO if:** ≥50 published candidate profiles **AND** ≥5 employers with repeat searches
  (≥2 searches on different days) **AND** Khmer parsing error rate ≤40%.
- **KILL if:** KC-1 `< 50` published profiles · KC-2 `< 5` repeat employers · KC-3 Khmer
  parsing fails on `> 40%` of real queries.

> These kill-criteria are **proposed** (Critic at intake) then **validated by Alex** — never
> self-set. ⚠️ VALIDATE the thresholds above. _(Startup-Factory RULE_27: Critic proposes →
> Alex validates → Developer blocks if absent.)_
