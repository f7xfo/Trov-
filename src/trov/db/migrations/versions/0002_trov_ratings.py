"""Trov rating system migration.

Revision ID: 0002_trov_ratings
Revises: 0001_initial
Create Date: 2026-05-23

This migration:
1. Replaces the old `ratings` table with the structured version
2. Adds `embedding_status` to candidate_profiles
3. Adds `is_verified` to employer_profiles
4. Adds `is_active` to job_searches
5. Adds `last_activity_at` and `rating_requested` to conversations
6. Creates indexes for rating lookups
"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0002_trov_ratings"
down_revision: str | Sequence[str] | None = "0001_initial"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # 1. Drop old ratings table (simplified schema from 0001)
    op.drop_table("ratings")

    # 2. Create new structured ratings table
    op.create_table(
        "ratings",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("conversation_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False),
        sa.Column("rater_user_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("users.id"), nullable=False),
        sa.Column("rated_user_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("users.id"), nullable=False),
        sa.Column("rater_role", sa.String(16), nullable=False),
        sa.Column("score", sa.Integer, nullable=False),
        # Candidate → Employer categories
        sa.Column("category_paid_on_time", sa.Boolean, nullable=True),
        sa.Column("category_conditions_match", sa.Boolean, nullable=True),
        sa.Column("category_communication", sa.Boolean, nullable=True),
        # Employer → Candidate categories
        sa.Column("category_showed_up", sa.Boolean, nullable=True),
        sa.Column("category_skills_match", sa.Boolean, nullable=True),
        sa.Column("category_professional", sa.Boolean, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        # One rating per conversation per rater
        sa.UniqueConstraint("conversation_id", "rater_user_id", name="uq_rating_per_conversation"),
    )

    # Rating lookup indexes
    op.create_index("idx_ratings_rated_user", "ratings", ["rated_user_id"])
    op.create_index("idx_ratings_conversation", "ratings", ["conversation_id"])
    op.create_index("idx_ratings_rater", "ratings", ["rater_user_id"])

    # 3. Add embedding_status to candidate_profiles
    op.add_column("candidate_profiles",
                  sa.Column("embedding_status", sa.String(16), nullable=False, server_default="pending"))

    # 4. Add is_verified to employer_profiles
    op.add_column("employer_profiles",
                  sa.Column("is_verified", sa.Boolean, nullable=False, server_default=sa.false()))

    # 5. Add is_active to job_searches
    op.add_column("job_searches",
                  sa.Column("is_active", sa.Boolean, nullable=False, server_default=sa.true()))

    # 6. Add conversation metadata
    op.add_column("conversations",
                  sa.Column("last_activity_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("conversations",
                  sa.Column("rating_requested", sa.Boolean, nullable=False, server_default=sa.false()))

    # 7. Revoke UPDATE/DELETE on ratings for the application role
    op.execute("REVOKE UPDATE, DELETE ON ratings FROM trov")


def downgrade() -> None:
    # Re-grant permissions
    op.execute("GRANT UPDATE, DELETE ON ratings TO trov")

    # Remove new columns from conversations
    op.drop_column("conversations", "rating_requested")
    op.drop_column("conversations", "last_activity_at")

    # Remove is_active from job_searches
    op.drop_column("job_searches", "is_active")

    # Remove is_verified from employer_profiles
    op.drop_column("employer_profiles", "is_verified")

    # Remove embedding_status from candidate_profiles
    op.drop_column("candidate_profiles", "embedding_status")

    # Drop new ratings indexes
    op.drop_index("idx_ratings_rater")
    op.drop_index("idx_ratings_conversation")
    op.drop_index("idx_ratings_rated_user")

    # Drop new ratings table
    op.drop_table("ratings")

    # Recreate old simplified ratings table
    op.create_table(
        "ratings",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("rater_user_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("users.id"), nullable=False),
        sa.Column("rated_user_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("users.id"), nullable=False),
        sa.Column("score", sa.Integer, nullable=False),
        sa.Column("comment", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
