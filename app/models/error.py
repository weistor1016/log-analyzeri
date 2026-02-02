from pydantic import BaseModel

def ErrorResponse(BaseModel):
    error_code: str
    message: str