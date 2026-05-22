"""Rating service — the core trust layer of Trov.

This service implements the structured, immutable, bidirectional-asymmetric
rating system that is Trov's competitive moat.

Principles:
- Structured only: score + binary categories. NO free text (anti-defamation).
- Verified interaction: must have a real conversation on-platform.
- Bidirectional asymmetric: different categories for candidates vs employers.
- Immutable: no delete/update API. DB permissions revoked.
- Decay-weighted: recent ratings have more weight (half-life 90 days).
"""

import math
from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from trov.db.models import CandidateProfile, Conversation, EmployerProfile, Message, Rating
from trov.core.logging import log


async def can_rate(
    db: AsyncSession, conversation_id: UUID, rater_user_id: UUID
) -> tuple[bool, str]:
    """
    Verify that a user is eligible to rate someone.

    Conditions:
    1. Conversation exists between both parties
    2. Each side has sent >= 2 messages
    3. Conversation is at least 24 hours old (prevents instant fake ratings)
    4. Rater hasn't already rated this conversation
    """
    # Check existing rating
    existing = await db.execute(
        select(Rating).where(
            Rating.conversation_id == conversation_id,
            Rating.rater_user_id == rater_user_id,
        )
    )
    if existing.scalar_one_or_none():
        return False, "already_rated"

    # Get conversation with message counts
    conv = await db.execute(
        select(Conversation).where(Conversation.id == conversation_id)
    )
    conversation = conv.scalar_one_or_none()
    if not conversation:
        return False, "conversation_not_found"

    # Count messages from each side
    from_rater = await db.scalar(
        select(func.count(Message.id)).where(
            Message.conversation_id == conversation_id,
            Message.sender_user_id == rater_user_id,
        )
    )
    other_user_id = (
        conversation.employer_user_id
        if rater_user_id == conversation.candidate_user_id
        else conversation.candidate_user_id
    )
    from_other = await db.scalar(
        select(func.count(Message.id)).where(
            Message.conversation_id == conversation_id,
            Message.sender_user_id == other_user_id,
        )
    )

    if from_rater < 2 or from_other < 2:
        return False, "insufficient_messages"

    hours_elapsed = (
        datetime.now(timezone.utc) - conversation.created_at
    ).total_seconds() / 3600
    if hours_elapsed < 24:
        return False, "too_soon"

    return True, "ok"


async def create_rating(
    db: AsyncSession,
    conversation_id: UUID,
    rater_user_id: UUID,
    rated_user_id: UUID,
    rater_role: str,
    score: int,
    categories: dict[str, bool | None],
) -> Rating:
    """Create an immutable rating. No update/delete possible."""
    rating = Rating(
        conversation_id=conversation_id,
        rater_user_id=rater_user_id,
        rated_user_id=rated_user_id,
        rater_role=rater_role,
        score=score,
        category_paid_on_time=categories.get("paid_on_time"),
        category_conditions_match=categories.get("conditions_match"),
        category_communication=categories.get("communication"),
        category_showed_up=categories.get("showed_up"),
        category_skills_match=categories.get("skills_match"),
        category_professional=categories.get("professional"),
    )
    db.add(rating)
    await db.flush()

    # Recalculate aggregate score for the rated user
    await _recalculate_rating(db, rated_user_id, rater_role)

    log.info("rating_created", rating_id=str(rating.id), score=score)
    return rating


async def _recalculate_rating(db: AsyncSession, user_id: UUID, rated_role: str) -> None:
    """
    Recalculate rating_avg and rating_count with decay weighting.
    Half-life: 90 days. Recent ratings count more.
    """
    HALF_LIFE_DAYS = 90.0
    decay_factor = math.log(2) / HALF_LIFE_DAYS

    ratings_query = await db.execute(
        select(Rating.score, Rating.created_at)
        .where(Rating.rated_user_id == user_id)
        .order_by(Rating.created_at.desc())
    )
    ratings = ratings_query.all()

    total_weight = 0.0
    weighted_sum = 0.0

    for score_val, created_at in ratings:
        days_ago = (datetime.now(timezone.utc) - created_at).days
        weight = math.exp(-decay_factor * days_ago)
        weighted_sum += score_val * weight
        total_weight += weight

    avg = weighted_sum / total_weight if total_weight > 0 else 0.0
    count = len(ratings)

    if rated_role == "employer":
        await db.execute(
            update(EmployerProfile)
            .where(EmployerProfile.user_id == user_id)
            .values(rating_avg=avg, rating_count=count)
        )
    else:
        await db.execute(
            update(CandidateProfile)
            .where(CandidateProfile.user_id == user_id)
            .values(rating_avg=avg, rating_count=count)
        )
    await db.flush()


async def get_user_ratings(db: AsyncSession, user_id: UUID) -> list[dict]:
    """Get all ratings for a user with aggregated category stats."""
    ratings = await db.execute(
        select(Rating).where(Rating.rated_user_id == user_id).order_by(Rating.created_at.desc())
    )
    rating_list = ratings.scalars().all()

    result = []
    for r in rating_list:
        result.append({
            "id": str(r.id),
            "score": r.score,
            "rater_role": r.rater_role,
            "categories": {
                "paid_on_time": r.category_paid_on_time,
                "conditions_match": r.category_conditions_match,
                "communication": r.category_communication,
                "showed_up": r.category_showed_up,
                "skills_match": r.category_skills_match,
                "professional": r.category_professional,
            },
            "created_at": r.created_at.isoformat(),
        })
    return result


def get_category_stats(ratings: list) -> dict[str, float]:
    """Calculate positive ratio for each category."""
    categories = ["paid_on_time", "conditions_match", "communication", "showed_up", "skills_match", "professional"]
    stats = {}
    for cat in categories:
        relevant = [
            r["categories"][cat]
            for r in ratings
            if r["categories"].get(cat) is not None
        ]
        stats[cat] = sum(1 for x in relevant if x) / len(relevant) if relevant else 0.0
    return stats
