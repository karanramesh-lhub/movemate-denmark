from movemate.agent.state import ProposedAction, ReasoningResult


def test_reasoning_result_can_represent_uncertainty_without_actions():
    result = ReasoningResult(
        interpretation=(
            "The available evidence does not establish a specific "
            "procedure for this situation."
        ),
        relevant_evidence_ids=[],
        proposed_actions=[],
        uncertainty=[
            "The exact applicable procedure should be checked "
            "against current official guidance."
        ],
        warnings=[],
    )

    assert result.proposed_actions == []
    assert result.uncertainty


def test_proposed_action_must_reference_supplied_evidence():
    supplied_evidence_ids = {"evidence-1", "evidence-2"}

    action = ProposedAction(
        action_id="check-guidance",
        title="Check current official guidance",
        description=(
            "Check the applicable official guidance for the "
            "user's circumstances."
        ),
        priority="medium",
        evidence_ids=["evidence-1"],
    )

    assert set(action.evidence_ids).issubset(supplied_evidence_ids)


def test_dependencies_must_reference_actions_in_same_response():
    actions = [
        ProposedAction(
            action_id="action-1",
            title="Check official guidance",
            description="Check the applicable official guidance.",
        ),
        ProposedAction(
            action_id="action-2",
            title="Continue settlement planning",
            description="Continue planning after checking the guidance.",
            depends_on=["action-1"],
        ),
    ]

    action_ids = {action.action_id for action in actions}

    for action in actions:
        assert set(action.depends_on).issubset(action_ids)