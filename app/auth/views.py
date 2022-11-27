from sqlite3 import IntegrityError as SQLIntegrityError
from asyncpg.exceptions import UniqueViolationError
from fastapi import APIRouter
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError
from starlette.exceptions import HTTPException

from app.auth.schemas import RegisterUser
from app.users.models import User
from app.users.schemas import UserOut

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(plain_password):
    return pwd_context.hash(plain_password)


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
