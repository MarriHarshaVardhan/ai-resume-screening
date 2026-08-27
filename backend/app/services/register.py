import hashlib
import secrets
from datetime import datetime, timedelta, timezone
 
import jwt
from sqlalchemy.orm import Session
 
from app.core.config import settings
from app.db.models.user import User
from app.dto.register import RegistrationRequestDTO, RegistrationResponseDTO
 
 
def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    password_hash = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 600_000)
    return f"pbkdf2_sha256$600000${salt.hex()}${password_hash.hex()}"
 
 
def create_access_token(user: User) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user.user_id),
        "email": user.email,
        "role": user.role,
        "iat": now,
        "exp": now + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
 
 
def register_user(request: RegistrationRequestDTO, db: Session) -> RegistrationResponseDTO:
    user = request.data.registration
    db_user = User(
        name=user.name,
        email=user.email,
        contact=user.contact,
        password_hash=hash_password(user.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    access_token = create_access_token(db_user)
 
    return RegistrationResponseDTO(
        message="Registration successful",
        data={
            "registration": {
                "user_id": db_user.user_id,
                "name": user.name,
                "email": user.email,
                "contact": user.contact,
            }
        },
        access_token=access_token,
    )