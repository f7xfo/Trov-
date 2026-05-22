"""Alert service — saved searches that notify employers of new matching candidates."""

from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from trov.db.models import JobSearch
from trov.core.logging import log


async def save_alert(
    db: AsyncSession,
    employer_id: UUID,
    raw_query: str,
    role: str | None = None,
    location: str | None = None,
    max_salary_usd: int | None = None,
    required_skills: list[str] | None = None,
    required_languages: list[str] | None = None,
    min_experience: int | None = None,
    embedding: list[float] | None = None,
) -> JobSearch:
    """Save a search as an active alert."""
    alert = JobSearch(
        employer_id=employer_id,
        raw_query=raw_query,
        role=role,
        location=location,
        max_salary_usd=max_salary_usd,
        required_skills=required_skills or [],
        required_languages=required_languages or [],
        min_experience=min_experience,
        embedding=embedding,
        is_alert=True,
        last_run_at=datetime.now(timezone.utc),
        is_active=True,
    )
    db.add(alert)
    await db.flush()
    log.info("alert_saved", alert_id=str(alert.id))
    return alert


async def get_active_alerts(db: AsyncSession) -> list[JobSearch]:
    """Get all alerts that are active and haven't been run in the last 10 minutes."""
    result = await db.execute(
        select(JobSearch)
        .where(
            JobSearch.is_alert == True,
            JobSearch.is_active == True,
        )
        .order_by(JobSearch.last_run_at.asc().nulls_first())
        .limit(100)
    )
    return list(result.scalars().all())


async def bump_alert(db: AsyncSession, alert_id: UUID) -> None:
    """Update last_run_at after alert sweep."""
    await db.execute(
        update(JobSearch)
        .where(JobSearch.id == alert_id)
        .values(last_run_at=datetime.now(timezone.utc))
    )
    await db.flush()


async def list_alerts(db: AsyncSession, employer_id: UUID) -> list[dict]:
    """List saved alerts for an employer."""
    result = await db.execute(
        select(JobSearch)
        .where(JobSearch.employer_id == employer_id, JobSearch.is_alert == True)
        .order_by(JobSearch.created_at.desc())
    )
    alerts = result.scalars().all()

    return [
        {
            "id": str(a.id),
            "raw_query": a.raw_query,
            "role": a.role,
            "location": a.location,
            "max_salary_usd": a.max_salary_usd,
            "created_at": a.created_at.isoformat(),
            "last_run_at": a.last_run_at.isoformat() if a.last_run_at else None,
        }
        for a in alerts
    ]


async def disable_alert(db: AsyncSession, alert_id: UUID) -> None:
    """Soft-delete an alert."""
    await db.execute(
        update(JobSearch)
        .where(JobSearch.id == alert_id)
        .values(is_active=False)
    )
    await db.flush()
