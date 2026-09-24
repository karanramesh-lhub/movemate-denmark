from fastapi import APIRouter
from pydantic import BaseModel

from movemate.agent.graph import graph
from movemate.domain.models import Evidence, Task, UserProfile


router = APIRouter(prefix="/api/v1", tags=["planning"])


class PlanRequest(BaseModel):
    profile: UserProfile
    question: str


class PlanResponse(BaseModel):
    interpretation: str | None = None
    tasks: list[Task]
    evidence: list[Evidence]
    uncertainty: list[str]
    warnings: list[str]


@router.post("/plan", response_model=PlanResponse)
def create_plan(request: PlanRequest) -> PlanResponse:
    result = graph.invoke(
        {
            "user_profile": request.profile,
            "current_question": request.question,
        }
    )

    reasoning_result = result.get("reasoning_result")

    return PlanResponse(
        interpretation=(
            reasoning_result.interpretation
            if reasoning_result
            else None
        ),
        tasks=result.get("task_graph", []),
        evidence=result.get("retrieved_evidence", []),
        uncertainty=(
            reasoning_result.uncertainty
            if reasoning_result
            else []
        ),
        warnings=(
            reasoning_result.warnings
            if reasoning_result
            else []
        ),
    )