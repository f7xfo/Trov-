"""Kill-criteria stats service — metrics for RULE_27 auto-monitoring."""

from datetime import date, datetime, timezone

from sqlalchemy import func, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from trov.db.models import CandidateProfile, JobSearch


async def get_kill_criteria_stats(
    db: AsyncSession, launch_date: date | None = None
) -> dict:
    """
    Compute Trov's kill-criteria metrics (RULE_27).

    Returns:
    - candidates_count: published candidate profiles
    - repeat_employers: employers who've run searches on >= 2 different days
    - khmer_parse_total: total searches with Khmer script queries
    - khmer_parse_errors: searches where parsing failed (role or location null)
    - khmer_parse_error_rate: error ratio
    - days_since_launch: days since launch
    """
    # Candidates with published profiles
    candidates = await db.scalar(
        select(func.count(CandidateProfile.id)).where(
            CandidateProfile.is_published == True
        )
    )

    # Repeat employers (>= 2 searches on different days)
    repeat_q = text("""
        SELECT COUNT(DISTINCT employer_id) FROM (
            SELECT employer_id, COUNT(DISTINCT DATE(created_at)) AS active_days
            FROM job_searches
            GROUP BY employer_id
            HAVING COUNT(DISTINCT DATE(created_at)) >= 2
        ) sub
    """)
    repeat_result = await db.execute(repeat_q)
    repeat_employers = repeat_result.scalar() or 0

    # Khmer parsing accuracy
    khmer_q = text("""
        SELECT
            COUNT(*) AS total,
            COUNT(*) FILTER (WHERE role IS NULL OR location IS NULL) AS errors
        FROM job_searches
        WHERE raw_query ~ '[ក-៝]'
    """)
    khmer_result = await db.execute(khmer_q)
    khmer_row = khmer_result.one()
    khmer_total = khmer_row.total or 0
    khmer_errors = khmer_row.errors or 0
    khmer_error_rate = khmer_errors / khmer_total if khmer_total > 0 else 0.0

    # Days since launch
    if launch_date:
        days_since = (date.today() - launch_date).days
    else:
        days_since = 0

    return {
        "days_since_launch": days_since,
        "candidates_count": candidates or 0,
        "repeat_employers": repeat_employers or 0,
        "khmer_parse_total": khmer_total,
        "khmer_parse_errors": khmer_errors,
        "khmer_parse_error_rate": round(khmer_error_rate, 3),
        "launch_date": launch_date.isoformat() if launch_date else None,
        "checked_at": datetime.now(timezone.utc).isoformat(),
    }
