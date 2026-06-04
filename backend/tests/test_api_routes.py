"""Tests for the API routes."""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


class TestWorkflowEndpoint:
    """Test POST /api/v1/workflow/generate."""

    def test_successful_generation(self, client: TestClient) -> None:
        response = client.post(
            "/api/v1/workflow/generate",
            json={"goal": "Build a portfolio website"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "goal" in data
        assert "deliverables" in data
        assert "recommended_tools" in data
        assert "workflow" in data
        assert "alternative_workflows" in data
        assert "knowledge_areas" in data
        assert "estimated_time" in data

    def test_response_matches_contract_structure(self, client: TestClient) -> None:
        response = client.post(
            "/api/v1/workflow/generate",
            json={"goal": "Launch a SaaS startup"},
        )
        data = response.json()
        # Goal structure
        assert "user_input" in data["goal"]
        assert "domain" in data["goal"]
        assert "goal_type" in data["goal"]
        assert "complexity" in data["goal"]
        # Deliverables structure
        assert isinstance(data["deliverables"], list)
        if data["deliverables"]:
            d = data["deliverables"][0]
            assert "id" in d
            assert "title" in d
            assert "description" in d
        # Workflow structure
        assert isinstance(data["workflow"], list)
        if data["workflow"]:
            step = data["workflow"][0]
            assert "step_number" in step
            assert "title" in step
            assert "tool" in step
            assert "why" in step
            assert "what_to_do" in step
            assert "prompt" in step
            assert "expected_result" in step

    def test_empty_goal_rejected(self, client: TestClient) -> None:
        response = client.post(
            "/api/v1/workflow/generate",
            json={"goal": ""},
        )
        assert response.status_code == 422

    def test_missing_goal_rejected(self, client: TestClient) -> None:
        response = client.post(
            "/api/v1/workflow/generate",
            json={},
        )
        assert response.status_code == 422

    def test_whitespace_only_goal_rejected(self, client: TestClient) -> None:
        response = client.post(
            "/api/v1/workflow/generate",
            json={"goal": "   "},
        )
        assert response.status_code == 422


class TestHealthEndpoint:
    """Test GET /api/v1/workflow/health."""

    def test_health_check(self, client: TestClient) -> None:
        response = client.get("/api/v1/workflow/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


class TestLegacyEndpoints:
    """Test backward-compatible endpoints."""

    def test_root_endpoint(self, client: TestClient) -> None:
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data

    def test_mock_workflow_endpoint(self, client: TestClient) -> None:
        response = client.get("/mock-workflow")
        assert response.status_code == 200
        data = response.json()
        assert "goal" in data
        assert data["goal"]["user_input"] == "Build a portfolio website"
