import uuid

from app.model import CaptchaItem, EmailCaptchaBody, ResponseBase
from app.utils.captcha_func import (
    generate_captcha_code,
    generate_captcha_img,
    img_to_base64,
)
from app.utils.email import send_email
from app.utils.log import logger
from app.utils.redis_api import redis_client
from fastapi import APIRouter, HTTPException, status
from pydantic import HttpUrl, validate_email
from pydantic_core import PydanticCustomError

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


@router.get(
    path="/captcha/email",
    status_code=status.HTTP_200_OK,
    response_model=ResponseBase,
)
async def get_email_captcha(
    item: EmailCaptchaBody,
) -> ResponseBase:
    # 校验邮箱格式
    try:
        _ = validate_email(value=item.email)
    except PydanticCustomError as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="邮箱格式错误",
        )
    # 查看邮箱验证码是否仍有效
    if redis_client.exists(item.email):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="验证码请求频繁",
        )

    captcha_code = generate_captcha_code()
    # 发送邮箱验证码
    try:
        await send_email(
            email=item.email,
            captcha=captcha_code,
        )
    except Exception as e:
        logger.error(msg=e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="服务器内部错误",
        )
    # 一分钟有效时间
    redis_client.setex(
        name=item.email,
        value=captcha_code,
        time=60,
    )
    return ResponseBase()


@router.post(
    path="/captcha/email",
    status_code=status.HTTP_200_OK,
    response_model=ResponseBase,
)
async def verify_email_captcha(
    item: EmailCaptchaBody,
) -> ResponseBase:
    # 校验邮箱格式
    try:
        _ = validate_email(value=item.email)
    except PydanticCustomError as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="邮箱格式错误",
        )

    # 查看邮箱验证码是否仍有效
    if not redis_client.exists(item.email):
        return ResponseBase(
            code="1",
            msg="验证码过期",
        )
    # 校验验证码
    code = redis_client.get(name=item.email)
    if code != item.email_code:
        redis_client.delete(item.email)
        return ResponseBase(
            code="2",
            msg="验证码错误",
        )

    return ResponseBase()
