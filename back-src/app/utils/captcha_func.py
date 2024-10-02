import base64
import random
import string
from io import BytesIO

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


if __name__ == "__main__":
    code = generate_captcha_code()
    img = generate_captcha_img(code)
    base64 = img_to_base64(img)
    print(base64)
