"""Database models — the core schema for Trov.

Design notes:
- `User` is the universal identity (can be candidate, employer, or both).
- `CandidateProfile` and `EmployerProfile` are role-specific extensions.
- `JobSearch` represents a saved natural-language search that can become an alert.
- Embeddings live on profiles (pgvector) for semantic search.
- The `Rating` model is structured, not free-text (anti-defamation design).
- All timestamps are UTC.
"""

from datetime import datetime
from enum import StrEnum
from uuid import UUID, uuid4

from pgvector.sqlalchemy import Vector
from sqlalchemy import JSON, BigInteger, Boolean, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

# Embedding dimension for text-embedding-3-small. Adjust per model.
EMBED_DIM = 1536


class Base(DeclarativeBase):
    pass


class Channel(StrEnum):
    TELEGRAM = "telegram"
    MESSENGER = "messenger"
    WEB = "web"


class Language(StrEnum):
    KM = "km"
    EN = "en"


class EmbeddingStatus(StrEnum):
    PENDING = "pending"
    DONE = "done"
    FAILED = "failed"


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    telegram_id: Mapped[int | None] = mapped_column(BigInteger, unique=True, nullable=True, index=True)
    messenger_id: Mapped[str | None] = mapped_column(String(128), unique=True, nullable=True, index=True)
    phone: Mapped[str | None] = mapped_column(String(32), unique=True, nullable=True)
    display_name: Mapped[str | None] = mapped_column(String(128))
    preferred_language: Mapped[Language] = mapped_column(String(8), default=Language.KM)
    primary_channel: Mapped[Channel] = mapped_column(String(16), default=Channel.TELEGRAM)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    last_seen_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    candidate_profile: Mapped["CandidateProfile | None"] = relationship(back_populates="user", uselist=False)
    employer_profile: Mapped["EmployerProfile | None"] = relationship(back_populates="user", uselist=False)


class CandidateProfile(Base):
    __tablename__ = "candidate_profiles"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True)

    # Structured fields extracted by the AI
    full_name: Mapped[str | None] = mapped_column(String(256))
    headline: Mapped[str | None] = mapped_column(String(256))  # e.g. "Cook, 5 years Siem Reap"
    location: Mapped[str | None] = mapped_column(String(128), index=True)
    skills: Mapped[list[str]] = mapped_column(JSON, default=list)
    languages: Mapped[list[str]] = mapped_column(JSON, default=list)
    years_experience: Mapped[int | None] = mapped_column()
    desired_salary_usd: Mapped[int | None] = mapped_column()
    summary: Mapped[str | None] = mapped_column(Text)  # AI-generated bilingual summary

    # Raw source — original CV text or transcript
    raw_text: Mapped[str | None] = mapped_column(Text)

    # Semantic search vector (built from headline + skills + summary)
    embedding: Mapped[list[float] | None] = mapped_column(Vector(EMBED_DIM))
    embedding_status: Mapped[EmbeddingStatus] = mapped_column(String(16), default=EmbeddingStatus.PENDING)

    # Reputation
    rating_avg: Mapped[float] = mapped_column(default=0.0)
    rating_count: Mapped[int] = mapped_column(default=0)

    # State
    is_published: Mapped[bool] = mapped_column(Boolean, default=False)
    needs_review: Mapped[bool] = mapped_column(Boolean, default=True)  # user must confirm extraction

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user: Mapped[User] = relationship(back_populates="candidate_profile")


class EmployerProfile(Base):
    __tablename__ = "employer_profiles"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True)

    company_name: Mapped[str | None] = mapped_column(String(256))
    company_type: Mapped[str | None] = mapped_column(String(64))  # restaurant, shop, ngo, etc.
    location: Mapped[str | None] = mapped_column(String(128))

    rating_avg: Mapped[float] = mapped_column(default=0.0)
    rating_count: Mapped[int] = mapped_column(default=0)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)  # institutional seed badge (Phase 1)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped[User] = relationship(back_populates="employer_profile")
    searches: Mapped[list["JobSearch"]] = relationship(back_populates="employer")


class JobSearch(Base):
    """A natural-language search. Becomes an alert if `is_alert = True`."""

    __tablename__ = "job_searches"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    employer_id: Mapped[UUID] = mapped_column(ForeignKey("employer_profiles.id", ondelete="CASCADE"))

    raw_query: Mapped[str] = mapped_column(Text)  # original NL query, any language
    # Extracted structured criteria
    role: Mapped[str | None] = mapped_column(String(128), index=True)
    location: Mapped[str | None] = mapped_column(String(128), index=True)
    max_salary_usd: Mapped[int | None] = mapped_column()
    required_skills: Mapped[list[str]] = mapped_column(JSON, default=list)
    required_languages: Mapped[list[str]] = mapped_column(JSON, default=list)
    min_experience: Mapped[int | None] = mapped_column()

    # Semantic vector for matching against candidate embeddings
    embedding: Mapped[list[float] | None] = mapped_column(Vector(EMBED_DIM))

    is_alert: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)  # soft-delete
    last_run_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    employer: Mapped[EmployerProfile] = relationship(back_populates="searches")


class Conversation(Base):
    """A relayed private chat between an employer and a candidate."""

    __tablename__ = "conversations"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    employer_user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    candidate_user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    last_activity_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    rating_requested: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    conversation_id: Mapped[UUID] = mapped_column(ForeignKey("conversations.id", ondelete="CASCADE"))
    sender_user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    body: Mapped[str] = mapped_column(Text)
    channel: Mapped[Channel] = mapped_column(String(16))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Rating(Base):
    """Structured, immutable rating. No free text — categories only.
    
    Governance:
    - Tied to a verified conversation (conversation_id FK).
    - One rating per conversation per rater (UNIQUE constraint).
    - Categories differ by rater_role (candidate rates employer differently).
    - No UPDATE or DELETE via API. Immutable at DB permission level.
    """

    __tablename__ = "ratings"
    __table_args__ = (
        UniqueConstraint("conversation_id", "rater_user_id", name="uq_rating_per_conversation"),
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    conversation_id: Mapped[UUID] = mapped_column(ForeignKey("conversations.id", ondelete="CASCADE"))

    # Who rates whom
    rater_user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    rated_user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    rater_role: Mapped[str] = mapped_column(String(16))  # 'candidate' or 'employer'

    # Score (1-5)
    score: Mapped[int] = mapped_column(Integer)

    # Structured categories — candidate rating employer
    category_paid_on_time: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    category_conditions_match: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    category_communication: Mapped[bool | None] = mapped_column(Boolean, nullable=True)

    # Structured categories — employer rating candidate
    category_showed_up: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    category_skills_match: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    category_professional: Mapped[bool | None] = mapped_column(Boolean, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
