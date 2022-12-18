import datetime
import json
from urllib import parse

import httpx
from fastapi import APIRouter, Depends, Security
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_events.dispatcher import dispatch
from jose import jwt, JWTError
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.auth.exceptions import invalid_username_password_exception, credentials_exception
from app.auth.schemas import RegisterUser, Token, RefreshToken, ActivateUserCode
from app.auth.utils import authenticate_user, create_access_token, register_user, create_refresh_token, \
    get_current_user, get_current_active_user, redirect_to_steam, validate_steam_callback, login_user
from app.db import get_redis
from app.roles.models import Role
from app.scopes.utils import get_scopesv3
from app.settings import Settings, get_settings
from app.steamprofile.utils import get_steam_user_info
from app.users.models import User
from app.users.schemas import UserOut, UserEvents
from app.auth.utils import activate_user

router = APIRouter()


@router.post("/register", response_model=UserOut)
async def register(user: RegisterUser, redis=Depends(get_redis)):
    registered_user: User = await register_user(user_data=user)
    registered_user_dict: dict = json.loads(registered_user.json())
    registered_user_dict.update({"redis": redis})
    dispatch(UserEvents.REGISTERED, payload=registered_user_dict)
    return registered_user


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 settings: Settings = Depends(get_settings)):
    token, user = await login_user(form_data, settings)
    dispatch(UserEvents.ACCESS_TOKEN, payload=user)
    return token


@router.post("/token/refresh", response_model=Token)
async def get_access_token_from_refresh_token(token: RefreshToken, settings: Settings = Depends(get_settings)):
    try:
        payload = jwt.decode(token.refresh_token, settings.REFRESH_SECRET_KEY, algorithms=[settings.ALGORITHM])
        if datetime.datetime.utcfromtimestamp(payload["exp"]) > datetime.datetime.utcnow():
            user_id: str = payload.get("sub")
            user = await User.objects.select_related(["roles", "roles__scopes"]).get(id=int(user_id))
            if user:
                await user.update(last_login=datetime.datetime.utcnow())
                scopes = await get_scopesv3(user.roles)
                access_token = create_access_token(settings, data={'sub': str(user.id), "scopes": scopes})
                dispatch(UserEvents.REFRESH_TOKEN, payload=user)
                return Token(access_token=access_token, refresh_token=token.refresh_token, token_type="bearer")
    except JWTError as e:
        raise credentials_exception


@router.post("/activate")
async def activate_user_by_code(activate_code: ActivateUserCode, redis=Depends(get_redis)):
    user_activated = await activate_user(activate_code=activate_code, redis=redis)
    return user_activated


@router.get("/connect/steam")
async def connect_steam_profile():
    return await redirect_to_steam()


@router.get("/callback/steam")
async def steam_profile_callback(request: Request, user: User = Depends(get_current_active_user)):
    return await validate_steam_callback(request, user)
