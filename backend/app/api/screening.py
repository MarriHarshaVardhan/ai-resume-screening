from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.screening import get_screening_result
from app.dto.screening import ScreeningResultResponse


router = APIRouter(
    prefix="/screening",
    tags=["Screening"]
)


@router.get(
    "/{screening_id}",
    response_model=ScreeningResultResponse
)
def view_screening_result(
    screening_id: int,
    db: Session = Depends(get_db)
):
    result = get_screening_result(
        db=db,
        screening_id=screening_id
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Screening result not found"
        )

    return result