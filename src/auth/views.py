import json
from datetime import timedelta

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_events.dispatcher import dispatch
from starlette.requests import Request

from src.auth.dependencies import get_access_token_service, get_refresh_token_service, get_current_active_user
from src.auth.enums import AuthEventsEnum
from src.auth.schemas import RegisterUserSchema, TokenSchema, RefreshTokenSchema, ActivateUserCodeSchema
from src.auth.services import JWTService, auth_service
from src.auth.utils import _activate_user, get_user_agent, _logout_user
from src.auth.utils import register_user, redirect_to_steam, validate_steam_callback, \
    _login_user, \
    _get_access_token_from_refresh_token
from src.db import get_redis
from src.settings import Settings, get_settings
from src.users.models import User
from src.users.schemas import UserOut

router = APIRouter()

"""@router.post("/register", response_model=UserOut)
async def register(user_data: RegisterUserSchema, redis=Depends(get_redis)) -> UserOut:
    
    dispatch(AuthEventsEnum.REGISTERED_PRE, payload={"user_data": user_data})
    registered_user: User = await register_user(user_data=user_data)
    registered_user_dict: dict = json.loads(registered_user.json())
    registered_user_dict.update({"redis": redis})
    dispatch(AuthEventsEnum.REGISTERED_POST, payload=registered_user_dict)
    return registered_user"""


@router.post("/register", response_model=UserOut)
async def register(user_data: RegisterUserSchema, redis=Depends(get_redis)) -> UserOut:
    """
    Register a new user
    :param user_data:
    :param redis:
    :return UserOut:
    """
    dispatch(AuthEventsEnum.REGISTERED_PRE, payload={"user_data": user_data})
    registered_user: User = await auth_service.register(user_data=user_data)
    registered_user_dict: dict = json.loads(registered_user.json())
    registered_user_dict.update({"redis": redis})
    dispatch(AuthEventsEnum.REGISTERED_POST, payload=registered_user_dict)
    return registered_user


@router.post("/token", response_model=TokenSchema)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends(),
                     access_token_service: JWTService = Depends(get_access_token_service),
                     refresh_token_service: JWTService = Depends(get_refresh_token_service)) -> TokenSchema:
    """
    Login user
    :param refresh_token_service:
    :param access_token_service:
    :param form_data:
    :return TokenSchema:
    """
    dispatch(AuthEventsEnum.ACCESS_TOKEN_PRE, payload={"form_data": form_data.__dict__})
    token, user = await auth_service.login(form_data, jwt_access_token_service=access_token_service,
                                           jwt_refresh_token_service=refresh_token_service)
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


@router.post("/logout")
async def logout_user(user: User = Depends(get_current_active_user)):
    """
    Logout user
    :param user:
    :return:
    """
    return await _logout_user(user)


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
