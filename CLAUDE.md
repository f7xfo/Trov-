# CLAUDE.md — Project operating manual

> Claude Code reads this file automatically at the start of every session.
> Keep it SHORT. Heavy detail lives in `/project-log/` and `/docs/`.

## What this project is
Trov (ទ្រូវ) — an open-source, free, AI-powered recruitment platform for Cambodia's
informal workforce (blue-collar / micro-SME). Natural-language matching (Khmer/EN) +
a verifiable reciprocal **rating system** (the moat), delivered on Telegram (Phase 0).
A public good: MIT-licensed, non-profit, no data selling. Repo: `git@github.com:f7xfo/Trov-.git`.

## Boot sequence — read these IN ORDER before doing anything
1. `project-log/00-BOUSSOLE.md`  → why we exist + the one milestone + red lines + kill-gate
2. `project-log/01-STATE.md`     → where we are right now (source of truth)
3. `project-log/03-HANDOFF.md`   → the exact next step from last session
4. `project-log/04-BUGS.md`      → what's currently broken / blocking deploy
Only read `project-log/02` / `05` / `06` / `07` when the task needs them.
For deep technical detail, `06-STACK.md` points into `docs/` (DEVELOPER_SPEC, ARCHITECTURE, …) —
the `docs/` set is authoritative and must NOT be duplicated into the log.
(The full `project-log/00→07` is the project memory — always start there.)

## Hard rules (red lines — never cross without asking Alex)
**Generic (kit):**
- Never invent progress. If a fact isn't in the log/docs, say "not documented" — don't guess.
- Never display or commit secrets (API keys, tokens, `.env`). Reference them by name only.
- "Done" means TESTED. Never mark anything Done in `01-STATE.md` unless it was actually run
  and verified (Alex can't read code to check — the test IS the proof).
- New idea mid-session → log it in `07-IDEAS.md` and keep going. Don't act unless Alex says "promote".
- Don't change the stack/architecture without writing it in `05-DECISIONS.md` first.
- Git: commit at every working checkpoint with a clear message (`feat:`, `fix: BUG-001 …`).
  Never `push --force`. Never commit `.env`. The log files tell the story; git holds the save.
- Everything written in English. Explain the "why" to Alex in plain language (French OK in chat).

**Trov-specific (house rules — from the dossier/spec):**
- ⚖️ **RULE_27 — Kill-Criteria (Day 60).** Trov is killed if, 60 days after the bot goes live,
  ANY holds: KC-1 `<50` published profiles · KC-2 `<5` repeat employers · KC-3 Khmer parsing
  error `>40%`. Auto-checked daily by n8n. Criteria are proposed by Critic, **validated by Alex** — never self-set.
- 🔒 **Ratings are immutable.** No deletion/modification API, no admin override. Removal only via
  2/3 maintainer governance vote, logged publicly. Enforced at DB level (REVOKE UPDATE/DELETE). Never weaken this.
- 📝 **Structured ratings only** — star + binary categories, NEVER free text (defamation risk under Cambodian law).
- 🆓 **Free forever · MIT · no data selling · no ads.** It's a public good — never introduce paywalls or data resale.
- 🤖 **Parsing agents return `null` for a missing field — never guess** a role/location/salary.
- 🚧 **Respect the Phase 0 scope boundary** (`docs/DEVELOPER_SPEC.md §2`). Phase 1/2 features (Messenger,
  PWA, voice, fine-tuning) live in `07-IDEAS.md`, not in the current sprint.

## If things break badly (recovery)
1. STOP editing. Run `git status` + `git log --oneline -5` and show Alex where we are.
2. Uncommitted mess → `git checkout -- <file>` restores the last committed version.
3. Bad commit → `git revert <hash>` (undoes it without rewriting history).
4. Log the incident in `04-BUGS.md` with what triggered it.
Never "fix forward" in panic — roll back to the last known-good commit first.

## End-of-session ritual (Alex will say "fais le handoff")
Update in this order: 1. `03-HANDOFF.md` · 2. `01-STATE.md` · 3. `04-BUGS.md` ·
4. `05-DECISIONS.md` · 5. `02-TODO.md` · 6. `07-IDEAS.md` · 7. `git add <paths> && git commit`
(message: `session: <date> — <one-line summary>`). Then give Alex a 4-line summary in French.

## Who is Alex
Non-technical founder. Wants direct recommendations + a plain-language "why".
Iterative, action-oriented. Decisions in French, deliverables in English.
