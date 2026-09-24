from datetime import date
from unittest.mock import MagicMock, patch

from movemate.agent.graph import graph
from movemate.agent.state import ReasoningResult, ProposedAction
from movemate.domain.models import UserProfile


def create_test_profile() -> UserProfile:
    return UserProfile(
        name="Alex",
        nationality="Indian",
        residency_type="non-EU",
        destination_city="Copenhagen",
        arrival_date=date(2026, 10, 15),
        employment_start_date=date(2026, 11, 1),
        employment_status="employed",
        accommodation_type="temporary",
        family_status="single",
        planned_stay_months=24,
    )

def create_test_reasoning_result() -> ReasoningResult:
    return ReasoningResult(
        interpretation="Registration should be considered based on the supplied evidence.",
        relevant_evidence_ids=["registration-1"],
        proposed_actions=[
            ProposedAction(
                action_id="verify-registration",
                title="Verify registration requirements",
                description="Verify the registration requirements applicable to the profile.",
                priority="high",
                depends_on=[],
                evidence_ids=["registration-1"],
            ),
            ProposedAction(
                action_id="review-housing",
                title="Review housing options",
                description="Review suitable housing options.",
                priority="medium",
                depends_on=["verify-registration"],
                evidence_ids=["housing-1"],
            ),
            ProposedAction(
                action_id="complete-employment",
                title="Complete employment setup",
                description="Complete the employment-related setup.",
                priority="medium",
                depends_on=["review-housing"],
                evidence_ids=["employment-1"],
            ),
        ],
        uncertainty=[
            "The exact registration procedure is not established by the supplied evidence."
        ],
        warnings=[],
    )

def mock_gemini_client():
    mock_client = MagicMock()
    mock_client.reason.return_value = create_test_reasoning_result()
    return mock_client

def test_agent_graph_retrieves_evidence_when_information_is_needed():
    with patch(
        "movemate.agent.nodes.GeminiReasoningClient",
        return_value=mock_gemini_client(),
    ):
        state = graph.invoke(
            {
                "user_profile": create_test_profile(),
                "current_question": (
                    "What registration steps should I consider "
                    "after moving to Denmark?"
                ),
            }
        )

    assert state["information_needed"] is True
    assert state["retrieved_evidence"]
    assert state["retrieved_evidence"][0].evidence_type.value == "official"

    evidence_text = " ".join(
        item.claim for item in state["retrieved_evidence"]
    ).lower()

    assert (
        "non-eu" in evidence_text
        or "cpr" in evidence_text
        or "residence" in evidence_text
    )


def test_agent_graph_skips_retrieval_when_information_is_not_needed():
    state = graph.invoke(
        {
            "user_profile": create_test_profile(),
            "current_question": "",
        }
    )

    assert state["information_needed"] is False
    assert "retrieved_evidence" not in state

def test_agent_graph_builds_personalized_task_plan():
    with patch(
        "movemate.agent.nodes.GeminiReasoningClient",
        return_value=mock_gemini_client(),
    ):
        state = graph.invoke(
            {
                "user_profile": create_test_profile(),
                "current_question": (
                    "What registration steps should I consider "
                    "after moving to Denmark?"
                ),
            }
        )

    task_ids = {task.id for task in state["task_graph"]}

    assert "verify-registration" in task_ids
    assert "review-housing" in task_ids
    assert "complete-employment" in task_ids

    tasks = state["task_graph"]

    assert tasks[0].dependencies == []
    assert tasks[1].dependencies == [
        "verify-registration"
    ]
    assert tasks[2].dependencies == [
        "review-housing"
    ]

def test_agent_graph_creates_reasoning_result():
    with patch(
        "movemate.agent.nodes.GeminiReasoningClient",
        return_value=mock_gemini_client(),
    ):
        result = graph.invoke(
            {
                "user_profile": create_test_profile(),
                "current_question": "What should I do first?",
            }
        )

    reasoning = result["reasoning_result"]

    assert reasoning.interpretation
    assert reasoning.proposed_actions
    assert reasoning.relevant_evidence_ids