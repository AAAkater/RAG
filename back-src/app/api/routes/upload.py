import os
import uuid
from typing import List

import app.metadata.audio as audio
import app.metadata.document as document
import app.metadata.image as image
import app.metadata.video as video
from app.core.log import logger
from app.model.model import UploadResponse
from fastapi import APIRouter, File, UploadFile

router = APIRouter()


@router.post("/uploadImage", response_model=UploadResponse)
async def upload_image(file: UploadFile) -> UploadResponse:

    image_uuid = str(uuid.uuid4())
    image_extension: str = file.filename.split(".")[-1]  # type: ignore
    new_name: str = f"{image_uuid}.{image_extension}"

    try:
        # 写入metadata/images
        path: str = os.path.join(os.path.dirname(image.__file__), new_name)  # type: ignore
        with open(path, "wb") as f:
            f.write(await file.read())
        return UploadResponse(code=0, data="上传成功", message="ok")
    except Exception as e:
        print(e)
        return UploadResponse(code=0, data=None, message="上传失败，网络不佳")


@router.post("/uploadDocument", response_model=UploadResponse)
async def upload_pdf(file: UploadFile) -> UploadResponse:
    pdf_uuid = str(uuid.uuid4())
    pdf_extension: str = file.filename.split(".")[-1]  # type: ignore
    new_name: str = f"{pdf_uuid}.{pdf_extension}"
    try:
        # 写入metadata/document
        path: str = os.path.join(os.path.dirname(document.__file__), new_name)  # type: ignore
        with open(path, "wb") as f:
            f.write(await file.read())
        return UploadResponse(code=0, data="上传成功", message="ok")
    except Exception as e:
        print(e)
        return UploadResponse(code=0, data=None, message="上传失败，网络不佳")


@router.post("/uploadAudio", response_model=UploadResponse)
async def upload_audio(file: UploadFile) -> UploadResponse:

    audio_uuid = str(uuid.uuid4())
    audio_extension: str = file.filename.split(".")[-1]  # type: ignore
    new_name: str = f"{audio_uuid}.{audio_extension}"
    try:
        # 写入metadata/audio
        path: str = os.path.join(os.path.dirname(audio.__file__), new_name)  # type: ignore
        content = await file.read()
        with open(path, "wb") as f:
            f.write(content)
        return UploadResponse(code=0, data="上传成功", message="ok")
    except Exception as e:
        print(e)
        return UploadResponse(code=0, data=None, message="上传失败，网络不佳")


@router.post("/uploadVideo", response_model=UploadResponse)
async def upload_Video(file: UploadFile) -> UploadResponse:

    video_uuid = str(uuid.uuid4())
    video_extension: str = file.filename.split(".")[-1]  # type: ignore
    new_name: str = f"{video_uuid}.{video_extension}"
    try:
        # 写入metadata/video
        path: str = os.path.join(os.path.dirname(video.__file__), new_name)  # type: ignore
        with open(path, "wb") as f:
            f.write(await file.read())
        return UploadResponse(code=0, data="上传成功", message="ok")
    except Exception as e:
        print(e)
        return UploadResponse(code=0, data=None, message="上传失败，网络不佳")
