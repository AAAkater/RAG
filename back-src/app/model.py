from typing import Any, Dict, List

from pydantic import BaseModel, Field


class State404Response(BaseModel):
    code: str = Field(default="0", description="Business Code")
    msg: str = Field(default="Resource does not exist")
    data: Any = None


class UploadMetadataItem(BaseModel):
    knowledge_base_name: str = Field(default="")
    files: List[str] = Field(default=[])


class UploadMetadataResponse(BaseModel):

    code: str = Field(default="0", description="Business Code")
    msg: str = Field(default="ok")
    data: UploadMetadataItem | None = Field(default=None)


class MetadataItem(BaseModel):
    knowledge_base_name: str
    metadata: List[str]
    curPageNum: int
    hasNext: bool
    hasPrev: bool
    numPerPage: int
    tasks: Any
    totalNum: int
    totalPageNum: int


class GetMetadataItemsResponse(BaseModel):

    code: str = Field(default="0", description="Business Code")
    msg: str = Field(default="ok")
    data: MetadataItem


class CaptchaItem(BaseModel):
    captchaId: str
    captchaImgBase64: str


class GetCaptchaResponse(BaseModel):
    code: str
    msg: str
    data: CaptchaItem


class VerifyGetCaptchaResponse(BaseModel):
    code: str
    msg: str
    data: Any


if __name__ == "__main__":
    data = State404Response(
        code="0",
        msg=f"The knowledge base does not exist:",
        data=None,
    ).model_dump_json()
    print(data)
