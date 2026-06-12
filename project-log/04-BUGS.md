# 04 — BUGS (Bug journal)

> Every bug gets an ID so you can refer to it ("fix BUG-007").
> Severity: 🔴 blocker · 🟠 major · 🟡 minor
> Source: `docs/AUDIT_2026-05-23.md` (findings A1-A3 critical, B1-B3 medium, C1-C2 low).
> Note: A1-A3 are deploy-blocking GAPS (missing implementation), kept here as blockers.

## Open
| ID | Sev | Symptom (what you see) | Repro (steps) | Status / notes |
|----|-----|------------------------|---------------|----------------|
| BUG-001 (A1) | 🔴 | Cannot create a rating or alert — `rater_user_id`/`employer_id` hardcoded `UUID("00000000-...")` | call rating/alert endpoint | Auth middleware absent. Fix: Telegram header → user UUID. `api/routes.py:235,272` |
| BUG-002 (A2) | 🔴 | Multi-step CV→extract→review→publish flow not orchestrated | run bot, try full CV intake | No `ConversationHandler`. `bots/telegram/bot.py` |
| BUG-003 (A3) | 🔴 | No message relay between employer & candidate | — | Service `conversations.py` absent |
| BUG-004 (B1) | 🟠 | New profiles never vectorized → invisible to search | publish a profile, search for it | No embedding trigger after `publish_profile()`. `services/profiles.py` |
| BUG-005 (B2) | 🟠 | Alert sweep + embedding sync + kill-criteria not automated | — | No n8n workflow JSON exists |
| BUG-006 (B3) | 🟡 | Embedding fallback fails silently | trigger an embedding error | `except Exception: pass` with no logging. `api/routes.py:145` |
| BUG-007 (C1) | 🟡 | No regression safety on core logic | — | Only 4 smoke tests; zero unit tests on ratings/matching/search. `tests/` |

## Resolved ✅
| ID | Sev | Symptom | Fix (what actually solved it) | Date |
|----|-----|---------|-------------------------------|------|
| — | — | (none yet) | — | — |

<!-- Why keep resolved bugs: the SAME bug comes back. The "Fix" column saves you
hours next time. Never delete this table. -->
