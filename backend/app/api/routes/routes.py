from fastapi import APIRouter
from app.api import login, registration, screening

router = APIRouter()

router.include_router(login.router)
router.include_router(registration.router)
router.include_router(screening.router)