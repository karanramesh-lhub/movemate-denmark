from pydantic import BaseModel, Field


class DocumentFact(BaseModel):
    field: str
    value: str
    confidence: float = Field(ge=0.0, le=1.0)
    source: str