from pydantic import BaseModel, ConfigDict
from datetime import datetime


class KnowledgeBaseCreate(BaseModel):

    name: str
    description: str | None = None
    domain: str | None = None


class KnowledgeBaseUpdate(BaseModel):

    name: str | None = None
    description: str | None = None
    domain: str | None = None


class KnowledgeBaseResponse(BaseModel):

    id: int
    name: str
    description: str | None
    domain: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )