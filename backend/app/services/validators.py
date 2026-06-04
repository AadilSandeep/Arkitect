"""
Response validation and repair layer for Gemini outputs.

Performs three levels of validation beyond Pydantic type checking:
  1. Schema validation — Pydantic model parsing
  2. Business rule validation — sequential IDs, enum values, bounds
  3. Quality validation — minimum/maximum counts, completeness

Also provides auto-repair for common fixable issues (e.g., misnumbered
steps, missing defaults).
"""

import logging
from dataclasses import dataclass, field

from app.schemas.response import (
    AlternativeWorkflows,
    Complexity,
    Deliverable,
    Goal,
    KnowledgeAreas,
    RecommendedTool,
    ToolCategory,
    WorkflowResponse,
    WorkflowStep,
)

logger = logging.getLogger(__name__)


# --------------------------------------------------------------------------
# Result containers
# --------------------------------------------------------------------------

@dataclass
class ValidationIssue:
    """A single validation issue found in the response."""
    level: str          # "error" | "warning"
    field: str          # e.g., "workflow[2].step_number"
    message: str        # Human-readable description
    repairable: bool    # Whether auto-repair can fix this


@dataclass
class ValidationResult:
    """Aggregated result of all validation checks."""
    is_valid: bool = True
    issues: list[ValidationIssue] = field(default_factory=list)

    def add(self, issue: ValidationIssue) -> None:
        self.issues.append(issue)
        if issue.level == "error":
            self.is_valid = False


# --------------------------------------------------------------------------
# Bounds constants
# --------------------------------------------------------------------------

_DELIVERABLE_BOUNDS = (3, 8)
_TOOL_BOUNDS = (4, 10)
_WORKFLOW_BOUNDS = (4, 12)
_VALID_COMPLEXITIES = {"Low", "Medium", "High"}
_VALID_CATEGORIES = {cat.value for cat in ToolCategory}


# --------------------------------------------------------------------------
# Validator
# --------------------------------------------------------------------------

class ResponseValidator:
    """
    Multi-level validator for Gemini workflow responses.

    Validates structure, business rules, and quality constraints.
    Can auto-repair common issues when possible.
    """

    def validate(self, data: dict) -> ValidationResult:
        """
        Run all validation checks on a raw Gemini response dict.

        Args:
            data: Parsed JSON dict from Gemini.

        Returns:
            ValidationResult with is_valid flag and any issues found.
        """
        result = ValidationResult()

        self._check_required_keys(data, result)
        self._check_goal(data.get("goal", {}), result)
        self._check_deliverables(data.get("deliverables", []), result)
        self._check_tools(data.get("recommended_tools", []), result)
        self._check_workflow(data.get("workflow", []), result)
        self._check_alternatives(data.get("alternative_workflows", {}), result)
        self._check_knowledge(data.get("knowledge_areas", {}), result)
        self._check_time(data.get("estimated_time", ""), result)

        return result

    def repair(self, data: dict, issues: list[ValidationIssue]) -> dict:
        """
        Attempt to auto-repair fixable issues in the response data.

        Modifies and returns the data dict in place.

        Args:
            data: Raw Gemini response dict.
            issues: List of validation issues to attempt fixing.

        Returns:
            The (possibly modified) data dict.
        """
        repaired = dict(data)

        for issue in issues:
            if not issue.repairable:
                continue

            try:
                if "step_number" in issue.field:
                    repaired = self._repair_step_numbers(repaired)
                elif "deliverable" in issue.field and "id" in issue.message.lower():
                    repaired = self._repair_deliverable_ids(repaired)
                elif "complexity" in issue.field:
                    repaired = self._repair_complexity(repaired)
                elif "category" in issue.field:
                    repaired = self._repair_tool_categories(repaired)
                elif "bounds" in issue.message.lower():
                    repaired = self._repair_bounds(repaired)
            except Exception as exc:
                logger.warning("Repair failed for %s: %s", issue.field, exc)

        return repaired

    def parse_response(self, data: dict) -> WorkflowResponse:
        """
        Parse a validated dict into a WorkflowResponse Pydantic model.

        Args:
            data: Validated (and possibly repaired) dict.

        Returns:
            WorkflowResponse model instance.

        Raises:
            ValueError: If Pydantic parsing fails.
        """
        return WorkflowResponse.model_validate(data)

    # ------------------------------------------------------------------
    # Required keys check
    # ------------------------------------------------------------------

    def _check_required_keys(self, data: dict, result: ValidationResult) -> None:
        required = {
            "goal", "deliverables", "recommended_tools", "workflow",
            "alternative_workflows", "knowledge_areas", "estimated_time",
        }
        missing = required - set(data.keys())
        for key in missing:
            result.add(ValidationIssue(
                level="error",
                field=key,
                message=f"Required top-level key '{key}' is missing",
                repairable=False,
            ))

    # ------------------------------------------------------------------
    # Goal validation
    # ------------------------------------------------------------------

    def _check_goal(self, goal: dict, result: ValidationResult) -> None:
        if not isinstance(goal, dict):
            result.add(ValidationIssue(
                level="error", field="goal",
                message="goal must be a dict", repairable=False,
            ))
            return

        if not goal.get("user_input", "").strip():
            result.add(ValidationIssue(
                level="error", field="goal.user_input",
                message="user_input is empty", repairable=False,
            ))

        complexity = goal.get("complexity", "")
        if complexity not in _VALID_COMPLEXITIES:
            result.add(ValidationIssue(
                level="warning", field="goal.complexity",
                message=f"Invalid complexity '{complexity}', expected one of {_VALID_COMPLEXITIES}",
                repairable=True,
            ))

    # ------------------------------------------------------------------
    # Deliverables validation
    # ------------------------------------------------------------------

    def _check_deliverables(self, deliverables: list, result: ValidationResult) -> None:
        if not isinstance(deliverables, list):
            result.add(ValidationIssue(
                level="error", field="deliverables",
                message="deliverables must be a list", repairable=False,
            ))
            return

        count = len(deliverables)
        lo, hi = _DELIVERABLE_BOUNDS
        if count < lo or count > hi:
            result.add(ValidationIssue(
                level="warning", field="deliverables",
                message=f"Deliverable count {count} out of bounds [{lo}, {hi}]",
                repairable=True,
            ))

        # Check sequential IDs
        ids = [d.get("id") for d in deliverables if isinstance(d, dict)]
        expected = list(range(1, len(ids) + 1))
        if ids != expected:
            result.add(ValidationIssue(
                level="warning", field="deliverables[*].id",
                message=f"Deliverable IDs {ids} are not sequential {expected}",
                repairable=True,
            ))

    # ------------------------------------------------------------------
    # Tools validation
    # ------------------------------------------------------------------

    def _check_tools(self, tools: list, result: ValidationResult) -> None:
        if not isinstance(tools, list):
            result.add(ValidationIssue(
                level="error", field="recommended_tools",
                message="recommended_tools must be a list", repairable=False,
            ))
            return

        count = len(tools)
        lo, hi = _TOOL_BOUNDS
        if count < lo or count > hi:
            result.add(ValidationIssue(
                level="warning", field="recommended_tools",
                message=f"Tool count {count} out of bounds [{lo}, {hi}]",
                repairable=True,
            ))

        for i, tool in enumerate(tools):
            if not isinstance(tool, dict):
                continue
            cat = tool.get("category", "")
            if cat not in _VALID_CATEGORIES:
                result.add(ValidationIssue(
                    level="warning", field=f"recommended_tools[{i}].category",
                    message=f"Invalid category '{cat}'",
                    repairable=True,
                ))

    # ------------------------------------------------------------------
    # Workflow validation
    # ------------------------------------------------------------------

    def _check_workflow(self, workflow: list, result: ValidationResult) -> None:
        if not isinstance(workflow, list):
            result.add(ValidationIssue(
                level="error", field="workflow",
                message="workflow must be a list", repairable=False,
            ))
            return

        count = len(workflow)
        lo, hi = _WORKFLOW_BOUNDS
        if count < lo or count > hi:
            result.add(ValidationIssue(
                level="warning", field="workflow",
                message=f"Workflow step count {count} out of bounds [{lo}, {hi}]",
                repairable=True,
            ))

        # Check sequential step_numbers
        step_nums = [
            s.get("step_number") for s in workflow if isinstance(s, dict)
        ]
        expected = list(range(1, len(step_nums) + 1))
        if step_nums != expected:
            result.add(ValidationIssue(
                level="warning", field="workflow[*].step_number",
                message=f"Step numbers {step_nums} are not sequential {expected}",
                repairable=True,
            ))

    # ------------------------------------------------------------------
    # Alternative workflows validation
    # ------------------------------------------------------------------

    def _check_alternatives(self, alternatives: dict, result: ValidationResult) -> None:
        if not isinstance(alternatives, dict):
            result.add(ValidationIssue(
                level="error", field="alternative_workflows",
                message="alternative_workflows must be a dict", repairable=False,
            ))
            return

        required_strategies = {"fastest", "cheapest", "highest_quality", "beginner_friendly"}
        missing = required_strategies - set(alternatives.keys())
        for strategy in missing:
            result.add(ValidationIssue(
                level="error", field=f"alternative_workflows.{strategy}",
                message=f"Missing alternative strategy '{strategy}'",
                repairable=False,
            ))

    # ------------------------------------------------------------------
    # Knowledge areas validation
    # ------------------------------------------------------------------

    def _check_knowledge(self, knowledge: dict, result: ValidationResult) -> None:
        if not isinstance(knowledge, dict):
            result.add(ValidationIssue(
                level="error", field="knowledge_areas",
                message="knowledge_areas must be a dict", repairable=False,
            ))
            return

        for level in ("high", "medium", "low"):
            items = knowledge.get(level, [])
            if not isinstance(items, list) or len(items) == 0:
                result.add(ValidationIssue(
                    level="warning", field=f"knowledge_areas.{level}",
                    message=f"Knowledge area '{level}' is empty",
                    repairable=False,
                ))

    # ------------------------------------------------------------------
    # Time estimate validation
    # ------------------------------------------------------------------

    def _check_time(self, time_str: str | dict, result: ValidationResult) -> None:
        if not isinstance(time_str, str) or not time_str.strip():
            result.add(ValidationIssue(
                level="warning", field="estimated_time",
                message="estimated_time is empty or not a string",
                repairable=False,
            ))

    # ------------------------------------------------------------------
    # Repair helpers
    # ------------------------------------------------------------------

    def _repair_step_numbers(self, data: dict) -> dict:
        """Re-number workflow steps sequentially starting from 1."""
        workflow = data.get("workflow", [])
        for idx, step in enumerate(workflow):
            if isinstance(step, dict):
                step["step_number"] = idx + 1
        logger.info("Repaired: re-numbered %d workflow steps", len(workflow))
        return data

    def _repair_deliverable_ids(self, data: dict) -> dict:
        """Re-number deliverable IDs sequentially starting from 1."""
        deliverables = data.get("deliverables", [])
        for idx, d in enumerate(deliverables):
            if isinstance(d, dict):
                d["id"] = idx + 1
        logger.info("Repaired: re-numbered %d deliverable IDs", len(deliverables))
        return data

    def _repair_complexity(self, data: dict) -> dict:
        """Default invalid complexity to 'Medium'."""
        goal = data.get("goal", {})
        if isinstance(goal, dict) and goal.get("complexity") not in _VALID_COMPLEXITIES:
            goal["complexity"] = "Medium"
            logger.info("Repaired: defaulted complexity to 'Medium'")
        return data

    def _repair_tool_categories(self, data: dict) -> dict:
        """Default invalid tool categories to 'Other'."""
        tools = data.get("recommended_tools", [])
        for tool in tools:
            if isinstance(tool, dict) and tool.get("category") not in _VALID_CATEGORIES:
                old = tool["category"]
                tool["category"] = "Other"
                logger.info("Repaired: tool category '%s' → 'Other'", old)
        return data

    def _repair_bounds(self, data: dict) -> dict:
        """Trim lists that exceed upper bounds."""
        deliverables = data.get("deliverables", [])
        if len(deliverables) > _DELIVERABLE_BOUNDS[1]:
            data["deliverables"] = deliverables[:_DELIVERABLE_BOUNDS[1]]
            logger.info("Repaired: trimmed deliverables to %d", _DELIVERABLE_BOUNDS[1])

        tools = data.get("recommended_tools", [])
        if len(tools) > _TOOL_BOUNDS[1]:
            data["recommended_tools"] = tools[:_TOOL_BOUNDS[1]]
            logger.info("Repaired: trimmed tools to %d", _TOOL_BOUNDS[1])

        workflow = data.get("workflow", [])
        if len(workflow) > _WORKFLOW_BOUNDS[1]:
            data["workflow"] = workflow[:_WORKFLOW_BOUNDS[1]]
            logger.info("Repaired: trimmed workflow to %d", _WORKFLOW_BOUNDS[1])

        return data
