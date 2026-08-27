import logging
import re

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from pwdlib import PasswordHash
import jwt
from datetime import datetime, timedelta, timezone

from app.core.config import settings
from app.db.models.user import User
from app.dto.login import LoginRequestDTO


logger = logging.getLogger(__name__)

password_hash = PasswordHash.recommended()


def login_user(request: LoginRequestDTO, db: Session):

    logger.info("Login request received")

    login_data = request.data.login

    email = login_data.email
    password = login_data.password

    # Email validation
    if not email:
        logger.warning("Login failed: Email is required")

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is required"
        )

    email_pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

    if not re.match(email_pattern, email):
        logger.warning("Login failed: Invalid email format")

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format"
        )

    # Password validation
    if not password:
        logger.warning("Login failed: Password is required")

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password is required"
        )

    # Find user
    user = (
        db.query(User)
        .filter(
            User.email == email,
            User.deleted_at.is_(None)
        )
        .first()
    )

    if not user:
        logger.warning(
            "Login failed: User not found for email %s",
            email
        )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Verify password
    try:
        password_valid = password_hash.verify(
            password,
            user.password_hash
        )
    except Exception:
        logger.exception("Password verification failed")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Password verification failed"
        )

    if not password_valid:
        logger.warning(
            "Login failed: Invalid password for email %s",
            email
        )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Create JWT token
    try:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        )

        payload = {
            "sub": str(user.user_id),
            "email": user.email,
            "role": user.role,
            "exp": expire
        }

        access_token = jwt.encode(
            payload,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM
        )

    except Exception:
        logger.exception("JWT token generation failed")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to generate access token"
        )

    logger.info(
        "Login successful for user_id=%s",
        user.user_id
    )

    return {
        "message": "Login successful",
        "data": {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "user_id": user.user_id,
                "name": user.name,
                "email": user.email,
                "role": user.role
            }
        }
    }