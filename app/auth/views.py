from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.auth.exceptions import invalid_username_password_exception
from app.auth.schemas import RegisterUser, Token
from app.auth.utils import authenticate_user, create_access_token, register_user
from app.settings import Settings, get_settings
from app.users.schemas import UserOut

router = APIRouter()


@router.post("/register", response_model=UserOut)
async def register(user: RegisterUser):
    return await register_user(user_data=user)


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 settings: Settings = Depends(get_settings)):
    user = await authenticate_user(username=form_data.username, password=form_data.password)
    if not user:
        raise invalid_username_password_exception
    access_token = create_access_token(settings, data={'sub': str(user.id)})
    return Token(access_token=access_token, token_type="bearer")
