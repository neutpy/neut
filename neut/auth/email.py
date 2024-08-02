from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from neut.core.settings import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
)

async def send_email(subject: str, recipients: list, body: str):
    message = MessageSchema(
        subject=subject,
        recipients=recipients,
        body=body,
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message)

async def send_password_reset_email(email: str, token: str):
    reset_url = f"{settings.FRONTEND_URL}/reset-password?token={token}"
    await send_email(
        "Password Reset",
        [email],
        f"Click here to reset your password: {reset_url}"
    )

async def send_verification_email(email: str, token: str):
    verify_url = f"{settings.FRONTEND_URL}/verify-email?token={token}"
    await send_email(
        "Verify Your Email",
        [email],
        f"Click here to verify your email: {verify_url}"
    )