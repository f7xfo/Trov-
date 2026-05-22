"""Profile service — CRUD, embedding computation, confirm/publish flow."""

from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from trov.agents.cv_extraction import ExtractedCV, extract_cv
from trov.db.models import CandidateProfile, User, EmbeddingStatus
from trov.core.logging import log


async def get_or_create_profile(
    db: AsyncSession, user: User
) -> CandidateProfile:
    """Get existing profile or create a new one."""
    result = await db.execute(
        select(CandidateProfile).where(CandidateProfile.user_id == user.id)
    )
    profile = result.scalar_one_or_none()

    if not profile:
        profile = CandidateProfile(user_id=user.id)
        db.add(profile)
        await db.flush()
        log.info("profile_created", user_id=str(user.id))

    return profile


async def extract_and_update_profile(
    db: AsyncSession, user: User, raw_text: str
) -> CandidateProfile:
    """Run CV extraction agent and update the profile draft."""
    profile = await get_or_create_profile(db, user)

    # Run AI extraction
    cv: ExtractedCV = await extract_cv(raw_text)

    # Update profile fields
    profile.full_name = cv.full_name or profile.full_name
    profile.headline = cv.headline or profile.headline
    profile.location = cv.location or profile.location
    profile.skills = cv.skills or []
    profile.languages = cv.languages or []
    profile.years_experience = cv.years_experience
    profile.desired_salary_usd = cv.desired_salary_usd
    profile.summary = cv.summary
    profile.raw_text = raw_text
    profile.needs_review = True  # User must confirm before publish
    profile.updated_at = datetime.now(timezone.utc)

    await db.flush()
    log.info("profile_extracted", user_id=str(user.id), headline=cv.headline)
    return profile


async def publish_profile(db: AsyncSession, user_id: UUID) -> CandidateProfile:
    """Confirm and publish a candidate profile."""
    result = await db.execute(
        select(CandidateProfile).where(CandidateProfile.user_id == user_id)
    )
    profile = result.scalar_one_or_none()
    if not profile:
        raise ValueError("profile_not_found")

    profile.is_published = True
    profile.needs_review = False
    profile.updated_at = datetime.now(timezone.utc)
    profile.embedding_status = EmbeddingStatus.PENDING
    await db.flush()
    log.info("profile_published", user_id=str(user_id))
    return profile


async def update_profile_field(
    db: AsyncSession, user_id: UUID, field: str, value: object
) -> CandidateProfile:
    """Update a single field on the profile."""
    allowed = {"full_name", "headline", "location", "skills", "languages",
               "years_experience", "desired_salary_usd", "summary"}
    if field not in allowed:
        raise ValueError(f"invalid_field: {field}")

    await db.execute(
        update(CandidateProfile)
        .where(CandidateProfile.user_id == user_id)
        .values(**{field: value, "updated_at": datetime.now(timezone.utc)})
    )
    await db.flush()

    result = await db.execute(
        select(CandidateProfile).where(CandidateProfile.user_id == user_id)
    )
    return result.scalar_one()


async def get_profile(db: AsyncSession, profile_id: UUID) -> dict | None:
    """Get a published candidate profile with aggregate rating stats."""
    result = await db.execute(
        select(CandidateProfile, User.display_name, User.preferred_language)
        .join(User, User.id == CandidateProfile.user_id)
        .where(CandidateProfile.id == profile_id, CandidateProfile.is_published == True)
    )
    row = result.one_or_none()
    if not row:
        return None

    cp = row[0]
    return {
        "id": str(cp.id),
        "user_id": str(cp.user_id),
        "display_name": row[1],
        "full_name": cp.full_name,
        "headline": cp.headline,
        "location": cp.location,
        "skills": cp.skills or [],
        "languages": cp.languages or [],
        "years_experience": cp.years_experience,
        "desired_salary_usd": cp.desired_salary_usd,
        "summary": cp.summary,
        "rating_avg": round(float(cp.rating_avg), 1),
        "rating_count": cp.rating_count,
        "created_at": cp.created_at.isoformat(),
    }


async def get_profiles_pending_embedding(db: AsyncSession, limit: int = 50) -> list[CandidateProfile]:
    """Get profiles that need embedding computation."""
    result = await db.execute(
        select(CandidateProfile)
        .where(
            CandidateProfile.is_published == True,
            CandidateProfile.embedding_status == EmbeddingStatus.PENDING,
        )
        .limit(limit)
    )
    return list(result.scalars().all())


async def set_embedding(
    db: AsyncSession, profile_id: UUID, embedding: list[float]
) -> None:
    """Store the computed embedding vector."""
    await db.execute(
        update(CandidateProfile)
        .where(CandidateProfile.id == profile_id)
        .values(embedding=embedding, embedding_status=EmbeddingStatus.DONE)
    )
    await db.flush()
