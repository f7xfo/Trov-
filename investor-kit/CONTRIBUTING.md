# Contributing to SrokWork

Thank you for considering a contribution. SrokWork is a community project — no company owns it, no investor controls it. Every contribution goes directly toward improving a free tool for Cambodian workers and employers.

---

## Before you start

Read the [README](./README.md) to understand the project's purpose, stack, and philosophy. Especially the **Privacy by design** section — it is non-negotiable and applies to every contribution.

---

## Ways to contribute

### 1. Khmer NLP dataset

This is the highest-impact contribution you can make.

The AI engine needs real-world Cambodian job queries to work well — informal language, code-switching between Khmer and English, abbreviations, provincial dialects.

**What we need:**
- Real or realistic job search queries in Khmer, English, and mixed
- Their expected parsed output (skills, location, salary, etc.)
- Corrections when the AI parses something wrong

**Format:**

```json
{
  "raw_query": "ខ្ញុំត្រូវការអ្នកធ្វើម្ហូបនៅសៀមរាប តម្លៃ $300",
  "expected": {
    "skills": ["cook"],
    "location_city": "Siem Reap",
    "salary_max": 300,
    "languages": []
  }
}
```

Add entries to `packages/ai/datasets/queries.json` and open a PR.

---

### 2. Code contributions

**Good first issues** are labeled `good first issue` on GitHub. They are scoped, documented, and do not require deep knowledge of the full codebase.

**Current priority areas:**
- Telegram bot conversation flows (Grammy.js, TypeScript)
- CV parsing prompt improvements
- pgvector matching algorithm tuning
- PWA components (Next.js, Tailwind)
- Self-hosting Docker Compose configuration
- Test coverage

**Before opening a PR:**
- Open an issue first for anything non-trivial
- One feature or fix per PR
- Include tests if you add logic
- Run `pnpm lint` and `pnpm test` before submitting

---

### 3. Translations and localization

All user-facing strings live in `packages/shared/i18n/`.

```
i18n/
├── en.json    # English (base)
├── km.json    # Khmer
└── zh.json    # Chinese (for Chinese-speaking community in Cambodia)
```

If you are a native Khmer speaker, the most valuable thing you can do is review `km.json` for naturalness. Many translations will be technically correct but sound robotic. Fix them.

---

### 4. Documentation

Good documentation is what turns a solo project into a community project.

**Priority docs needed:**
- Self-hosting guide (VPS + Docker)
- Self-hosting guide (homelab + Cloudflare tunnel)
- Local development setup on Windows, Mac, Linux
- DeepSeek API integration guide (default provider)
- Local inference guide (Ollama + DeepSeek-R1 or Qwen3)
- Bot setup walkthrough (Telegram BotFather + Meta Developer Portal)

All docs live in `/docs` as Markdown files.

---

### 5. Bug reports

Open a GitHub Issue with:
- What you did
- What you expected
- What happened instead
- Your environment (OS, Node version, browser if PWA)

For bot bugs, include the exact message sequence that triggered the issue.

---

### 6. Feature requests

Open a GitHub Discussion (not an Issue) with:
- The problem you are trying to solve
- Who it affects (candidates, employers, admins)
- Your proposed solution (optional)

Features that add complexity without clear user benefit will not be merged. This is a tool for a specific market, not a general-purpose HR platform.

---

## What will not be merged

- Any feature that collects additional user data beyond what is necessary for matching
- Third-party analytics, tracking pixels, or ad network integrations
- Monetization features (this project is free forever)
- Features that only work with a specific paid cloud provider
- Breaking changes to the privacy model without community consensus

---

## Development setup

```bash
# Prerequisites: Node.js 20+, pnpm, Docker

git clone https://github.com/yourusername/trov
cd trov
pnpm install

# Start local services (PostgreSQL + Redis)
docker-compose up -d

# Run database migrations
pnpm db:migrate

# Start all apps in development mode
pnpm dev
```

**Environment variables:** copy `.env.example` to `.env.local` and fill in your keys.

**Default AI provider — DeepSeek API:**
```bash
AI_PROVIDER=deepseek
DEEPSEEK_API_KEY=your_key_here
DEEPSEEK_MODEL=deepseek-chat
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
```

**Alternative — fully local via Ollama (no API key needed):**
```bash
AI_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434/v1
OLLAMA_MODEL=deepseek-r1:7b   # or qwen2.5:7b for lighter hardware
```

The AI engine uses the OpenAI-compatible interface — any provider that implements it works.

---

## Commit convention

```
feat: add Messenger CV upload flow
fix: correct Khmer salary parsing for ranges
docs: add self-hosting guide for Ubuntu
test: add query parser edge cases
chore: update Grammy.js to v2.4
```

---

## Code of conduct

This project serves a community that includes workers in vulnerable economic situations. Treat that with respect.

- Be direct and constructive in code review
- Assume good intent
- Khmer speakers and non-technical contributors are as valuable as senior engineers
- Decisions about cultural accuracy in Khmer UX belong to Khmer speakers, not to whoever wrote the code

---

## Recognition

All contributors are listed in [CONTRIBUTORS.md](./CONTRIBUTORS.md). Significant contributions are acknowledged in release notes.

---

*Questions? Open a GitHub Discussion. We will respond.*
