from pydantic import BaseModel


class ScreeningResultResponse(BaseModel):
    screening_id: int
    candidate_name: str
    job_title: str
    match_score: float
    matched_skills: list[str]
    missing_skills: list[str]
    experience: str | None = None
    qualification: str | None = None
    certifications: list[str] = []
    recommendation: str | None = None
    summary: str | None = None

    class Config:
        from_attributes = True