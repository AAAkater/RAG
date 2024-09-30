import uuid

from fastapi import APIRouter, HTTPException, status

from app.model import CaptchaItem, GetCaptchaResponse, VerifyGetCaptchaResponse
from app.utils.captcha_ import (
    generate_captcha_code,
    generate_captcha_img,
    img_to_base64,
)

router = APIRouter()


@router.get(
    path="/captcha",
    status_code=status.HTTP_200_OK,
    response_model=GetCaptchaResponse,
    summary="",
)
async def get_captcha() -> GetCaptchaResponse:
    captcha_id = uuid.uuid4().hex
    captcha_code = generate_captcha_code()
    captcha_img = generate_captcha_img(code=captcha_code)
    captcha_img_base64 = img_to_base64(captcha_img)
    return GetCaptchaResponse(
        code="0",
        msg="ok",
        data=CaptchaItem(captchaId=captcha_id, captchaImgBase64=captcha_img_base64),
    )


@router.post(
    path="/captcha/{captcha_id}/{captcha_code}",
    status_code=status.HTTP_200_OK,
    response_model=VerifyGetCaptchaResponse,
)
async def verify_captcha(
    captcha_id: str, captcha_code: str
) -> VerifyGetCaptchaResponse:
    # mock
    if captcha_id == "2fc1176d85aa45589e463a1897397484":
        if captcha_code == "1234":
            return VerifyGetCaptchaResponse(code="0", msg="ok", data=None)
        else:
            return VerifyGetCaptchaResponse(code="1", msg="验证码错误", data=None)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"不存在该验证码:{captcha_id}"
        )


@router.put(
    path="/captcha/{captcha_id}",
    status_code=status.HTTP_200_OK,
    response_model=GetCaptchaResponse,
)
async def refresh_captcha(captcha_id: str) -> GetCaptchaResponse:
    # mock
    new_captcha_id = captcha_id
    return GetCaptchaResponse(
        code="0",
        msg="ok",
        data=CaptchaItem(captchaId=new_captcha_id, captchaImgBase64="asfsafasa"),
    )
