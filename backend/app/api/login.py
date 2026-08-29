import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dto.login import LoginRequestDTO
from app.services.login import login_user

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/login")
def login(
    request: LoginRequestDTO,
    db: Session = Depends(get_db)
):
    logger.info("POST /auth/login")

    return login_user(request, db)