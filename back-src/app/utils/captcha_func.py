import base64
import random
import string
import uuid
from io import BytesIO

from app.utils.log import logger
from app.utils.redis_api import redis_client
from captcha.image import ImageCaptcha
from PIL.Image import Image


def generate_captcha_code(length: int = 4) -> str:
    chr_all = string.ascii_letters + string.digits
    return "".join(random.choices(population=chr_all, k=length))


def generate_captcha_img(code: str):
    image: Image = ImageCaptcha().generate_image(chars=code)
    return image


def img_to_base64(img: Image, fmt: str = "PNG"):
    out_buffer = BytesIO()
    img.save(out_buffer, format=fmt)
    byte_data: bytes = out_buffer.getvalue()
    base64_str: str = base64.b64encode(byte_data).decode(encoding="utf-8")
    return base64_str


def init_captcha():
    captcha_id = uuid.uuid4().hex
    captcha_code = generate_captcha_code()
    logger.info(f"{captcha_code=}")
    # * 写入redis 有效期两分钟
    redis_client.setex(name=captcha_id, time=120, value=captcha_code)

    captcha_img = generate_captcha_img(code=captcha_code)
    captcha_img_base64: str = img_to_base64(captcha_img)
    return (captcha_id, captcha_code, captcha_img_base64)


def verify_captcha(*, captcha_id: str, captcha_code: str) -> bool:
    code = redis_client.get(name=captcha_id)
    redis_client.delete(captcha_id)
    return True if code == captcha_code else False


if __name__ == "__main__":
    code = generate_captcha_code()
    img = generate_captcha_img(code)
    base64 = img_to_base64(img)
    print(base64)
