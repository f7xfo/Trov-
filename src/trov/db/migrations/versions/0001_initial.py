"""initial schema

Revision ID: 0001_initial
Revises:
Create Date: 2026-05-15 12:00:00.000000

"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from pgvector.sqlalchemy import Vector
from sqlalchemy.dialects import postgresql

revision: str = "0001_initial"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

EMBED_DIM = 1536


def upgrade() -> None:
    # Enable pgvector
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("telegram_id", sa.BigInteger, unique=True, nullable=True),
        sa.Column("messenger_id", sa.String(128), unique=True, nullable=True),
        sa.Column("phone", sa.String(32), unique=True, nullable=True),
        sa.Column("display_name", sa.String(128)),
        sa.Column("preferred_language", sa.String(8), nullable=False, server_default="km"),
        sa.Column("primary_channel", sa.String(16), nullable=False, server_default="telegram"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("last_seen_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_users_telegram_id", "users", ["telegram_id"])
    op.create_index("ix_users_messenger_id", "users", ["messenger_id"])

    op.create_table(
        "candidate_profiles",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False),
        sa.Column("full_name", sa.String(256)),
        sa.Column("headline", sa.String(256)),
        sa.Column("location", sa.String(128)),
        sa.Column("skills", sa.JSON, server_default="[]"),
        sa.Column("languages", sa.JSON, server_default="[]"),
        sa.Column("years_experience", sa.Integer),
        sa.Column("desired_salary_usd", sa.Integer),
        sa.Column("summary", sa.Text),
        sa.Column("raw_text", sa.Text),
        sa.Column("embedding", Vector(EMBED_DIM)),
        sa.Column("rating_avg", sa.Float, server_default="0.0"),
        sa.Column("rating_count", sa.Integer, server_default="0"),
        sa.Column("is_published", sa.Boolean, server_default=sa.false()),
        sa.Column("needs_review", sa.Boolean, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_candidate_profiles_location", "candidate_profiles", ["location"])

    # IVFFlat index for fast vector search. Tune `lists` as data grows.
    op.execute(
        "CREATE INDEX ix_candidate_profiles_embedding "
        "ON candidate_profiles USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100)"
    )

    op.create_table(
        "employer_profiles",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False),
        sa.Column("company_name", sa.String(256)),
        sa.Column("company_type", sa.String(64)),
        sa.Column("location", sa.String(128)),
        sa.Column("rating_avg", sa.Float, server_default="0.0"),
        sa.Column("rating_count", sa.Integer, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        "job_searches",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("employer_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("employer_profiles.id", ondelete="CASCADE"), nullable=False),
        sa.Column("raw_query", sa.Text, nullable=False),
        sa.Column("role", sa.String(128)),
        sa.Column("location", sa.String(128)),
        sa.Column("max_salary_usd", sa.Integer),
        sa.Column("required_skills", sa.JSON, server_default="[]"),
        sa.Column("required_languages", sa.JSON, server_default="[]"),
        sa.Column("min_experience", sa.Integer),
        sa.Column("embedding", Vector(EMBED_DIM)),
        sa.Column("is_alert", sa.Boolean, server_default=sa.false()),
        sa.Column("last_run_at", sa.DateTime(timezone=True)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_job_searches_role", "job_searches", ["role"])
    op.create_index("ix_job_searches_location", "job_searches", ["location"])

    op.create_table(
        "conversations",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("employer_user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("candidate_user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        "messages",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("conversation_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False),
        sa.Column("sender_user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("body", sa.Text, nullable=False),
        sa.Column("channel", sa.String(16), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        "ratings",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("rater_user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("rated_user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("score", sa.Integer, nullable=False),
        sa.Column("comment", sa.Text),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("ratings")
    op.drop_table("messages")
    op.drop_table("conversations")
    op.drop_table("job_searches")
    op.drop_table("employer_profiles")
    op.execute("DROP INDEX IF EXISTS ix_candidate_profiles_embedding")
    op.drop_table("candidate_profiles")
    op.drop_table("users")
