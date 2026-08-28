from fastapi import APIRouter, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.screening import create_screening
from app.dto.screening import ScreeningResponse

router = APIRouter(prefix="/screening", tags=["Screening"])


@router.post("/start", response_model=ScreeningResponse)
def start_screening(
    job_title: str = Form(...),
    required_skills: str = Form(...),
    resume: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    screening = create_screening(db, job_title, required_skills, resume)

    return ScreeningResponse(
        id=screening.id,
        job_title=screening.job_title,
        required_skills=[skill.strip() for skill in screening.required_skills.split(",")],
        resume_filename=screening.resume_filename,
        status=screening.status
    )