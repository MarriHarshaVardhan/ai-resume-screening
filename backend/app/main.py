from fastapi import FastAPI

from app.api.routes.routes import router

app = FastAPI()

app.include_router(router)