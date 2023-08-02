from fastapi import Depends
from fastapi_limiter.depends import RateLimiter
from fastapi_mail import ConnectionConfig, FastMail
from fastapi_mail.email_utils import DefaultChecker

from src.services import EmailService, UploadService
from src.settings import get_settings, Settings

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
    VALIDATE_CERTS=settings.VALIDATE_CERTS,
)


async def get_email_checker() -> DefaultChecker:
    checker = DefaultChecker()  # you can pass source argument for your own email domains
    await checker.fetch_temp_email_domains()  # require to fetch temporary email domains
    return checker


async def get_email_service(checker: DefaultChecker = Depends(get_email_checker)) -> EmailService:
    mailer = FastMail(conf)
    return EmailService(_mailer=mailer, checker=checker)


async def get_upload_service(settings: Settings = Depends(get_settings)) -> UploadService:
    return UploadService(settings=settings)


def get_limiter(settings_: Settings = Depends(get_settings), limitter: RateLimiter = Depends(RateLimiter(times=2, seconds=60))):
    if settings_.TESTING:
        return None
    return limitter
