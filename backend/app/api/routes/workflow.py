"""
Workflow API Routes.

Exposes the workflow generation endpoint and health check.
"""

import logging
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.database.db import get_db
from app.database.models import User, Workflow
from app.schemas.response import WorkflowRequest, WorkflowResponse
from app.services.orchestrator import WorkflowOrchestrator

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/v1/workflow",
    tags=["workflow"],
)

# Single orchestrator instance (stateless, safe to share)
_orchestrator = WorkflowOrchestrator()


# ---------------------------------------------------------------------------
# Response schema — extends WorkflowResponse with the saved workflow ID
# ---------------------------------------------------------------------------

class SavedWorkflowResponse(BaseModel):
    """WorkflowResponse enriched with the saved database record ID."""
    id: uuid.UUID = Field(..., description="Saved workflow UUID")
    workflow_data: WorkflowResponse = Field(
        ..., description="The full generated workflow"
    )


@router.post(
    "/generate",
    response_model=SavedWorkflowResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate a workflow from a goal",
    description=(
        "Accepts a natural-language goal and returns a complete execution plan "
        "including deliverables, tool recommendations, workflow steps with AI "
        "prompts, alternative approaches, knowledge areas, and time estimate. "
        "The generated workflow is automatically saved to the user's account."
    ),
)
async def generate_workflow(
    request: WorkflowRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> SavedWorkflowResponse:
    """
    Generate a complete workflow for the given goal.

    - **goal**: A natural-language description of what the user wants to achieve.

    Returns a structured execution plan conforming to the system contract,
    along with the saved workflow UUID.
    """
    try:
        response = _orchestrator.process(request)
    except ValueError as exc:
        logger.error("Validation error during workflow generation: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        logger.exception("Unexpected error during workflow generation")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal error occurred while generating the workflow.",
        ) from exc

    # Save to database
    response_dict = response.model_dump(mode="json")

    workflow_record = Workflow(
        user_id=user.id,
        goal=response.goal.user_input,
        domain=response.goal.domain,
        complexity=response.goal.complexity.value,
        estimated_time=response.estimated_time,
        response_data=response_dict,
    )
    db.add(workflow_record)
    await db.flush()
    await db.refresh(workflow_record)

    logger.info(
        "Workflow saved: id=%s, user=%s, domain=%s",
        workflow_record.id,
        user.id,
        response.goal.domain,
    )

    return SavedWorkflowResponse(
        id=workflow_record.id,
        workflow_data=response,
    )


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    summary="Health check",
    description="Returns the health status of the workflow service.",
)
async def health_check() -> dict[str, str]:
    """Check if the workflow service is running."""
    return {"status": "healthy", "service": "workflow"}
