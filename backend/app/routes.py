from fastapi import APIRouter

from app.api.login import router as login_router


router = APIRouter()

router.include_router(login_router)