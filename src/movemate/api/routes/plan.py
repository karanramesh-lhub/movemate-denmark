from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from movemate.agent.graph import graph
from movemate.domain.documents import DocumentFact
from movemate.domain.models import Evidence, Task, UserProfile
from movemate.infrastructure.observability import get_langfuse_client
from movemate.infrastructure.repository import save_plan
from movemate.llm.client import LLMServiceError


router = APIRouter(prefix="/api/v1", tags=["planning"])


class PlanRequest(BaseModel):
    profile: UserProfile
    question: str
    document_facts: list[DocumentFact] = Field(default_factory=list)


class PlanResponse(BaseModel):
    plan_id: str
    interpretation: str | None = None
    tasks: list[Task]
    evidence: list[Evidence]
    uncertainty: list[str]
    warnings: list[str]


@router.post("/plan", response_model=PlanResponse)
async def create_plan(request: PlanRequest) -> PlanResponse:
    def run_graph():
        return graph.invoke(
            {
                "user_profile": request.profile,
                "current_question": request.question,
                "document_facts": request.document_facts,
            }
        )

    langfuse = get_langfuse_client()

    try:
        if langfuse is not None:
            with langfuse.start_as_current_observation(
                as_type="agent",
                name="movemate-plan-request",
                input={
                    "question": request.question,
                    "destination_city": request.profile.destination_city,
                    "residency_type": request.profile.residency_type,
                },
                metadata={
                    "document_facts_count": len(request.document_facts),
                    "environment": "development",
                },
            ) as observation:
                result = run_graph()

                observation.update(
                    output={
                        "evidence_count": len(
                            result.get("retrieved_evidence", [])
                        ),
                        "task_count": len(
                            result.get("task_graph", [])
                        ),
                    }
                )
        else:
            result = run_graph()

    except LLMServiceError as exc:
        raise HTTPException(
            status_code=503,
            detail="The reasoning service is temporarily unavailable.",
        ) from exc

    reasoning_result = result.get("reasoning_result")

    tasks = result.get("task_graph", [])
    evidence = result.get("retrieved_evidence", [])

    interpretation = (
        reasoning_result.interpretation
        if reasoning_result
        else None
    )

    uncertainty = (
        reasoning_result.uncertainty
        if reasoning_result
        else []
    )

    warnings = (
        reasoning_result.warnings
        if reasoning_result
        else []
    )

    plan_id = await save_plan(
        profile=request.profile,
        question=request.question,
        interpretation=interpretation,
        uncertainty=uncertainty,
        warnings=warnings,
        tasks=tasks,
    )

    return PlanResponse(
        plan_id=plan_id,
        interpretation=interpretation,
        tasks=tasks,
        evidence=evidence,
        uncertainty=uncertainty,
        warnings=warnings,
    )