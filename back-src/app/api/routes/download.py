import os

import app.metadata.audio as audio
import app.metadata.document as document
import app.metadata.image as image
import app.metadata.video as video
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

router = APIRouter()


@router.get("/getImage")
async def get_image(id: str) -> FileResponse:

    image_path: str = os.path.join(os.path.dirname(image.__file__), f"{id}")

    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail=f"图片 {id}不存在")

    return FileResponse(path=image_path, media_type="image/jpeg")


@router.get("/getDocument")
async def get_pdf(id: str) -> FileResponse:

    pdf_path: str = os.path.join(os.path.dirname(document.__file__), f"{id}")

    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail=f"pdf {id}不存在")

    return FileResponse(path=pdf_path, media_type="application/pdf")


@router.get("/getAudio")
async def get_audio(id: str) -> FileResponse:

    audio_path: str = os.path.join(os.path.dirname(audio.__file__), f"{id}")

    if not os.path.exists(audio_path):
        raise HTTPException(status_code=404, detail=f"音频 {id}不存在")

    return FileResponse(path=audio_path, media_type="audio/*")


@router.get("/getVideo")
async def get_video(id: str) -> FileResponse:

    video_path: str = os.path.join(os.path.dirname(video.__file__), f"{id}")

    if not os.path.exists(video_path):
        raise HTTPException(status_code=404, detail=f"视频 {id}不存在")

    return FileResponse(path=video_path, media_type="video/*")
