from fastapi import APIRouter

from app.api.routes.v1 import v1_router
from app.api.routes.v2 import v2_router

api_router = APIRouter()

api_router.include_router(
    router=v1_router,
    prefix="/api",
)
api_router.include_router(
    router=v2_router,
    prefix="/api",
)
