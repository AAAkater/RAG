from app.core.retrieval_qa import retrieval
from app.model.model import ClearResponse, QueryResponse
from fastapi import APIRouter

router = APIRouter()


@router.post("/clear", response_model=ClearResponse)
def clear_context() -> ClearResponse:
    retrieval.clear_history()
    return ClearResponse(code=0, data="清空成功", message="ok")


@router.get("/query", response_model=QueryResponse)
async def get_answer(desc: str) -> QueryResponse:

    result = retrieval.invoke(desc)
    answer = result["answer"]
    image_ids: list[str] = [doc.metadata["id"] for doc in result["context"]]
    image_names: list[str] = [doc.metadata["metadata"] for doc in result["context"]]

    metadata = [
        {"type": "image", "filename": image_name, "id": id}
        for image_name, id in zip(image_names, image_ids)
    ]

    return QueryResponse(
        code=0, data={"answer": answer, "metadata": metadata}, message="ok"
    )
