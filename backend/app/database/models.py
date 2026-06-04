"""
SQLAlchemy ORM models for the Arkitect database.

Tables:
  - users     — synced from Supabase Auth
  - workflows — generated execution plans (response stored as JSONB)
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Index,
    String,
    Text,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from app.database.db import Base


def _utcnow() -> datetime:
    """Return timezone-aware UTC now."""
    return datetime.now(timezone.utc)


class User(Base):
    """
    Application user — synced from Supabase Auth on first login.

    The `id` matches the Supabase Auth UID so we can correlate JWTs
    with database records without an extra lookup table.
    """

    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
    )
    email = Column(String(255), unique=True, nullable=False, index=True)
    full_name = Column(String(255), nullable=False, server_default="")
    avatar_url = Column(Text, nullable=False, server_default="")
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=_utcnow,
        server_default=text("now()"),
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=_utcnow,
        server_default=text("now()"),
        onupdate=_utcnow,
    )

    # Relationships
    workflows = relationship(
        "Workflow",
        back_populates="owner",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<User {self.email}>"


class Workflow(Base):
    """
    A generated workflow / execution plan.

    Design decisions:
    - `response_data` (JSONB) stores the full WorkflowResponse as a JSON
      blob.  This avoids 7+ join tables for deliverables, tools, steps,
      etc.  Correct for a read-heavy, write-once workload.
    - Extracted `goal`, `domain`, `complexity`, `estimated_time` as
      indexed top-level columns for filtering and searching.
    - `deleted_at` enables soft-delete — workflows can be recovered.
    """

    __tablename__ = "workflows"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    goal = Column(Text, nullable=False)
    domain = Column(String(100), nullable=False, server_default="General")
    complexity = Column(String(10), nullable=False, server_default="Medium")
    estimated_time = Column(String(50), nullable=False, server_default="")
    response_data = Column(JSONB, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=_utcnow,
        server_default=text("now()"),
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=_utcnow,
        server_default=text("now()"),
        onupdate=_utcnow,
    )
    deleted_at = Column(
        DateTime(timezone=True),
        nullable=True,
        default=None,
    )

    # Relationships
    owner = relationship("User", back_populates="workflows")

    # Indexes
    __table_args__ = (
        Index("idx_workflows_user_id", "user_id"),
        Index("idx_workflows_created_at", "created_at"),
        Index("idx_workflows_user_active", "user_id", "deleted_at"),
    )

    def __repr__(self) -> str:
        return f"<Workflow {self.id} goal={self.goal[:40]!r}>"
