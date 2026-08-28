from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dto.registration import RegistrationRequestDTO, RegistrationResponseDTO
from app.services.auth import register
from app.db.database import get_db


router = APIRouter()


def register_user(
    request: RegistrationRequestDTO,
    db: Session,
) -> RegistrationResponseDTO:
    user = request.data.registration
    created_user = register(
        db=db,
        name=user.name,
        email=user.email,
        contact=user.contact,
        password=user.password,
    )

    return RegistrationResponseDTO(
        message="Registration successful",
        data={
            "registration": {
                "user_id": created_user.user_id,
                "name": created_user.name,
                "email": created_user.email,
                "contact": created_user.contact,
            }
        }
    )


@router.post(
    "/register",
    response_model=RegistrationResponseDTO,
    status_code=status.HTTP_201_CREATED,
)
def registration(
    request: RegistrationRequestDTO,
    db: Session = Depends(get_db),
):
    return register_user(request, db)
