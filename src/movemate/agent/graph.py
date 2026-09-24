from langgraph.graph import END, START, StateGraph

from movemate.agent.nodes import (
    analyze_profile,
    build_task_plan,
    determine_information_needed,
    reason_about_situation,
    retrieve_evidence,
    route_after_information_check,
)
from movemate.agent.state import AgentState


builder = StateGraph(AgentState)

builder.add_node("analyze_profile", analyze_profile)
builder.add_node("determine_information_needed", determine_information_needed)
builder.add_node("retrieve_evidence", retrieve_evidence)
builder.add_node("build_task_plan", build_task_plan)
builder.add_node("reason_about_situation", reason_about_situation)

builder.add_edge(START, "analyze_profile")
builder.add_edge("analyze_profile", "determine_information_needed")
builder.add_conditional_edges(
    "determine_information_needed",
    route_after_information_check,
    {
        "retrieve_evidence": "retrieve_evidence",
        "end": END,
    },
)
builder.add_edge("retrieve_evidence","reason_about_situation")
builder.add_edge("reason_about_situation","build_task_plan",)
builder.add_edge("build_task_plan", END)

graph = builder.compile()