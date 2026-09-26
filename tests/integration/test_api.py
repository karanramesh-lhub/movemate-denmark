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

def test_plan_endpoint_accepts_document_facts(monkeypatch):
    from movemate.agent.state import ReasoningResult, ProposedAction

    def fake_reason(*args, **kwargs):
        return ReasoningResult(
            interpretation=(
                "The uploaded employment information indicates "
                "that employment begins on 2026-11-01."
            ),
            proposed_actions=[
                ProposedAction(
                    action_id="prepare-employment-start",
                    title="Prepare for employment start",
                    description=(
                        "Prepare for the employment start date stated "
                        "in the uploaded document."
                    ),
                    priority="high",
                    depends_on=[],
                    evidence_ids=[],
                )
            ],
            uncertainty=[],
            warnings=[],
        )

    monkeypatch.setattr(
        "movemate.agent.nodes.GeminiReasoningClient.reason",
        fake_reason,
    )

    response = client.post(
        "/api/v1/plan",
        json={
            "profile": {
                "nationality": "Indian",
                "residency_type": "non-EU",
                "destination_city": "Copenhagen",
                "employment_status": "employed",
            },
            "question": "What should I prepare before starting work?",
            "document_facts": [
                {
                    "field": "employment start date",
                    "value": "2026-11-01",
                    "confidence": 1.0,
                    "source": "employment_contract.txt",
                }
            ],
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["interpretation"]
    assert len(data["tasks"]) == 1
    assert data["tasks"][0]["id"] == "prepare-employment-start"

def test_plan_endpoint_returns_503_when_llm_fails(monkeypatch):
    from movemate.llm.client import LLMServiceError

    def failing_reason(*args, **kwargs):
        raise LLMServiceError(
            "The reasoning service could not be reached."
        )

    monkeypatch.setattr(
        "movemate.agent.nodes.GeminiReasoningClient.reason",
        failing_reason,
    )

    response = client.post(
        "/api/v1/plan",
        json={
            "profile": {
                "nationality": "Indian",
                "residency_type": "non-EU",
                "destination_city": "Copenhagen",
            },
            "question": "What should I do first?",
        },
    )

    assert response.status_code == 503
    assert response.json()["detail"] == (
        "The reasoning service is temporarily unavailable."
    )