from app.middleware.token import TokenMiddleware
from starlette.middleware import Middleware

app_middlewares = [Middleware(TokenMiddleware)]
