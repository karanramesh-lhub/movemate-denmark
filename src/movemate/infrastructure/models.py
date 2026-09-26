from datetime import date
from uuid import uuid4

from sqlalchemy import Date, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class ProfileRecord(Base):
    __tablename__ = "profiles"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    nationality: Mapped[str] = mapped_column(String(100))
    residency_type: Mapped[str] = mapped_column(String(100))
    destination_city: Mapped[str] = mapped_column(String(100))
    arrival_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    employment_start_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )
    employment_status: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )
    accommodation_type: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )
    family_status: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )
    planned_stay_months: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    plans: Mapped[list["PlanRecord"]] = relationship(
        back_populates="profile",
        cascade="all, delete-orphan",
    )


class PlanRecord(Base):
    __tablename__ = "plans"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    profile_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("profiles.id"),
        nullable=False,
    )

    question: Mapped[str] = mapped_column(Text, nullable=False)
    interpretation: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    uncertainty: Mapped[list[str]] = mapped_column(
        JSONB,
        default=list,
    )

    warnings: Mapped[list[str]] = mapped_column(
        JSONB,
        default=list,
    )

    profile: Mapped["ProfileRecord"] = relationship(
        back_populates="plans",
    )

    tasks: Mapped[list["TaskRecord"]] = relationship(
        back_populates="plan",
        cascade="all, delete-orphan",
    )


class TaskRecord(Base):
    __tablename__ = "tasks"

    id: Mapped[str] = mapped_column(
    UUID(as_uuid=False),
    primary_key=True,
    default=lambda: str(uuid4()),
    )

    task_id: Mapped[str] = mapped_column(
    String(255),
    nullable=False,
    )
    
    plan_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("plans.id"),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    category: Mapped[str] = mapped_column(String(50))
    status: Mapped[str] = mapped_column(String(50))
    priority: Mapped[str] = mapped_column(String(50))

    dependencies: Mapped[list[str]] = mapped_column(
        JSONB,
        default=list,
    )

    evidence_ids: Mapped[list[str]] = mapped_column(
        JSONB,
        default=list,
    )

    plan: Mapped["PlanRecord"] = relationship(
        back_populates="tasks",
    )