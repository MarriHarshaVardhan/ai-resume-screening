from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse  # type: ignore
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.screening_result import (
    generate_screening_report,
    get_screening_result,
)

router = APIRouter(
    prefix="/screening-result",
    tags=["Screening Result"],
)


@router.get("/{screening_id}")
def view_screening_result(
    screening_id: int,
    db: Session = Depends(get_db),
):
    result = get_screening_result(
        db=db,
        screening_id=screening_id,
    )

    return {
        "screening_id": result.screening_id,
        "candidate_name": result.user.name,
        "job_title": result.job.job_title,
        "match_score": result.match_score,
        "matched_skills": result.matched_skills,
        "missing_skills": result.missing_skills,
        "experience": result.resume.experience,
        "qualification": result.resume.qualification,
        "certifications": result.resume.certifications,
        "recommendation": result.recommendation,
        "summary": result.screening_result,
    }


@router.get("/{screening_id}/download")
def download_screening_report(
    screening_id: int,
    db: Session = Depends(get_db),
):
    pdf_file = generate_screening_report(
        db=db,
        screening_id=screening_id,
    )

    return StreamingResponse(
        pdf_file,
        media_type="application/pdf",
        headers={
            "Content-Disposition": (
                f'attachment; filename="screening_report_{screening_id}.pdf"'
            )
        },
    )