from fastapi import APIRouter

from app.api.routes.v1 import metadata

api_router = APIRouter()

api_router.include_router(metadata.router)
