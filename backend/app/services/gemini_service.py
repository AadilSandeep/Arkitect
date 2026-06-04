"""
High-level Gemini integration service.

Orchestrates the full Gemini workflow:
  1. Build prompt from templates
  2. Derive JSON schema from Pydantic models
  3. Call GeminiClient
  4. Validate and repair the response
  5. Return a WorkflowResponse or raise

This is the only class the orchestrator needs to interact with.
"""

import logging

from app.config import settings
from app.integrations.exceptions import (
    GeminiError,
    GeminiValidationError,
)
from app.integrations.gemini_client import GeminiClient
from app.schemas.response import WorkflowResponse
from app.services.prompts.gemini_prompts import SYSTEM_INSTRUCTION, build_user_prompt
from app.services.validators import ResponseValidator

logger = logging.getLogger(__name__)


class GeminiService:
    """
    High-level service for generating workflows via Gemini.

    Combines prompt construction, API transport, and response
    validation into a single generate_workflow() call.
    """

    def __init__(self) -> None:
        self._client = GeminiClient()
        self._validator = ResponseValidator()
        self._response_schema = self._build_response_schema()

    def generate_workflow(self, user_input: str) -> WorkflowResponse:
        """
        Generate a complete workflow via Gemini.

        Steps:
          1. Build user prompt from template
          2. Call Gemini with JSON schema constraint
          3. Validate response against business rules
          4. Attempt repair if validation finds fixable issues
          5. Parse into WorkflowResponse

        Args:
            user_input: Raw goal string from the user.

        Returns:
            Validated WorkflowResponse.

        Raises:
            GeminiError: If Gemini call fails after retries.
            GeminiValidationError: If response is invalid and unrepairable.
        """
        # Step 1: Build prompt
        user_prompt = build_user_prompt(user_input)
        logger.info("Calling Gemini for goal: %s", user_input[:80])

        # Step 2: Call Gemini
        raw_data = self._client.generate(
            user_prompt=user_prompt,
            system_instruction=SYSTEM_INSTRUCTION,
            response_schema=self._response_schema,
        )

        # Inject user_input into goal (Gemini may echo it, but ensure it)
        if isinstance(raw_data.get("goal"), dict):
            raw_data["goal"]["user_input"] = user_input.strip()

        # Step 3: Validate
        validation_result = self._validator.validate(raw_data)

        if not validation_result.is_valid:
            # Check if all errors are repairable
            fatal_issues = [
                i for i in validation_result.issues
                if i.level == "error" and not i.repairable
            ]

            if fatal_issues:
                issue_msgs = [f"{i.field}: {i.message}" for i in fatal_issues]
                logger.error("Fatal validation issues: %s", issue_msgs)
                raise GeminiValidationError(
                    f"Response failed validation with {len(fatal_issues)} fatal issues",
                    raw_data=raw_data,
                    issues=issue_msgs,
                )

        # Step 4: Repair fixable issues
        repairable = [i for i in validation_result.issues if i.repairable]
        if repairable:
            logger.info("Repairing %d fixable issues", len(repairable))
            raw_data = self._validator.repair(raw_data, repairable)

        # Step 5: Parse into Pydantic model
        try:
            response = self._validator.parse_response(raw_data)
            logger.info(
                "Gemini workflow generated — domain=%s, steps=%d, tools=%d",
                response.goal.domain,
                len(response.workflow),
                len(response.recommended_tools),
            )
            return response

        except Exception as exc:
            logger.error("Pydantic parsing failed after validation: %s", exc)
            raise GeminiValidationError(
                f"Response parsing failed: {exc}",
                raw_data=raw_data,
                issues=[str(exc)],
            ) from exc

    # ------------------------------------------------------------------
    # Schema builder
    # ------------------------------------------------------------------

    @staticmethod
    def _build_response_schema() -> dict:
        """
        Build the JSON schema from the WorkflowResponse Pydantic model.

        This schema is passed to Gemini via response_schema to constrain
        its output structure, saving ~500 tokens of prompt space.
        """
        schema = WorkflowResponse.model_json_schema()
        logger.debug("Built response schema with %d keys", len(schema))
        return schema
