# TROV — Developer Specification v1.0

**Phase 0 : Telegram Bot + Matching NLP + Rating System**
**Date : 2026-05-23 | Status : BUILD (post-Critic RESHAPE→BUILD)**

---

## Table des matières

1. [Architecture Overview](#1-architecture-overview)
2. [Phase 0 Scope Boundary](#2-phase-0-scope-boundary)
3. [Telegram Bot Conversation Flows](#3-telegram-bot-conversation-flows)
4. [Rating System Design](#4-rating-system-design)
5. [DeepSeek Prompt Contracts](#5-deepseek-prompt-contracts)
6. [Database Schema](#6-database-schema)
7. [API Endpoints](#7-api-endpoints)
8. [n8n Orchestration](#8-n8n-orchestration)
10. [Deployment](#10-deployment)
11. [Migration from SrokWork](#11-migration-from-srokwork)
12. [FLAGS & Open Questions](#12-flags--open-questions)

---

## 1. Architecture Overview

```
┌──────────────────────────────────────────────────────────────┐
│                        PHASE 0                                │
│                                                               │
│  ┌──────────────┐     HTTP/REST      ┌──────────────────┐   │
│  │  Telegram    │───────────────────▶│  FastAPI Backend  │   │
│  │  Bot         │                    │  (Python 3.12)   │   │
│  │  (Grammy.js) │◀───────────────────│  Port 8000       │   │
│  │  Node.js/TS  │     JSON           │                  │   │
│  └──────────────┘                    │  ┌────────────┐  │   │
│                                      │  │ Agents     │  │   │
│                                      │  │ (PydanticAI)│  │   │
│                                      │  └─────┬──────┘  │   │
│                                      │        │          │   │
│  ┌──────────────┐                    │  ┌─────▼──────┐  │   │
│  │  n8n         │───────────────────▶│  │ Services   │  │   │
│  │  (orchestra- │                    │  └─────┬──────┘  │   │
│  │   tion)      │                    │        │          │   │
│  └──────┬───────┘                    │  ┌─────▼──────┐  │   │
│         │                            │  │ DB (SQLAl- │  │   │
│         │                            │  │ chemy 2.0) │  │   │
│         │                            │  └─────┬──────┘  │   │
│         │                            └────────┼─────────┘   │
│         │                                     │              │
│         │         ┌───────────────────────────┼──────┐      │
│         └────────▶│  PostgreSQL 16 + pgvector │      │      │
│                   │  Redis                    │      │      │
│                   └──────────────┬────────────┘      │      │
│                                  │                    │      │
│                   ┌──────────────▼────────────┐      │      │
│                   │  DeepSeek API             │      │      │
│                   │  (deepseek-chat +          │      │      │
│                   │   text-embedding-3-small)  │      │      │
│                   └───────────────────────────┘      │      │
└──────────────────────────────────────────────────────────────┘
```

### Pourquoi Grammy.js pour le bot Telegram (et pas python-telegram-bot)

Le brief prescrit Grammy.js en Phase 0. Justification technique :

- **Conversation state machine native** : Grammy.js a un système de sessions (`conversations`) intégré, supérieur au state management manuel de python-telegram-bot
- **Middleware pipeline** : injection de `ctx.session`, i18n, logging — plus propre
- **Séparation des concerns** : le bot Node.js est un *thin interaction layer*. Tout le travail lourd (LLM, DB, matching) reste dans le backend Python FastAPI. Le bot ne fait que du routing de messages et du formatting UI Telegram
- **Coût de migration acceptable** : le code bot existant (~250 lignes) est le plus petit module de SrokWork. Les agents Python (`cv_extraction.py`, `query_parsing.py`), le schéma DB, et les services sont intégralement conservés

### Stack finale Phase 0

| Layer | Technology | Rationale |
|---|---|---|
| Bot Telegram | Grammy.js (Node 22, TypeScript) | Prescrit. Sessions, middleware, i18n natif |
| API Backend | FastAPI (Python 3.12) | Agents PydanticAI, SQLAlchemy async, écosystème NLP Python |
| LLM | DeepSeek V3 (`deepseek-chat`) | Moins cher pour le bilinguisme KM/EN. Swappable |
| Embeddings | `text-embedding-3-small` (OpenAI) ou `deepseek-embedding` | 1536 dimensions |
| Database | PostgreSQL 16 + pgvector | Une seule DB, pas de vector store séparé |
| Cache / Sessions | Redis | Session state bot + cache matching |

| Container | Docker Compose | 4 services : api, bot, postgres, redis (n8n séparé) |

---

## 2. Phase 0 Scope Boundary

### ✅ IN SCOPE (Phase 0 — 60 jours)

| Feature | Description |
|---|---|
| Telegram bot — candidate onboarding | `/start` → role pick → CV input (text) → AI extraction → confirm/edit → publish |
| Telegram bot — employer search | `/start` → role pick → NL query → AI parsing → hybrid search → results cards |
| CV extraction agent | DeepSeek : texte brut Khmer/EN/mixte → `ExtractedCV` structuré |
| Query parsing agent | DeepSeek : requête NL Khmer/EN/mixte → `ParsedQuery` structuré |
| Hybrid search | Filtres structurés (location, salaire, skills) + cosine similarity pgvector |
| Embedding computation | Candidate profiles → embedding via API → stockage pgvector |
| **Rating system — full** | Star score + catégories structurées + vérification interaction + bidirectionnel asymétrique + immuable (voir §4) |
| Profile confirmation flow | Candidate review → accept/edit → publish |
| Save search as alert | Employer peut sauvegarder une recherche. n8n sweep toutes les 15 min |
| i18n KM/EN | Tous les messages bot en Khmer et Anglais |


### ❌ OUT OF SCOPE (Phase 1+)

| Feature | Target Phase |
|---|---|
| Messenger bot | Phase 1 (v0.3) |
| PWA / SrokWork-web | Phase 1 (v0.5) |
| PDF/Image CV parsing (OCR) | Phase 1 |
| Voice CV intake (Whisper) | Phase 1 |
| Cross-channel relayed messaging | Phase 1 |
| Khmer NLP fine-tuning | Phase 1 (v0.4) |
| Job posting flow (reverse search) | Phase 1 |
| Admin dashboard | Phase 1 |
| Self-hosting documentation | Phase 1 |

---

## 3. Telegram Bot Conversation Flows

### 3.1 Candidate Onboarding Flow

```
┌─────────┐    ┌──────────┐    ┌───────────┐    ┌──────────┐    ┌──────────┐
│ /start  │───▶│ ask_role │───▶│ candidate │───▶│ cv_input │───▶│ extract  │
│ welcome │    │ inline   │    │ welcome   │    │ free text │    │ AI call  │
└─────────┘    │ keyboard │    │ prompt    │    │ (KM/EN)   │    │ (POST    │
               └──────────┘    └───────────┘    └──────────┘    │ /agents  │
                                                     │         │ /cv)     │
                                                     │         └────┬─────┘
                                                     │              │
                                                     ▼              ▼
                                              ┌──────────┐  ┌──────────┐
                                              │ confirm  │◀─│ extracted│
                                              │ "Is this │  │ profile  │
                                              │  right?" │  │ preview  │
                                              └────┬─────┘  └──────────┘
                                                   │
                                          ┌────────┼────────┐
                                          ▼        ▼        ▼
                                     ┌──────┐ ┌──────┐ ┌──────┐
                                     │  ✅  │ │ edit │ │  ❌  │
                                     │confirm│ │correc-│ │cancel│
                                     └──┬───┘ │tions  │ └──┬───┘
                                        │     └──┬───┘    │
                                        ▼        ▼        ▼
                                   ┌────────┐ ┌──────┐ ┌──────┐
                                   │PUBLISH │ │re-   │ │delete│
                                   │profile │ │extract│ │draft │
                                   │+embed  │ │      │ │      │
                                   └────────┘ └──────┘ └──────┘
```

**États de session (Redis) :**

```typescript
// Grammy.js session state
interface CandidateSession {
  step: 'idle' | 'awaiting_cv' | 'confirming_cv' | 'editing_cv';
  draftCv: ExtractedCV | null;  // latest AI extraction
  retryCount: number;           // max 3 extraction attempts
}
```

**Messages clés (bilingues) :**

| Étape | KM | EN |
|---|---|---|
| ask_role | "តើអ្នកកំពុងស្វែងរកការងារ ឬកំពុងជ្រើសរើសបុគ្គលិក?" | "Are you looking for work, or hiring?" |
| cv_input | "ផ្ញើប្រវត្តិរូបរបស់អ្នកមកខ្ញុំ — សរសេរអំពីបទពិសោធន៍ ជំនាញ និងទីតាំងរបស់អ្នក" | "Tell me about your experience, skills, and where you're based — in Khmer or English" |
| cv_extracted | "នេះជាអ្វីដែលខ្ញុំយល់៖ [profile]. ត្រឹមត្រូវទេ?" | "Here's what I understood: [profile]. Is this right?" |
| cv_published | "ប្រវត្តិរូបរបស់អ្នកបានផ្សាយហើយ ✨" | "Your profile is live ✨" |

### 3.2 Employer Search Flow

```
┌─────────┐    ┌──────────┐    ┌───────────┐    ┌──────────┐    ┌──────────┐
│ /start  │───▶│ ask_role │───▶│ employer  │───▶│ search   │───▶│ parse    │
│ welcome │    │ inline   │    │ welcome   │    │ NL query │    │ AI call  │
└─────────┘    │ keyboard │    │ prompt    │    │ (KM/EN)  │    │ (POST    │
               └──────────┘    └───────────┘    └──────────┘    │ /agents  │
                                                                 │ /query)  │
                                                                 └────┬─────┘
                                                                      │
                                                                      ▼
                                                               ┌──────────┐
                                                               │ hybrid   │
                                                               │ search   │
                                                               │ (PG      │
                                                               │ filters  │
                                                               │ + vector)│
                                                               └────┬─────┘
                                                                    │
                                                         ┌──────────┼──────────┐
                                                         ▼          ▼          ▼
                                                    ┌────────┐ ┌──────┐  ┌────────┐
                                                    │results │ │ 0    │  │ error  │
                                                    │ cards  │ │matches│  │        │
                                                    │ (top N)│ └──┬───┘  └────────┘
                                                    └───┬────┘    │
                                                        │         ▼
                                          ┌─────────────┤    ┌──────────┐
                                          ▼             │    │ "Save as │
                                    ┌──────────┐        │    │ alert?"  │
                                    │ "Contact"│        │    │ → n8n    │
                                    │ button   │        │    │ workflow │
                                    │ starts   │        │    └──────────┘
                                    │ conversa-│
                                    │ tion     │
                                    └──────────┘
```

**Format des résultats de recherche (inline keyboard) :**

```
🔍 Résultats pour "អ្នកធ្វើម្ហូប សៀមរាប ក្រោម $400" :

1. សុខ ម៉ាលី — Cook, 5 ans, Siem Reap 🇰🇭
   💰 $350/mois | ⭐ 4.8 (12 ratings)
   [📩 Contacter] [📋 Voir profil]

2. ជា ដារ៉ា — Cook, 3 ans, Siem Reap 🇰🇭
   💰 $280/mois | ⭐ 4.2 (5 ratings)
   [📩 Contacter] [📋 Voir profil]

3. ...

🔔 [Sauvegarder comme alerte]
🔄 [Nouvelle recherche]
```

### 3.3 Rating Flow (post-interaction)

```
┌──────────────┐
│ Conversation │  (employer ↔ candidate, relayed via bot)
│  ended       │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Bot prompts  │  "How was your experience with [name]?"
│ BOTH parties │  → Only if conversation had ≥ 2 messages each side
└──────┬───────┘
       │
       ▼
┌──────────────────────────────────────────────┐
│ Rating UI (inline keyboard)                   │
│                                               │
│ ⭐ Overall: [1] [2] [3] [4] [5]              │
│                                               │
│ For CANDIDATE rating employer:                │
│ □ Paid on time?      [Yes] [No]              │
│ □ Conditions matched listing? [Yes] [No]      │
│ □ Communication clear? [Yes] [No]             │
│                                               │
│ For EMPLOYER rating candidate:                │
│ □ Showed up on time?  [Yes] [No]              │
│ □ Skills matched profile? [Yes] [No]          │
│ □ Professional conduct? [Yes] [No]             │
└──────────────────────────────────────────────┘
       │
       ▼
┌──────────────┐
│ Rating saved │  → DB: ratings table
│ (immutable)  │  → Recalculate rating_avg, rating_count
└──────────────┘
```

---

## 4. Rating System Design

**⚠️ CECI EST LE MOAT. La spécification ci-dessous est la partie la plus importante du système. Une implémentation générique "5 étoiles + commentaire" détruit tout l'avantage compétitif.**

### 4.1 Principes de gouvernance (codifiés en base et dans le code)

| # | Principe | Implémentation |
|---|---|---|
| R1 | **Structuré, pas texte libre** | Score 1-5 + 3 catégories binaires (oui/non). Jamais de champ texte libre. |
| R2 | **Lié à une interaction vérifiée** | On ne peut noter que quelqu'un avec qui on a échangé ≥ 2 messages de chaque côté dans une conversation sur la plateforme. |
| R3 | **Bidirectionnel asymétrique** | Les deux parties se notent, mais les candidats ont des catégories différentes de celles des employeurs. Protection accrue des candidats. |
| R4 | **Immuable / non-achetable** | Un rating ne peut jamais être modifié ou supprimé, sauf par un processus de gouvernance communautaire (vote des mainteneurs). Aucune API de suppression. |
| R5 | **Les ratings alimentent le classement** | `rating_avg` et `rating_count` sont des facteurs de boosted ranking dans la recherche hybride. |
| R6 | **Cold-start transparent** | Un profil sans rating affiche "Nouveau — pas encore évalué" (pas 0 étoiles). Pas de pénalité pour les nouveaux entrants. |

### 4.2 Modèle de données

```sql
-- Table ratings (remplace le modèle simplifié existant)
CREATE TABLE ratings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID NOT NULL REFERENCES conversations(id),
    
    -- Who rates whom
    rater_user_id UUID NOT NULL REFERENCES users(id),
    rated_user_id UUID NOT NULL REFERENCES users(id),
    rater_role VARCHAR(16) NOT NULL CHECK (rater_role IN ('candidate', 'employer')),
    
    -- Score principal (1-5)
    score INTEGER NOT NULL CHECK (score >= 1 AND score <= 5),
    
    -- Catégories structurées (dépendent du rôle de l'évaluateur)
    -- NULL si la catégorie n'est pas applicable au rôle
    category_paid_on_time BOOLEAN,          -- candidat → employeur
    category_conditions_match BOOLEAN,       -- candidat → employeur
    category_communication BOOLEAN,          -- candidat → employeur
    category_showed_up BOOLEAN,              -- employeur → candidat
    category_skills_match BOOLEAN,           -- employeur → candidat
    category_professional BOOLEAN,           -- employeur → candidat
    
    -- Métadonnées
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    
    -- Contrainte : un seul rating par conversation par évaluateur
    UNIQUE(conversation_id, rater_user_id)
);

-- Index pour le calcul rapide des moyennes
CREATE INDEX idx_ratings_rated_user ON ratings(rated_user_id);
CREATE INDEX idx_ratings_conversation ON ratings(conversation_id);
```

### 4.3 Catégories structurées — justification anti-défamation

Le droit cambodgien (comme la plupart des juridictions d'Asie du Sud-Est) a des lois de diffamation larges. Un champ "commentaire libre" expose Trov à :

- Des plaintes pour diffamation si un employeur écrit "ce candidat est un voleur"
- Des pressions pour supprimer des avis négatifs
- Une modération impossible à scale

**Solution :** Pas de texte libre. Uniquement des scores + cases à cocher binaires. C'est :

- **Défendable juridiquement** : ce sont des faits structurés, pas des opinions
- **Automatisable** : pas de modération humaine nécessaire
- **Utile** : les catégories sont exactement ce qu'un futur employeur veut savoir

### 4.4 Vérification d'interaction (anti-fraude)

```python
# services/ratings.py

async def can_rate(conversation_id: UUID, rater_user_id: UUID) -> bool:
    """
    Un utilisateur ne peut noter que s'il a eu une vraie interaction.
    Critères :
    1. La conversation existe entre les deux parties
    2. Chaque partie a envoyé ≥ 2 messages
    3. La conversation a au moins 24h (évite les ratings instantanés frauduleux)
    """
    result = await db.execute(
        select(
            func.count(Message.id).filter(Message.sender_user_id == rater_user_id).label("from_rater"),
            func.count(Message.id).filter(Message.sender_user_id != rater_user_id).label("from_rated"),
            func.min(Message.created_at).label("first_msg"),
        )
        .where(Message.conversation_id == conversation_id)
        .group_by(Message.conversation_id)
    )
    row = result.one_or_none()
    if not row:
        return False
    
    hours_elapsed = (datetime.utcnow() - row.first_msg).total_seconds() / 3600
    return (
        row.from_rater >= 2
        and row.from_rated >= 2
        and hours_elapsed >= 24
    )
```

### 4.5 Calcul du score agrégé

```python
# services/ratings.py

async def recalculate_rating(user_id: UUID, role: str) -> None:
    """
    Recalcule rating_avg et rating_count après chaque nouveau rating.
    
    - Candidat : moyenne de tous les ratings reçus des employeurs
    - Employeur : moyenne de tous les ratings reçus des candidats
    
    La moyenne est pondérée par la récence (décroissance exponentielle, demi-vie 90 jours)
    pour que les ratings récents pèsent plus que les anciens. Cela permet aux travailleurs
    de se racheter et aux employeurs de s'améliorer.
    """
    HALF_LIFE_DAYS = 90
    decay_factor = math.log(2) / HALF_LIFE_DAYS
    
    ratings = await db.execute(
        select(Rating.score, Rating.created_at)
        .where(Rating.rated_user_id == user_id)
        .order_by(Rating.created_at.desc())
    )
    
    total_weight = 0.0
    weighted_sum = 0.0
    
    for score, created_at in ratings:
        days_ago = (datetime.utcnow() - created_at).days
        weight = math.exp(-decay_factor * days_ago)
        weighted_sum += score * weight
        total_weight += weight
    
    avg = weighted_sum / total_weight if total_weight > 0 else 0.0
    count = len(ratings)
    
    # Update candidate_profiles ou employer_profiles
    if role == "candidate":
        await db.execute(
            update(CandidateProfile)
            .where(CandidateProfile.user_id == user_id)
            .values(rating_avg=avg, rating_count=count)
        )
    else:
        await db.execute(
            update(EmployerProfile)
            .where(EmployerProfile.user_id == user_id)
            .values(rating_avg=avg, rating_count=count)
        )
```

### 4.6 Cold-start bootstrap

**Problème :** J1 = 0 ratings. Comment rendre le système crédible ?

**Stratégie :**

1. **Affichage transparent** : un profil sans rating montre « Nouveau — pas encore évalué » (pas 0⭐)
2. **Boost de visibilité pour les nouveaux** : les profils non évalués apparaissent aléatoirement dans le top 20% des résultats pour éviter le "winner-takes-all" des early raters
3. **Focus vertical prioritaire** : concentrer le déploiement initial sur 3 verticales (hospitality/restauration, retail/commerce, services) pour que les ratings s'accumulent visiblement vite dans chaque communauté
4. **Seed par validation institutionnelle (Phase 1)** : partenariat avec des associations d'employeurs connues pour "vérifier" les premiers employeurs — badge "Employeur Vérifié" distinct des ratings

### 4.7 Immuabilité — implémentation

```python
# API : AUCUN endpoint DELETE/PATCH pour les ratings
# La seule opération est CREATE

# api/routes/ratings.py
@router.post("/ratings", status_code=201)
async def create_rating(rating: RatingCreate, user_id: UUID = Depends(get_current_user)):
    """
    Crée un rating. Aucune modification ou suppression possible.
    
    Seul un processus de gouvernance hors-bande (vote des mainteneurs)
    peut supprimer un rating frauduleux — via accès direct à la DB,
    pas via l'API.
    """
    # ... validation + insert
```

```sql
-- Révocation des privilèges de modification sur la table ratings
-- (exécuté par Alembic migration)
REVOKE UPDATE, DELETE ON ratings FROM srokwork;
-- Seul le superuser PostgreSQL peut modifier
```

### 4.8 Impact sur le search ranking

Le score final d'un candidat dans les résultats de recherche est :

```
score_final = 0.60 × cosine_similarity(query_embedding, profile_embedding)
            + 0.25 × normalized_rating_score
            + 0.15 × recency_boost

normalized_rating_score = 
    si rating_count == 0 → 0.5  (neutral, ni pénalisé ni boosté)
    sinon → (rating_avg / 5.0) × min(1.0, rating_count / 10)
    # La confiance augmente avec le nombre de ratings, plafonne à 10

recency_boost = 1.0 / (1 + days_since_created / 30)
    # Les profils récents ont un léger boost, décroissance sur 30 jours
```

---

## 5. DeepSeek Prompt Contracts

### 5.1 CV Extraction Agent

**Endpoint :** `POST /agents/cv/extract`
**Model :** `deepseek-chat` (DeepSeek V3)
**Temperature :** 0.0 (déterministe — structuré)

```json
// REQUEST
{
  "raw_text": "ខ្ញុំឈ្មោះ សុខ ម៉ាលី អាយុ 28 ឆ្នាំ នៅសៀមរាប។ ខ្ញុំធ្វើជាចុងភៅ 5 ឆ្នាំ ជំនាញខ្មែរ និងថៃ។ ចេះភាសាអង់គ្លេសបន្តិច។ ចង់បានប្រាក់ខែ 350$។",
  "language_hint": "km"
}

// RESPONSE
{
  "full_name": "សុខ ម៉ាលី",
  "headline": "Cook, 5 years experience, Siem Reap",
  "location": "Siem Reap",
  "skills": ["Khmer cooking", "Thai cooking"],
  "languages": ["Khmer", "English (basic)"],
  "years_experience": 5,
  "desired_salary_usd": 350,
  "summary": "ចុងភៅជំនាញខ្មែរ និងថៃ មានបទពិសោធន៍ ៥ ឆ្នាំ នៅសៀមរាប។ ស្វែងរកការងារក្នុងតម្លៃ $350/ខែ។ Skilled in both Khmer and Thai cuisine with basic English."
}
```

**System Prompt (inchangé — validé par le code existant) :**

```
You are a CV extraction assistant for Trov, a recruitment platform for Cambodia.
Your job: read raw CV text and extract structured fields.
CRITICAL CONTEXT:
- Input may be Khmer, English, or code-switched. Both are normal.
- The candidate is typically a Cambodian worker: cook, driver, security guard,
  receptionist, salesperson, teacher, accountant, NGO staff, etc.
- Salaries are usually USD/month in Cambodia (50-2000 range).
  If you see KHR, convert at ~4100 KHR = 1 USD.
- Locations: use English names (Phnom Penh, Siem Reap, etc.)
- Skills should be concrete and short.
- If a field is genuinely missing, return null — do NOT guess.
- Summary: 2-3 sentences, bilingual if the source was.
```

### 5.2 Query Parsing Agent

**Endpoint :** `POST /agents/query/parse`
**Model :** `deepseek-chat`
**Temperature :** 0.0

```json
// REQUEST
{
  "raw_query": "ខ្ញុំត្រូវការអ្នកបើកឡានក្រុងនៅភ្នំពេញ ចេះភាសាអង់គ្លេស ប្រាក់ខែក្រោម 500 ដុល្លារ",
  "language_hint": "km"
}

// RESPONSE
{
  "role": "bus driver",
  "location": "Phnom Penh",
  "max_salary_usd": 500,
  "required_skills": [],
  "required_languages": ["English"],
  "min_experience": null
}
```

```python
# tests/test_parsing_khmer.py
# Ce fichier DOIT exister et être exécuté par n8n à J60

KHMER_TEST_QUERIES = [
    # (query, expected_role, expected_location)
    ("ខ្ញុំត្រូវការអ្នកធ្វើម្ហូបនៅសៀមរាប", "cook", "Siem Reap"),
    ("ត្រូវការបុគ្គលិកលក់នៅភ្នំពេញ ៣០០ដុល្លារ", "sales staff", "Phnom Penh"),
    ("រកអ្នកបើកឡាន នៅបាត់ដំបង", "driver", "Battambang"),
    ("ត្រូវការសន្តិសុខ ភ្នំពេញ ក្រោម ៤០០$", "security guard", "Phnom Penh"),
    ("ខ្ញុំចង់បានអ្នកធ្វើម្ហូបនៅកំពត", "cook", "Kampot"),
    ("រកគ្រូបង្រៀនភាសាអង់គ្លេស នៅសៀមរាប", "english teacher", "Siem Reap"),
    ("ហាងត្រូវការអ្នកគិតលុយ ភ្នំពេញ", "cashier", "Phnom Penh"),
    ("ត្រូវការបុគ្គលិកសំអាត នៅព្រលានយន្តហោះភ្នំពេញ", "cleaner", "Phnom Penh"),
    ("រកអ្នករត់តុ ភ្នំពេញ ចេះអង់គ្លេស", "waiter", "Phnom Penh"),
    ("ត្រូវការជាងសក់ នៅសៀមរាប", "hairdresser", "Siem Reap"),
    # Edge cases — informal/code-switched
    ("need cook siem reap cheap", "cook", "Siem Reap"),
    ("រកអ្នក delivery នៅភ្នំពេញ មានម៉ូតូ", "delivery driver", "Phnom Penh"),
    ("ត្រូវការ barista នៅផ្សារទំនើបក្នុងភ្នំពេញ", "barista", "Phnom Penh"),
    ("construction worker needed phnom penh", "construction worker", "Phnom Penh"),
    ("រកអ្នកថែទាំសួន ភ្នំពេញ", "gardener", "Phnom Penh"),
    ("ត្រូវការអ្នកបើកម៉ូតូឌុប ស្គាល់ផ្លូវភ្នំពេញ", "motorbike taxi driver", "Phnom Penh"),
    ("រកនារីរត់តុ សៀមរាប មានបទពិសោធ", "waitress", "Siem Reap"),
    ("cari tukang masak khmer di phnom penh murah", "cook", "Phnom Penh"),  # Malay/Khmer-influenced
    ("need nanny phnom penh english speaking", "nanny", "Phnom Penh"),
]


# n'extraient pas le bon role AND location
```

---

## 6. Database Schema

### 6.1 Diagramme Entité-Relation

```
users (id, telegram_id, messenger_id, phone, display_name,
       preferred_language, primary_channel, created_at, last_seen_at)
  │
  ├── candidate_profiles (1:1)
  │     id, user_id, full_name, headline, location, skills[], languages[],
  │     years_experience, desired_salary_usd, summary, raw_text,
  │     embedding(vector 1536), rating_avg, rating_count,
  │     is_published, needs_review, created_at, updated_at
  │
  ├── employer_profiles (1:1)
  │     id, user_id, company_name, company_type, location,
  │     rating_avg, rating_count, is_verified, created_at
  │
  └── job_searches (1:N via employer_profiles)
        id, employer_id, raw_query, role, location, max_salary_usd,
        required_skills[], required_languages[], min_experience,
        embedding(vector 1536), is_alert, last_run_at, created_at

conversations
  id, employer_user_id, candidate_user_id, created_at, last_activity_at
    │
    └── messages (1:N)
          id, conversation_id, sender_user_id, body, channel, created_at

ratings (nouveau — voir §4.2)
  id, conversation_id, rater_user_id, rated_user_id, rater_role,
  score, category_*, created_at
```

### 6.2 Migration complète

⚠️ **L'Alembic migration `0001_initial` doit être remplacée** pour intégrer :
- Le nouveau schéma `ratings` (catégories structurées)
- `employer_profiles.is_verified` (badge institutionnel seed Phase 1)
- `job_searches.is_active` (soft-delete)
- `conversations.last_activity_at`
- `conversations.rating_requested` (booléen : est-ce que le prompt de rating a été envoyé)

Le fichier de migration existant (`src/srokwork/db/migrations/versions/0001_initial.py`) sert de base. Les modifications sont documentées dans le code ci-dessous et doivent être appliquées via une nouvelle migration `0002_trov_ratings`.

### 6.3 Index pgvector

```sql
-- IVFFlat pour la recherche vectorielle rapide
-- lists=100 pour <100K profils. Passer à lists=sqrt(n_rows) au-delà
CREATE INDEX ix_candidate_profiles_embedding
  ON candidate_profiles
  USING ivfflat (embedding vector_cosine_ops)
  WITH (lists = 100);

-- Index pour les searches (alert sweep)
CREATE INDEX ix_job_searches_embedding
  ON job_searches
  USING ivfflat (embedding vector_cosine_ops)
  WITH (lists = 50);
```

### 6.4 Hybride Search SQL

```sql
-- Recherche hybride : filtres structurés + similarité vectorielle
-- Paramètres : $query_embedding, $location, $max_salary, $required_skills

WITH vector_matches AS (
    SELECT
        id,
        user_id,
        1 - (embedding <=> $query_embedding) AS similarity
    FROM candidate_profiles
    WHERE embedding IS NOT NULL
      AND is_published = true
    ORDER BY embedding <=> $query_embedding
    LIMIT 200  -- broad pool for re-ranking
),
filtered AS (
    SELECT vm.*, cp.rating_avg, cp.rating_count, cp.created_at
    FROM vector_matches vm
    JOIN candidate_profiles cp ON cp.id = vm.id
    WHERE ($location IS NULL OR cp.location ILIKE '%' || $location || '%')
      AND ($max_salary IS NULL OR cp.desired_salary_usd <= $max_salary)
      AND ($required_skills = '[]'::jsonb OR cp.skills @> $required_skills::jsonb)
)
SELECT
    *,
    (0.60 * similarity
     + 0.25 * CASE
         WHEN rating_count = 0 THEN 0.5
         ELSE (rating_avg / 5.0) * LEAST(1.0, rating_count::float / 10)
       END
     + 0.15 * (1.0 / (1 + EXTRACT(DAY FROM now() - created_at) / 30))
    ) AS final_score
FROM filtered
ORDER BY final_score DESC
LIMIT 20;
```

---

## 7. API Endpoints

### 7.1 Backend FastAPI (Python)

| Method | Path | Description | Phase |
|---|---|---|---|
| `GET` | `/health` | Health check | 0 |
| `POST` | `/agents/cv/extract` | CV extraction (DeepSeek) | 0 |
| `POST` | `/agents/query/parse` | Query parsing (DeepSeek) | 0 |
| `POST` | `/search` | Hybrid search (filters + vector) | 0 |
| `GET` | `/profiles/{id}` | Get candidate profile | 0 |
| `POST` | `/profiles` | Create/update profile + compute embedding | 0 |
| `POST` | `/conversations` | Start conversation (employer→candidate) | 0 |
| `POST` | `/conversations/{id}/messages` | Send message (relayed) | 0 |
| `GET` | `/conversations/{id}/messages` | Get messages | 0 |
| `POST` | `/ratings` | Create rating (immutable) | 0 |
| `GET` | `/ratings/user/{id}` | Get user's ratings | 0 |
| `POST` | `/alerts` | Save search as alert | 0 |
| `GET` | `/alerts/{user_id}` | List user's alerts | 0 |


### 7.2 Grammy.js Bot (Node.js/TypeScript)

Le bot est un *thin client* : pas de logique métier, pas d'accès direct à la DB.

```
Grammy.js Bot
├── src/
│   ├── bot.ts          # Entry point, middleware setup
│   ├── sessions.ts     # Redis session store
│   ├── i18n/
│   │   ├── km.ts       # Khmer message catalog
│   │   └── en.ts       # English message catalog
│   ├── conversations/
│   │   ├── candidate.ts # Candidate onboarding flow
│   │   ├── employer.ts  # Employer search flow
│   │   └── rating.ts    # Post-conversation rating flow
│   ├── api/
│   │   └── client.ts    # HTTP client to FastAPI backend
│   └── utils/
│       ├── keyboards.ts # Inline keyboard builders
│       └── formatting.ts # Message formatters
├── package.json
├── tsconfig.json
└── Dockerfile
```

**Dépendances Grammy.js :**
```json
{
  "dependencies": {
    "grammy": "^1.30.0",
    "@grammyjs/conversations": "^1.2.0",
    "@grammyjs/i18n": "^1.1.0",
    "@grammyjs/storage-redis": "^1.0.0",
    "ioredis": "^5.4.0"
  }
}
```

---

## 8. n8n Orchestration

### 8.1 Workflows

| Workflow | Trigger | Action |
|---|---|---|
| **alert_sweep** | Cron every 15 min | Query `GET /alerts/active` → for each alert, run hybrid search → if new matches since `last_run_at`, POST to Grammy.js bot webhook → bot sends notification to employer |

| **embedding_sync** | Cron every 5 min | Query profiles where `embedding IS NULL AND is_published = true` → compute embedding via DeepSeek API → PATCH profile |
| **inactive_cleanup** | Cron weekly | Soft-delete profiles not updated in 90 days, conversations with no activity in 30 days |
| **rating_prompt** | Cron daily | Query conversations where `last_activity_at > 24h ago AND rating_requested = false AND messages >= 4` → POST to bot webhook to send rating prompt |


```yaml


trigger:
  - type: cron
    every: 1440  # daily
    
nodes:
  - id: fetch_metrics
    type: http
    config:

      method: GET
      headers:
        Authorization: "Bearer {{API_KEY}}"
      
  - id: store_metrics
    type: database
    config:
      query: |

        (date, candidates_count, repeat_employers, khmer_parse_errors, khmer_parse_total)
        VALUES ($date, $candidates, $employers, $errors, $total)
        
  - id: check_day_60
    type: conditional
    config:
      condition: "{{$json.days_since_launch}} >= 60"
      
  - id: evaluate
    type: code
    config:
      code: |
        const { candidates_count, repeat_employers, khmer_parse_error_rate } = $json;
        const failures = [];
        if (candidates_count < 50) failures.push('CANDIDATES < 50');
        if (repeat_employers < 5) failures.push('REPEAT_EMPLOYERS < 5');
        if (khmer_parse_error_rate > 0.40) failures.push('KHMER_PARSE_ERROR > 40%');
        
        return {
          status: failures.length === 0 ? 'PASS' : 'FAIL',
          failures,
          metrics: { candidates_count, repeat_employers, khmer_parse_error_rate }
        };
        
  - id: notify_fail
    type: telegram
    config:
      chat_id: "{{ADMIN_CHAT_ID}}"
      text: |

        Failures: {{failures}}
        
  - id: notify_pass
    type: telegram
    config:
      chat_id: "{{ADMIN_CHAT_ID}}"
      text: |

```

---

## 10. Deployment

### 10.1 Docker Compose (Phase 0)

```yaml
# docker-compose.yml
version: '3.8'

services:
  postgres:
    image: pgvector/pgvector:pg16
    environment:
      POSTGRES_DB: trov
      POSTGRES_USER: trov
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - pgdata:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U trov"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    volumes:
      - redisdata:/data
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s

  api:
    build:
      context: ./api
      dockerfile: Dockerfile
    environment:
      DATABASE_URL: "postgresql+asyncpg://trov:${DB_PASSWORD}@postgres:5432/trov"
      REDIS_URL: "redis://redis:6379/0"
      LLM_API_KEY: ${LLM_API_KEY}
      LLM_BASE_URL: ${LLM_BASE_URL:-https://api.deepseek.com/v1}
      LLM_MODEL: ${LLM_MODEL:-deepseek-chat}
      LLM_EMBEDDING_MODEL: ${LLM_EMBEDDING_MODEL:-text-embedding-3-small}
      APP_ENV: ${APP_ENV:-production}
      SECRET_KEY: ${SECRET_KEY}
    ports:
      - "8000:8000"
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy

  bot:
    build:
      context: ./bot
      dockerfile: Dockerfile
    environment:
      API_BASE_URL: "http://api:8000"
      TELEGRAM_BOT_TOKEN: ${TELEGRAM_BOT_TOKEN}
      REDIS_URL: "redis://redis:6379/1"
    depends_on:
      - api
    # Bot uses polling in dev, webhook in prod
    # In prod: expose port and configure webhook via Telegram API

volumes:
  pgdata:
  redisdata:
```

### 10.2 n8n (séparé)

n8n est déployé séparément (pas dans le même docker-compose) car c'est de l'infrastructure partagée. Configuration minimale :

```bash
docker run -d \
  --name n8n \
  -p 5678:5678 \
  -v n8n_data:/home/node/.n8n \
  -e N8N_BASIC_AUTH_ACTIVE=true \
  -e N8N_BASIC_AUTH_USER=admin \
  -e N8N_BASIC_AUTH_PASSWORD=${N8N_PASSWORD} \
  n8nio/n8n
```

---

## 11. Migration from SrokWork

### 11.1 Ce qui est conservé

| Composant | Statut | Action |
|---|---|---|
| `agents/cv_extraction.py` | ✅ Conservé | Renommer `srokwork` → `trov` dans les imports |
| `agents/query_parsing.py` | ✅ Conservé | Idem |
| `agents/models.py` | ✅ Conservé | Idem |
| `db/models.py` | ⚠️ Modifié | Ajouter `Rating` structuré, `is_verified`, `last_activity_at`, `rating_requested` |
| `services/users.py` | ✅ Conservé | Renommer |
| `services/worker.py` | ❌ Supprimé | Remplacé par n8n |
| `i18n/km.json` | ✅ Conservé | Ajouter les clés rating |
| `i18n/en.json` | ✅ Conservé | Ajouter les clés rating |
| `core/config.py` | ✅ Conservé | Renommer, ajouter `llm_embedding_model` |
| `api/main.py` | ⚠️ Modifié | Ajouter les endpoints Phase 0 |
| `bots/telegram/bot.py` | ❌ Remplacé | Remplacé par Grammy.js |
| `db/migrations/` | ⚠️ Conservé | Nouvelle migration `0002_trov_ratings` |
| `pyproject.toml` | ⚠️ Modifié | Renommer projet `trov`, dépendances à jour |

### 11.2 Plan de migration

1. **Fork** `srokwork-core` vers un nouveau repo `trov`
2. **Renommer** : `srokwork` → `trov` dans tout le code
3. **Créer** le projet Grammy.js `trov-bot/`
4. **Migration DB** : `0002_trov_ratings.py` (ALTER TABLE ratings + nouvelles colonnes)
5. **Supprimer** `services/worker.py` et `bots/telegram/bot.py`
6. **Configurer** n8n avec les 5 workflows
7. **Déployer** docker compose avec les 4 services
8. **Lancer** le Telegram bot en mode polling → webhook quand stable

---

## 12. FLAGS & Open Questions

### 🔴 CRITICAL — À trancher avant le premier commit

| # | Question | Options | Recommandation |
|---|---|---|---|
| F1 | **Grammy.js vs garder python-telegram-bot ?** | A: Grammy.js (prescrit) — Node.js séparé. B: Garder python-telegram-bot + envelopper avec les patterns de conversation du brief | **B** pour le Phase 0 MVP. Le code bot existant est fonctionnel et testé. Grammy.js introduit un nouveau langage, un nouveau build pipeline, et un bridge HTTP entre Node et Python qui ajoute de la latence. Si le brief est inflexible sur Grammy.js → Phase 1. |
| F2 | **Embedding model** — DeepSeek ou OpenAI ? | A: `text-embedding-3-small` (OpenAI, $0.02/1M tokens). B: `deepseek-embedding` (si disponible). C: Modèle local | **A** par défaut. Si DeepSeek sort un modèle d'embedding compétitif, switcher. |
| F3 | **Hébergement Phase 0** | A: VPS Cambodia (e.g. Shinjiru, $20-40/mo). B: Fly.io/Railway. C: Homelab | **A** pour la souveraineté des données et la latence. Un VPS à Phnom Penh ou Bangkok. |

### 🟡 IMPORTANT — À clarifier avant la fin Phase 0

| # | Question |
|---|----------|
| F4 | Nom de domaine : `trov.org` ? `trov.kh` ? Autre ? |
| F5 | Identité visuelle : le brief mentionne "dark + gold" — le design system doit être défini (couleurs exactes, typographie, logo) |
| F6 | Le nom "Trov" est-il définitif ? Vérifier disponibilité du domaine et absence de conflit de marque |
| F7 | Stratégie de seed pour les 50 premiers profils candidats — campagne Facebook ? Partenariat ONG ? Ambassadeurs Telegram ? |
| F8 | Modèle de gouvernance open-source : quel org GitHub ? Qui sont les 2-3 premiers mainteneurs ? |

---

## Appendice A : Convention de code

### Python (API Backend)
- Python 3.12+, async par défaut
- Ruff pour linting (ligne 100 car.)
- Mypy strict
- Pytest asyncio pour les tests
- Tous les appels LLM sont wrappés dans `agents/` — jamais d'appel direct dans `services/` ou `bots/`

### TypeScript (Grammy.js Bot)
- Node 22, ESM
- TypeScript strict
- Biome pour linting/formatting
- Vitest pour les tests
- Le bot ne fait JAMAIS d'appel direct à la DB. Tout passe par l'API.

### Git
- Convention de commits : [Conventional Commits](https://www.conventionalcommits.org/)
- Branches : `feat/`, `fix/`, `docs/` préfixes
- PR obligatoire pour merge dans `main`

---

## Appendice B : Glossaire

| Terme | Définition |
|---|---|
| **Candidate** | Chercheur d'emploi. Ne paie jamais. |
| **Employer** | PME/entreprise qui recrute. Gratuit. |
| **Rating** | Évaluation structurée (score + catégories) après une interaction vérifiée |
| **NL Query** | Requête en langage naturel ("ខ្ញុំត្រូវការអ្នកធ្វើម្ហូប") |
| **Hybrid Search** | Combinaison de filtres SQL structurés + similarité cosinus vectorielle (pgvector) |
| **Alert** | Recherche sauvegardée qui notifie l'employeur des nouveaux matchs |
| **LPDP** | Loi sur la Protection des Données Personnelles (Cambodge, en cours d'adoption) |
| **MoLVT** | Ministry of Labour and Vocational Training |
| **NEA** | National Employment Agency (Cambodge) |


---

*Document rédigé par Architect (OpenClaw) le 2026-05-23.*
*Basé sur l'audit du code SrokWork existant + ARCHITECT BRIEF Trov.*
*Prochaine étape : Developer handoff → implémentation Phase 0.*