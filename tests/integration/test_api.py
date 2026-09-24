from unittest.mock import patch

from fastapi.testclient import TestClient

from movemate.api.main import app
from movemate.agent.state import ReasoningResult


client = TestClient(app)


def test_plan_endpoint_returns_structured_plan():
    mock_reasoning = ReasoningResult(
        interpretation="Registration should be considered.",
        relevant_evidence_ids=["evidence-1"],
        proposed_actions=[],
        uncertainty=["The exact procedure is not established."],
        warnings=[],
    )

    with patch(
        "movemate.agent.nodes.GeminiReasoningClient"
    ) as mock_client_class:
        mock_client = mock_client_class.return_value
        mock_client.reason.return_value = mock_reasoning

        response = client.post(
            "/api/v1/plan",
            json={
                "profile": {
                    "name": "Alex",
                    "nationality": "Indian",
                    "residency_type": "non-EU",
                    "destination_city": "Copenhagen",
                    "arrival_date": "2026-10-15",
                    "employment_start_date": "2026-11-01",
                    "employment_status": "employed",
                    "accommodation_type": "temporary",
                    "family_status": "single",
                    "planned_stay_months": 24,
                },
                "question": "What should I take care of first?",
            },
        )

    assert response.status_code == 200

    data = response.json()

    assert "interpretation" in data
    assert "tasks" in data
    assert "evidence" in data
    assert "uncertainty" in data
    assert "warnings" in data