from datetime import date
from pydantic import BaseModel, Field
from enum import Enum  


class UserProfile(BaseModel):

    name: str | None = None
    nationality: str
    residency_type: str
    destination_city: str
    arrival_date: date | None = None
    employment_start_date: date | None = None
    employment_status: str | None = None
    accommodation_type: str | None = None
    family_status: str | None = None
    planned_stay_months: int | None = Field(default=None, gt=0)

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"


class TaskCategory(str, Enum):
    IMMIGRATION = "immigration"
    REGISTRATION = "registration"
    HOUSING = "housing"
    EMPLOYMENT = "employment"
    TRANSPORT = "transport"
    FINANCE = "finance"
    HEALTHCARE = "healthcare"
    DOCUMENTS = "documents"
    OTHER = "other"


class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Task(BaseModel):
    id: str
    title: str
    description: str | None = None

    category: TaskCategory = TaskCategory.OTHER
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.MEDIUM

    dependencies: list[str] = Field(default_factory=list)

    evidence_ids: list[str] = Field(default_factory=list)

class EvidenceType(str, Enum):
    OFFICIAL = "official"
    USER_PROVIDED = "user_provided"
    INFERENCE = "inference"

class Evidence(BaseModel):
    id: str
    evidence_type: EvidenceType

    title: str
    claim: str

    source_name: str | None = None
    source_url: str | None = None

    confidence: float | None = Field(default=None,ge=0.0,le=1.0,)