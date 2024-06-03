import os

import app.metadata.document as document
import app.metadata.images as images
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
async def get_pdf(id: str):

    pdf_path: str = os.path.join(os.path.dirname(document.__file__), f"{id}.pdf")

    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="pdf不存在")

    return FileResponse(path=pdf_path, media_type="application/pdf")
