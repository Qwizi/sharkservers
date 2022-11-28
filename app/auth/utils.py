import random
import string
from datetime import timedelta, datetime
from sqlite3 import IntegrityError as SQLIntegrityError

from asyncpg import UniqueViolationError
from cryptography.fernet import Fernet
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError
from starlette.exceptions import HTTPException

from app.auth.exceptions import credentials_exception, invalid_username_password_exception, inactive_user_exception
from app.auth.schemas import TokenData, RegisterUser
from app.settings import Settings, get_settings
from app.users.exceptions import UserNotFound
from app.users.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

crypto_key = Fernet.generate_key()

fernet = Fernet(crypto_key)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(plain_password):
    return pwd_context.hash(plain_password)


async def authenticate_user(username: str, password: str) -> User | bool:
    try:
        user = await User.objects.get(username=username)
        if not verify_password(password, user.password):
            return False
    except UserNotFound as e:
        return False
    return user


def create_access_token(settings: Settings = Depends(get_settings), data: dict = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme), settings: Settings = Depends(get_settings)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        print(payload)
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id)
    except JWTError as e:
        raise credentials_exception
    try:
        user = await User.objects.get(id=int(token_data.user_id))
    except UserNotFound:
        raise invalid_username_password_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_activated:
        raise inactive_user_exception
    return current_user


async def register_user(user_data: RegisterUser):
    password = get_password_hash(user_data.password)
    try:
        created_user = User(
            username=user_data.username,
            email=user_data.email,
            password=password)
        await created_user.save()
    except (IntegrityError, SQLIntegrityError, UniqueViolationError) as e:
        raise HTTPException(status_code=422, detail=f"Email or username already exists")

    return created_user


def generate_code(number: int = 8):
    return ''.join(random.choice(string.digits) for _ in range(number))
