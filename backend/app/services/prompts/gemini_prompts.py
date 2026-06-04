"""
Prompt templates for the Gemini integration.

Contains the system instruction and user prompt template used to
generate the complete WorkflowResponse in a single API call.

Design principles:
  - Compact prompts to minimize input token cost (~270 tokens total).
  - Explicit "JSON only" rules to prevent markdown/prose leakage.
  - Schema details are passed via response_schema, NOT in the prompt.
"""

# --------------------------------------------------------------------------
# System instruction (fixed, sent once per request)
# --------------------------------------------------------------------------

SYSTEM_INSTRUCTION: str = (
    "You are Arkitect, an AI-powered workflow architect. "
    "You analyze user goals and produce structured execution plans.\n\n"
    "RULES:\n"
    "1. Return ONLY valid JSON. No markdown. No code fences. No explanatory text.\n"
    "2. Every field in the schema MUST be populated. "
    'Use "" for empty strings, [] for empty arrays.\n'
    "3. Workflow steps MUST be sequential and actionable.\n"
    "4. Tool recommendations MUST include real, existing tools.\n"
    "5. Prompts in workflow steps should be ready-to-use with the specified AI tool.\n"
    "6. Alternative workflows must represent genuinely different approaches.\n"
    "7. Knowledge areas must be relevant to the specific goal, not generic.\n"
    "8. Time estimates should be realistic for a motivated individual."
)

# --------------------------------------------------------------------------
# User prompt template (dynamic — {user_input} is substituted per request)
# --------------------------------------------------------------------------

USER_PROMPT_TEMPLATE: str = (
    "Analyze the following goal and generate a complete execution plan.\n\n"
    'USER GOAL: "{user_input}"\n\n'
    "Generate a JSON response with these sections:\n"
    "1. goal: Analyze the goal — detect domain, goal_type, "
    "complexity (Low/Medium/High)\n"
    "2. deliverables: 3-8 major outputs needed (scaled by complexity)\n"
    "3. recommended_tools: 4-10 best tools with category "
    "(AI/Development/Design/Productivity/Marketing/Other) and reason\n"
    "4. workflow: 4-12 sequential steps — each with tool, why, "
    "what_to_do, prompt (ready-to-use AI prompt or empty string), "
    "expected_result\n"
    "5. alternative_workflows: four strategies — fastest, cheapest, "
    "highest_quality, beginner_friendly — each with summary and tools list\n"
    "6. knowledge_areas: relevant skills grouped by high/medium/low importance\n"
    "7. estimated_time: realistic completion time estimate as a string"
)


def build_user_prompt(user_input: str) -> str:
    """
    Build the user prompt for a Gemini request.

    Args:
        user_input: The raw goal string from the user.

    Returns:
        Formatted prompt string with the user's goal inserted.
    """
    return USER_PROMPT_TEMPLATE.format(user_input=user_input)
