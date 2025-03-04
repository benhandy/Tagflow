from pydantic import BaseModel
from typing import Optional

class ErrorDetail(BaseModel):
    type: str
    code: str
    message: str
    details: Optional[dict] = None

class ErrorResponse(BaseModel):
    error: ErrorDetail 