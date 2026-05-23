# Trov — Pitch Deck
## Open-source, free recruitment for Cambodia's invisible workforce

**Audience :** Plug and Play Cambodia + Ministry of Labour and Vocational Training / National Employment Agency  
**Format :** 14 slides | Public-good / institutional partnership framing  
**Date :** 2026-05-23

---

## Slide 1 — Title

**TROV**
*ប្រទេសកម្ពុជា — ការងារសម្រាប់គ្រប់គ្នា*
*Cambodia — Work for everyone.*

Open-source, free recruitment platform for the workers who don't have LinkedIn.

---

## Slide 2 — The Reality

### Cambodia's job market has two worlds.

| | World A — LinkedIn Cambodia | World B — The Real Market |
|---|---|---|
| **Who** | White-collar, university graduates, English-speaking | Blue-collar, SME workers, informal economy |
| **Where** | WorkingNA ($89/mo), LinkedIn, BongThom | Telegram groups, Facebook comments, word of mouth |
| **How many** | ~50,000 | **~3,000,000** |
| **Trust** | CV verification, company branding | Anonymous usernames, "trust me bro" |

**World B is where 95% of Cambodians look for work. It is completely unstructured.**

A cook in Siem Reap and a restaurant owner in Phnom Penh are looking for each other right now — inside a Telegram group with 80,000 anonymous members, no search, no profiles, and no way to know who can be trusted.

---

## Slide 3 — The Problem, Specifically

### Three failures of the status quo

**1. No structure.**
"SrokWork Telegram" channels have 80K members posting "ខ្ញុំរកការងារ" into a firehose. No search. No matching. Just noise.

**2. No trust.**
Recruitment scams are rampant. Workers pay "fees" for jobs that don't exist. Employers hire strangers with no work history. There is no reputation layer.

**3. No protection.**
Cambodia's Labour Law guarantees rights, but informal workers cannot enforce them because they have no record of who they worked for. The rating system is a portable work history — a form of protection.

---

## Slide 4 — What Trov Is

### Three words: Search. Trust. Free.

A Telegram bot (Phase 0), then Messenger + PWA (Phase 1), where:

- **Candidates** describe their experience in plain Khmer or English — AI extracts a structured profile. **Free. Always.**
- **Employers** describe who they need — a cook in Siem Reap, under $400 — and get ranked matches with verified ratings. **Free. Always.**
- **Both rate each other** after a verified interaction. The rating is **the product.**

**Open-source. Non-profit trajectory. No data selling. No ads. No venture capital.**

---

## Slide 5 — The Rating System Is The Moat

*Anyone can build a Telegram bot with LLM matching. No one has the trust layer.*

### How it works

- ⭐ **Star score + structured categories** (not free text — no defamation risk under Cambodian law)
- 🔗 **Tied to a verified interaction** — you can only rate someone you actually exchanged with on-platform
- 🔄 **Bidirectional but asymmetric** — workers rate employers on "paid on time?", employers rate workers on "showed up?"
- 🔒 **Immutable and non-purchasable** — no one can delete a truthful rating for money
- 📊 **Feeds search ranking** — trust is infrastructure

### Why this matters in Cambodia

A domestic worker who has 12 verified ratings saying "paid on time, conditions matched" has **portable trust** — something that does not exist today for informal workers. This is worker protection, not a feature.

---

## Slide 6 — Why It Works: Regional Proof

This model is proven across developing Southeast Asian markets. Cambodia is simply the last to get it.

| Platform | Country | Segment | Scale |
|---|---|---|---|
| **WorkIndia** | India | Blue-collar, 100M+ downloads | Series D, profitable |
| **Apna** | India | SME/blue-collar, vernacular | Unicorn ($1.1B) |
| **Pintarnya** | Indonesia | F&B/Hospitality/Retail | 2M+ users |
| **Bossjob** | SEA (PH, ID) | Chat-based AI hiring, Gen-Z | Growing rapidly |

**The Cambodian blue-collar niche is empty.** Trov fills it.

These are not competitors — they are proof that chat-based, vernacular-first, blue-collar recruitment works in Southeast Asia.

---

## Slide 7 — Positioning: Not Against WorkingNA

WorkingNA dominates Cambodian white-collar recruitment at $89/mo. We are not competing.

| | WorkingNA | Trov |
|---|---|---|
| **Target** | Corporate, white-collar, degree-required | Blue-collar, SME, informal |
| **Price** | $89/mo (employers) | Free (both sides) |
| **Language** | English/Khmer | Khmer-first, English-second |
| **Channel** | Web | Telegram → Messenger → PWA |
| **Trust layer** | Company branding | Portable worker ratings |
| **Market size** | ~50,000 jobs | ~3,000,000 workers |

WorkingNA serves the structured top of the pyramid. Trov serves the base — where the volume, the need, and the Ministry's mandate all sit.

**We go where they structurally cannot.**

---

## Slide 8 — Product: Phase 0 (60 Days to Launch)

### What ships in 60 days

| Feature | Status |
|---|---|
| Telegram bot — bilingual Khmer/English | Build |
| Natural-language CV extraction (AI) | Build |
| Natural-language job search (AI) | Build |
| Hybrid matching (filters + AI ranking) | Build |
| **Structured rating system** | Build |
| Saved search alerts | Build |


### Stack
DeepSeek V3 (LLM) · Grammy.js (Telegram) · FastAPI (Python) · PostgreSQL + pgvector · Redis · n8n (orchestration) · Self-hosted

### Cost to run
**~$25-40/month** on a small VPS in Phnom Penh. Free to operate. Free to use.

---

## Slide 9 — What We Need From Plug and Play

### Not money. Legitimacy, network, and the first 1,000 users.

1. **Institutional introduction** — warm connection to Ministry of Labour (MoLVT) and National Employment Agency (NEA). Trov is free infrastructure that advances their mandate.

2. **Employer seed network** — introduction to 10-20 reputable SMEs in Phnom Penh's hospitality/retail/service sectors who can seed the first ratings.

3. **Mentorship on non-profit governance** — how to structure a Cambodian tech non-profit. Fiscal sponsorship options. Grant pathways (UNDP, GIZ, ADB digital inclusion programs).

4. **Visibility** — a public-good tech project built in Cambodia, for Cambodia. This is a story Plug and Play can tell.

---

## Slide 10 — What We Need From MoLVT / NEA

### Partnership, not funding

- **Endorsement** — "Trov is recognized by NEA as a free job-matching service." This single line on the bot's `/start` message transforms credibility for both workers and employers.
- **Job fair integration** — NEA runs regular job fairs. A Trov station where workers create profiles in 2 minutes via Telegram.
- **Data sharing** — NEA's occupation taxonomy and salary benchmarks improve matching accuracy.
- **No cost to government.** Trov is self-hosted, open-source infrastructure.

---

## Slide 11 — 18-Month Roadmap

```
Phase 0 (Months 1-2)     Phase 1 (Months 3-12)       Phase 2 (Months 13-18)
┌──────────────────┐    ┌─────────────────────┐     ┌──────────────────────┐
│ Telegram Bot     │───▶│ Messenger Bot        │────▶│ PWA (mobile web app) │
│ CV Extraction    │    │ Cross-channel relay  │     │ Voice CV (Whisper)   │
│ NL Search        │    │ Rating system v2     │     │ Khmer NLP fine-tune  │
│ Rating System    │    │ Job posting flow     │     │ Local LLM (Ollama)   │

└──────────────────┘    └─────────────────────┘     └──────────────────────┘
       │                          │                           │
  60-day gate               Public launch              Scale + replicate

```

### Metrics (18-month targets)
- ≥ 10,000 published candidate profiles
- ≥ 500 active employers
- ≥ 5,000 verified ratings
- Khmer parsing accuracy ≥ 85%

---

## Slide 13 — Why Open Source + Non-Profit

### The trust physics of recruitment

A recruitment platform has a structural trust problem:
- "How do I know you won't sell my data?"
- "How do I know ratings are real?"
- "How do I know this will still be free next year?"

**Open source answers all three.**

- The code is public. Privacy claims are verifiable, not marketing.
- Ratings are immutable in a public schema. Auditable by anyone.
- MIT license. Anyone can self-host. Trov can never be taken away.

A VC-backed recruitment platform **cannot** make these promises. The business model contradicts them.

**Trov's competitive advantage is that it has no business model.** It is infrastructure for a public purpose, built in the open, free forever — because being free is the only way to earn the trust of millions.

---

## Slide 14 — Ask

### We are not asking for investment. We are asking to build something useful, together.

**Plug and Play Cambodia:**
Mentorship, network, visibility, and an introduction to the ecosystem that makes this credible.

**MoLVT / NEA:**
Endorsement and integration — make Trov visible to the workers who need it most.

**The commitment from our side:**


---

*Trov — ការងារសម្រាប់គ្រប់គ្នា*
*Trov — Work for everyone.*
*github.com/trov (coming soon)*
