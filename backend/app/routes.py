from fastapi import APIRouter

from app.api.login import router as login_router
from app.api.auth import router as auth_router
from app.api.register import router as register_router
from app.api.screening_result import router as screening_result_router

router = APIRouter()

router.include_router(register_router, prefix="/api")
router.include_router(login_router)
router.include_router(auth_router, prefix="/api")
router.include_router(screening_result_router, prefix="/api")