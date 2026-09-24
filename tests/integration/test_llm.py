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

    assert result.interpretation
    assert result.proposed_actions
    assert isinstance(result.relevant_evidence_ids, list)
    assert isinstance(result.uncertainty, list)
    assert isinstance(result.warnings, list)