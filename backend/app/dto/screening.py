from pydantic import BaseModel
from typing import List, Optional


class ScreeningResultResponse(BaseModel):
    screening_id: int
    candidate_name: str
    job_title: str
    match_score: float
    matched_skills: List[str]
    missing_skills: List[str]
    experience: Optional[str] = None
    qualification: Optional[str] = None
    certifications: List[str] = []
    recommendation: Optional[str] = None
    summary: Optional[str] = None

    class Config:
        from_attributes = True