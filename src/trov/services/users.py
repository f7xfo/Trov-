"""User-related services."""

from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from telegram import User as TgUser

from trov.db.models import Channel, Language, User
from trov.db.session import SessionLocal


def _detect_language(tg_lang: str | None) -> Language:
    """Default to Khmer unless Telegram says otherwise."""
    if tg_lang and tg_lang.lower().startswith("en"):
        return Language.EN
    return Language.KM


async def get_or_create_user_from_telegram(tg_user: TgUser) -> User:
    """Look up or create a User given a Telegram user object."""
    async with SessionLocal() as session:
        result = await session.execute(select(User).where(User.telegram_id == tg_user.id))
        user = result.scalar_one_or_none()
        if user is not None:
            user.last_seen_at = datetime.now(UTC)
            user.display_name = tg_user.full_name or user.display_name
            await session.commit()
            return user

        user = User(
            telegram_id=tg_user.id,
            display_name=tg_user.full_name,
            preferred_language=_detect_language(tg_user.language_code),
            primary_channel=Channel.TELEGRAM,
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user


async def get_user(db: AsyncSession, user_id: UUID) -> User | None:
    """Get a user by ID."""
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()
