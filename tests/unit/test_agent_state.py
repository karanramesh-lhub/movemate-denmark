from movemate.agent.state import AgentState
from movemate.domain.models import UserProfile


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