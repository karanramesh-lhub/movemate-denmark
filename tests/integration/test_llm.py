from unittest import result

import pytest

from movemate.llm.client import GeminiReasoningClient


@pytest.mark.integration
def test_gemini_can_generate_reasoning():
    client = GeminiReasoningClient()

    result = client.reason(
        profile=(
            "Name: Alex\n"
            "Nationality: Indian\n"
            "Residency type: non-EU\n"
            "Destination: Copenhagen\n"
            "Employment status: employed\n"
            "Accommodation: temporary"
        ),
        question="What should I take care of first?",
        evidence=(
            "International residents moving to Denmark may need to "
            "complete registration steps. Exact requirements depend "
            "on nationality, residence status, destination municipality "
            "and employment situation."
        ),
    )

    assert result.uncertainty
    assert result.warnings
    for action in result.proposed_actions:
        assert action.action_id
        assert action.title
        assert action.description
        assert action.priority in {"low", "medium", "high"}

    for action in result.proposed_actions:
        assert set(action.evidence_ids).issubset(
            {"evidence-1"}
        )