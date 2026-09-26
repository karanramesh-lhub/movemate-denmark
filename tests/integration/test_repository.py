import pytest

from movemate.domain.models import (
    Task,
    TaskCategory,
    TaskPriority,
    TaskStatus,
    UserProfile,
)
from movemate.infrastructure.repository import (
    get_plan,
    save_plan,
)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_save_and_get_plan():
    profile = UserProfile(
        name="Test User",
        nationality="Indian",
        residency_type="non-EU",
        destination_city="Copenhagen",
        employment_status="employed",
    )

    task = Task(
        id="test-registration",
        title="Complete registration",
        description="Complete applicable registration steps.",
        category=TaskCategory.REGISTRATION,
        status=TaskStatus.PENDING,
        priority=TaskPriority.HIGH,
        dependencies=[],
        evidence_ids=["evidence-1"],
    )

    plan_id = await save_plan(
        profile=profile,
        question="What should I do first?",
        interpretation="Registration should be considered.",
        uncertainty=["Exact procedure depends on the user's circumstances."],
        warnings=[],
        tasks=[task],
    )

    saved_plan = await get_plan(plan_id)

    assert saved_plan is not None
    assert saved_plan.id == plan_id
    assert saved_plan.question == "What should I do first?"
    assert saved_plan.interpretation == "Registration should be considered."

    assert saved_plan.profile is not None
    assert saved_plan.profile.nationality == "Indian"
    assert saved_plan.profile.destination_city == "Copenhagen"

    assert len(saved_plan.tasks) == 1

    saved_task = saved_plan.tasks[0]

    assert saved_task.task_id == "test-registration"
    assert saved_task.title == "Complete registration"
    assert saved_task.category == "registration"
    assert saved_task.priority == "high"
    assert saved_task.evidence_ids == ["evidence-1"]