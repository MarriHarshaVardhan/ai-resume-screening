import logging
from fastapi import FastAPI

from app.routes import router


logging.basicConfig(level=logging.INFO,format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Resume Screening API",version="1.0.0")
app.include_router(router)



@app.get("/")
def root():
    logger.info("Root endpoint called")

    return {
        "message": "AI Resume Screening API is running"
    }