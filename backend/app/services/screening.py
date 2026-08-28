import os
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from app.db.models.screening import Screening

ALLOWED_EXTENSIONS = [".pdf", ".doc", ".docx"]


def read_resume_file(resume: UploadFile) -> tuple[str, bytes]:
    original_filename = resume.filename or "resume"
    file_ext = os.path.splitext(original_filename)[1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Only PDF, DOC, DOCX files are allowed")

    return original_filename, resume.file.read()


def create_screening(db: Session, job_title: str, required_skills: str, resume: UploadFile) -> Screening:
    # Job title is required to confirm and start screening
    if not job_title or job_title.strip() == "":
        raise HTTPException(status_code=400, detail="Job title is required to start screening")

    if not required_skills or required_skills.strip() == "":
        raise HTTPException(status_code=400, detail="Required skills cannot be empty")

    original_filename, resume_content = read_resume_file(resume)

    screening = Screening(
        job_title=job_title.strip(),
        required_skills=required_skills.strip(),
        resume_filename=original_filename,
        resume_content=resume_content,
        status="pending"
    )

    db.add(screening)
    db.commit()
    db.refresh(screening)

    return screening