from src.logger import logger
from src.services import EmailService


async def send_activation_account_email(
    email_service: EmailService, email: str, code: str
):
    logger.info(f"Sending activation email to {email} with code {code}")
