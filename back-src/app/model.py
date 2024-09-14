from typing import Any, Dict, List

from pydantic import BaseModel, Field


class State404Response(BaseModel):
    code: str = Field(default="0", description="Business Code")
    msg: str = Field(default="Resource does not exist")
    data: Any = None


class UploadMetadataResponse(BaseModel):
    class UploadMetadataItem(BaseModel):
        knowledge_base_name: str = Field(default="")
        files: List[str] = Field(default=[])

    code: str = Field(default="0", description="Business Code")
    msg: str = Field(default="ok")
    data: UploadMetadataItem | None = Field(default=None)


class GetMetadataItemsResponse(BaseModel):
    class MetadataItems(BaseModel):
        knowledge_base_name: str
        metadata: List[str]
        curPageNum: int
        hasNext: bool
        hasPrev: bool
        numPerPage: 10
        tasks: Any
        totalNum: int
        totalPageNum: int

    code: str = Field(default="0", description="Business Code")
    msg: str = Field(default="ok")
    data: MetadataItems


if __name__ == "__main__":
    data = State404Response(
        code="0",
        msg=f"The knowledge base does not exist:",
        data=None,
    ).model_dump_json()
    print(data)
