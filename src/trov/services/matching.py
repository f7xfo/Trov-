"""Matching service — hybrid search combining structured filters + pgvector cosine similarity.

The search pipeline:
1. Vector similarity: find nearest candidates by embedding cosine distance
2. Structured filters: location, salary, skills, languages, experience
3. Ranking formula: 0.60 × similarity + 0.25 × rating_score + 0.15 × recency_boost
"""

from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from trov.core.logging import log


async def hybrid_search(
    db: AsyncSession,
    query_embedding: list[float] | None,
    location: str | None = None,
    max_salary: int | None = None,
    required_skills: list[str] | None = None,
    required_languages: list[str] | None = None,
    min_experience: int | None = None,
    limit: int = 20,
) -> list[dict]:
    """
    Hybrid search: vector similarity + structured filters + rating-aware ranking.

    Returns candidates ranked by final_score:
    - 60% vector similarity (cosine)
    - 25% normalized rating (with confidence weighting)
    - 15% recency boost (newer profiles get slight edge)
    """
    has_filters = location or max_salary or required_skills or required_languages or min_experience

    if query_embedding:
        embedding_str = "[" + ",".join(str(x) for x in query_embedding) + "]"
    else:
        embedding_str = None

    # Build the SQL with parameterized query
    sql = """
    WITH ranked AS (
        SELECT
            cp.id,
            cp.user_id,
            cp.full_name,
            cp.headline,
            cp.location,
            cp.skills,
            cp.languages,
            cp.years_experience,
            cp.desired_salary_usd,
            cp.summary,
            cp.rating_avg,
            cp.rating_count,
            cp.created_at,
            u.display_name,
            u.preferred_language,
            CASE
                WHEN cp.rating_count = 0 THEN 0.5
                ELSE (cp.rating_avg / 5.0) * LEAST(1.0, cp.rating_count::float / 10)
            END AS rating_score
        FROM candidate_profiles cp
        JOIN users u ON u.id = cp.user_id
        WHERE cp.is_published = true
            AND cp.embedding IS NOT NULL
    """.strip()

    params: dict = {}

    if query_embedding:
        sql += "\n        ORDER BY cp.embedding <=> :query_embedding\n        LIMIT 200"
        params["query_embedding"] = embedding_str

    sql += """
    )
    SELECT
        r.*,
        (
            0.60 * COALESCE(1 - (r.embedding <=> :query_embedding_cos), 0.5)
            + 0.25 * r.rating_score
            + 0.15 * (1.0 / (1 + EXTRACT(DAY FROM now() - r.created_at) / 30))
        ) AS final_score
    FROM ranked r
    WHERE 1=1
    """

    if location:
        sql += "\n        AND LOWER(r.location) LIKE :location_filter"
        params["location_filter"] = f"%{location.lower()}%"
    if max_salary is not None:
        sql += "\n        AND (r.desired_salary_usd IS NULL OR r.desired_salary_usd <= :max_salary)"
        params["max_salary"] = max_salary
    if required_skills:
        sql += "\n        AND r.skills @> :skills_filter"
        params["skills_filter"] = str(required_skills).replace("'", '"')
    if required_languages:
        sql += "\n        AND r.languages && :langs_filter"
        params["langs_filter"] = str(required_languages).replace("'", '"')
    if min_experience is not None:
        sql += "\n        AND r.years_experience >= :min_exp"
        params["min_exp"] = min_experience

    sql += "\n    ORDER BY final_score DESC\n    LIMIT :limit"
    params["limit"] = limit
    if query_embedding:
        params["query_embedding_cos"] = embedding_str

    try:
        result = await db.execute(text(sql), params)
        rows = result.mappings().all()

        candidates = []
        for row in rows:
            candidates.append({
                "id": str(row["id"]),
                "user_id": str(row["user_id"]),
                "full_name": row["full_name"],
                "display_name": row["display_name"],
                "headline": row["headline"],
                "location": row["location"],
                "skills": row["skills"] or [],
                "languages": row["languages"] or [],
                "years_experience": row["years_experience"],
                "desired_salary_usd": row["desired_salary_usd"],
                "summary": row["summary"],
                "rating_avg": round(float(row["rating_avg"]), 1),
                "rating_count": row["rating_count"],
                "final_score": round(float(row["final_score"]), 4),
                "created_at": row["created_at"].isoformat() if row["created_at"] else None,
            })

        log.info("hybrid_search", count=len(candidates))
        return candidates

    except Exception as e:
        log.error("hybrid_search_failed", error=str(e))
        raise


async def find_candidates_by_filters(
    db: AsyncSession,
    location: str | None = None,
    max_salary: int | None = None,
    required_skills: list[str] | None = None,
    limit: int = 20,
) -> list[dict]:
    """Fallback search without embeddings — structured filters only."""
    return await hybrid_search(
        db,
        query_embedding=None,
        location=location,
        max_salary=max_salary,
        required_skills=required_skills,
        limit=limit,
    )
