from movemate.agent.state import ReasoningResult


def test_reasoning_result_accepts_structured_output():
    result = ReasoningResult(
        interpretation="User is moving to Copenhagen for employment.",
        relevant_evidence_ids=["registration-001"],
        proposed_actions=[
            "Review registration requirements",
            "Plan longer-term housing",
        ],
        uncertainty=[
            "Exact requirements depend on residence status.",
        ],
        warnings=[
            "Verify current requirements using official sources.",
        ],
    )

    assert result.interpretation
    assert result.relevant_evidence_ids == ["registration-001"]
    assert len(result.proposed_actions) == 2
    assert len(result.uncertainty) == 1
    assert len(result.warnings) == 1

def test_reasoning_result_has_safe_defaults():
    result = ReasoningResult(
        interpretation="Situation understood."
    )

    assert result.relevant_evidence_ids == []
    assert result.proposed_actions == []
    assert result.uncertainty == []
    assert result.warnings == []