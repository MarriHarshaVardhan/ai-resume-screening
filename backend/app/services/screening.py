from sqlalchemy.orm import Session

from app.db.models.user import ScreeningResult


def get_screening_result(
    db: Session,
    screening_id: int
):
    result = (
        db.query(ScreeningResult)
        .filter(ScreeningResult.screening_id == screening_id)
        .first()
    )

    return result