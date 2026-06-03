# SrokWork — Agentic Recruitment Platform for Cambodia
## Master Strategic & Technical Document v1.0

---

# PART 1 — BUSINESS MODEL CANVAS

## Value Propositions

**For Candidates:**
- Submit a CV in 2 minutes via Telegram or Messenger — no account creation
- Be found by employers without actively searching
- Control your own profile; hide it anytime
- Rate employers and see their reputation before accepting contact
- Completely free, always

**For Employers (SMEs, NGOs, restaurants, shops):**
- Describe the candidate you want in plain Khmer, English, or Chinese — no forms, no filters
- Get ranked, verified profiles in seconds
- Save your search as an alert; get notified the instant a match appears
- Private messaging without sharing phone numbers
- Free in Phase 1; paid power features from Month 18

---

## Customer Segments

| Segment | Profile | Channel Preference |
|---|---|---|
| Urban candidates (18–35) | Factory workers, hospitality staff, office juniors | Telegram, Messenger |
| Rural/provincial candidates | Domestic work, construction, agriculture | Messenger (dominant outside Phnom Penh) |
| SME employers | Restaurants, guesthouses, shops, clinics | PWA + Telegram |
| NGO / INGO HR | Professional hiring, compliance-sensitive | PWA |
| Staffing agencies | Volume hiring, multiple clients | PWA (paid tier) |

---

## Channels

1. **PWA** — full-featured web app, installable, offline-capable
2. **Telegram Bot** (@TrovBot) — zero-install, 2.4M+ Cambodian users
3. **Messenger Bot** — dominant in provincial Cambodia, older demographics
4. **Facebook Groups** — seeding & viral growth (CV posting announcements)
5. **QR Codes** — physical: universities, pagodas, job fairs, bus stations
6. **University partnerships** — ITC, RUPP, AUPP, Zaman, Norton

---

## Customer Relationships

- **Self-service**: bots handle 90% of interactions autonomously
- **Community trust**: reciprocal ratings, verified employer badges
- **Grandfathering loyalty**: early adopters keep free access permanently
- **Telegram channel**: @TrovNews — job tips, platform updates

---

## Revenue Streams

| Tier | Price | Features | Timeline |
|---|---|---|---|
| Free | $0 | 5 searches/day, 3 alerts, basic messaging | Always |
| Starter | $29/mo | Unlimited search, 20 alerts, priority ranking | Month 18+ |
| Pro | $59/mo | All Starter + bulk export, API access, team seats | Month 18+ |
| Featured Listing | $9/post | Boosted visibility for 7 days | Month 12+ |
| Agency License | $199/mo | White-label + multi-user | Year 2+ |

**Payment rails**: ABA Pay, Wing Money, KHQR, Visa/Mastercard (via Stripe)

---

## Key Resources

- AI engine (NLP + matching)
- Candidate profile database
- Bot infrastructure (Telegram + Messenger APIs)
- Brand trust (ratings, data protection posture)
- Founding team (tech + business development)

---

## Key Activities

- Continuous AI model improvement (Khmer NLP)
- Candidate & employer acquisition
- Bot conversation design & iteration
- Community management (Facebook, Telegram)
- Compliance monitoring (LPDP readiness)

---

## Key Partnerships

- **Universities**: RUPP, ITC, AUPP, Norton, Zaman — candidate pipeline
- **NGOs**: CARE, Mith Samlanh, local women's orgs — vulnerable worker outreach
- **ABA Bank / Wing**: payment integration
- **Ministry of Labour**: compliance & credibility
- **Coworking spaces / accelerators**: Trybe, Emerald Hub — employer network

---

## Cost Structure

| Category | Monthly (Phase 1) | Monthly (Scale) |
|---|---|---|
| Cloud infra (Render/Railway + PlanetScale) | $20–40 | $200–500 |
| AI API (OpenAI/Gemini) | $15–30 | $150–400 |
| Telegram/Messenger API | Free | Free |
| Push notifications (Firebase) | Free | Free |
| Domain + SSL + email | $5 | $10 |
| **Total** | **~$60–75** | **$400–900** |

---

---

# PART 2 — DETAILED BUSINESS PLAN

## 2.1 Acquisition Strategy

### Candidate Acquisition

**Phase 1 — Telegram-first seeding (Month 1–3)**

The Telegram bot is the zero-friction entry point. A candidate needs no account, no email, no form. They message the bot, upload or describe their experience, and are profiled in 3 minutes.

Tactics:
- Post in 30+ Cambodian job Facebook groups weekly: "Submit your CV in 3 minutes on Telegram — ត្រូវការការងារ? Submit ខ្លីៗ"
- Partner with 5 universities for "digital CV day" — QR codes on campus, 20-minute demo by a campus ambassador
- Offer first 500 candidates a "Verified Profile" badge (gamification)
- Khmer-language YouTube shorts (30 seconds): "How to submit your CV via Telegram"

**Phase 2 — Messenger expansion (Month 3–6)**

Messenger penetration is higher in provinces (Siem Reap, Battambang, Kampong Cham). Mirror all bot flows to Messenger. Partner with provincial vocational training centers.

**Phase 3 — PWA organic (Month 6+)**

SEO in Khmer for "ស្វែងរកការងារ", "ការងារ Phnom Penh", "job Siem Reap". Google Ads targeting $0.05–0.15 CPC in Cambodia. Install PWA prompt shown after 2nd visit.

---

### Employer Acquisition

**Primary target**: Restaurant/hospitality owners, shop managers, NGO HR coordinators.

Tactics:
- Direct outreach to 200 restaurants/guesthouses on Google Maps in Phnom Penh + Siem Reap via Facebook DM and WhatsApp
- "Post a job free in 60 seconds" — frictionless demo
- Sponsor 3 startup/SME events (Emerald Hub, Trybe meetups) in Month 1–3
- Partner with Cambodia Chamber of Commerce for member newsletter feature
- Referral: employers who refer 3 others get Starter tier free for 3 months
- Printed A5 cards distributed at Phsar Thmei, Olympic Market, Sorya Mall: QR code to PWA

---

## 2.2 Free-to-Paid Transition Plan

### Milestone Trigger
Transition begins when ALL THREE conditions are met simultaneously:
- ≥ 1,000 active candidate profiles
- ≥ 200 regular employers (searched ≥ 2× in last 30 days)
- ≥ 50 saved active alert criteria

Expected: Month 16–20.

### Communication Sequence (6 weeks before paywall)

**Week -6**: Telegram/Messenger broadcast + email: "SrokWork is growing. We're preparing something. 🙏"

**Week -4**: Announce paid tiers with pricing. Emphasize: "If you're already using SrokWork, you keep everything you have — for free, forever."

**Week -2**: Last call for grandfathering registration. Simple one-click opt-in to lock free access.

**Week 0**: Paywall activates. Free tier limits apply to new users only.

### Grandfathering Rules
- Employers who registered before paywall: unlimited searches forever, 10 alerts (vs 3 for new free)
- Candidates: always free, no change
- Early employers invited to "Founding Member" program: their logo on the website, priority support

### Free Tier (Post-Transition)
| Feature | Limit |
|---|---|
| Natural language searches | 5/day |
| Saved alerts | 3 |
| Profile views | 10/day |
| Messaging | 3 active threads |
| CV exports | 0 (paid only) |

---

## 2.3 Financial Projections

### Assumptions
- Month 1 launch
- Employer conversion rate to paid: 15% of active employers at Month 18
- Average revenue per paying employer: $38/month (blended Starter + Pro)
- Churn: 8%/month in Year 2, 5% in Year 3
- 2 co-founders, no salaries Year 1 (sweat equity)

### Revenue Model (MRR)

| Month | Active Employers | Paying | MRR | Cumul. Revenue |
|---|---|---|---|---|
| 1–6 | 0–80 | 0 | $0 | $0 |
| 12 | 150 | 0 | $0 | $0 |
| 18 | 280 | 42 | $1,596 | $0 |
| 24 | 500 | 90 | $3,420 | $28K |
| 30 | 800 | 160 | $6,080 | $82K |
| 36 | 1,200 | 250 | $9,500 | $174K |
| 48 | 2,000 | 420 | $15,960 | $420K |
| 60 | 3,000 | 600 | $22,800 | $820K |

*Featured listings and agency licenses add ~20% on top from Year 2*

### Cost Projections

| Year | Infra | AI APIs | Salaries | Marketing | Legal/Admin | Total |
|---|---|---|---|---|---|---|
| Y1 | $900 | $400 | $0 | $3,000 | $1,500 | $5,800 |
| Y2 | $4,800 | $2,400 | $24,000 | $8,000 | $2,000 | $41,200 |
| Y3 | $9,600 | $6,000 | $48,000 | $15,000 | $3,000 | $81,600 |
| Y4 | $15,000 | $10,000 | $72,000 | $20,000 | $4,000 | $121,000 |
| Y5 | $20,000 | $14,000 | $96,000 | $25,000 | $5,000 | $160,000 |

### Break-Even Analysis

Break-even at ~120 paying employers (MRR ~$4,560 vs monthly burn ~$3,500 in Year 2).
Expected: Month 22–24.

### Initial Funding Required

| Category | Amount |
|---|---|
| 18 months infra + AI APIs | $1,500 |
| Marketing (events, ads, print) | $3,000 |
| Legal (company registration, LPDP prep) | $1,500 |
| Design + content production | $1,000 |
| Contingency | $1,000 |
| **Total Seed Required** | **$8,000** |

This is bootstrappable. Plug and Play Cambodia or similar accelerator could provide $10–25K + mentorship as an ideal first external support.

---

---

# PART 3 — TECHNICAL ARCHITECTURE

## 3.1 Stack Overview

```
┌─────────────────────────────────────────────────────┐
│                   CLIENT LAYER                       │
│  PWA (Next.js)  │  Telegram Bot  │  Messenger Bot   │
└────────────────────────┬────────────────────────────┘
                         │ HTTPS / Webhooks
┌────────────────────────▼────────────────────────────┐
│                   API GATEWAY                        │
│            Next.js API Routes / tRPC                 │
└────────────────────────┬────────────────────────────┘
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
   ┌─────────────┐ ┌──────────┐ ┌────────────┐
   │  AI Engine  │ │  Auth    │ │  Messaging │
   │  (NLP/Match)│ │  Clerk   │ │  Layer     │
   └─────────────┘ └──────────┘ └────────────┘
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
   ┌─────────────┐ ┌──────────┐ ┌────────────┐
   │  PostgreSQL  │ │  Redis   │ │  S3/R2     │
   │  (Neon.tech) │ │  (Upstash│ │  (CV files)│
   └─────────────┘ └──────────┘ └────────────┘
```

## 3.2 Technology Choices (Justified)

| Component | Tool | Why | Monthly Cost |
|---|---|---|---|
| PWA Framework | Next.js 14 (App Router) | SSR + PWA manifest + API routes in one | Free (Vercel hobby) |
| Hosting | Vercel (frontend) + Railway (backend workers) | Free tiers cover MVP | $5–15 |
| Database | Neon.tech (PostgreSQL serverless) | Free tier 0.5GB, scales pay-per-use | $0–19 |
| Cache/Queue | Upstash Redis | Serverless, free 10K req/day | $0 |
| File Storage | Cloudflare R2 | Free 10GB, no egress fees | $0 |
| Auth | Clerk.dev | Social login + phone OTP, Khmer-ready | $0 (free tier) |
| Telegram Bot | Grammy.js (Node.js) | Best Telegram bot framework, TypeScript-native | Free |
| Messenger Bot | Meta Cloud API (Node.js) | Official, free webhooks | Free |
| AI / NLP | OpenAI GPT-4o-mini | Best cost/quality for structured extraction | $15–30 |
| CV Parsing | Custom prompt + pdf-parse npm | Extract text → GPT structures it | Included above |
| Push Notifications | Firebase FCM | Free, PWA-compatible | Free |
| Email | Resend.com | 3K emails/month free | $0 |
| Search/Ranking | PostgreSQL full-text + pgvector | Semantic search without Pinecone | Included in DB |
| Monitoring | Sentry (free tier) | Error tracking | $0 |
| **TOTAL** | | | **~$35–65/month** |

## 3.3 Database Schema

```sql
-- USERS (unified across channels)
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  channel TEXT NOT NULL, -- 'pwa' | 'telegram' | 'messenger'
  channel_id TEXT, -- telegram user_id or messenger psid
  phone TEXT,
  email TEXT,
  role TEXT NOT NULL, -- 'candidate' | 'employer'
  language TEXT DEFAULT 'km', -- 'km' | 'en' | 'zh'
  verified BOOLEAN DEFAULT false,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- CANDIDATE PROFILES
CREATE TABLE candidates (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  full_name TEXT,
  full_name_km TEXT,
  location_city TEXT,
  location_province TEXT,
  skills TEXT[], -- ['cooking', 'english', 'cashier']
  experience_years INT,
  education_level TEXT,
  languages TEXT[], -- ['km', 'en', 'zh']
  desired_salary_min INT, -- USD
  desired_salary_max INT,
  job_types TEXT[], -- ['full-time', 'part-time', 'contract']
  industries TEXT[], -- ['hospitality', 'retail', 'ngo']
  availability TEXT, -- 'immediate' | 'two_weeks' | 'one_month'
  cv_file_url TEXT,
  bio_km TEXT,
  bio_en TEXT,
  embedding VECTOR(1536), -- pgvector for semantic search
  visible BOOLEAN DEFAULT true,
  rating_avg DECIMAL(3,2) DEFAULT 0,
  rating_count INT DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- EMPLOYER PROFILES
CREATE TABLE employers (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  company_name TEXT,
  company_name_km TEXT,
  industry TEXT,
  location_city TEXT,
  contact_name TEXT,
  verified BOOLEAN DEFAULT false,
  tier TEXT DEFAULT 'free', -- 'free' | 'starter' | 'pro'
  tier_expires_at TIMESTAMPTZ,
  rating_avg DECIMAL(3,2) DEFAULT 0,
  rating_count INT DEFAULT 0,
  is_founding_member BOOLEAN DEFAULT false,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- SEARCH ALERTS (saved employer queries)
CREATE TABLE alerts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  employer_id UUID REFERENCES employers(id),
  raw_query TEXT, -- original natural language
  parsed_criteria JSONB, -- {skills, location, salary_max, etc.}
  embedding VECTOR(1536),
  active BOOLEAN DEFAULT true,
  last_triggered_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- MESSAGES (cross-channel private chat)
CREATE TABLE messages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  thread_id UUID NOT NULL,
  sender_id UUID REFERENCES users(id),
  receiver_id UUID REFERENCES users(id),
  content TEXT,
  channel TEXT, -- 'pwa' | 'telegram' | 'messenger'
  read_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- RATINGS
CREATE TABLE ratings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  rater_id UUID REFERENCES users(id),
  ratee_id UUID REFERENCES users(id),
  score INT CHECK (score BETWEEN 1 AND 5),
  comment TEXT,
  context TEXT, -- 'hire' | 'interview' | 'inquiry'
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(rater_id, ratee_id, context)
);

-- SEARCH LOG (analytics + alert matching)
CREATE TABLE search_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  employer_id UUID REFERENCES employers(id),
  raw_query TEXT,
  parsed_criteria JSONB,
  results_count INT,
  channel TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

## 3.4 AI Engine Design

### CV Extraction Prompt (GPT-4o-mini)

```
System: You are a structured CV parser. Extract data from the following CV text 
(may be in Khmer, English, or mixed). Return ONLY valid JSON.

User: [raw CV text]

Expected output:
{
  "full_name": "...",
  "full_name_km": "...",
  "location_city": "Phnom Penh",
  "location_province": "Phnom Penh",
  "skills": ["cooking", "english", "customer service"],
  "experience_years": 3,
  "education_level": "high_school",
  "languages": ["km", "en"],
  "desired_salary_min": 250,
  "desired_salary_max": 400,
  "job_types": ["full-time"],
  "industries": ["hospitality"],
  "availability": "immediate",
  "bio_en": "Experienced cook with 3 years in Phnom Penh restaurants..."
}
```

### Natural Language Search Extraction

```
System: You are a recruitment search parser for Cambodia. 
Extract hiring criteria from this query. Handle Khmer, English, and mixed language.
Return ONLY valid JSON.

Examples:
"ខ្ញុំត្រូវការអ្នកធ្វើម្ហូបនៅសៀមរាប" → cook, Siem Reap
"need cashier under $300 phnom penh, can speak chinese" → cashier, Phnom Penh, max $300, Chinese speaker
"receptionist hotel bkk1" → receptionist, hospitality, Boeng Keng Kang

Input: [user query]
Output: {
  "skills": [],
  "location_city": null,
  "location_province": null,
  "salary_max": null,
  "salary_min": null,
  "languages": [],
  "experience_min": null,
  "job_type": null,
  "industries": []
}
```

### Matching Algorithm

```javascript
async function searchCandidates(criteria) {
  // Step 1: Generate embedding of the raw query
  const queryEmbedding = await openai.embeddings.create({
    model: "text-embedding-3-small",
    input: JSON.stringify(criteria)
  });

  // Step 2: Semantic similarity via pgvector (cosine)
  // Step 3: Hard filters (salary, location, availability)
  // Step 4: Boost score for: rating, profile completeness, recency
  // Step 5: Return top 10 ranked results

  const results = await db.query(`
    SELECT c.*, 
      1 - (c.embedding <=> $1) AS semantic_score,
      (c.rating_avg * 0.2 + 
       (1 - (c.embedding <=> $1)) * 0.5 +
       CASE WHEN c.availability = 'immediate' THEN 0.1 ELSE 0 END +
       LEAST(profile_completeness(c.id) / 100.0 * 0.2, 0.2)) AS final_score
    FROM candidates c
    WHERE c.visible = true
      AND ($2::int IS NULL OR c.desired_salary_max <= $2)
      AND ($3::text IS NULL OR c.location_city ILIKE $3)
    ORDER BY final_score DESC
    LIMIT 10
  `, [queryEmbedding, criteria.salary_max, criteria.location_city]);

  return results;
}
```

---

## 3.5 Bot Conversation Flows

### Telegram Bot — Candidate Onboarding

```
User: /start
Bot: 🙏 សូមស្វាគមន៍មកកាន់ SrokWork!
     Welcome to SrokWork!
     
     Are you looking for work or hiring?
     [🔍 Find a Job]  [👔 Hire Someone]

User: [taps 🔍 Find a Job]
Bot: Great! Let's build your profile in 3 minutes.
     What's your name? / តើឈ្មោះអ្នកជាអ្វី?

User: ចន្ទ័រ សុភ័ក្ត្រ
Bot: Nice to meet you, ចន្ទ័រ!
     What kind of work do you do?
     (e.g. "cook", "cashier", "driver", "security", "teacher")
     
User: I work as a cook, 4 years experience

Bot: 👍 Cook with 4 years experience.
     Which city are you in / willing to work in?
     [📍 Share Location]  or type city name

User: Siem Reap

Bot: What is your expected monthly salary (USD)?
     e.g. "300" or "250-400"

User: 300-400

Bot: Last question — do you have a CV to upload?
     [📎 Upload CV]  [Skip — I'll enter manually]

User: [uploads PDF]
Bot: ⚙️ Reading your CV... (10 seconds)
     
     ✅ Profile created!
     Name: ចន្ទ័រ សុភ័ក្ត្រ
     Skills: Cook, Kitchen Management
     Location: Siem Reap
     Salary: $300–400/month
     Experience: 4 years
     
     [✏️ Edit]  [✅ Confirm & Go Live]

User: [taps ✅ Confirm]
Bot: 🎉 You're live! Employers can now find you.
     We'll message you when someone is interested.
     
     [👁️ View My Profile]  [🔔 Notification Settings]
```

---

### Telegram Bot — Employer Search Flow

```
User: /hire
Bot: Tell me what you're looking for — in Khmer, English, or 中文.
     Example: "I need a cook in Siem Reap under $400"  /  "需要一个在金边会说中文的会计"

User: ខ្ញុំត្រូវការអ្នករក្សាការណ៍នៅ BKK1 ចេះភាសាចិន

Bot: 🔍 Searching...
     Looking for: Security guard, BKK1, Chinese speaker
     
     ─────────────────────
     👤 #1 — ដារ៉ា វិចិត្រ ⭐4.8
     📍 Phnom Penh | 💰 $300–380 | ✅ Available now
     Skills: Security, Basic Chinese, Night shift
     [View Profile]  [Message]
     ─────────────────────
     👤 #2 — Sok Chanthy ⭐4.5
     📍 Phnom Penh | 💰 $280–350 | 📅 Available in 2 weeks
     Skills: Security guard (3 yrs), Mandarin basic
     [View Profile]  [Message]
     ─────────────────────
     👤 #3 — លី ម៉េងហ័រ ⭐4.2
     📍 Phnom Penh | 💰 $320–400 | ✅ Available now
     [View Profile]  [Message]
     
     [💾 Save as Alert]  [🔄 Refine Search]

User: [taps 💾 Save as Alert]
Bot: ✅ Alert saved! I'll notify you instantly when a new matching 
     candidate appears.
     You have 2/3 alerts used (free tier).
```

---

### Messenger Bot — Simplified Flow (less technical users)

```
Bot: សួស្តី! 👋 SrokWork — រកការងារ ឬ​ជ្រើសរើសបុគ្គលិក?
     [រកការងារ]  [ជ្រើសរើស]

[If "រកការងារ" / Find Work]
Bot: ✍️ សរសេរពីខ្លួនអ្នក: ធ្វើការអ្វី? នៅទីណា? ចង់បានប្រាក់ប៉ុន្មាន?
     (Write about yourself: What work? Where? Desired salary?)

User: ខ្ញុំជាអ្នកលក់ទំនិញ នៅភ្នំពេញ ចង់បាន 250-300$

Bot: ✅ ព័ត៌មានរបស់អ្នក:
     - ការងារ: Sales / Retail
     - ទីតាំង: ភ្នំពេញ
     - ប្រាក់ខែ: $250–300
     
     ត្រឹមត្រូវទេ? [✅ ត្រូវហើយ]  [✏️ កែ]

User: [✅ ត្រូវហើយ]
Bot: 🎉 Profile របស់អ្នករួចរាល់!
     នៅពេលដែលចៅហ្វាយចាប់អារម្មណ៍ ខ្ញុំនឹងជូនដំណឹងភ្លាម។
```

---

## 3.6 PWA Wireframe Descriptions

### Screen 1 — Home / Search (Employer View)
```
┌─────────────────────────────────┐
│  🟡 SrokWork    [KM|EN]  [👤]  │
│─────────────────────────────────│
│                                 │
│  ┌─────────────────────────┐    │
│  │ 🔍 Describe who you     │    │
│  │    need...              │    │
│  │                         │    │
│  │  e.g. "Cook Siem Reap  │    │
│  │  under $400"            │    │
│  └─────────────────────────┘    │
│         [Search →]              │
│                                 │
│  ── Recent Searches ──          │
│  🕐 Security guard BKK1         │
│  🕐 Receptionist hotel english  │
│                                 │
│  ── Your Active Alerts (2) ──   │
│  🔔 Cook, Siem Reap, <$400     │
│  🔔 Driver, Phnom Penh         │
│                                 │
└─────────────────────────────────┘
```

### Screen 2 — Search Results
```
┌─────────────────────────────────┐
│  ← "cook siem reap under $400"  │
│  12 matches found               │
│─────────────────────────────────│
│  Sort: [Best Match▼] [Avail.]   │
│                                 │
│  ┌──────────────────────────┐   │
│  │ 👤  ចន្ទ័រ វ.    ⭐4.8   │   │
│  │ 📍 Siem Reap  💰$300-400 │   │
│  │ ✅ Available now          │   │
│  │ Cook · 4 yrs · KM/EN     │   │
│  │ [View]  [💬 Message]     │   │
│  └──────────────────────────┘   │
│                                 │
│  ┌──────────────────────────┐   │
│  │ 👤  Srey Mom    ⭐4.5    │   │
│  │ 📍 Siem Reap  💰$280-350 │   │
│  │ 📅 Available Jan 15       │   │
│  │ Cook · Pastry · 2 yrs    │   │
│  │ [View]  [💬 Message]     │   │
│  └──────────────────────────┘   │
│                                 │
│  [💾 Save this search as Alert] │
└─────────────────────────────────┘
```

### Screen 3 — Candidate Profile
```
┌─────────────────────────────────┐
│  ← Results                      │
│                                 │
│  👤  [avatar placeholder]        │
│  ចន្ទ័រ វិចិត្រ                   │
│  ⭐ 4.8 (12 ratings)             │
│                                 │
│  📍 Siem Reap  ✅ Available now  │
│  💰 $300 – $400/month            │
│                                 │
│  ── Skills ──                   │
│  [Cook] [Kitchen Mgmt] [Khmer]  │
│  [English Basic]                │
│                                 │
│  ── Experience ──               │
│  4 years in hotel restaurants   │
│  Angkor Village Resort (2 yrs)  │
│  La Résidence d'Angkor (2 yrs)  │
│                                 │
│  ── Languages ──                │
│  Khmer (Native) · English (B1)  │
│                                 │
│  ── Ratings ──                  │
│  "Very reliable, hardworking"   │
│  "Good attitude, clean kitchen" │
│                                 │
│  [💬 Send Message]              │
│  [⭐ Rate this candidate]       │
└─────────────────────────────────┘
```

### Screen 4 — CV Submission (Candidate)
```
┌─────────────────────────────────┐
│  Create Your Profile            │
│─────────────────────────────────│
│                                 │
│  Upload your CV (optional):     │
│  ┌──────────────────────────┐   │
│  │  📎 Drop CV here or      │   │
│  │     [Browse Files]       │   │
│  │  PDF, DOC, image OK      │   │
│  └──────────────────────────┘   │
│                                 │
│  — OR fill in manually —        │
│                                 │
│  Full Name:  [_____________]    │
│  City:       [Phnom Penh ▼]     │
│  Skills:     [Add skills +]     │
│  Experience: [__ years]         │
│  Salary:     [$___ to $___]     │
│  Languages:  [KM✓] [EN] [ZH]   │
│  Available:  [Immediately ▼]    │
│                                 │
│  [🚀 Create My Profile]         │
└─────────────────────────────────┘
```

---

## 3.7 Alert & Notification Engine

```javascript
// Runs every time a new candidate profile is created or updated
async function triggerAlertMatching(candidateId) {
  const candidate = await getCandidateWithEmbedding(candidateId);
  
  // Find all active alerts with semantic similarity > 0.75
  const matchingAlerts = await db.query(`
    SELECT a.*, e.user_id, u.channel, u.channel_id
    FROM alerts a
    JOIN employers e ON a.employer_id = e.id
    JOIN users u ON e.user_id = u.id
    WHERE a.active = true
      AND 1 - (a.embedding <=> $1) > 0.75
      AND (a.parsed_criteria->>'salary_max' IS NULL 
           OR $2 <= (a.parsed_criteria->>'salary_max')::int)
      AND (a.parsed_criteria->>'location_city' IS NULL 
           OR $3 ILIKE a.parsed_criteria->>'location_city')
  `, [candidate.embedding, candidate.desired_salary_max, candidate.location_city]);

  for (const alert of matchingAlerts) {
    await sendNotification(alert, candidate);
    await updateAlertLastTriggered(alert.id);
  }
}

async function sendNotification(alert, candidate) {
  switch(alert.channel) {
    case 'telegram':
      await telegramBot.sendMessage(alert.channel_id, 
        formatCandidateCard(candidate));
      break;
    case 'messenger':
      await messengerBot.sendMessage(alert.channel_id,
        formatCandidateCard(candidate));
      break;
    case 'pwa':
      await firebase.sendPushNotification(alert.user_id,
        { title: 'New Match!', body: `${candidate.full_name} — ${candidate.location_city}` });
      break;
  }
}
```

---

---

# PART 4 — 18-MONTH OPERATIONAL ROADMAP

## Month 1–2: Foundation

**Tech**
- [ ] Register company (Cambodia MoC, ~$300)
- [ ] Set up Neon DB, Vercel, Railway, Cloudflare R2
- [ ] Build core Next.js PWA: home, search, CV upload, profile view
- [ ] Build Telegram bot (Grammy.js): /start, CV flow, search flow
- [ ] Integrate OpenAI GPT-4o-mini for CV parsing + query parsing
- [ ] Implement pgvector semantic search
- [ ] Set up Firebase FCM push notifications

**Business**
- [ ] Create @TrovBot on Telegram + SrokWork page on Facebook
- [ ] Outreach to 5 universities for partnership MOU
- [ ] Design QR code cards (500 copies printed, ~$30)
- [ ] Begin daily posting in 20 Facebook job groups

**KPIs**: 50 candidate profiles, 10 employers tested

---

## Month 3–4: Messenger + Content

**Tech**
- [ ] Build Messenger bot (Meta Cloud API): mirror Telegram flows
- [ ] Implement cross-channel private messaging relay
- [ ] Build rating system (both directions)
- [ ] Add alert creation + basic notification dispatch

**Business**
- [ ] Launch on Messenger (Facebook page bot)
- [ ] 2 university events (QR code CV submission day)
- [ ] First employer case study published (restaurant in Phnom Penh)
- [ ] Khmer-language YouTube channel: 4 tutorial videos

**KPIs**: 200 candidates, 40 employers, 5 successful hires tracked

---

## Month 5–6: Quality & Trust

**Tech**
- [ ] Implement verified employer badge (manual verification + email)
- [ ] Build admin dashboard (internal) for moderation
- [ ] Implement profile completeness scoring
- [ ] A/B test bot conversation flows (measure drop-off)
- [ ] LPDP compliance audit: data retention policy, consent flows

**Business**
- [ ] Launch "Founding Employer" badge program
- [ ] Press release to Khmer Times, Phnom Penh Post
- [ ] First cohort of 10 employers on referral program
- [ ] NGO outreach: CARE, Mith Samlanh

**KPIs**: 400 candidates, 80 employers, 15 active alerts

---

## Month 7–9: Scale Acquisition

**Tech**
- [ ] SEO optimization: Khmer + English + Chinese keywords
- [ ] PWA install prompt A/B testing
- [ ] Improve Khmer NLP: fine-tune prompt with 500 real query examples
- [ ] Implement duplicate profile detection
- [ ] Province expansion: Siem Reap-specific location features

**Business**
- [ ] Siem Reap expansion: 2 campus ambassador hires ($50/month each)
- [ ] Google Ads campaign: $200 budget over 3 months
- [ ] Attend 2 business events (Emerald Hub, CCIFCC)
- [ ] Begin tracking employer NPS monthly

**KPIs**: 600 candidates, 130 employers, 30 active alerts, NPS >40

---

## Month 10–12: Pre-Monetization Preparation

**Tech**
- [ ] Build subscription payment system (ABA Pay + Stripe)
- [ ] Implement tier-gating logic (limits, paywalls)
- [ ] Build employer dashboard: saved searches, match history, analytics
- [ ] Build "Founding Member" grandfathering registration flow
- [ ] Load testing + performance optimization

**Business**
- [ ] Featured listing product soft-launch ($9/post)
- [ ] Begin announcing upcoming paid tiers (transparency-first)
- [ ] Document and publish privacy policy (LPDP-ready)
- [ ] Identify top 50 most-active employers for VIP outreach

**KPIs**: 800 candidates, 180 employers, 45 alerts, 5 paid featured listings

---

## Month 13–15: Critical Mass & Monetization Readiness

**Tech**
- [ ] Finalize paid tier feature set
- [ ] Implement ABA Pay / Wing Money subscription billing
- [ ] Build employer analytics dashboard (search performance, response rates)
- [ ] Mobile app consideration: PWA vs React Native assessment

**Business**
- [ ] Monitor trigger metrics daily (1K candidates, 200 employers, 50 alerts)
- [ ] Run founding member registration campaign
- [ ] Train 2 customer success volunteers (university interns)

**KPIs**: 1,000 candidates, 200 employers, 50 alerts → TRIGGER MET

---

## Month 16–18: Monetization Launch

**Tech**
- [ ] Activate paywall for new users
- [ ] Grandfather all qualifying early employers automatically
- [ ] Launch $29 Starter + $59 Pro tiers
- [ ] Implement churn prevention: in-app downgrade warnings, pause option

**Business**
- [ ] 6-week communication campaign (see transition plan above)
- [ ] Press coverage: "Cambodia's first AI recruitment platform goes pro"
- [ ] Apply to Plug and Play Cambodia Demo Day
- [ ] First financial reporting: MRR, CAC, churn, NPS

**KPIs**: 30+ paying employers, MRR > $1,000, churn < 12%

---

---

# PART 5 — RISK ANALYSIS & MITIGATION

## Risk Matrix

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| Low candidate adoption | Medium | Critical | Bot-first UX, zero friction, Facebook seeding |
| Khmer NLP failures | High | High | Human fallback, continuous prompt iteration, user correction UI |
| Facebook/Meta bot policy changes | Medium | High | Telegram-first strategy; Messenger is secondary |
| Telegram API changes | Low | Medium | All data in own DB; bots are just notification layer |
| Data breach / LPDP non-compliance | Low | Critical | Encrypt PII, GDPR-style consent, minimal data collection |
| Employer unwillingness to pay | Medium | High | Long free phase, grandfathering, ROI communication |
| Competitor enters (BongThom adds AI) | Medium | Medium | Network effects + rating trust moat; move fast |
| Fake profiles / spam | High | Medium | Phone OTP verification, employer can flag, admin review queue |
| Key person risk (solo founder tech) | High | High | Document everything, modular codebase, hire intern early |
| Currency / payment friction | Medium | Medium | ABA (most used), Wing (rural), Stripe fallback |

## Critical Mitigations

**Khmer NLP quality**: Keep a human-readable log of all failed parses. Review weekly. Build a corrections dataset. After 3 months, fine-tune a local prompt library with 200+ real Cambodian job query examples. Consider partnering with RUPP linguistics department.

**Trust & safety**: Every profile linked to a phone number (OTP). Employers can report profiles. Candidates can report employers. A community moderator (volunteer in Month 1–6, paid in Year 2) reviews flags within 24 hours.

**LPDP compliance**: Cambodia's LPDP is imminent. Build consent flows from Day 1. Store only what's necessary. Give users data export and deletion rights via /mydata command in bots. Appoint a data officer (can be a founder initially).

**Competitive moat**: The rating system creates lock-in — employers and candidates build reputation over time that can't be migrated. This is the most defensible asset.

---

# ACTIONABLE KPI DASHBOARD

## Monthly KPIs to Track

| Metric | Target M6 | Target M12 | Target M18 |
|---|---|---|---|
| Active candidate profiles | 400 | 800 | 1,500 |
| Employers who searched ≥2× in 30 days | 80 | 180 | 350 |
| Active saved alerts | 15 | 45 | 100 |
| Successful hires tracked | 10 | 40 | 120 |
| Bot conversation completion rate | >60% | >70% | >75% |
| Profile completeness score avg | >60% | >70% | >75% |
| Employer NPS | >30 | >40 | >45 |
| Monthly search queries | 200 | 800 | 2,500 |
| Rating entries | 20 | 150 | 500 |
| MRR | $0 | $0 | $1,500+ |
| Infra cost | <$75 | <$80 | <$200 |

---

*Document version 1.0 — SrokWork Master Plan*
*Prepared for: Alex | SrokWork*
*May 2026*
