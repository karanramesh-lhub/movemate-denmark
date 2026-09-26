from sqlalchemy import select
from sqlalchemy.orm import selectinload

from movemate.domain.models import Task, UserProfile
from movemate.infrastructure.database import AsyncSessionLocal
from movemate.infrastructure.models import (PlanRecord,ProfileRecord,TaskRecord,)


async def save_plan(profile: UserProfile,question: str,interpretation: str | None,uncertainty: list[str],warnings: list[str],tasks: list[Task]) -> str:
    async with AsyncSessionLocal() as session:
        profile_record = ProfileRecord(
            name=profile.name,
            nationality=profile.nationality,
            residency_type=profile.residency_type,
            destination_city=profile.destination_city,
            arrival_date=profile.arrival_date,
            employment_start_date=profile.employment_start_date,
            employment_status=profile.employment_status,
            accommodation_type=profile.accommodation_type,
            family_status=profile.family_status,
            planned_stay_months=profile.planned_stay_months,
        )

        plan_record = PlanRecord(
            question=question,
            interpretation=interpretation,
            uncertainty=uncertainty,
            warnings=warnings,
            profile=profile_record,
        )

        for task in tasks:
            plan_record.tasks.append(
                TaskRecord(
                    task_id=task.id,
                    title=task.title,
                    description=task.description,
                    category=task.category.value,
                    status=task.status.value,
                    priority=task.priority.value,
                    dependencies=task.dependencies,
                    evidence_ids=task.evidence_ids,
                )
            )

        session.add(plan_record)

        await session.commit()
        await session.refresh(plan_record)

        return plan_record.id


async def get_plan(plan_id: str) -> PlanRecord | None:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(PlanRecord)
            .options(
                selectinload(PlanRecord.profile),
                selectinload(PlanRecord.tasks),
            )
            .where(
                PlanRecord.id == plan_id
            )
        )   

        return result.scalar_one_or_none()