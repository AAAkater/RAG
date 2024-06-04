import os

import app.metadata.audio as audio
import app.metadata.document as document
import app.metadata.images as images
import app.metadata.video as video
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

router = APIRouter()


@router.get("/getImage")
async def get_image(id: str) -> FileResponse:

    image_path: str = os.path.join(os.path.dirname(images.__file__), f"{id}.jpg")

    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="图片不存在")

    return FileResponse(path=image_path, media_type="image/jpeg")


@router.get("/getDocument")
async def get_pdf(id: str) -> FileResponse:

    pdf_path: str = os.path.join(os.path.dirname(document.__file__), f"{id}.pdf")

    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="pdf不存在")

    return FileResponse(path=pdf_path, media_type="application/pdf")


@router.get("/getAudio")
async def get_audio(id: str) -> FileResponse:

    pdf_path: str = os.path.join(os.path.dirname(audio.__file__), f"{id}.mp3")

    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="音频不存在")

    return FileResponse(path=pdf_path, media_type="audio/mpeg")


@router.get("/getVideo")
async def get_video(id: str) -> FileResponse:

    pdf_path: str = os.path.join(os.path.dirname(video.__file__), f"{id}.mp4")

    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="视频不存在")

    return FileResponse(path=pdf_path, media_type="video/mp4")
