from unittest import result
from unittest.mock import MagicMock, patch

from movemate.llm.client import GeminiReasoningClient


def test_gemini_reasoning_client_returns_reasoning_result():
    mock_interaction = MagicMock()
    mock_interaction.output_text = """
    {
        "interpretation": "The user is moving to Copenhagen for employment.",
        "relevant_evidence_ids": ["registration-001"],
        "proposed_actions": [
    {
        "action_id": "verify-registration",
        "title": "Verify registration requirements",
        "description": "Verify the registration requirements applicable to the profile.",
        "priority": "high",
        "depends_on": [],
        "evidence_ids": ["registration-1"]
    },
    {
        "action_id": "review-housing",
        "title": "Review housing options",
        "description": "Review suitable housing options.",
        "priority": "medium",
        "depends_on": ["verify-registration"],
        "evidence_ids": ["housing-1"]
    },
    {
        "action_id": "complete-employment",
        "title": "Complete employment setup",
        "description": "Complete the employment-related setup.",
        "priority": "medium",
        "depends_on": ["review-housing"],
        "evidence_ids": ["employment-1"]
    }
],
        "uncertainty": ["Exact requirements depend on residence status."],
        "warnings": ["Verify current requirements using official sources."]
    }
    """

    with patch(
        "movemate.llm.client.genai.Client"
    ) as mock_client_class:
        mock_client = mock_client_class.return_value
        mock_client.interactions.create.return_value = mock_interaction

        client = GeminiReasoningClient()

        result = client.reason(
            profile="Indian, non-EU, moving to Copenhagen",
            question="What should I do first?",
            evidence="Registration requirements depend on residence status.",
        )

    assert result.interpretation
    assert result.uncertainty
    assert result.warnings
    assert len(result.proposed_actions) == 3

    assert result.proposed_actions[0].action_id == "verify-registration"
    assert result.proposed_actions[1].action_id == "review-housing"
    assert result.proposed_actions[2].action_id == "complete-employment"

    assert result.proposed_actions[1].depends_on == [
        "verify-registration"
    ]

    assert result.proposed_actions[2].depends_on == [
        "review-housing"
    ]