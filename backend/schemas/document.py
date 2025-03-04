from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class DocumentBase(BaseModel):
    content: str
    status: Optional[str] = "pending"

class DocumentCreate(DocumentBase):
    project_id: UUID

class DocumentResponse(DocumentBase):
    id: UUID
    project_id: UUID
    created_by: UUID
    created_at: datetime

    class Config:
        from_attributes = True 