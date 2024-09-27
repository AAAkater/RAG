from fastapi import APIRouter

import app.api.routes.v1.dialog as dialog
import app.api.routes.v1.knowledge_base as knowledge_base
import app.api.routes.v1.metadata as metadata
import app.api.routes.v1.user as user

v1_router = APIRouter()

v1_router.include_router(router=metadata.router, prefix="/v1", tags=["metadata"])
v1_router.include_router(router=dialog.router, prefix="/v1", tags=["dialog"])
v1_router.include_router(
    router=knowledge_base.router, prefix="/v1", tags=["knowledge_base"]
)
v1_router.include_router(router=user.router, prefix="v1", tags=["user"])
