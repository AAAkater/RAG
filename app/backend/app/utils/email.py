import asyncio
from smtplib import SMTPResponseException

from app.core.config import settings
from app.utils.log import logger
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema
from pydantic import EmailStr

_conf = ConnectionConfig(
    MAIL_USERNAME=settings.SMTP_USERNAME,
    MAIL_PASSWORD=settings.SMTP_PASSWORD,
    MAIL_FROM=settings.SMTP_USERNAME,
    MAIL_SERVER=settings.SMTP_HOST,
    MAIL_FROM_NAME=settings.EMAIL_FROM_NAME,
    MAIL_PORT=settings.SMTP_PORT,
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
)
fm = FastMail(config=_conf)


async def send_email(email: EmailStr, captcha: str):
    template = f"""
        <html>
        <body>
            <p>验证码:{captcha}</p>
            <p>60秒后失效</p>
        </body>
        </html>
    """

    message = MessageSchema(
        subject="RAG",
        recipients=[email],
        body=template,
        subtype="html",
    )

    try:
        await fm.send_message(message)
    except SMTPResponseException as e1:
        # qq的 Malformed SMTP response可能有点大病,实际不影响发送邮箱
        pass
    except ValueError as e2:
        # qq的 Malformed SMTP response可能有点大病,实际不影响发送邮箱
        pass
    except Exception as e:
        logger.error(e)


if __name__ == "__main__":

    test_email = "ym20030308@gmail.com"
    test_captcha = "abcd"
    try:
        asyncio.run(
            send_email(
                email=test_email,
                captcha=test_captcha,
            )
        )
    except Exception as e:
        print(e)
    else:
        print("ok")
