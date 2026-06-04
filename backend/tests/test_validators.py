"""
Tests for the ResponseValidator.

Covers schema validation, business rule checks, quality constraints,
and the auto-repair logic for fixable issues.
"""

import pytest

from app.services.validators import ResponseValidator, ValidationResult


# --------------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------------

@pytest.fixture
def validator():
    return ResponseValidator()


@pytest.fixture
def valid_data():
    """A fully valid Gemini response dict."""
    return {
        "goal": {
            "user_input": "Build a portfolio website",
            "domain": "Web Development",
            "goal_type": "Portfolio Website",
            "complexity": "Medium",
        },
        "deliverables": [
            {"id": 1, "title": "Design", "description": "Create visual design."},
            {"id": 2, "title": "Development", "description": "Build the site."},
            {"id": 3, "title": "Testing", "description": "Test the site."},
            {"id": 4, "title": "Deployment", "description": "Deploy the site."},
        ],
        "recommended_tools": [
            {"name": "Figma", "category": "Design", "reason": "UI design tool."},
            {"name": "React", "category": "Development", "reason": "UI framework."},
            {"name": "Vercel", "category": "Development", "reason": "Hosting."},
            {"name": "ChatGPT", "category": "AI", "reason": "Code help."},
        ],
        "workflow": [
            {
                "step_number": 1,
                "title": "Plan",
                "tool": "ChatGPT",
                "why": "Planning assistance",
                "what_to_do": "Outline project structure",
                "prompt": "Help me plan a portfolio website",
                "expected_result": "Project outline",
            },
            {
                "step_number": 2,
                "title": "Design",
                "tool": "Figma",
                "why": "Design tool",
                "what_to_do": "Create mockups",
                "prompt": "",
                "expected_result": "Design mockups",
            },
            {
                "step_number": 3,
                "title": "Develop",
                "tool": "React",
                "why": "UI framework",
                "what_to_do": "Build components",
                "prompt": "",
                "expected_result": "Working components",
            },
            {
                "step_number": 4,
                "title": "Deploy",
                "tool": "Vercel",
                "why": "Easy deployment",
                "what_to_do": "Deploy to production",
                "prompt": "",
                "expected_result": "Live website",
            },
        ],
        "alternative_workflows": {
            "fastest": {"summary": "Use a website builder", "tools": ["Wix"]},
            "cheapest": {"summary": "HTML/CSS only", "tools": ["VS Code"]},
            "highest_quality": {
                "summary": "Full custom stack",
                "tools": ["React", "Tailwind"],
            },
            "beginner_friendly": {
                "summary": "No-code platform",
                "tools": ["Squarespace"],
            },
        },
        "knowledge_areas": {
            "high": ["HTML", "CSS", "Git"],
            "medium": ["JavaScript", "React"],
            "low": ["SEO", "DevOps"],
        },
        "estimated_time": "8-12 hours",
    }


# --------------------------------------------------------------------------
# Tests: Valid data passes
# --------------------------------------------------------------------------

class TestValidDataPasses:
    """Tests that a fully valid response passes all checks."""

    def test_valid_response_passes(self, validator, valid_data):
        result = validator.validate(valid_data)
        assert result.is_valid
        # May have warnings but no errors
        errors = [i for i in result.issues if i.level == "error"]
        assert len(errors) == 0

    def test_parse_valid_response(self, validator, valid_data):
        response = validator.parse_response(valid_data)
        assert response.goal.user_input == "Build a portfolio website"
        assert response.goal.domain == "Web Development"
        assert len(response.deliverables) == 4
        assert len(response.workflow) == 4


# --------------------------------------------------------------------------
# Tests: Missing required keys
# --------------------------------------------------------------------------

class TestMissingKeys:
    """Tests for missing top-level keys."""

    def test_missing_goal_key(self, validator, valid_data):
        del valid_data["goal"]
        result = validator.validate(valid_data)
        assert not result.is_valid
        assert any("goal" in i.field for i in result.issues)

    def test_missing_workflow_key(self, validator, valid_data):
        del valid_data["workflow"]
        result = validator.validate(valid_data)
        assert not result.is_valid

    def test_missing_multiple_keys(self, validator):
        result = validator.validate({})
        assert not result.is_valid
        assert len(result.issues) >= 7  # All keys missing


# --------------------------------------------------------------------------
# Tests: Goal validation
# --------------------------------------------------------------------------

class TestGoalValidation:
    """Tests for goal field validation."""

    def test_empty_user_input(self, validator, valid_data):
        valid_data["goal"]["user_input"] = ""
        result = validator.validate(valid_data)
        assert not result.is_valid

    def test_invalid_complexity(self, validator, valid_data):
        valid_data["goal"]["complexity"] = "SuperHard"
        result = validator.validate(valid_data)
        issues = [i for i in result.issues if "complexity" in i.field]
        assert len(issues) == 1
        assert issues[0].repairable


# --------------------------------------------------------------------------
# Tests: Deliverables validation
# --------------------------------------------------------------------------

class TestDeliverablesValidation:
    """Tests for deliverable list validation."""

    def test_non_sequential_ids(self, validator, valid_data):
        valid_data["deliverables"][1]["id"] = 5  # Break sequence
        result = validator.validate(valid_data)
        issues = [i for i in result.issues if "id" in i.field.lower() or "id" in i.message.lower()]
        assert len(issues) >= 1

    def test_too_few_deliverables(self, validator, valid_data):
        valid_data["deliverables"] = valid_data["deliverables"][:2]  # Only 2
        result = validator.validate(valid_data)
        issues = [i for i in result.issues if "bounds" in i.message.lower()]
        assert len(issues) >= 1

    def test_too_many_deliverables(self, validator, valid_data):
        for i in range(5, 15):
            valid_data["deliverables"].append(
                {"id": i, "title": f"Extra {i}", "description": "Extra"}
            )
        result = validator.validate(valid_data)
        issues = [i for i in result.issues if "bounds" in i.message.lower()]
        assert len(issues) >= 1


# --------------------------------------------------------------------------
# Tests: Workflow validation
# --------------------------------------------------------------------------

class TestWorkflowValidation:
    """Tests for workflow step validation."""

    def test_non_sequential_step_numbers(self, validator, valid_data):
        valid_data["workflow"][2]["step_number"] = 99  # Break sequence
        result = validator.validate(valid_data)
        issues = [i for i in result.issues if "step_number" in i.field]
        assert len(issues) >= 1
        assert issues[0].repairable

    def test_too_few_steps(self, validator, valid_data):
        valid_data["workflow"] = valid_data["workflow"][:2]  # Only 2
        result = validator.validate(valid_data)
        issues = [i for i in result.issues if "bounds" in i.message.lower()]
        assert len(issues) >= 1


# --------------------------------------------------------------------------
# Tests: Tool validation
# --------------------------------------------------------------------------

class TestToolValidation:
    """Tests for tool recommendation validation."""

    def test_invalid_category(self, validator, valid_data):
        valid_data["recommended_tools"][0]["category"] = "InvalidCategory"
        result = validator.validate(valid_data)
        issues = [i for i in result.issues if "category" in i.field]
        assert len(issues) == 1
        assert issues[0].repairable


# --------------------------------------------------------------------------
# Tests: Alternative workflows validation
# --------------------------------------------------------------------------

class TestAlternativesValidation:
    """Tests for alternative workflows validation."""

    def test_missing_strategy(self, validator, valid_data):
        del valid_data["alternative_workflows"]["fastest"]
        result = validator.validate(valid_data)
        assert not result.is_valid
        issues = [i for i in result.issues if "fastest" in i.field]
        assert len(issues) == 1


# --------------------------------------------------------------------------
# Tests: Auto-repair
# --------------------------------------------------------------------------

class TestRepair:
    """Tests for the auto-repair logic."""

    def test_repair_step_numbers(self, validator, valid_data):
        valid_data["workflow"][0]["step_number"] = 10
        valid_data["workflow"][1]["step_number"] = 20
        valid_data["workflow"][2]["step_number"] = 30
        valid_data["workflow"][3]["step_number"] = 40

        result = validator.validate(valid_data)
        repairable = [i for i in result.issues if i.repairable]
        repaired = validator.repair(valid_data, repairable)

        assert repaired["workflow"][0]["step_number"] == 1
        assert repaired["workflow"][1]["step_number"] == 2
        assert repaired["workflow"][2]["step_number"] == 3
        assert repaired["workflow"][3]["step_number"] == 4

    def test_repair_complexity(self, validator, valid_data):
        valid_data["goal"]["complexity"] = "Impossible"
        result = validator.validate(valid_data)
        repairable = [i for i in result.issues if i.repairable]
        repaired = validator.repair(valid_data, repairable)

        assert repaired["goal"]["complexity"] == "Medium"

    def test_repair_tool_categories(self, validator, valid_data):
        valid_data["recommended_tools"][0]["category"] = "Magic"
        result = validator.validate(valid_data)
        repairable = [i for i in result.issues if i.repairable]
        repaired = validator.repair(valid_data, repairable)

        assert repaired["recommended_tools"][0]["category"] == "Other"

    def test_repair_deliverable_ids(self, validator, valid_data):
        valid_data["deliverables"][0]["id"] = 99
        valid_data["deliverables"][1]["id"] = 100
        result = validator.validate(valid_data)
        repairable = [i for i in result.issues if i.repairable]
        repaired = validator.repair(valid_data, repairable)

        ids = [d["id"] for d in repaired["deliverables"]]
        assert ids == [1, 2, 3, 4]

    def test_repair_excess_bounds(self, validator, valid_data):
        # Add 15 tools (max is 10)
        for i in range(15):
            valid_data["recommended_tools"].append(
                {"name": f"Tool{i}", "category": "Other", "reason": "Test"}
            )
        result = validator.validate(valid_data)
        repairable = [i for i in result.issues if i.repairable]
        repaired = validator.repair(valid_data, repairable)

        assert len(repaired["recommended_tools"]) <= 10
