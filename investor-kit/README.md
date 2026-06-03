# SrokWork 🇰🇭

**Open-source AI-powered recruitment platform for Cambodia.**  
Natural language job matching via PWA, Telegram bot, and Messenger bot — built for a mobile-first, trilingual (Khmer/English/Chinese) market.

> No venture capital. No data selling. No ads. Just a tool that helps Cambodian workers find jobs and SMEs find people — for free, forever.

---

## Why this exists

Cambodia's recruitment market is stuck in 2010. Passive job boards (BongThom, Pelprek) and Facebook groups are the dominant tools. There is no AI-powered search, no multi-channel integration, no reputation system.

Meanwhile:
- Mobile penetration is >120%
- Telegram and Messenger are how Cambodians communicate daily
- SMEs (restaurants, guesthouses, shops, NGOs) hire without HR departments
- Workers — cooks, drivers, security guards, receptionists — have no trusted platform to be found

SrokWork is the infrastructure this market is missing. It is open source because this problem is too important to be locked behind a VC growth model.

---

## What it does

- **Natural language search** — employers describe who they need in plain Khmer, English, or Chinese: *"ខ្ញុំត្រូវការអ្នកធ្វើម្ហូបនៅសៀមរាប"* or *"I need a cook Siem Reap under $400"*. The AI understands, extracts criteria, and returns ranked profiles instantly.
- **Smart CV intake** — candidates submit via PWA, Telegram, or Messenger. AI extracts structured data from any format: PDF, image, plain text, or voice description.
- **Cross-channel messaging** — private chat between employer and candidate without sharing phone numbers, relayed across all three channels.
- **Reciprocal rating system** — employers rate candidates, candidates rate employers. Ratings influence search ranking and build long-term trust in a market where reputation is culturally central.
- **Instant alerts** — employers save a search in one click. New matching candidates trigger push notifications (PWA) or bot messages instantly.
- **Three channels, one backend** — PWA, Telegram bot, and Messenger bot share a single database, AI engine, and API.

---

## Stack

| Layer | Technology |
|---|---|
| PWA | Next.js 14 (App Router) |
| Telegram Bot | Grammy.js |
| Messenger Bot | Meta Cloud API |
| Database | PostgreSQL + pgvector |
| AI / NLP | DeepSeek V3 (`deepseek-chat`) — or any OpenAI-compatible API / local Ollama |
| Auth | Clerk.dev (or self-hosted with NextAuth) |
| File Storage | S3-compatible (Cloudflare R2, MinIO, or self-hosted) |
| Cache / Queue | Redis (Upstash or self-hosted) |
| Push Notifications | Firebase FCM |
| Hosting | Vercel + Railway, or fully self-hosted |

**Philosophy:** every component can be swapped for a self-hosted alternative. No vendor lock-in. No proprietary dependencies.

---

## Self-hosting

The platform is designed to run on minimal infrastructure:

```bash
# Minimum viable self-hosted setup
- PostgreSQL with pgvector extension
- Redis instance
- Any S3-compatible object storage
- Node.js 20+ runtime
- DeepSeek API (default) or any OpenAI-compatible LLM endpoint (local Ollama works)
```

Monthly cost on a VPS: **~$20–40**. Can run on a homelab with a static IP or Cloudflare tunnel.

---

## Privacy by design

- **Minimal data collection** — only what is necessary for matching
- **No third-party tracking** — no analytics pixels, no ad networks
- **User data export and deletion** — `/mydata` command available in all bots
- **No data selling** — ever, to anyone, under any circumstances
- **LPDP-ready** — built with Cambodia's upcoming Personal Data Protection Law in mind
- **Local inference option** — the AI engine can run entirely on-premise with open-weight models (DeepSeek-R1, Qwen3, GLM)

---

## Project structure

```
trov/
├── apps/
│   ├── web/              # Next.js PWA
│   ├── telegram/         # Grammy.js bot
│   └── messenger/        # Meta Cloud API bot
├── packages/
│   ├── ai/               # NLP engine (CV parsing, query extraction, matching)
│   ├── db/               # Prisma schema + migrations
│   ├── shared/           # Types, utilities, constants
│   └── notifications/    # FCM + bot alert dispatcher
├── docs/                 # Architecture, API reference, deployment guides
└── docker-compose.yml
```

---

## Roadmap

| Phase | Focus | Status |
|---|---|---|
| v0.1 | Telegram bot + CV parsing + basic search | 🔨 In progress |
| v0.2 | Messenger bot + cross-channel messaging | Planned |
| v0.3 | PWA + rating system + alerts | Planned |
| v0.4 | Khmer NLP fine-tuning + local model support | Planned |
| v1.0 | Full multi-channel platform + self-hosting docs | Planned |

---

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for full guidelines.

**We especially need help with:**
- 🇰🇭 **Khmer NLP** — building query datasets, testing parsing accuracy on informal language
- 🇨🇳 **Chinese NLP** — supporting the large Chinese-speaking employer and candidate segment in Cambodia — building query datasets, testing parsing accuracy on informal language
- 🎨 **UI/UX** — mobile-first design for low-bandwidth environments
- 🌏 **Localization** — Khmer and Chinese translations, cultural accuracy review
- 📖 **Documentation** — deployment guides, API reference, self-hosting tutorials
- 🧪 **Testing** — bot conversation flow testing, edge cases, load testing

No contribution is too small. Fixing a typo in a Khmer translation matters.

---

## Who should contribute

- **Cambodian developers** — you know this market better than anyone
- **Diaspora devs** — contribute to your home country from anywhere in the world
- **Southeast Asia devs** — this model is directly replicable in Myanmar, Laos, and Vietnam
- **NLP researchers** — especially anyone working on low-resource Southeast Asian languages
- **NGO tech teams** — if your organization works in Cambodian labor rights or workforce development, let's talk integration

---

## License

MIT — do whatever you want with it, including deploying your own instance for another market.

If you adapt it for another country, please open-source your changes too.

---

## Contact

- GitHub Issues for bugs and feature requests
- GitHub Discussions for everything else

---

*Built in Phnom Penh. Open to the world.*
