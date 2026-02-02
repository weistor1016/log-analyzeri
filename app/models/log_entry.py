from pydantic import BaseModel, Field
from typing import Optional

class LogEntry(BaseModel):
    timestamp: str
    level: str = Field(..., examples=["INFO", "ERROR"])
    service: str
    event: str
    message: str

    user_id: Optional[str] = None
    request_id: Optional[str] = None
    error_code: Optional[str] = None