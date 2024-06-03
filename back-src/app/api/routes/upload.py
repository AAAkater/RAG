import os

import app.metadata.document as document
import app.metadata.images as images
from app.model.model import UploadResponse
from fastapi import APIRouter, UploadFile

router = APIRouter()


@router.post("/uploadImage", response_model=UploadResponse)
async def upload_image(file: UploadFile = UploadFile(...)) -> UploadResponse:
    try:
        # 写入metadata/images
        path: str = os.path.join(os.path.dirname(images.__file__), file.filename)
        with open(path, "wb") as f:
            f.write(await file.read())
        return UploadResponse(code=0, data="上传成功", message="ok")
    except Exception as e:
        print(e)
        return UploadResponse(code=0, data=None, message="上传失败，网络不佳")


@router.post("/uploadDocument", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = UploadFile(...)) -> UploadResponse:
    try:
        # 写入metadata/images
        path: str = os.path.join(os.path.dirname(document.__file__), file.filename)
        with open(path, "wb") as f:
            f.write(await file.read())
        return UploadResponse(code=0, data="上传成功", message="ok")
    except Exception as e:
        print(e)
        return UploadResponse(code=0, data=None, message="上传失败，网络不佳")
