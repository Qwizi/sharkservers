import datetime
from datetime import timedelta
from sqlite3 import IntegrityError as SQLIntegrityError
from asyncpg.exceptions import UniqueViolationError
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError
from starlette.exceptions import HTTPException

from app.auth.exceptions import credentials_exception, inactive_user_exception, invalid_username_password_exception
from app.auth.schemas import RegisterUser, TokenData, Token
from app.settings import Settings, get_settings
from app.users.exceptions import UserNotFound
from app.users.models import User
from app.users.schemas import UserOut

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


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
    expire = datetime.datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES)
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


@router.post("/register", response_model=UserOut)
async def register(user: RegisterUser):
    # Find if user exists
    avatar = "/media/images/avatars/default_avatar.png"
    password = get_password_hash(user.password)
    try:
        created_user = User(
            username=user.username,
            email=user.email,
            password=password
            , avatar=avatar)
        await created_user.save()
    except (IntegrityError, SQLIntegrityError, UniqueViolationError) as e:
        raise HTTPException(status_code=422, detail=f"Email or username already exists")

    return created_user


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 settings: Settings = Depends(get_settings)):
    user = await authenticate_user(username=form_data.username, password=form_data.password)
    if not user:
        raise invalid_username_password_exception
    access_token = create_access_token(settings, data={'sub': str(user.id)})
    return Token(access_token=access_token, token_type="bearer")
