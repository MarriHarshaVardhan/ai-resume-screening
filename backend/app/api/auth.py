from fastapi import APIRouter, Depends
 
from app.core.security import get_current_user
from app.db.models.user import User
 
 
router = APIRouter(prefix="/auth", tags=["Authentication"])
 
 
@router.get("/me")
def current_user(user: User = Depends(get_current_user)):
    return {
        "user_id": user.user_id,
        "name": user.name,
        "email": user.email,
        "contact": user.contact,
        "role": user.role,
    }
 
 