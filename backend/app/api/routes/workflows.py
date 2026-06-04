"""
Workflow CRUD routes.

Provides list, get, and delete operations for saved workflows.
The generate endpoint (which also saves) lives in workflow.py.
"""

import logging
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.database.db import get_db
from app.database.models import User, Workflow

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/v1/workflows",
    tags=["workflows"],
)


# ---------------------------------------------------------------------------
# Response schemas
# ---------------------------------------------------------------------------

class WorkflowSummary(BaseModel):
    """Lightweight workflow summary for list views."""
    id: uuid.UUID
    goal: str
    domain: str
    complexity: str
    estimated_time: str
    created_at: datetime

    model_config = {"from_attributes": True}


class WorkflowDetail(BaseModel):
    """Full workflow detail including the response data."""
    id: uuid.UUID
    goal: str
    domain: str
    complexity: str
    estimated_time: str
    response_data: dict
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class PaginatedWorkflows(BaseModel):
    """Paginated list of workflow summaries."""
    items: list[WorkflowSummary]
    total: int
    page: int
    per_page: int
    pages: int


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@router.get(
    "/",
    response_model=PaginatedWorkflows,
    summary="List workflows",
    description="List the current user's workflows, newest first.",
)
async def list_workflows(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
) -> PaginatedWorkflows:
    """List the current user's non-deleted workflows, paginated."""

    # Base filter: belongs to user, not soft-deleted
    base_filter = (
        (Workflow.user_id == user.id) & (Workflow.deleted_at.is_(None))
    )

    # Count total
    count_query = select(func.count()).select_from(Workflow).where(base_filter)
    total_result = await db.execute(count_query)
    total = total_result.scalar_one()

    # Fetch page
    offset = (page - 1) * per_page
    items_query = (
        select(Workflow)
        .where(base_filter)
        .order_by(Workflow.created_at.desc())
        .offset(offset)
        .limit(per_page)
    )
    items_result = await db.execute(items_query)
    workflows = items_result.scalars().all()

    pages = max(1, (total + per_page - 1) // per_page)

    return PaginatedWorkflows(
        items=[WorkflowSummary.model_validate(w) for w in workflows],
        total=total,
        page=page,
        per_page=per_page,
        pages=pages,
    )


@router.get(
    "/{workflow_id}",
    response_model=WorkflowDetail,
    summary="Get workflow",
    description="Get a single workflow by ID (must belong to the current user).",
)
async def get_workflow(
    workflow_id: uuid.UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> WorkflowDetail:
    """Get a single workflow (must belong to the current user)."""

    result = await db.execute(
        select(Workflow).where(
            (Workflow.id == workflow_id)
            & (Workflow.user_id == user.id)
            & (Workflow.deleted_at.is_(None))
        )
    )
    workflow = result.scalar_one_or_none()

    if workflow is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workflow not found.",
        )

    return WorkflowDetail.model_validate(workflow)


@router.delete(
    "/{workflow_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete workflow",
    description="Soft-delete a workflow (mark as deleted, recoverable).",
)
async def delete_workflow(
    workflow_id: uuid.UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    """Soft-delete a workflow (must belong to the current user)."""

    result = await db.execute(
        select(Workflow).where(
            (Workflow.id == workflow_id)
            & (Workflow.user_id == user.id)
            & (Workflow.deleted_at.is_(None))
        )
    )
    workflow = result.scalar_one_or_none()

    if workflow is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workflow not found.",
        )

    workflow.deleted_at = datetime.now(timezone.utc)
    await db.flush()
    logger.info("Soft-deleted workflow %s for user %s", workflow_id, user.id)
