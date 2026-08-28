from typing import Any, Optional

from pydantic import BaseModel


class ScreeningResultResponse(BaseModel):
    screening_id: int
    candidate_name: Optional[str] = None
    job_title: Optional[str] = None
    match_score: Optional[float] = None
    matched_skills: Any = None
    missing_skills: Any = None
    experience: Optional[str] = None
    qualification: Optional[str] = None
    certifications: Any = None
    recommendation: Optional[str] = None
    summary: Optional[str] = None