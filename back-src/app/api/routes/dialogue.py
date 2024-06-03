from fastapi import APIRouter

from app.model.model import ClearResponse, QueryResponse

router = APIRouter()


@router.post("/clear", response_model=ClearResponse)
def clear_context() -> ClearResponse:

    return ClearResponse(code=0, data="清空成功", message="ok")


@router.get("/query", response_model=QueryResponse)
def get_answer() -> QueryResponse:

    return QueryResponse(
        code=0,
        data={
            "answer": "一些死数据",
            "metadata": [
                {
                    "type": "image",
                    "filename": "asdasd",
                    "id": "00b0ddf9b7737dc34ca23c36ae6f0688a0fca215c910bc2d33089f96fc4234bf",
                },
                {
                    "type": "pdf",
                    "filename": "asdasd",
                    "id": "0ca66aa3fd5718b7addf3665ae200d86c79fc31eb31204a53c11204f1f0c8951",
                },
                {
                    "type": "mp4",
                    "filename": "asdasd",
                    "id": "1e3fd8c58f8df392c7c5269b65e1ab70b1b1a8414f01da9a9b672945a507f80c",
                },
                {
                    "type": "mp3",
                    "filename": "asdasd",
                    "id": "1f9839a22c058c24634b53372dab9c66b2703efa2ffe28a3b6f6686937e044c7",
                },
            ],
        },
        message="ok",
    )
