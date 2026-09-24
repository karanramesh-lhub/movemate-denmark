from movemate.agent.state import AgentState, ReasoningResult
from movemate.tools.knowledge_tool import knowledge_search_tool
from movemate.domain.tasks import build_task_plan as create_task_plan
from movemate.llm.client import GeminiReasoningClient


def analyze_profile(state: AgentState) -> dict:
    profile = state["user_profile"]

    decision = (
        f"Profile analyzed for {profile.destination_city} "
        f"with {profile.residency_type} residency."
    )

    return {
        "decisions": state.get("decisions", []) + [decision],
    }

def retrieve_evidence(state: AgentState) -> dict:
    profile = state["user_profile"]
    question = state["current_question"]

    retrieval_query = (
        f"{question}. "
        f"Nationality: {profile.nationality}. "
        f"Residency type: {profile.residency_type}. "
        f"Destination city: {profile.destination_city}. "
        f"Employment status: {profile.employment_status or 'unknown'}. "
        f"Accommodation type: {profile.accommodation_type or 'unknown'}. "
        f"Planned stay: {profile.planned_stay_months or 'unknown'} months."
    )

    evidence = knowledge_search_tool(
        query=retrieval_query,
        limit=5,
    )

    return {"retrieved_evidence": evidence}

def determine_information_needed(state: AgentState) -> dict:
    question = state["current_question"]

    information_needed = bool(question.strip())

    return {
        "information_needed": information_needed,
    }

def route_after_information_check(state: AgentState) -> str:
    if state["information_needed"]:
        return "retrieve_evidence"

    return "end"

def build_task_plan(state: AgentState) -> dict:
    profile = state["user_profile"]
    evidence = state.get("retrieved_evidence", [])
    reasoning_result = state.get("reasoning_result")

    tasks = create_task_plan(
        profile=profile,
        evidence=evidence,
        reasoning_result=reasoning_result,
    )

    return {"task_graph": tasks}

def reason_about_situation(state: AgentState) -> dict:
    profile = state["user_profile"]
    question = state["current_question"]
    evidence = state.get("retrieved_evidence", [])

    profile_text = profile.model_dump_json(indent=2)

    evidence_text = "\n\n".join(
        (
            f"Evidence ID: {item.id}\n"
            f"Type: {item.evidence_type.value}\n"
            f"Title: {item.title}\n"
            f"Claim: {item.claim}\n"
            f"Source: {item.source_name or 'Unknown'}"
        )
        for item in evidence
    )

    client = GeminiReasoningClient()

    reasoning_result = client.reason(
        profile=profile_text,
        question=question,
        evidence=evidence_text or "No evidence was retrieved.",
    )

    return {
        "reasoning_result": reasoning_result,
    }