from typing import Any, Dict, List

from pydantic import BaseModel, Field


class ResponseBase(BaseModel):
    code: str = Field(default="0", description="Business Code")
    msg: str = Field(default="ok")


class UploadMetadataItem(BaseModel):
    knowledge_base_name: str = Field(default="")
    files: List[str] = Field(default=[])


class UploadMetadataResponse(ResponseBase):
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


class GetMetadataItemsResponse(ResponseBase):
    data: MetadataItem


class CaptchaItem(BaseModel):
    captchaId: str
    captchaImgBase64: str


class GetCaptchaResponse(ResponseBase):
    data: CaptchaItem


class VerifyGetCaptchaResponse(ResponseBase):
    data: Any


# class UserBody(BaseModel):


if __name__ == "__main__":
    data = UploadMetadataResponse(
        code="0",
        msg=f"The knowledge base does not exist:",
        data=UploadMetadataItem(knowledge_base_name="hello", files=["ddd.png"]),
    ).model_dump_json()
    print(data)
