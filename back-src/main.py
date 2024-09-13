from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.api.main import api_router

app = FastAPI()


app.include_router(api_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
