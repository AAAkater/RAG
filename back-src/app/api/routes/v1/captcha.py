import uuid

from app.model import CaptchaItem, ResponseBase
from app.utils.captcha_func import (
    generate_captcha_code,
    generate_captcha_img,
    img_to_base64,
)
from app.utils.log import logger
from app.utils.redis_api import redis_client
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import RedirectResponse

router = APIRouter()


def init_captcha():
    captcha_id = uuid.uuid4().hex
    captcha_code = generate_captcha_code()
    logger.info(f"{captcha_code=}")
    # * 写入redis 有效期两分钟
    redis_client.setex(name=captcha_id, time=120, value=captcha_code)

    captcha_img = generate_captcha_img(code=captcha_code)
    captcha_img_base64: str = img_to_base64(captcha_img)
    return (captcha_id, captcha_code, captcha_img_base64)


@router.get(
    path="/captcha",
    status_code=status.HTTP_200_OK,
    response_model=ResponseBase[CaptchaItem],
    summary="",
)
async def get_captcha() -> ResponseBase[CaptchaItem]:
    id, code, img_base64 = init_captcha()
    return ResponseBase[CaptchaItem](
        data=CaptchaItem(captchaId=id, captchaImgBase64=img_base64),
    )


@router.post(
    path="/captcha/{captcha_id}/{captcha_code}",
    status_code=status.HTTP_200_OK,
    response_model=ResponseBase,
)
async def verify_captcha(captcha_id: str, captcha_code: str):
    code = redis_client.get(name=captcha_id)
    if code is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"不存在该验证码:{captcha_id}"
        )
    logger.info(f"{code=}")
    if code == captcha_code:
        return ResponseBase()
    else:
        return ResponseBase(code="1", msg="验证码错误", data=None)


@router.put(
    path="/captcha/{old_captcha_id}",
    status_code=status.HTTP_200_OK,
    response_model=ResponseBase[CaptchaItem],
)
async def refresh_captcha(old_captcha_id: str) -> ResponseBase[CaptchaItem]:

    # 删除该验证码
    redis_client.delete(old_captcha_id)
    logger.info(f"{old_captcha_id=}")

    id, code, img_base64 = init_captcha()
    return ResponseBase[CaptchaItem](
        data=CaptchaItem(captchaId=id, captchaImgBase64=img_base64),
    )
