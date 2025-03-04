from pydantic import BaseModel
from typing import Optional, Any, List
from datetime import datetime
from uuid import UUID
from .base import AnnotationResponse

class AnnotationBase(BaseModel):
    content: Any  # JSON content
    confidence_score: Optional[float] = None

class AnnotationCreate(AnnotationBase):
    pass

class AnnotationResponse(AnnotationBase):
    id: UUID
    document_id: UUID
    created_by: UUID
    verified: bool
    verified_by: Optional[UUID]
    created_at: datetime

    class Config:
        from_attributes = True

class BatchAnnotationResponse(BaseModel):
    message: str
    annotations: List[AnnotationResponse] 