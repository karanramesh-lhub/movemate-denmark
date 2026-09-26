from typing import TypedDict
from pydantic import BaseModel, Field

from movemate.domain.models import Evidence, Task, UserProfile
from movemate.domain.documents import DocumentFact

class ProposedAction(BaseModel):
    action_id: str
    title: str
    description: str
    priority: str = "medium"
    depends_on: list[str] = Field(default_factory=list)
    evidence_ids: list[str] = Field(default_factory=list)


class ReasoningResult(BaseModel):
    interpretation: str
    relevant_evidence_ids: list[str] = Field(default_factory=list)
    proposed_actions: list[ProposedAction] = Field(default_factory=list)
    uncertainty: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class AgentState(TypedDict, total=False):

    user_profile: UserProfile
    current_question: str
    document_facts: list[DocumentFact]
    information_needed: bool
    retrieved_evidence: list[Evidence]
    reasoning_result: ReasoningResult
    task_graph: list[Task]
    completed_tasks: list[str]
    pending_tasks: list[str]
    decisions: list[str]
    warnings: list[str]
    final_response: str

