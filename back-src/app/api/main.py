from app.api.routes import dialogue, download, upload
from fastapi import APIRouter

api_router = APIRouter()


api_router.include_router(dialogue.router)
api_router.include_router(upload.router)
api_router.include_router(download.router)
