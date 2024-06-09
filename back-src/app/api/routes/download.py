import os

import app.metadata.audio as audio
import app.metadata.document as document
import app.metadata.image as image
import app.metadata.video as video
from app.core.crud import database
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

router = APIRouter()


@router.get("/getImage")
async def get_image(id: str) -> FileResponse:
    """_summary_

    Args:
        id (str): _description_

    Raises:
        HTTPException: _description_
        HTTPException: _description_

    Returns:
        FileResponse: _description_
    """
    ok, image_name = database.search_image_metadata(image_id=id)
    if not ok:
        raise HTTPException(status_code=404, detail=f"图片 {id}不存在")

    image_path: str = os.path.join(os.path.dirname(image.__file__), image_name)

    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail=f"图片 {id}不存在")

    return FileResponse(path=image_path, media_type="image/jpeg")


@router.get("/getDocument")
async def get_pdf(id: str) -> FileResponse:
    """_summary_

    Args:
        id (str): _description_

    Raises:
        HTTPException: _description_
        HTTPException: _description_

    Returns:
        FileResponse: _description_
    """
    ok, document_name = database.search_document_metadata(document_id=id)
    if not ok:
        raise HTTPException(status_code=404, detail=f"文档 {id}不存在")

    document_path: str = os.path.join(os.path.dirname(document.__file__), document_name)

    if not os.path.exists(document_path):
        raise HTTPException(status_code=404, detail=f"pdf {id}不存在")

    return FileResponse(path=document_path, media_type="application/pdf")


@router.get("/getAudio")
async def get_audio(id: str) -> FileResponse:
    """_summary_

    Args:
        id (str): _description_

    Raises:
        HTTPException: _description_
        HTTPException: _description_

    Returns:
        FileResponse: _description_
    """
    ok, document_name = database.search_audio_metadata(audio_id=id)
    if not ok:
        raise HTTPException(status_code=404, detail=f"音频 {id}不存在")
    audio_path: str = os.path.join(os.path.dirname(audio.__file__), document_name)

    if not os.path.exists(audio_path):
        raise HTTPException(status_code=404, detail=f"音频 {id}不存在")

    return FileResponse(path=audio_path, media_type="audio/*")


@router.get("/getVideo")
async def get_video(id: str) -> FileResponse:
    """_summary_

    Args:
        id (str): _description_

    Raises:
        HTTPException: _description_
        HTTPException: _description_

    Returns:
        FileResponse: _description_
    """
    ok, video_name = database.search_video_metadata(video_id=id)
    if not ok:
        raise HTTPException(status_code=404, detail=f"视频 {id}不存在")
    video_path: str = os.path.join(os.path.dirname(video.__file__), video_name)

    if not os.path.exists(video_path):
        raise HTTPException(status_code=404, detail=f"视频 {id}不存在")

    return FileResponse(path=video_path, media_type="video/*")
