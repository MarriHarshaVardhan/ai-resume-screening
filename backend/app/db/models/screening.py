from sqlalchemy import Column, Integer, String, Text, LargeBinary
from app.db.database import Base

class Screening(Base):
    __tablename__ = "screenings"

    id = Column(Integer, primary_key=True, index=True)
    job_title = Column(String(255), nullable=False)
    required_skills = Column(Text, nullable=False)  # stored as comma separated string
    resume_filename = Column(String(255), nullable=False)
    resume_path = Column(String(500), nullable=True)
    resume_content = Column(LargeBinary, nullable=True)
    status = Column(String(50), default="pending")