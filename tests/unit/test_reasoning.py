from movemate.agent.state import ProposedAction, ReasoningResult
from movemate.agent.nodes import reason_about_situation
from movemate.domain.documents import DocumentFact
from movemate.domain.models import UserProfile


def test_reasoning_result_accepts_structured_output():
    result = ReasoningResult(
        interpretation="User is moving to Copenhagen for employment.",
        relevant_evidence_ids=["registration-001"],
        proposed_actions=[
            ProposedAction(
                action_id="review-registration",
                title="Review registration requirements",
                description="Review the registration requirements applicable to the user.",
                priority="high",
                depends_on=[],
                evidence_ids=["registration-001"],
            ),
            ProposedAction(
                action_id="plan-housing",
                title="Plan longer-term housing",
                description="Plan suitable longer-term housing.",
                priority="medium",
                depends_on=["review-registration"],
                evidence_ids=[],
            ),
        ],
        uncertainty=[
            "Exact requirements depend on residence status.",
        ],
        warnings=[
            "Verify current requirements using official sources.",
        ],
    )

    assert result.interpretation
    assert len(result.proposed_actions) == 2
    assert result.proposed_actions[0].action_id == "review-registration"
    assert result.proposed_actions[1].depends_on == [
        "review-registration"
    ]


def test_reasoning_includes_document_facts(monkeypatch):
    captured = {}

    class FakeGeminiReasoningClient:
        def reason(
            self,
            *,
            profile,
            question,
            evidence,
            document_facts,
        ):
            captured["profile"] = profile
            captured["question"] = question
            captured["evidence"] = evidence
            captured["document_facts"] = document_facts

            return ReasoningResult(
                interpretation="Document facts were considered.",
                proposed_actions=[],
                uncertainty=[],
                warnings=[],
            )

    monkeypatch.setattr(
        "movemate.agent.nodes.GeminiReasoningClient",
        FakeGeminiReasoningClient,
    )

    profile = UserProfile(
        nationality="Indian",
        residency_type="non-EU",
        destination_city="Copenhagen",
        employment_status="employed",
    )

    document_facts = [
        DocumentFact(
            field="employment start date",
            value="2026-11-01",
            confidence=1.0,
            source="employment_contract.txt",
        )
    ]

    result = reason_about_situation(
        {
            "user_profile": profile,
            "current_question": "What should I prepare before starting work?",
            "retrieved_evidence": [],
            "document_facts": document_facts,
        }
    )

    assert result["reasoning_result"].interpretation == (
        "Document facts were considered."
    )

    assert "employment start date" in captured["document_facts"]
    assert "2026-11-01" in captured["document_facts"]
    assert "employment_contract.txt" in captured["document_facts"]