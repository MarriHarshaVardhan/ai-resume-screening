from fastapi import APIRouter  # type: ignore

from app.api.auth import router as auth_router
from app.api.login import router as login_router
from app.api.register import router as register_router
from app.api.resume_upload import router as resume_upload_router

router = APIRouter()

router.include_router(register_router, prefix="/api")
router.include_router(auth_router, prefix="/api")
router.include_router(resume_upload_router, prefix="/api")
router.include_router(login_router, prefix="/api")
