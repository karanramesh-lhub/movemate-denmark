import re

from movemate.agent.state import ReasoningResult
from movemate.domain.models import (Evidence,EvidenceType,Task,TaskCategory,TaskPriority,UserProfile,)

def _infer_task_category(action: str) -> TaskCategory:
    action_lower = action.lower()

    if any(word in action_lower for word in ["registration", "residence", "register"]):
        return TaskCategory.REGISTRATION

    if any(word in action_lower for word in ["housing", "accommodation", "apartment"]):
        return TaskCategory.HOUSING

    if any(word in action_lower for word in ["employment", "job", "work"]):
        return TaskCategory.EMPLOYMENT

    if any(word in action_lower for word in ["transport", "travel", "metro", "bus"]):
        return TaskCategory.TRANSPORT

    if any(word in action_lower for word in ["health", "doctor", "healthcare"]):
        return TaskCategory.HEALTHCARE

    if any(word in action_lower for word in ["finance", "bank", "banking"]):
        return TaskCategory.FINANCE

    if any(word in action_lower for word in ["document", "passport", "certificate"]):
        return TaskCategory.DOCUMENTS

    return TaskCategory.OTHER


def build_task_plan(profile: UserProfile,evidence: list[Evidence],reasoning_result: ReasoningResult | None = None,) -> list[Task]:
    tasks: list[Task] = []

    evidence_ids = [
        item.id
        for item in evidence
        if item.evidence_type == EvidenceType.OFFICIAL
    ]

    if reasoning_result:
        for action in reasoning_result.proposed_actions:
            action_evidence_ids = (
                action.evidence_ids
                if action.evidence_ids
                else evidence_ids
            )

            try:
                priority = TaskPriority(action.priority.lower())
            except ValueError:
                priority = TaskPriority.MEDIUM

            tasks.append(
                Task(
                    id=action.action_id,
                    title=action.title,
                    description=action.description,
                    category=_infer_task_category(action.title),
                    priority=priority,
                    dependencies=list(action.depends_on),
                    evidence_ids=action_evidence_ids,
                )
            )

        return tasks

    if profile.residency_type == "non-EU":
        tasks.append(
            Task(
                id="complete-registration",
                title="Complete applicable registration",
                description=(
                    "Complete the registration steps applicable "
                    "to your residence status."
                ),
                category=TaskCategory.REGISTRATION,
                priority=TaskPriority.HIGH,
                evidence_ids=evidence_ids,
            )
        )

    if profile.accommodation_type == "temporary":
        tasks.append(
            Task(
                id="secure-long-term-housing",
                title="Secure longer-term housing",
                description=(
                    "Review housing options before the temporary "
                    "accommodation period ends."
                ),
                category=TaskCategory.HOUSING,
                priority=TaskPriority.MEDIUM,
            )
        )

    if profile.employment_status == "employed":
        tasks.append(
            Task(
                id="complete-employment-setup",
                title="Complete employment setup",
                description=(
                    "Complete the onboarding and employment-related "
                    "steps applicable to your situation."
                ),
                category=TaskCategory.EMPLOYMENT,
                priority=TaskPriority.MEDIUM,
            )
        )

    return tasks

def _action_to_task_id(action: str) -> str:

    normalized = action.lower().strip()
    normalized = re.sub(r"[^a-z0-9]+", "-", normalized)
    normalized = normalized.strip("-")

    return f"action-{normalized}"

def _add_sequential_dependencies(tasks: list[Task]) -> list[Task]:
    for index in range(1, len(tasks)):
        current_task = tasks[index]
        previous_task = tasks[index - 1]

        current_task.dependencies.append(previous_task.id)

    return tasks