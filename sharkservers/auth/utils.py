"""
Utils for auth module.

Functions:
- verify_password: Verifies a password.
- get_password_hash: Hashes a password.
- now_datetime: Returns the current datetime.
"""  # noqa: EXE002

from datetime import datetime

from cryptography.fernet import Fernet
from passlib.context import CryptContext
from zoneinfo import ZoneInfo

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

crypto_key = Fernet.generate_key()

fernet = Fernet(crypto_key)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify if a plain password matches a hashed password.

    Args:
    ----
        plain_password (str): The plain password to verify.
        hashed_password (str): The hashed password to compare against.

    Returns:
    -------
        bool: True if the plain password matches the hashed password, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(plain_password: str) -> str:
    """
    Hashes the given plain password using the pwd_context.

    Args:
    ----
        plain_password (str): The plain password to be hashed.

    Returns:
    -------
        str: The hashed password.
    """
    return pwd_context.hash(plain_password)


def now_datetime() -> datetime:
    """
    Return the current datetime in the timezone "Europe/Warsaw".

    Returns
    -------
        datetime: The current datetime without timezone information.
    """
    return datetime.now(tz=ZoneInfo("Europe/Warsaw")).replace(tzinfo=None)
