from pydantic import BaseModel
from typing import List

class ScreeningResponse(BaseModel):
    id: int
    job_title: str
    required_skills: List[str]
    resume_filename: str
    status: str

    class Config:
        from_attributes = True