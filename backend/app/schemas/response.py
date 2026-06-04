"""
Pydantic schemas matching the Arkitect system contract.

This module defines every data model used in the API request/response cycle.
All field names and structures conform to SYSTEM_CONTRACT.md.
"""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class Complexity(str, Enum):
    """Goal complexity levels."""
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class ToolCategory(str, Enum):
    """Standardized tool categories."""
    AI = "AI"
    DEVELOPMENT = "Development"
    DESIGN = "Design"
    PRODUCTIVITY = "Productivity"
    MARKETING = "Marketing"
    OTHER = "Other"


# ---------------------------------------------------------------------------
# Core Models
# ---------------------------------------------------------------------------

class Goal(BaseModel):
    """
    Analyzed understanding of the user's objective.

    Represents the output of the GoalAnalyzer service, containing the
    original user input plus extracted domain, goal type, and complexity.
    """
    user_input: str = Field(
        ...,
        min_length=1,
        description="The original natural-language goal from the user.",
    )
    domain: str = Field(
        default="General",
        description="Detected knowledge domain (e.g., 'Web Development').",
    )
    goal_type: str = Field(
        default="Custom Project",
        description="Classified goal type (e.g., 'Portfolio Website').",
    )
    complexity: Complexity = Field(
        default=Complexity.MEDIUM,
        description="Estimated complexity: Low, Medium, or High.",
    )

    @field_validator("user_input")
    @classmethod
    def user_input_not_blank(cls, v: str) -> str:
        stripped = v.strip()
        if not stripped:
            raise ValueError("user_input must not be blank")
        return stripped


class Deliverable(BaseModel):
    """
    A major output required to achieve the goal.

    Deliverables serve as workflow anchors — each one maps to one or more
    workflow steps.
    """
    id: int = Field(..., ge=1, description="Unique sequential identifier.")
    title: str = Field(..., min_length=1, description="Short deliverable name.")
    description: str = Field(
        ..., min_length=1, description="What this deliverable entails."
    )


class RecommendedTool(BaseModel):
    """
    A tool recommended for achieving the goal.

    Each recommendation includes the tool name, its category, and the
    rationale for why it's relevant.
    """
    name: str = Field(..., min_length=1, description="Tool name (e.g., 'Figma').")
    category: ToolCategory = Field(
        ..., description="Tool category: AI, Development, Design, etc."
    )
    reason: str = Field(
        ..., min_length=1, description="Why this tool is recommended."
    )


class WorkflowStep(BaseModel):
    """
    A single actionable step in the execution workflow.

    Steps are sequential and may include an AI prompt when the tool is
    an AI assistant.
    """
    step_number: int = Field(..., ge=1, description="Sequential step number.")
    title: str = Field(..., min_length=1, description="Step title.")
    tool: str = Field(..., min_length=1, description="Tool to use for this step.")
    why: str = Field(
        ..., min_length=1, description="Why this tool is used for this step."
    )
    what_to_do: str = Field(
        ..., min_length=1, description="Actionable instruction."
    )
    prompt: str = Field(
        default="",
        description="Ready-to-use AI prompt (empty string if not applicable).",
    )
    expected_result: str = Field(
        ..., min_length=1, description="What the user should have after this step."
    )


# ---------------------------------------------------------------------------
# Composite Models
# ---------------------------------------------------------------------------

class AlternativeWorkflow(BaseModel):
    """A single alternative approach for achieving the goal."""
    summary: str = Field(
        ..., min_length=1, description="Brief description of this approach."
    )
    tools: list[str] = Field(
        default_factory=list, description="Tools used in this approach."
    )


class AlternativeWorkflows(BaseModel):
    """
    Four alternative strategies for achieving the same goal.

    Each strategy optimises for a different axis: speed, cost, quality,
    or accessibility.
    """
    fastest: AlternativeWorkflow = Field(
        ..., description="Speed-optimized approach."
    )
    cheapest: AlternativeWorkflow = Field(
        ..., description="Cost-optimized approach."
    )
    highest_quality: AlternativeWorkflow = Field(
        ..., description="Quality-optimized approach."
    )
    beginner_friendly: AlternativeWorkflow = Field(
        ..., description="Accessibility-optimized approach."
    )


class KnowledgeAreas(BaseModel):
    """
    Knowledge domains relevant to the goal, grouped by importance.

    These are informational only — no learning roadmap is generated.
    """
    high: list[str] = Field(
        default_factory=list, description="High-importance knowledge areas."
    )
    medium: list[str] = Field(
        default_factory=list, description="Medium-importance knowledge areas."
    )
    low: list[str] = Field(
        default_factory=list, description="Low-importance knowledge areas."
    )


# ---------------------------------------------------------------------------
# Request / Response
# ---------------------------------------------------------------------------

class WorkflowRequest(BaseModel):
    """Incoming request to generate a workflow."""
    goal: str = Field(
        ...,
        min_length=1,
        description="Natural-language goal from the user.",
        examples=["Build a portfolio website", "Launch a SaaS startup"],
    )

    @field_validator("goal")
    @classmethod
    def goal_not_blank(cls, v: str) -> str:
        stripped = v.strip()
        if not stripped:
            raise ValueError("goal must not be blank")
        return stripped


class WorkflowResponse(BaseModel):
    """
    Top-level API response matching the system contract.

    Contains the complete execution plan: analyzed goal, deliverables,
    tools, workflow steps, alternatives, knowledge areas, and time estimate.
    """
    goal: Goal
    deliverables: list[Deliverable] = Field(default_factory=list)
    recommended_tools: list[RecommendedTool] = Field(default_factory=list)
    workflow: list[WorkflowStep] = Field(default_factory=list)
    alternative_workflows: AlternativeWorkflows
    knowledge_areas: KnowledgeAreas = Field(default_factory=KnowledgeAreas)
    estimated_time: str = Field(
        default="", description="Approximate completion time."
    )