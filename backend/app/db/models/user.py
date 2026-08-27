from datetime import datetime

from sqlalchemy import String, Text, DateTime, ForeignKey, Float
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


# Base

class Base(DeclarativeBase):
    pass


# Mixins

class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow,
        onupdate=datetime.utcnow, nullable=False
    )


class SoftDeleteMixin:
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True
    )


# 1. USERS

class User(TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True
    )
    contact: Mapped[str] = mapped_column(
        String(20), unique=True, nullable=False, index=True
    )
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(
        String(20), default="candidate", nullable=False
    )

    resumes = relationship("Resume", back_populates="user")
    screening_results = relationship("ScreeningResult", back_populates="user")
    admin = relationship("Admin", back_populates="user", uselist=False)


# 2. RESUMES

class Resume(TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "resumes"

    resume_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    resume_file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    resume_file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    resume_text: Mapped[str | None] = mapped_column(Text)
    skills: Mapped[list | None] = mapped_column(JSONB)
    experience: Mapped[str | None] = mapped_column(String(100))
    qualification: Mapped[str | None] = mapped_column(String(255))
    certifications: Mapped[list | None] = mapped_column(JSONB)

    user = relationship("User", back_populates="resumes")
    screening_results = relationship("ScreeningResult", back_populates="resume")


# 3. JOBS

class Job(TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "jobs"

    job_id: Mapped[int] = mapped_column(primary_key=True)
    job_title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    job_description: Mapped[str | None] = mapped_column(Text)
    required_skills: Mapped[list | None] = mapped_column(JSONB)
    required_experience: Mapped[str | None] = mapped_column(String(100))
    location: Mapped[str | None] = mapped_column(String(255))
    category: Mapped[str | None] = mapped_column(String(100))

    screening_results = relationship("ScreeningResult", back_populates="job")


# 4. SCREENING RESULTS  (no soft delete, per spec)

class ScreeningResult(TimestampMixin, Base):
    __tablename__ = "screening_results"

    screening_id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True
    )
    resume_id: Mapped[int] = mapped_column(
        ForeignKey("resumes.resume_id", ondelete="CASCADE"), nullable=False, index=True
    )
    job_id: Mapped[int] = mapped_column(
        ForeignKey("jobs.job_id", ondelete="CASCADE"), nullable=False, index=True
    )

    matched_skills: Mapped[list | None] = mapped_column(JSONB)
    missing_skills: Mapped[list | None] = mapped_column(JSONB)
    match_score: Mapped[float] = mapped_column(Float, nullable=False)
    screening_result: Mapped[str] = mapped_column(String(50), nullable=False)
    recommendation: Mapped[str | None] = mapped_column(Text)

    user = relationship("User", back_populates="screening_results")
    resume = relationship("Resume", back_populates="screening_results")
    job = relationship("Job", back_populates="screening_results")


# 5. ADMINS

class Admin(TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "admins"

    admin_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id", ondelete="CASCADE"), unique=True, nullable=False
    )
    admin_name: Mapped[str] = mapped_column(String(100), nullable=False)
    admin_email: Mapped[str] = mapped_column(String(255), nullable=False)
    admin_contact: Mapped[str | None] = mapped_column(String(20))

    user = relationship("User", back_populates="admin")