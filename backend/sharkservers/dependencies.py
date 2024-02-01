"""Dependencies for the application."""
import resend
from fastapi import Depends
from fastapi_mail import ConnectionConfig
from fastapi_mail.email_utils import DefaultChecker

from sharkservers.services import EmailService, UploadService
from sharkservers.settings import Settings, get_settings

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
    """
    Retrieve the default email checker.

    Returns
    -------
        DefaultChecker: The default email checker.
    """
    checker = (
        DefaultChecker()
    )  # you can pass source argument for your own email domains
    await checker.fetch_temp_email_domains()  # require to fetch temporary email domains
    return checker


async def get_email_service(
    settings: Settings = Depends(get_settings),
    checker: DefaultChecker = Depends(get_email_checker),
) -> EmailService:
    """
    Retrieve the email service.

    Args:
    ----
        settings (Settings, optional): The application settings. Defaults to Depends(get_settings).
        checker (DefaultChecker, optional): The default email checker. Defaults to Depends(get_email_checker).

    Returns:
    -------
        EmailService: The email service.
    """
    resend.api_key = settings.RESEND_API_KEY
    return EmailService(resend=resend, checker=checker)


async def get_upload_service(
    settings: Settings = Depends(get_settings),
) -> UploadService:
    """
    Retrieve the upload service.

    Args:
    ----
        settings (Settings, optional): The application settings. Defaults to Depends(get_settings).

    Returns:
    -------
        UploadService: The upload service.
    """
    return UploadService(settings=settings)
