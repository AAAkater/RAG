from app.api import api_router
from fastapi import FastAPI

app = FastAPI()


app.include_router(api_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
