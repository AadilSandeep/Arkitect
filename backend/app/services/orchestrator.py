"""
Workflow Orchestrator — the pipeline coordinator.

Manages the end-to-end workflow generation process. Tries the
AI-powered Gemini path first; falls back to the deterministic
knowledge-base pipeline on any failure.
"""

import logging

from app.config import settings
from app.integrations.exceptions import GeminiError
from app.schemas.response import WorkflowRequest, WorkflowResponse
from app.services.goal_analysis.analyzer import GoalAnalyzer
from app.services.deliverables.detector import DeliverableDetector
from app.services.recommendations.recommender import ToolRecommender
from app.services.workflow.generator import WorkflowGenerator
from app.services.prompts.prompt_generator import PromptGenerator
from app.services.alternatives.alternative_generator import AlternativeGenerator
from app.services.knowledge.knowledge_generator import KnowledgeGenerator
from app.services.time_estimator import TimeEstimator

logger = logging.getLogger(__name__)


class WorkflowOrchestrator:
    """
    Coordinates workflow generation with AI-first, deterministic-fallback.

    Pipeline:
      PRIMARY  → GeminiService (single API call, structured JSON)
      FALLBACK → Deterministic pipeline (8 knowledge-base services)

    The deterministic fallback guarantees the user always gets a valid
    response, even when the AI path is unavailable or produces bad output.
    """

    def __init__(self) -> None:
        # AI-powered path (lazy import to avoid import errors when disabled)
        self._gemini_service = None
        if settings.GEMINI_ENABLED and settings.GEMINI_API_KEY:
            try:
                from app.services.gemini_service import GeminiService
                self._gemini_service = GeminiService()
                logger.info("Gemini integration enabled (model=%s)", settings.GEMINI_MODEL)
            except Exception as exc:
                logger.warning("Failed to initialize GeminiService: %s", exc)

        # Deterministic path (always available as fallback)
        self.goal_analyzer = GoalAnalyzer()
        self.deliverable_detector = DeliverableDetector()
        self.tool_recommender = ToolRecommender()
        self.workflow_generator = WorkflowGenerator()
        self.prompt_generator = PromptGenerator()
        self.alternative_generator = AlternativeGenerator()
        self.knowledge_generator = KnowledgeGenerator()
        self.time_estimator = TimeEstimator()

    def process(self, request: WorkflowRequest) -> WorkflowResponse:
        """
        Execute the workflow generation pipeline.

        Tries Gemini first; falls back to deterministic on any failure.

        Args:
            request: Incoming WorkflowRequest with a goal string.

        Returns:
            Complete WorkflowResponse conforming to the system contract.
        """
        # --- Primary path: Gemini AI ---
        if self._gemini_service is not None:
            try:
                logger.info("Attempting Gemini-powered generation")
                response = self._gemini_service.generate_workflow(request.goal)
                logger.info("Gemini generation succeeded")
                return response
            except GeminiError as exc:
                logger.warning(
                    "Gemini failed (%s: %s), falling back to deterministic pipeline",
                    type(exc).__name__,
                    exc,
                )
            except Exception as exc:
                logger.warning(
                    "Unexpected error in Gemini path (%s), falling back to deterministic",
                    exc,
                )

        # --- Fallback path: Deterministic pipeline ---
        logger.info("Using deterministic pipeline for goal: %s", request.goal[:80])
        return self._deterministic_pipeline(request)

    def _deterministic_pipeline(self, request: WorkflowRequest) -> WorkflowResponse:
        """
        Execute the full deterministic pipeline using knowledge-base services.

        This is the original pipeline logic, preserved unchanged as the
        reliability fallback.

        Args:
            request: Incoming WorkflowRequest with a goal string.

        Returns:
            Complete WorkflowResponse conforming to the system contract.

        Raises:
            ValueError: If any service produces invalid output.
        """
        user_input = request.goal
        logger.info("Starting deterministic pipeline for goal: %s", user_input[:80])

        # Step 1: Analyze the goal
        logger.debug("Step 1/8: Goal Analysis")
        goal = self.goal_analyzer.analyze(user_input)

        # Step 2: Detect deliverables
        logger.debug("Step 2/8: Deliverable Detection")
        deliverables = self.deliverable_detector.detect(goal)

        # Step 3: Recommend tools
        logger.debug("Step 3/8: Tool Recommendation")
        tools = self.tool_recommender.recommend(goal, deliverables)

        # Step 4: Generate workflow steps
        logger.debug("Step 4/8: Workflow Generation")
        workflow_steps = self.workflow_generator.generate(goal, deliverables, tools)

        # Step 5: Enrich steps with AI prompts
        logger.debug("Step 5/8: Prompt Generation")
        workflow_steps = self.prompt_generator.generate(workflow_steps, goal)

        # Step 6: Generate alternative workflows
        logger.debug("Step 6/8: Alternative Workflows")
        alternatives = self.alternative_generator.generate(goal)

        # Step 7: Generate knowledge areas
        logger.debug("Step 7/8: Knowledge Areas")
        knowledge = self.knowledge_generator.generate(goal)

        # Step 8: Estimate time
        logger.debug("Step 8/8: Time Estimation")
        estimated_time = self.time_estimator.estimate(goal, deliverables)

        logger.info(
            "Deterministic pipeline complete — domain=%s, deliverables=%d, tools=%d, steps=%d",
            goal.domain,
            len(deliverables),
            len(tools),
            len(workflow_steps),
        )

        return WorkflowResponse(
            goal=goal,
            deliverables=deliverables,
            recommended_tools=tools,
            workflow=workflow_steps,
            alternative_workflows=alternatives,
            knowledge_areas=knowledge,
            estimated_time=estimated_time,
        )
