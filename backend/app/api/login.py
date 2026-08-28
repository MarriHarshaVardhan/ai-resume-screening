from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dto.login import LoginRequestDTO, LoginResponseDTO
from app.services.auth import authenticate
from app.db.database import get_db


router = APIRouter()


def login_user(
    request: LoginRequestDTO,
    db: Session,
) -> LoginResponseDTO:
    user = request.data
    authenticated_user = authenticate(
        db=db,
        email=user.email,
        password=user.password,
    )

    return LoginResponseDTO(
        message="Login successful",
        data={
            "login": {
                "email": user.email
            }
        }
    )


@router.post(
    "/login",
    response_model=LoginResponseDTO,
    status_code=status.HTTP_200_OK,
)
def login(
    request: LoginRequestDTO,
    db: Session = Depends(get_db),
):
    return login_user(request, db)
