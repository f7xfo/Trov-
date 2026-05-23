"""Trov API routes — all Phase 0 endpoints.

Design note:
- All endpoints are async.
- Authentication is minimal in Phase 0 (Telegram user ID via header).
- Full auth (JWT/API keys) comes in Phase 1 for PWA.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field

from trov.core.logging import log
from trov.db.session import get_db
from trov.services import alerts, matching, profiles, ratings, users

router = APIRouter()


# ── Pydantic Schemas ──

class CVExtractRequest(BaseModel):
    raw_text: str = Field(..., min_length=10, max_length=5000)
    language_hint: str | None = None  # 'km' or 'en'


class CVExtractResponse(BaseModel):
    full_name: str | None = None
    headline: str | None = None
    location: str | None = None
    skills: list[str] = []
    languages: list[str] = []
    years_experience: int | None = None
    desired_salary_usd: int | None = None
    summary: str | None = None


class QueryParseRequest(BaseModel):
    raw_query: str = Field(..., min_length=3, max_length=500)
    language_hint: str | None = None


class QueryParseResponse(BaseModel):
    role: str | None = None
    location: str | None = None
    max_salary_usd: int | None = None
    required_skills: list[str] = []
    required_languages: list[str] = []
    min_experience: int | None = None


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=500)
    location: str | None = None
    max_salary: int | None = None
    required_skills: list[str] | None = None


class RatingCreateRequest(BaseModel):
    conversation_id: UUID
    rated_user_id: UUID
    rater_role: str = Field(..., pattern="^(candidate|employer)$")
    score: int = Field(..., ge=1, le=5)
    categories: dict[str, bool | None] = {}


class AlertCreateRequest(BaseModel):
    raw_query: str
    role: str | None = None
    location: str | None = None
    max_salary_usd: int | None = None
    required_skills: list[str] | None = None
    required_languages: list[str] | None = None
    min_experience: int | None = None


# ── Health ──

@router.get("/health")
async def health():
    return {"status": "ok", "service": "trov"}


# ── Agent Endpoints ──

@router.post("/agents/cv/extract", response_model=CVExtractResponse)
async def agent_cv_extract(req: CVExtractRequest, db=Depends(get_db)):
    """Extract structured CV data from raw text using DeepSeek."""
    try:
        from trov.agents.cv_extraction import extract_cv
        cv = await extract_cv(req.raw_text)
        log.info("cv_extracted_api")
        return CVExtractResponse(
            full_name=cv.full_name,
            headline=cv.headline,
            location=cv.location,
            skills=cv.skills,
            languages=cv.languages,
            years_experience=cv.years_experience,
            desired_salary_usd=cv.desired_salary_usd,
            summary=cv.summary,
        )
    except Exception as e:
        log.error("cv_extract_failed", error=str(e))
        raise HTTPException(status_code=500, detail="CV extraction failed")


@router.post("/agents/query/parse", response_model=QueryParseResponse)
async def agent_query_parse(req: QueryParseRequest, db=Depends(get_db)):
    """Parse a natural-language search query into structured criteria."""
    try:
        from trov.agents.query_parsing import parse_query
        parsed = await parse_query(req.raw_query)
        log.info("query_parsed_api")
        return QueryParseResponse(
            role=parsed.role,
            location=parsed.location,
            max_salary_usd=parsed.max_salary_usd,
            required_skills=parsed.required_skills,
            required_languages=parsed.required_languages,
            min_experience=parsed.min_experience,
        )
    except Exception as e:
        log.error("query_parse_failed", error=str(e))
        raise HTTPException(status_code=500, detail="Query parsing failed")


# ── Search ──

@router.post("/search")
async def search(req: SearchRequest, db=Depends(get_db)):
    """Hybrid search: parse query + find matching candidates."""
    from trov.agents.query_parsing import parse_query

    # Parse the query
    parsed = await parse_query(req.query)

    # Generate embedding from query text for vector search
    # (In production: call embedding API; for now we use structured filters)
    query_embedding = None
    try:
        from trov.agents.models import get_embedding
        query_embedding = await get_embedding(req.query)
    except Exception:
        pass  # Vector search degrades gracefully

    # Run hybrid search
    candidates = await matching.hybrid_search(
        db,
        query_embedding=query_embedding,
        location=parsed.location or req.location,
        max_salary=parsed.max_salary_usd or req.max_salary,
        required_skills=parsed.required_skills or req.required_skills,
    )

    return {
        "query": req.query,
        "parsed": {
            "role": parsed.role,
            "location": parsed.location,
            "max_salary_usd": parsed.max_salary_usd,
        },
        "results": candidates,
        "count": len(candidates),
    }


# ── Profiles ──

@router.get("/profiles/{profile_id}")
async def get_profile(profile_id: UUID, db=Depends(get_db)):
    """Get a candidate's public profile."""
    profile = await profiles.get_profile(db, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@router.post("/profiles")
async def create_or_update_profile(
    raw_text: str = None,
    user_id: UUID = None,
    db=Depends(get_db),
):
    """Extract CV and create/update profile draft."""
    if not user_id:
        raise HTTPException(status_code=400, detail="user_id required")
    user = await users.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not raw_text:
        raise HTTPException(status_code=400, detail="raw_text required")

    profile = await profiles.extract_and_update_profile(db, user, raw_text)
    return {
        "id": str(profile.id),
        "headline": profile.headline,
        "location": profile.location,
        "skills": profile.skills,
        "needs_review": profile.needs_review,
    }


@router.post("/profiles/{user_id}/publish")
async def publish_profile(user_id: UUID, db=Depends(get_db)):
    """Confirm and publish a profile."""
    try:
        profile = await profiles.publish_profile(db, user_id)
        return {"status": "published", "profile_id": str(profile.id)}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ── Ratings ──

@router.post("/ratings", status_code=201)
async def create_rating(req: RatingCreateRequest, db=Depends(get_db)):
    """
    Create an immutable rating. No update or delete possible.

    Requirements:
    - Both parties had a real conversation (>= 2 messages each, >= 24h old)
    - Rater hasn't already rated this conversation
    """
    # Verify eligibility
    can, reason = await ratings.can_rate(db, req.conversation_id, ...)  # rater_user_id from auth
    if not can:
        raise HTTPException(status_code=400, detail=f"Cannot rate: {reason}")

    rating_obj = await ratings.create_rating(
        db,
        conversation_id=req.conversation_id,
        # rater_user_id from auth context
        rater_user_id=UUID("00000000-0000-0000-0000-000000000000"),  # placeholder
        rated_user_id=req.rated_user_id,
        rater_role=req.rater_role,
        score=req.score,
        categories=req.categories,
    )
    return {
        "id": str(rating_obj.id),
        "score": rating_obj.score,
        "created_at": rating_obj.created_at.isoformat(),
    }


@router.get("/ratings/user/{user_id}")
async def get_user_ratings(user_id: UUID, db=Depends(get_db)):
    """Get all ratings for a user with category stats."""
    rating_list = await ratings.get_user_ratings(db, user_id)
    category_stats = ratings.get_category_stats(rating_list)
    return {
        "user_id": str(user_id),
        "ratings": rating_list,
        "category_stats": category_stats,
        "count": len(rating_list),
    }


# ── Alerts ──

@router.post("/alerts")
async def create_alert(req: AlertCreateRequest, db=Depends(get_db)):
    """Save a search as an alert."""
    from trov.agents.query_parsing import parse_query

    parsed = await parse_query(req.raw_query)

    alert = await alerts.save_alert(
        db,
        employer_id=UUID("00000000-0000-0000-0000-000000000000"),  # placeholder
        raw_query=req.raw_query,
        role=parsed.role or req.role,
        location=parsed.location or req.location,
        max_salary_usd=parsed.max_salary_usd or req.max_salary_usd,
        required_skills=parsed.required_skills or req.required_skills,
        required_languages=parsed.required_languages or req.required_languages,
        min_experience=parsed.min_experience or req.min_experience,
    )
    return {"id": str(alert.id), "status": "active"}


@router.get("/alerts/{user_id}")
async def list_alerts(user_id: UUID, db=Depends(get_db)):
    """List saved alerts for an employer."""
    alert_list = await alerts.list_alerts(db, user_id)
    return {"alerts": alert_list, "count": len(alert_list)}



