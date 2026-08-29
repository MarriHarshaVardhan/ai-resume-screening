from pydantic import BaseModel


class ResumeUploadResponse(BaseModel):
    resume_id: int
    resume_file_name: str

    class Config:
        from_attributes = True