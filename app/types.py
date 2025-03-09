from pydantic import BaseModel


class GenerateRequest(BaseModel):
    type: str
    job_role: str
    days_off: int
    constraints: str


class GenerateResponse(BaseModel):
    excuse: str
