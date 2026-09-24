from unittest.mock import MagicMock, patch

from movemate.llm.client import GeminiReasoningClient


def test_gemini_client_uses_grounding_instructions():
    mock_interaction = MagicMock()
    mock_interaction.output_text = """
    {
        "interpretation": "The evidence does not establish the exact registration procedure.",
        "relevant_evidence_ids": ["registration-001"],
        "proposed_actions": [],
        "uncertainty": [
            "The exact registration procedure is not established by the supplied evidence."
        ],
        "warnings": []
    }
    """

    with patch(
        "movemate.llm.client.genai.Client"
    ) as mock_client_class:
        mock_client = mock_client_class.return_value
        mock_client.interactions.create.return_value = mock_interaction

        client = GeminiReasoningClient()

        result = client.reason(
            profile="Non-EU employee moving to Copenhagen",
            question="What exact registration appointment should I book?",
            evidence=(
                "Registration requirements depend on residence status. "
                "The exact procedure should be checked against current "
                "official guidance."
            ),
        )

        call = mock_client.interactions.create.call_args
        system_instruction = call.kwargs["system_instruction"]

    assert result.proposed_actions == []
    assert result.uncertainty

    assert "Do NOT introduce specific government procedures" in system_instruction

    normalized_instruction = " ".join(system_instruction.split())

    assert "It is better to return fewer actions" in normalized_instruction
