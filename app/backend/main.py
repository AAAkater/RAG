from app.api import api_router
from app.middleware import app_middlewares
from fastapi import FastAPI

app = FastAPI(middleware=app_middlewares)
app.include_router(api_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
