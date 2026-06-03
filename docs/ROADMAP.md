# Roadmap

## v0.1 — Telegram MVP (current)

- [x] Project scaffolding, license, contributing guide
- [x] Database schema (users, candidates, employers, searches, ratings, conversations)
- [x] CV extraction agent (text → structured profile)
- [x] Query parsing agent (NL → structured criteria)
- [x] Telegram bot — `/start`, role pick, free-text routing
- [x] Bilingual messages (Khmer + English)
- [x] Docker Compose for local + prod
- [ ] Persist extracted profile + compute embedding
- [ ] PDF and image CV input (OCR via DeepSeek vision or local Tesseract)
- [ ] Confirm/correct flow before publish

## v0.2 — Real matching + alerts

- [ ] Hybrid search: structured filters + cosine similarity on pgvector
- [ ] Search results UI with inline contact buttons
- [ ] "Save as alert" flow
- [ ] arq worker: sweep alerts every 15 min, push notifications
- [ ] Reciprocal rating after a conversation
- [ ] Conversation state in Redis (replace v0.1 heuristics)

## v0.3 — Messenger + relayed messaging

- [ ] Messenger bot (Meta Cloud API)
- [ ] Cross-channel conversation relay (employer on Telegram ↔ candidate on Messenger)
- [ ] No phone number sharing — all comms go through SrokWork
- [ ] Audit log for compliance with LPDP

## v0.4 — Khmer NLP quality

- [ ] Test set of ≥500 real Khmer + code-switched queries
- [ ] Eval harness comparing DeepSeek vs Claude vs Qwen on extraction accuracy
- [ ] Fine-tune embeddings on Khmer recruitment vocabulary
- [ ] Local Ollama setup docs for fully offline operation

## v0.5 — Progressive Web App

- [ ] `srokwork-web` repo (Next.js 14)
- [ ] Mobile-first single-search-bar UI
- [ ] PWA installable on Android home screen
- [ ] Push notifications via web push
- [ ] Same backend, no new endpoints

## v1.0

- [ ] All three channels production-ready
- [ ] Self-hosting documentation complete
- [ ] ≥1,000 published candidate profiles
- [ ] ≥200 active employers
- [ ] Public deployment at srokwork.org

## Beyond v1.0

- Voice CV intake (Telegram voice messages → Whisper → CV extraction)
- Job posting flow (currently we only match candidates to queries — adding stored job posts opens reverse search)
- Skills taxonomy specific to Cambodian labour market
- Partnerships with universities and NGOs for graduate placement
- Replication template for Laos, Myanmar, Vietnam
