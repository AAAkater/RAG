from typing import Any, Dict, Optional
from pydantic import BaseModel


class UploadResponse(BaseModel):
    code: int
    data: Optional[str]
    message: str


class ClearResponse(BaseModel):
    code: int
    data: Optional[str]
    message: str


class QueryResponse(BaseModel):
    code: int
    data: Dict[str, Any]
    message: str
