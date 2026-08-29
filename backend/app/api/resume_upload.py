from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dto.resume_upload import ResumeUploadResponse
from app.services.resume_upload import create_resume_upload

router = APIRouter(prefix="/resume", tags=["Resume Upload"])


@router.post("/upload", response_model=ResumeUploadResponse)
def upload_resume(
    resume: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Only resume file is needed for this endpoint
    resume_upload = create_resume_upload(db, resume)
    return resume_upload