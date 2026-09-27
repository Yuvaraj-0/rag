from datetime import datetime
from pydantic import BaseModel


class DocumentResponse(BaseModel):
    id: int
    knowledge_base_id: int
    file_name: str
    file_path: str
    file_type: str
    file_size: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True