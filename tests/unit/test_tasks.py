from asyncio import tasks
from datetime import date
from movemate.domain import tasks

from movemate.domain.models import (
    Evidence,
    EvidenceType,
    UserProfile,
)
from movemate.domain.tasks import build_task_plan
from movemate.agent.state import ProposedAction, ReasoningResult
from movemate.domain.models import TaskCategory


def create_alex_profile() -> UserProfile:
    return UserProfile(
        name="Alex",
        nationality="Indian",
        residency_type="non-EU",
        destination_city="Copenhagen",
        arrival_date=date(2026, 10, 15),
        employment_start_date=date(2026, 11, 1),
        employment_status="employed",
        accommodation_type="temporary",
        family_status="single",
        planned_stay_months=24,
    )


def test_task_plan_is_personalized_to_profile():
    profile = create_alex_profile()

    tasks = build_task_plan(
        profile=profile,
        evidence=[],
    )

    task_ids = {task.id for task in tasks}

    assert "complete-registration" in task_ids
    assert "secure-long-term-housing" in task_ids
    assert "complete-employment-setup" in task_ids


def test_registration_task_contains_official_evidence():
    profile = create_alex_profile()

    evidence = [
        Evidence(
            id="registration-evidence-001",
            evidence_type=EvidenceType.OFFICIAL,
            title="Registration guidance",
            claim="Registration requirements depend on residence status.",
            source_name="Danish public authorities",
        )
    ]

    tasks = build_task_plan(
        profile=profile,
        evidence=evidence,
    )

    registration_task = next(
        task
        for task in tasks
        if task.id == "complete-registration"
    )

    assert registration_task.evidence_ids == [
        "registration-evidence-001"
    ]

def test_task_plan_uses_reasoning_actions():
    profile = create_alex_profile()

    reasoning_result = ReasoningResult(
        interpretation="Registration should be considered first.",
        relevant_evidence_ids=[],
        proposed_actions=[
    ProposedAction(
        action_id="verify-registration",
        title="Verify registration requirements",
        description="Verify the registration requirements applicable to the profile.",
        priority="high",
        depends_on=[],
        evidence_ids=["registration-1"],
    ),
    ProposedAction(
        action_id="review-housing",
        title="Review housing options",
        description="Review suitable housing options.",
        priority="medium",
        depends_on=["verify-registration"],
        evidence_ids=["housing-1"],
    ),
    ProposedAction(
        action_id="complete-employment",
        title="Complete employment setup",
        description="Complete the employment-related setup.",
        priority="medium",
        depends_on=["review-housing"],
        evidence_ids=["employment-1"],
    ),
],
        uncertainty=[],
        warnings=[],
    )

    tasks = build_task_plan(
        profile=profile,
        evidence=[],
        reasoning_result=reasoning_result,
    )

    assert len(tasks) == 3
    assert tasks[0].title == "Verify registration requirements"
    assert tasks[0].category == TaskCategory.REGISTRATION
    assert tasks[1].category == TaskCategory.HOUSING

def test_reasoning_action_generates_stable_task_id():
    profile = create_alex_profile()

    reasoning_result = ReasoningResult(
        interpretation="Registration should be considered first.",
        proposed_actions=[
    ProposedAction(
        action_id="verify-registration",
        title="Verify registration requirements",
        description="Verify the registration requirements applicable to the profile.",
        priority="high",
        depends_on=[],
        evidence_ids=["registration-1"],
    ),
    ProposedAction(
        action_id="review-housing",
        title="Review housing options",
        description="Review suitable housing options.",
        priority="medium",
        depends_on=["verify-registration"],
        evidence_ids=["housing-1"],
    ),
    ProposedAction(
        action_id="complete-employment",
        title="Complete employment setup",
        description="Complete the employment-related setup.",
        priority="medium",
        depends_on=["review-housing"],
        evidence_ids=["employment-1"],
    ),
],
    )

    tasks = build_task_plan(
        profile=profile,
        evidence=[],
        reasoning_result=reasoning_result,
    )

    assert tasks[0].id == "verify-registration"

def test_reasoning_tasks_preserve_declared_dependencies():
    profile = create_alex_profile()

    reasoning_result = ReasoningResult(
        interpretation="Multiple actions are relevant.",
        proposed_actions=[
    ProposedAction(
        action_id="verify-registration",
        title="Verify registration requirements",
        description="Verify the registration requirements applicable to the profile.",
        priority="high",
        depends_on=[],
        evidence_ids=["registration-1"],
    ),
    ProposedAction(
        action_id="review-housing",
        title="Review housing options",
        description="Review suitable housing options.",
        priority="medium",
        depends_on=["verify-registration"],
        evidence_ids=["housing-1"],
    ),
    ProposedAction(
        action_id="complete-employment",
        title="Complete employment setup",
        description="Complete the employment-related setup.",
        priority="medium",
        depends_on=["review-housing"],
        evidence_ids=["employment-1"],
    ),
],
    )

    tasks = build_task_plan(
        profile=profile,
        evidence=[],
        reasoning_result=reasoning_result,
    )

    assert tasks[0].dependencies == []

    assert tasks[0].dependencies == []
    assert tasks[1].dependencies == ["verify-registration"]
    assert tasks[2].dependencies == ["review-housing"]