# TROV — Project Dossier

**Open-source, free recruitment platform for Cambodia's informal workforce.**
**Date : 2026-05-23 | Version : 1.0 | Status : BUILD**

---

## Executive Summary

Trov is an open-source, AI-powered recruitment platform designed for the 3+ million Cambodian workers who find jobs through chaotic Telegram groups, Facebook comments, and word of mouth — not through LinkedIn or paid job boards. It structures the informal hiring market with natural-language matching and a verifiable trust layer (reciprocal rating system), delivered through the messaging apps workers already use.

Trov is a **public good**, not a startup. It will be housed in a non-profit entity and seek institutional partnership with Cambodia's Ministry of Labour and Vocational Training (MoLVT) and National Employment Agency (NEA). It is free for all users, forever. It does not sell data. It is MIT-licensed and self-hostable.

---

## 1. Mission

**Make finding work in Cambodia free, safe, and structured — for the workers who don't have LinkedIn.**

Cambodia's informal workforce — cooks, drivers, cleaners, security guards, retail staff, construction workers — represents ~85% of the labour market. These workers find jobs through anonymous messaging groups with no search, no profiles, no reputation system, and no protection against scams. Trov gives them a tool that works in their language, on their phones, through the apps they already use.

---

## 2. The Problem

### 2.1 The Chaos of Telegram Job Channels

Cambodia's informal hiring happens primarily in Telegram groups. "SrokWork Telegram" and similar channels have 60,000-80,000 members posting unstructured messages:

> "ខ្ញុំរកការងារនៅភ្នំពេញ" (I'm looking for work in Phnom Penh)
> "ត្រូវការអ្នកធ្វើម្ហូបនៅសៀមរាប" (Need a cook in Siem Reap)

There is no search. No filtering by location, salary, or skills. No way to match a cook in Siem Reap with a restaurant owner in Siem Reap unless they happen to see each other's messages in the firehose.

### 2.2 Recruitment Scams Against Vulnerable Workers

Cambodia's informal job market is rife with exploitation:

- Workers pay "placement fees" (sometimes $50-200) for jobs that don't exist
- Employers hire strangers with no work history — no references, no ratings, no accountability
- Domestic workers and service staff have no portable record of employment
- When disputes happen (unpaid wages, conditions different from what was promised), the worker has no evidence and no recourse

### 2.3 The Structural Blind Spot of Existing Solutions

WorkingNA, Cambodia's dominant recruitment platform, serves corporate/white-collar hiring at **$89/month per employer**. It is a legitimate, useful product — for the 5% of the market that can afford it and needs its features.

The other 95% — blue-collar workers, micro-SMEs, restaurants, shops, cleaning services — has no tool.

### 2.4 Why This Matters for Cambodia's Development

Cambodia's economy is SME-driven. According to the Ministry of Industry, SMEs account for ~70% of employment. These businesses cannot afford $89/month recruitment tools. Their hiring is entirely informal, entirely unstructured, and entirely dependent on personal networks — which limits mobility, suppresses wages, and excludes workers without connections.

---

## 3. The Solution

### 3.1 What Trov Does

Trov is a Telegram bot (Phase 0), expanding to Messenger and PWA (Phase 1+), that provides:

1. **Structured candidate profiles** — extracted by AI from natural-language descriptions (text, PDF, images, voice in future phases)
2. **Natural-language search** — employers describe who they need in plain Khmer or English; AI extracts criteria, ranks profiles, returns instant matches
3. **A verifiable trust layer** — the **reciprocal rating system** is the core product, not a feature

### 3.2 The Rating System Is The Product

Anyone can build a Telegram bot with LLM matching. The moat is trust.

Trov's rating system is:

- **Structured, not free text** — star score + predefined yes/no categories (e.g., "paid on time", "conditions matched"). No open text fields. This avoids defamation risk under Cambodian law.
- **Tied to a verified interaction** — both parties must have exchanged ≥ 2 messages each in a conversation on-platform before they can rate
- **Bidirectional but asymmetric** — employers rate candidates on "showed up on time / skills matched", candidates rate employers on "paid on time / conditions matched"
- **Immutable and non-purchasable** — truthful ratings cannot be deleted. No API for deletion. No admin override. The code enforces this.
- **Feeds search ranking directly** — trust is not cosmetic; it determines who appears in results

For a domestic worker who accumulates 12 verified ratings over 2 years, this becomes a **portable work history** — something that does not exist today for informal workers in Cambodia. It is worker protection, implemented in code.

### 3.3 Why Free Matters

"Free" is not the value proposition — structured matching + verifiable trust is. But free is essential for two reasons:

1. **Critical mass for ratings** — a rating system is only useful with volume. Charging candidates would block the volume needed. Charging employers would block the SME adoption needed.

2. **Trust signal** — being free, open-source, and self-hostable answers the question "how do I know you won't sell my data or start charging me?" in a way no privacy policy can.

---

## 4. Governance Model

### 4.1 Why Open Source + Non-Profit

A recruitment platform has a structural trust problem. Users must trust that:
- Their data won't be sold
- Ratings are genuine and permanent
- The service will remain free
- There is no hidden monetization

A VC-backed company cannot credibly make all four promises. The business model contradicts them. A non-profit with open-source code can.

### 4.2 Proposed Structure

| Stage | Entity | Rationale |
|---|---|---|
| **Phase 0-1 (Months 1-12)** | Individual maintainers, MIT license, public GitHub | Speed. No legal overhead needed yet. |
| **Phase 2 (Months 12-18)** | Cambodian-registered non-profit association (សមាគម) | Enables MoLVT partnership, grant eligibility, institutional credibility |
| **Beyond** | Fiscal sponsorship (e.g., Open Collective, NumFocus, or Cambodian foundation) | International grant access (UNDP, GIZ, ADB) |

### 4.3 Maintainer Governance

- 3-5 core maintainers with commit access
- Community contributors via pull requests
- Rating deletions (the single sensitive action) require **2/3 maintainer vote** — and are logged publicly
- No single person can delete a rating

### 4.4 Data Governance

- All user data stored in PostgreSQL on a self-hosted or Cambodian VPS
- `/mydata` command allows any user to export or delete their data (GDPR/LPDP-compatible)
- No third-party analytics, no tracking pixels, no ad networks
- Privacy policy in Khmer and English, reviewed by a Cambodian legal professional before public launch

---

## 5. 18-Month Roadmap

```
┌──────────────────────────────────────────────────────────────────────────┐
│ PHASE 0 — Telegram MVP                               Months 1-2 (Day 60) │
├──────────────────────────────────────────────────────────────────────────┤
│ • Telegram bot (Grammy.js) — bilingual KM/EN                            │
│ • CV extraction agent (DeepSeek)                                        │
│ • Query parsing agent (DeepSeek)                                        │
│ • Hybrid search (SQL filters + pgvector cosine similarity)              │
│ • Rating system v1.0 (structured, immutable, interaction-verified)      │
│ • Saved search alerts                                                   │
│ • Kill-criteria auto-monitoring (n8n)                                   │
│ • Docker Compose deployment                                             │
├──────────────────────────────────────────────────────────────────────────┤
│ KILL GATE at Day 60:                                                     │
│   ✓ ≥ 50 candidates with published profiles                             │
│   ✓ ≥ 5 employers with repeat searches                                  │
│   ✓ Khmer parsing error rate ≤ 40%                                      │
├──────────────────────────────────────────────────────────────────────────┤
│ PHASE 1 — Messenger + Trust Deepening              Months 3-12           │
├──────────────────────────────────────────────────────────────────────────┤
│ • Messenger bot (Meta Cloud API)                                        │
│ • Cross-channel relayed messaging (employer Telegram ↔ candidate Msgr)  │
│ • PDF/Image CV parsing (OCR via DeepSeek vision)                        │
│ • Conversation state in Redis (replace v0 heuristics)                   │
│ • Rating system v2.0: decay-weighted, verification badges               │
│ • Job posting flow (stored job posts, reverse candidate search)         │
│ • Audit log for LPDP compliance                                         │
│ • Self-hosting documentation                                            │
│ • ≥ 1,000 published profiles                                            │
│ • MoLVT/NEA partnership formalized                                      │
├──────────────────────────────────────────────────────────────────────────┤
│ PHASE 2 — PWA + Scale                               Months 13-18         │
├──────────────────────────────────────────────────────────────────────────┤
│ • Progressive Web App (srokwork-web, Next.js 14)                        │
│ • Voice CV intake (Telegram voice → Whisper → CV extraction)           │
│ • Khmer NLP fine-tuning (≥ 500 labeled queries, eval harness)           │
│ • Local Ollama deployment option (fully offline)                        │
│ • Skills taxonomy for Cambodian labour market                           │
│ • University/NGO graduate placement partnerships                        │
│ • Replication template for Laos, Myanmar, Vietnam                       │
│ • ≥ 10,000 profiles, ≥ 500 active employers, ≥ 5,000 verified ratings   │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 6. Kill-Criteria (RULE_27)

Trov is declared dead if, 60 days after the Telegram bot goes live, **any** of the following are true:

| # | Criterion | Threshold | Measurement |
|---|---|---|---|
| KC-1 | Fewer than 50 candidates created a published profile | < 50 | `COUNT(candidate_profiles WHERE is_published = true)` |
| KC-2 | Fewer than 5 employers ran a repeat search | < 5 | `COUNT(DISTINCT employer_id) WHERE employer has ≥ 2 searches on different days` |
| KC-3 | Khmer query parsing fails on more than 40% of real queries | > 40% error rate | `COUNT(role IS NULL OR location IS NULL) / COUNT(*) for queries containing Khmer script` |

These are **auto-checked daily** by an n8n workflow and reported cold at Day 60. This is not pessimism — it is the discipline required to ensure that a "public good" is actually useful to the public.

---

## 7. Target Verticals (Phase 0 Wedge)

**Geography:** Phnom Penh first (highest density, fastest rating accumulation).

**Three priority verticals** (high turnover = rapid rating volume):

| Vertical | Example Roles | Why |
|---|---|---|
| **Hospitality / Restaurant** | Cooks, waiters, cashiers, cleaners | Cambodia's largest employer of informal workers. Extreme turnover. Siem Reap + Phnom Penh density. |
| **Retail / Commerce** | Sales staff, stock clerks, delivery drivers | Growing sector. High churn. Russian Market, Central Market, Aeon Mall ecosystem. |
| **Services** | Security guards, drivers, nannies, gardeners | Fragmented, no existing platform, high trust premium. |

Multi-sector, but marketing and employer outreach concentrate on these three to ensure rating density.

---

## 8. Competitive Landscape

### 8.1 Cambodia

| Platform | Segment | Price | Our Position |
|---|---|---|---|
| **WorkingNA** | White-collar, corporate | $89/mo | Not competing. Trov serves the segment they cannot reach. |
| **BongThom** | Mixed, web-based | Free/Paid | Web-only. No AI matching. No messaging integration. English-first. |
| **Telegram groups** | Everything | Free | This is our actual competition. Chaos. Trov replaces chaos with structure. |
| **Facebook groups** | Everything | Free | Same problem — unstructured feed, no search, no trust. Future Messenger integration addresses this. |

### 8.2 Regional Analogues (Proof Points, Not Competitors)

| Platform | Country | Scale | Model |
|---|---|---|---|
| **WorkIndia** | India | 100M+ downloads | Blue-collar, vernacular, profitable |
| **Apna** | India | Unicorn ($1.1B) | SME/blue-collar, vernacular communities |
| **Pintarnya** | Indonesia | 2M+ users | F&B/Hospitality/Retail, chat-based |
| **Bossjob** | SEA (PH, ID) | Growing | Chat-based AI hiring, Gen-Z focused |

These platforms validate the model: chat-based, vernacular-first, blue-collar/SME recruitment works at scale in developing Southeast Asian markets. Cambodia is the last major SEA market without a specialized player in this space.

---

## 9. Technology

### 9.1 Stack (Phase 0)

| Layer | Technology |
|---|---|
| Telegram Bot | Grammy.js (Node.js/TypeScript) |
| API Backend | FastAPI (Python 3.12) |
| AI/NLP | DeepSeek V3 (chat) + text-embedding-3-small |
| Database | PostgreSQL 16 + pgvector |
| Cache/Sessions | Redis |
| Orchestration | n8n (self-hosted) |
| Container | Docker Compose |

### 9.2 Why This Stack

- **DeepSeek V3**: ~$0.10/million tokens. Cheapest production-grade LLM for bilingual (Khmer/English) NLP. Swappable to any OpenAI-compatible endpoint.
- **PostgreSQL + pgvector**: One database, one backup. No separate vector store. pgvector handles tens of thousands of embeddings on commodity hardware.
- **Grammy.js**: Superior conversation state management vs python-telegram-bot. Native i18n, session middleware, Redis storage.
- **n8n**: Visual workflow builder. Non-engineers can inspect/modify the alert sweep and kill-criteria monitoring. Open-source, self-hosted.
- **Monolith-first**: Phase 0 fits in one process + one DB. We split only when something breaks.

### 9.3 Cost to Operate

| Resource | Monthly Cost (Estimate) |
|---|---|
| VPS (Phnom Penh/Bangkok, 2 vCPU, 4GB RAM) | $20-30 |
| DeepSeek API (NLP + embeddings) | $5-10 (at Phase 0 scale) |
| Domain + DNS | $2-5 |
| **Total** | **~$25-45/month** |

Fully operational at under $50/month. Free to run. Free to use.

---

## 10. Risk Register

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| **Low adoption** — fewer than 50 candidates in 60 days | Medium | CRITICAL (kill) | Concentrated marketing in 3 verticals. Telegram channel cross-posting. Partner with existing job groups. |
| **Khmer NLP quality** — parsing fails >40% | Medium-High | CRITICAL (kill) | Test suite of 20+ real Khmer queries. Iterate prompt engineering. Fallback: structured form as backup input. |
| **Telegram API policy change** — restrictions on bots in groups | Low | High | Messenger bot is Phase 1 mitigation. PWA is platform-independent. |
| **Defamation claims** — employer sues over a negative structured rating | Low | Medium | Structured-only ratings (no free text). Legal review of category design. Immutability with governance override. |
| **Government indifference** — MoLVT/NEA don't engage | Medium | Low | Trov works without government endorsement. It helps, but is not required. |
| **Competitor entry** — a funded player enters Cambodian blue-collar recruitment | Low-Medium | Medium | Open-source + non-profit positioning is structurally hard to compete with. Free forever is a genuine moat against VC-backed competitors who must eventually monetize. |
| **Maintainer burnout** — solo developer cannot sustain | Medium | Medium | Open-source from day one. Build contributor community. Non-profit structure enables grant-funded maintenance. |

---

## 11. Team & Contributors

### Phase 0

| Role | Description |
|---|---|
| **Project Lead / Architect** | Alex — technical architecture, agent design, infrastructure |
| **Backend Developer** | Python/FastAPI, PostgreSQL, pgvector, Redis |
| **Bot Developer** | Grammy.js/TypeScript, Telegram API, i18n |
| **n8n Workflow Developer** | Alert sweep, kill-criteria monitoring, embedding sync |

### Seeking

- **Khmer NLP contributor** — test set creation, prompt evaluation, accuracy measurement
- **UI/UX designer** — mobile-first design for low-bandwidth conditions
- **Legal reviewer (Cambodia)** — LPDP compliance review, terms of service
- **Community manager (Khmer-speaking)** — Telegram group moderation, user support

---

## 12. Appendix: Why "Trov"?

- **Short**: 4 letters. Easy to remember, type, and search.
- **Evocative**: Echoes "trouver" (French: to find), "treasure trove", "trovão" — discovery across languages
- **Language-neutral**: Works in Khmer script (ទ្រូវ), English, and French — Cambodia's three operating languages
- **Domain-friendly**: `trov.org`, `trov.kh`, `trov.app` are viable

---

*Document prepared by Architect (OpenClaw) for the Trov project.*
*Based on: ARCHITECT BRIEF (2026-05-23), SrokWork codebase audit, Critic evaluation (RESHAPE→BUILD).*
*Next: Developer handoff → Phase 0 implementation.*
