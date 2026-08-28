import os
import shutil
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from app.db.models.user import Resume

UPLOAD_DIR = "uploaded_resumes"
ALLOWED_EXTENSIONS = [".pdf", ".doc", ".docx"]


def save_resume_file(resume: UploadFile) -> str:
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    file_ext = os.path.splitext(resume.filename)[1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Only PDF, DOC, DOCX files are allowed")

    file_path = os.path.join(UPLOAD_DIR, resume.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(resume.file, buffer)

    return file_path


def create_resume_upload(db: Session, resume: UploadFile) -> Resume:
    file_path = save_resume_file(resume)

    resume_entry = Resume(
        resume_file_name=resume.filename,
        resume_file_path=file_path
    )

    db.add(resume_entry)
    db.commit()
    db.refresh(resume_entry)

    return resume_entry