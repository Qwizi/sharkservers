from datetime import datetime
from zoneinfo import ZoneInfo

from cryptography.fernet import Fernet
from fastapi.security import (
    OAuth2PasswordBearer,
)
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

crypto_key = Fernet.generate_key()

fernet = Fernet(crypto_key)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(plain_password):
    return pwd_context.hash(plain_password)


def now_datetime() -> datetime:
    return datetime.now(tz=ZoneInfo("Europe/Warsaw")).replace(tzinfo=None)
