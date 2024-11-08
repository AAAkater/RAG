from typing import Any, Generic, List, TypeVar

from pydantic import BaseModel, EmailStr, Field

T = TypeVar("T")


class ResponseBase(BaseModel, Generic[T]):
    code: str = Field(default="0", description="Business Code")
    msg: str = Field(default="ok")
    data: T | None = None


class UploadMetadataItem(BaseModel):
    knowledge_base_name: str = Field(default="")
    files: List[str] = Field(default=[])


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


class CaptchaItem(BaseModel):
    captchaId: str
    captchaImgBase64: str


class EmailCaptchaBody(BaseModel):
    email: str
    email_code: str | None = None


class UserRegisterBody(BaseModel):
    email: str
    email_code: str
    password: str


class UserLoginBody(BaseModel):
    username: str
    password: str
    captcha_id: str
    captcha_code: str


class TokenPayLoad(BaseModel):
    exp: str
    sub: str


if __name__ == "__main__":
    data = ResponseBase[UploadMetadataItem](
        code="0",
        msg="ok",
        data=UploadMetadataItem(knowledge_base_name="ddd", files=["asdasd.png"]),
    )
    print(data.model_dump())
