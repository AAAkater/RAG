import os

import app.metadata.audio as audio
import app.metadata.document as document
import app.metadata.images as images
import app.metadata.video as video
from app.model.model import UploadResponse
from fastapi import APIRouter, UploadFile

router = APIRouter()


@router.post("/uploadImage", response_model=UploadResponse)
async def upload_image(file: UploadFile) -> UploadResponse:
    try:
        # 写入metadata/images
        path: str = os.path.join(os.path.dirname(images.__file__), file.filename)  # type: ignore
        with open(path, "wb") as f:
            f.write(await file.read())
        return UploadResponse(code=0, data="上传成功", message="ok")
    except Exception as e:
        print(e)
        return UploadResponse(code=0, data=None, message="上传失败，网络不佳")


@router.post("/uploadDocument", response_model=UploadResponse)
async def upload_pdf(file: UploadFile) -> UploadResponse:
    try:
        # 写入metadata/document
        path: str = os.path.join(os.path.dirname(document.__file__), file.filename)  # type: ignore
        with open(path, "wb") as f:
            f.write(await file.read())
        return UploadResponse(code=0, data="上传成功", message="ok")
    except Exception as e:
        print(e)
        return UploadResponse(code=0, data=None, message="上传失败，网络不佳")


@router.post("/uploadAudio", response_model=UploadResponse)
async def upload_audio(file: UploadFile) -> UploadResponse:
    try:
        # 写入metadata/audio
        path: str = os.path.join(os.path.dirname(audio.__file__), file.filename)  # type: ignore
        with open(path, "wb") as f:
            f.write(await file.read())
        return UploadResponse(code=0, data="上传成功", message="ok")
    except Exception as e:
        print(e)
        return UploadResponse(code=0, data=None, message="上传失败，网络不佳")


@router.post("/uploadVideo", response_model=UploadResponse)
async def upload_Video(file: UploadFile) -> UploadResponse:
    try:
        # 写入metadata/video
        path: str = os.path.join(os.path.dirname(video.__file__), file.filename)  # type: ignore
        with open(path, "wb") as f:
            f.write(await file.read())
        return UploadResponse(code=0, data="上传成功", message="ok")
    except Exception as e:
        print(e)
        return UploadResponse(code=0, data=None, message="上传失败，网络不佳")
