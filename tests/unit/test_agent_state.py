from movemate.agent.state import AgentState
from movemate.domain.models import UserProfile
from movemate.domain.documents import DocumentFact


def test_agent_state_can_hold_profile_and_question():
    profile = UserProfile(
        nationality="India",
        residency_type="non-EU",
        destination_city="Copenhagen",
    )

    state: AgentState = {
        "user_profile": profile,
        "current_question": "What should I do first?",
    }

    assert state["user_profile"].nationality == "India"
    assert state["current_question"] == "What should I do first?"

def test_agent_state_accepts_document_facts():
    facts = [
        DocumentFact(
            field="employment_start_date",
            value="2026-11-01",
            confidence=1.0,
            source="employment_contract.txt",
        )
    ]

    state = {
        "document_facts": facts,
    }

    assert state["document_facts"][0].field == "employment_start_date"
    assert state["document_facts"][0].value == "2026-11-01"