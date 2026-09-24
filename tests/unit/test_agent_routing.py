from movemate.agent.nodes import (
    determine_information_needed,
    route_after_information_check,
)


def test_information_is_needed_for_non_empty_question():
    state = {
        "current_question": "What registration steps should I complete?"
    }

    result = determine_information_needed(state)

    assert result["information_needed"] is True


def test_information_is_not_needed_for_empty_question():
    state = {
        "current_question": ""
    }

    result = determine_information_needed(state)

    assert result["information_needed"] is False


def test_router_selects_retrieval_when_information_is_needed():
    state = {
        "information_needed": True
    }

    assert route_after_information_check(state) == "retrieve_evidence"


def test_router_selects_end_when_information_is_not_needed():
    state = {
        "information_needed": False
    }

    assert route_after_information_check(state) == "end"