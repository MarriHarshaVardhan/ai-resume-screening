from typing import Any

from pydantic import BaseModel


class ScreeningResultResponse(BaseModel):
    screening_id: int
    candidate_name: str | None = None
    job_title: str | None = None
    match_score: float | None = None
    matched_skills: Any = None
    missing_skills: Any = None
    experience: str | None = None
    qualification: str | None = None
    certifications: Any = None
    recommendation: str | None = None
    summary: str | None = None