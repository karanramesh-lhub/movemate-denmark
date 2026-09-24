from datetime import date

import pytest

from movemate.domain.models import UserProfile
from movemate.domain.models import (
    Task,
    TaskCategory,
    TaskPriority,
    TaskStatus,
    Evidence,
    EvidenceType
)


def test_user_profile_accepts_valid_profile():
    profile = UserProfile(
        name="Alex",
        nationality="India",
        residency_type="non-EU",
        destination_city="Copenhagen",
        arrival_date=date(2026, 10, 15),
        employment_start_date=date(2026, 11, 1),
        employment_status="Software Engineer",
        accommodation_type="Temporary",
        family_status="No family",
        planned_stay_months=24,
    )

    assert profile.name == "Alex"
    assert profile.nationality == "India"
    assert profile.destination_city == "Copenhagen"
    assert profile.arrival_date == date(2026, 10, 15)
    assert profile.planned_stay_months == 24

def test_task_uses_valid_defaults():
    task = Task(
        id="task-001",
        title="Complete registration",
    )

    assert task.status == TaskStatus.PENDING
    assert task.priority == TaskPriority.MEDIUM
    assert task.category == TaskCategory.OTHER
    assert task.dependencies == []
    assert task.evidence_ids == []

def test_task_accepts_dependencies_and_evidence():
    task = Task(
        id="task-002",
        title="Complete municipal registration",
        description="Complete the required registration after the prerequisite step.",
        category=TaskCategory.REGISTRATION,
        status=TaskStatus.BLOCKED,
        priority=TaskPriority.HIGH,
        dependencies=["task-001"],
        evidence_ids=["evidence-001"],
    )

    assert task.category == TaskCategory.REGISTRATION
    assert task.status == TaskStatus.BLOCKED
    assert task.priority == TaskPriority.HIGH
    assert task.dependencies == ["task-001"]
    assert task.evidence_ids == ["evidence-001"]

def test_official_evidence():
    evidence = Evidence(
        id="evidence-001",
        evidence_type=EvidenceType.OFFICIAL,
        title="Registration requirement",
        claim="The user needs to complete the required registration.",
        source_name="Danish authority",
        source_url="https://example.gov.dk/registration",
        confidence=0.95,
    )

    assert evidence.evidence_type == EvidenceType.OFFICIAL
    assert evidence.source_name == "Danish authority"
    assert evidence.confidence == 0.95

def test_evidence_rejects_invalid_confidence():
    with pytest.raises(ValueError):
        Evidence(
            id="evidence-002",
            evidence_type=EvidenceType.INFERENCE,
            title="Invalid confidence",
            claim="This should fail.",
            confidence=1.5,
        )