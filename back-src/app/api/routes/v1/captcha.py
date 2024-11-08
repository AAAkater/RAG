from app.model import CaptchaItem, EmailCaptchaBody, ResponseBase
from app.utils.captcha_func import generate_captcha_code, init_captcha, verify_captcha
from app.utils.email import send_email
from app.utils.log import logger
from app.utils.redis_api import redis_client
from fastapi import APIRouter, HTTPException, status
from pydantic import validate_email
from pydantic_core import PydanticCustomError

router = APIRouter()


@router.get(
    path="/captcha",
    status_code=status.HTTP_200_OK,
    response_model=ResponseBase[CaptchaItem],
    summary="生成图片验证码",
)
async def get_image_captcha() -> ResponseBase[CaptchaItem]:
    id, _, img_base64 = init_captcha()
    return ResponseBase[CaptchaItem](
        data=CaptchaItem(
            captchaId=id,
            captchaImgBase64=img_base64,
        ),
    )


@router.post(
    path="/captcha/{captcha_id}/{captcha_code}",
    status_code=status.HTTP_200_OK,
    response_model=ResponseBase,
    summary="校验图片验证码",
)
async def verify_image_captcha(captcha_id: str, captcha_code: str) -> ResponseBase:
    if verify_captcha(
        captcha_id=captcha_id,
        captcha_code=captcha_code,
    ):
        return ResponseBase()
    else:
        return ResponseBase(code="1", msg="验证码错误", data=None)


@router.put(
    path="/captcha/{old_captcha_id}",
    status_code=status.HTTP_200_OK,
    response_model=ResponseBase[CaptchaItem],
    summary="刷新图像验证码",
)
async def refresh_captcha(old_captcha_id: str) -> ResponseBase[CaptchaItem]:

    # 删除该验证码
    redis_client.delete(old_captcha_id)
    logger.info(f"{old_captcha_id=}")

    id, _, img_base64 = init_captcha()
    return ResponseBase[CaptchaItem](
        data=CaptchaItem(
            captchaId=id,
            captchaImgBase64=img_base64,
        ),
    )


@router.get(
    path="/captcha/email",
    status_code=status.HTTP_200_OK,
    response_model=ResponseBase,
    summary="获取邮箱验证码",
)
async def get_email_captcha(item: EmailCaptchaBody) -> ResponseBase:
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
    summary="校验邮箱验证码",
)
async def verify_email_captcha(item: EmailCaptchaBody) -> ResponseBase:
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
        return ResponseBase(code="1", msg="验证码过期")

    # 校验验证码
    if verify_captcha(
        captcha_id=item.email,
        captcha_code=item.email_code,
    ):
        return ResponseBase()
    else:
        return ResponseBase(code="2", msg="验证码错误")
