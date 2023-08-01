import json

from fastapi import APIRouter, Depends, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_events.dispatcher import dispatch
from fastapi_mail.email_utils import DefaultChecker
from pydantic import EmailStr
from starlette.requests import Request

from src.apps.dependencies import get_app_service
from src.apps.services import AppService
from src.auth.dependencies import (get_access_token_service, get_refresh_token_service, get_current_active_user,
                                   get_auth_service, get_activation_account_code_service, )
from src.auth.enums import AuthEventsEnum, RedisAuthKeyEnum
from src.auth.exceptions import invalid_activation_code_exception
from src.auth.schemas import (RegisterUserSchema, TokenSchema, RefreshTokenSchema, ActivateUserCodeSchema,
                              ResendActivationCodeSchema, UserActivatedSchema, )
from src.auth.services.auth import AuthService, OAuth2ClientSecretRequestForm
from src.auth.services.code import CodeService
from src.auth.services.jwt import JWTService
from src.db import get_redis
from src.dependencies import get_email_service, get_email_checker
from src.enums import ActivationEmailTypeEnum
from src.logger import logger
from src.players.dependencies import get_players_service
from src.players.services import PlayerService
from src.services import EmailService
from src.settings import Settings, get_settings
from src.users.models import User
from src.users.schemas import UserOut

router = APIRouter()


@router.post("/register")
async def register(user_data: RegisterUserSchema, background_tasks: BackgroundTasks,
                   auth_service: AuthService = Depends(get_auth_service),
                   code_service: CodeService = Depends(get_activation_account_code_service),
                   email_service: EmailService = Depends(get_email_service),
                   settings: Settings = Depends(get_settings),
                   ) -> UserOut:
    """
    Register a new user
    :param settings:
    :param email_checker:
    :param email_service:
    :param code_service:
    :param background_tasks:
    :param auth_service:
    :param user_data:
    :return UserOut:
    """
    # dispatch(AuthEventsEnum.REGISTERED_PRE, payload={"user_data": user_data})
    registered_user: User = await auth_service.register(user_data=user_data)
    activation_code, _user_id = await code_service.create(data=registered_user.id, code_len=5, expire=900)
    # registered_user_dict: dict = json.loads(registered_user.json())
    # registered_user_dict.update({"redis": redis})
    # dispatch(AuthEventsEnum.REGISTERED_POST, payload=registered_user_dict)
    logger.info(f"Activation code: {activation_code}")
    # Send activation email only if not testing
    if not settings.TESTING:
        background_tasks.add_task(email_service.send_confirmation_email, ActivationEmailTypeEnum.ACCOUNT, registered_user.email, activation_code)
    return registered_user


@router.post("/token")
async def login_user(form_data: OAuth2PasswordRequestForm = Depends(),
                     access_token_service: JWTService = Depends(get_access_token_service),
                     refresh_token_service: JWTService = Depends(get_refresh_token_service),
                     auth_service: AuthService = Depends(get_auth_service), ) -> TokenSchema:
    """
    Login user
    :param auth_service:
    :param refresh_token_service:
    :param access_token_service:
    :param form_data:
    :return TokenSchema:
    """
    dispatch(AuthEventsEnum.ACCESS_TOKEN_PRE, payload={"form_data": form_data.__dict__})
    token, user = await auth_service.login(form_data, jwt_access_token_service=access_token_service,
                                           jwt_refresh_token_service=refresh_token_service, )
    payload = {"user": json.loads(user.json()), "token": json.loads(token.json())}
    dispatch(AuthEventsEnum.ACCESS_TOKEN_POST, payload=payload)
    return token


@router.post("/token/refresh")
async def get_access_token_from_refresh_token(token_data: RefreshTokenSchema,
                                              access_token_service: JWTService = Depends(get_access_token_service),
                                              refresh_token_service: JWTService = Depends(get_refresh_token_service),
                                              auth_service: AuthService = Depends(get_auth_service), ) -> TokenSchema:
    """
    Get access token from refresh token
    :param auth_service:
    :param refresh_token_service:
    :param access_token_service:
    :param token_data:
    :return TokenSchema:
    """
    token, user = await auth_service.create_access_token_from_refresh_token(token_data,
                                                                            jwt_access_token_service=access_token_service,
                                                                            jwt_refresh_token_service=refresh_token_service, )
    payload = {"user": json.loads(user.json()), "token": json.loads(token.json())}
    dispatch(AuthEventsEnum.REFRESH_TOKEN_POST, payload=payload)
    return token


@router.post("/logout")
async def logout_user(user: User = Depends(get_current_active_user),
                      auth_service: AuthService = Depends(get_auth_service), ) -> UserOut:
    """
    Logout user
    :param auth_service:
    :param user:
    :return:
    """
    return await auth_service.logout(user)


@router.post("/activate")
async def activate_user(
        activate_code_data: ActivateUserCodeSchema,
        auth_service: AuthService = Depends(get_auth_service),
        activate_code_service: CodeService = Depends(get_activation_account_code_service),
) -> UserActivatedSchema:
    """
    Activate user
    :param activate_code_service:
    :param auth_service:
    :param activate_code_data:
    :return bool:
    """
    dispatch(AuthEventsEnum.ACTIVATED_PRE, payload={"activate_code": activate_code_data})
    user_activated, user = await auth_service.activate_user(code=activate_code_data.code, code_service=activate_code_service)
    if not user_activated:
        raise invalid_activation_code_exception
    dispatch(AuthEventsEnum.ACTIVATED_POST, payload={"activated": user_activated, "user": user}, )
    return user


@router.post("/activate/resend")
async def resend_activate_code(
        data: ResendActivationCodeSchema,
        background_tasks: BackgroundTasks,
        auth_service: AuthService = Depends(get_auth_service),
        code_service: CodeService = Depends(get_activation_account_code_service),
        email_service: EmailService = Depends(get_email_service)
) -> dict[str, str]:
    """
    Resend activate code
    :param code_service:
    :param background_tasks:
    :param email_service:
    :param auth_service:
    :param data:
    :return bool:
    """
    background_tasks.add_task(auth_service.resend_activation_code, data.email, code_service=code_service, email_service=email_service)
    return {"msg": "If email is correct, you will receive an email with activation code"}


@router.get("/connect/steam")
async def connect_steam_profile(auth_service: AuthService = Depends(get_auth_service), ):
    return auth_service.redirect_to_steam()


@router.get("/callback/steam")
async def steam_profile_callback(request: Request, user: User = Depends(get_current_active_user),
                                 auth_service: AuthService = Depends(get_auth_service),
                                 players_service: PlayerService = Depends(get_players_service), ):
    return await auth_service.authenticate_steam_user(request, user, player_service=players_service)


@router.post("/apps/token")
async def get_app_token(form_data: OAuth2ClientSecretRequestForm = Depends(),
                        access_token_service: JWTService = Depends(get_access_token_service),
                        jwt_refresh_token_service: JWTService = Depends(get_refresh_token_service),
                        auth_service: AuthService = Depends(get_auth_service),
                        apps_service: AppService = Depends(get_app_service), ) -> TokenSchema:
    """
    Get app token
    :param auth_service:
    :param access_token_service:
    :param form_data:
    :return TokenSchema:
    """
    return await auth_service.get_app_token(form_data, jwt_access_token_service=access_token_service,
                                            jwt_refresh_token_service=jwt_refresh_token_service,
                                            apps_service=apps_service, )


async def default_checker():
    checker = DefaultChecker()  # you can pass source argument for your own email domains
    await checker.fetch_temp_email_domains()  # require to fetch temporary email domains
    return checker


@router.post("/email")
async def test_email_send(background_tasks: BackgroundTasks, email_service: EmailService = Depends(get_email_service),
                          code_service: CodeService = Depends(get_activation_account_code_service),
                          email_checker: DefaultChecker = Depends(get_email_checker)):
    """
    Test email send
    :param code_service:
    :param email_service:
    :return:
    """
    # code, _user_id = await code_service.create(data="test", expire=60, code_len=5)
    await email_service.send_confirmation_email(EmailStr("ciolek.adrian@protonmail.com"), "12345")
    return {}
