import datetime

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError

from app.auth.exceptions import invalid_username_password_exception, credentials_exception
from app.auth.schemas import RegisterUser, Token, RefreshToken
from app.auth.utils import authenticate_user, create_access_token, register_user, create_refresh_token
from app.roles.models import Role
from app.scopes.utils import get_scopesv2, get_scopesv3
from app.settings import Settings, get_settings
from app.users.models import User
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

    scopes = await get_scopesv3(user.roles)
    access_token = create_access_token(settings, data={'sub': str(user.id), "scopes": scopes})
    refresh_token = create_refresh_token(settings, data={'sub': str(user.id)})
    return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")


@router.post("/token/refresh", response_model=Token)
async def get_access_token_from_refresh_token(token: RefreshToken, settings: Settings = Depends(get_settings)):
    try:
        payload = jwt.decode(token.refresh_token, settings.REFRESH_SECRET_KEY, algorithms=[settings.ALGORITHM])
        if datetime.datetime.utcfromtimestamp(payload["exp"]) > datetime.datetime.utcnow():
            user_id: str = payload.get("sub")
            user = await User.objects.select_related(["roles", "roles__scopes"]).get(id=int(user_id))
            if user:
                scopes = await get_scopesv3(user.roles)
                access_token = create_access_token(settings, data={'sub': str(user.id), "scopes": scopes})
                return Token(access_token=access_token, refresh_token=token.refresh_token, token_type="bearer")
    except JWTError as e:
        raise credentials_exception
