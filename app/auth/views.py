import json

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_events.dispatcher import dispatch
from starlette.requests import Request

from app.auth.enums import AuthEventsEnum
from app.auth.schemas import RegisterUserSchema, TokenSchema, RefreshTokenSchema, ActivateUserCodeSchema
from app.auth.utils import _activate_user
from app.auth.utils import register_user, get_current_active_user, redirect_to_steam, validate_steam_callback, \
    _login_user, \
    _get_access_token_from_refresh_token
from app.db import get_redis
from app.settings import Settings, get_settings
from app.users.models import User
from app.users.schemas import UserOut

router = APIRouter()


@router.post("/register", response_model=UserOut)
async def register(user_data: RegisterUserSchema, redis=Depends(get_redis)) -> UserOut:
    """
    Register a new user
    :param user_data:
    :param redis:
    :return UserOut:
    """
    dispatch(AuthEventsEnum.REGISTERED_PRE, payload={"user_data": user_data})
    registered_user: User = await register_user(user_data=user_data)
    registered_user_dict: dict = json.loads(registered_user.json())
    registered_user_dict.update({"redis": redis})
    dispatch(AuthEventsEnum.REGISTERED_POST, payload=registered_user_dict)
    return registered_user


@router.post("/token", response_model=TokenSchema)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends(),
                     settings: Settings = Depends(get_settings)) -> TokenSchema:
    """
    Login user
    :param form_data:
    :param settings:
    :return TokenSchema:
    """
    dispatch(AuthEventsEnum.ACCESS_TOKEN_PRE, payload={"form_data": form_data.__dict__})
    token, user = await _login_user(form_data, settings)
    payload = {
        "user": json.loads(user.json()),
        "token": json.loads(token.json())
    }
    dispatch(AuthEventsEnum.ACCESS_TOKEN_POST, payload=payload)
    return token


@router.post("/token/refresh", response_model=TokenSchema)
async def get_access_token_from_refresh_token(token_data: RefreshTokenSchema,
                                              settings: Settings = Depends(get_settings)) -> TokenSchema:
    """
    Get access token from refresh token
    :param token_data:
    :param settings:
    :return TokenSchema:
    """
    token, user = await _get_access_token_from_refresh_token(token_data, settings)
    payload = {
        "user": json.loads(user.json()),
        "token": json.loads(token.json())
    }
    dispatch(AuthEventsEnum.REFRESH_TOKEN_POST, payload=payload)
    return token


@router.post("/activate")
async def activate_user(activate_code_data: ActivateUserCodeSchema, redis=Depends(get_redis)) -> bool:
    """
    Activate user
    :param activate_code_data:
    :param redis:
    :return bool:
    """
    dispatch(AuthEventsEnum.ACTIVATED_PRE, payload={"activate_code": activate_code_data})
    user_activated, user = await _activate_user(activate_code=activate_code_data, redis=redis)
    dispatch(AuthEventsEnum.ACTIVATED_POST, payload={"activated": user_activated, "user": user})
    return user_activated


@router.get("/connect/steam")
async def connect_steam_profile():
    return await redirect_to_steam()


@router.get("/callback/steam")
async def steam_profile_callback(request: Request, user: User = Depends(get_current_active_user)):
    return await validate_steam_callback(request, user)
