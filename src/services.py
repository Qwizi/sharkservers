from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
from pydantic import EmailStr

from src.settings import get_settings


class EmailService:
    mailer: FastMail

    def __init__(self, _mailer: FastMail):
        self.mailer = _mailer

    @staticmethod
    def activation_email_template(code: str):
        return f"""
        Witaj twój kod aktywacyjny to: {code}
        """

    async def send_activation_email(self, email: EmailStr, code: str):
        await self.mailer.send_message(message=MessageSchema(
            subject="Aktywacja konta",
            recipients=[email],
            body=self.activation_email_template(code),
            subtype=MessageType.html
        ))


settings = get_settings()

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
    USE_CREDENTIALS=settings.USE_CREDENTIALS,
    VALIDATE_CERTS=settings.VALIDATE_CERTS
)

mailer = FastMail(conf)
email_service = EmailService(_mailer=mailer)
