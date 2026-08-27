from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
 
from app.db.database import get_db
from app.dto.register import RegistrationRequestDTO, RegistrationResponseDTO
from app.services.register import register_user
 
 
router = APIRouter()
 
 
@router.post("/register", response_model=RegistrationResponseDTO, status_code=status.HTTP_201_CREATED)
def registration(request: RegistrationRequestDTO, db: Session = Depends(get_db)):
    return register_user(request, db)
 