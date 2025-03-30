from app.core.config import settings
from app.utils.log import logger
from app.utils.security import get_current_user
from fastapi import HTTPException, Request, Response, status
from starlette.middleware.base import BaseHTTPMiddleware

no_auth_paths = [
    f"{settings.API_VER_STR}/login",
    f"{settings.API_VER_STR}/user",
    f"{settings.API_VER_STR}/captcha",
    f"{settings.API_VER_STR}/captcha/email",
    "/docs",
    "/openapi.json",
]


class TokenMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, req: Request, call_next) -> Response:

        # 忽略不需要鉴权的接口
        path: str = req.url.path
        if path in no_auth_paths:
            return await call_next(req)
        # 检查权限
        authorization = req.headers.get("Authorization")
        if not authorization:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="无权限",
            )
        token = authorization.split(" ")[1]
        if get_current_user(token):
            return await call_next(req)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="无权限",
            )
