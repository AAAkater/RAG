import app.api.routes.v1.captcha as captcha
import app.api.routes.v1.chat as chat
import app.api.routes.v1.knowledge_base as knowledge_base
import app.api.routes.v1.metadata as metadata
import app.api.routes.v1.user as user
from fastapi import APIRouter

v1_router = APIRouter()

v1_router.include_router(
    router=metadata.router,
    prefix="/v1",
    tags=["metadata"],
)
v1_router.include_router(
    router=chat.router,
    prefix="/v1",
    tags=["chat"],
)
v1_router.include_router(
    router=knowledge_base.router,
    prefix="/v1",
    tags=["knowledge_base"],
)
v1_router.include_router(
    router=user.router,
    prefix="/v1",
    tags=["user"],
)
v1_router.include_router(
    router=captcha.router,
    prefix="/v1",
    tags=["verify"],
)
