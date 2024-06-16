import os
import uuid
from typing import List

import app.metadata.audio as audio
import app.metadata.document as document
import app.metadata.image as image
import app.metadata.video as video
from app.core.crud import database
from app.core.log import logger
from app.model.model import UploadResponse
from fastapi import APIRouter, File, UploadFile

router = APIRouter()


@router.post("/uploadImage", response_model=UploadResponse)
async def upload_image(file: UploadFile) -> UploadResponse:
    """_summary_

    Args:
        file (UploadFile): _description_

    Returns:
        UploadResponse: _description_
    """
    # 文件名修改
    image_uuid = str(uuid.uuid4())
    image_extension: str = file.filename.split(".")[-1]  # type: ignore
    new_name: str = f"{image_uuid}.{image_extension}"

    try:
        # 写入metadata/images本地
        path: str = os.path.join(os.path.dirname(image.__file__), new_name)  # type: ignore
        with open(path, "wb") as f:
            f.write(await file.read())
        # 写入milvus
        database.insert_image(
            uuid=image_uuid, new_name=new_name, old_name=file.filename
        )
        # print(f"{image_uuid=}")
        # print(f"{new_name}")
        return UploadResponse(code=0, data="上传成功", message="ok")
    except Exception as e:
        print(e)
        return UploadResponse(code=0, data=None, message="上传失败，网络不佳")


@router.post("/uploadDocument", response_model=UploadResponse)
async def upload_document(file: UploadFile) -> UploadResponse:
    """_summary_

    Args:
        file (UploadFile): _description_

    Returns:
        UploadResponse: _description_
    """
    try:
        # 写入metadata/document
        path: str = os.path.join(os.path.dirname(document.__file__), file.filename)  # type: ignore
        with open(path, "wb") as f:
            f.write(await file.read())
        # 写入milvus
        database.insert_document(file_name=file.filename)
        return UploadResponse(code=0, data="上传成功", message="ok")
    except Exception as e:
        print(e)
        return UploadResponse(code=0, data=None, message="上传失败，网络不佳")


@router.post("/uploadAudio", response_model=UploadResponse)
async def upload_audio(file: UploadFile) -> UploadResponse:
    """_summary_

    Args:
        file (UploadFile): _description_

    Returns:
        UploadResponse: _description_
    """
    try:
        # 写入metadata/audio
        path: str = os.path.join(os.path.dirname(audio.__file__), file.filename)  # type: ignore
        content = await file.read()
        with open(path, "wb") as f:
            f.write(content)
        # 写入milvus
        database.insert_audio(file_name=file.filename)
        return UploadResponse(code=0, data="上传成功", message="ok")
    except Exception as e:
        print(e)
        return UploadResponse(code=0, data=None, message="上传失败，网络不佳")


@router.post("/uploadVideo", response_model=UploadResponse)
async def upload_Video(file: UploadFile) -> UploadResponse:
    """_summary_

    Args:
        file (UploadFile): _description_

    Returns:
        UploadResponse: _description_
    """
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
