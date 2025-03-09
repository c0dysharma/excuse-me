from pydantic import BaseModel


class GenerateRequest(BaseModel):
    type: str
    days_off: int

class GenerateResponse(BaseModel):
    excuse: str
