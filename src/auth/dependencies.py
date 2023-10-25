from datetime import timedelta
import uuid

from fastapi import Depends
from fastapi.security import SecurityScopes
from jose import JWTError
from ormar import Model
from redis.client import Redis
from src.auth.services.steam import SteamAuthService
from src.players.dependencies import get_players_service
from src.players.services import PlayerService

from src.apps.dependencies import get_app_service
from src.apps.services import AppService
from src.auth.enums import RedisAuthKeyEnum
from src.auth.exceptions import (
    no_permissions_exception,
    invalid_credentials_exception,
    inactivate_user_exception,
    not_admin_user_exception,
)
from src.auth.services.auth import AuthService
from src.auth.services.code import CodeService
from src.auth.services.jwt import JWTService
from src.db import get_redis
from src.roles.dependencies import get_roles_service
from src.roles.services import RoleService
from src.scopes.dependencies import get_scopes_service
from src.scopes.services import ScopeService
from src.settings import Settings, get_settings
from src.users.dependencies import get_users_service, get_users_sessions_service
from src.users.models import User
from src.users.services import UserService, UserSessionService


async def get_access_token_service(
        settings: Settings = Depends(get_settings),
) -> JWTService:
    """
    Get access token service
    :param settings:
    :return JWTService:
    """
    return JWTService(
        secret_key=settings.SECRET_KEY,
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES),
    )


async def get_refresh_token_service(
        settings: Settings = Depends(get_settings),
) -> JWTService:
    """
    Get refresh token service
    :param settings:
    :return JWTService:
    """
    return JWTService(
        secret_key=settings.REFRESH_SECRET_KEY,
        expires_delta=timedelta(minutes=settings.REFRESH_TOKEN_EXPIRES),
    )


async def get_auth_service(
        users_service: UserService = Depends(get_users_service),
        roles_service: RoleService = Depends(get_roles_service),
        scopes_service: ScopeService = Depends(get_scopes_service),
        users_sessions_service: UserSessionService = Depends(get_users_sessions_service)
) -> AuthService:
    return AuthService(
        users_service=users_service,
        roles_service=roles_service,
        scopes_service=scopes_service,
        users_sessions_service=users_sessions_service
    )


async def get_current_user(
        security_scopes: SecurityScopes,
        token: str = Depends(AuthService.oauth2_scheme),
        access_token_service: JWTService = Depends(get_access_token_service),
        users_service: UserService = Depends(get_users_service),
        users_sessions_service: UserSessionService = Depends(get_users_sessions_service)
) -> Model:
    """
    Get current user
    :param users_service:
    :param security_scopes:
    :param token:
    :param access_token_service:
    :return dict:
    """
    token_data = access_token_service.decode_token(token)
    session_id = token_data.session_id
    if not session_id:
        raise invalid_credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise no_permissions_exception
    user = await users_service.get_one(
        id=token_data.user_id,
        related=["roles", "display_role", "roles__scopes", "player", "player__steamrep_profile", "sessions"],
    )
    session_exists = await users_sessions_service.Meta.model.objects.filter(
        id=uuid.UUID(session_id)
    ).exists()
    user_session_exists = False
    if session_exists:
        user_session = await users_sessions_service.Meta.model.objects.get(id=uuid.UUID(session_id))
        for session in user.sessions:
            if session.id == user_session.id:
                user_session_exists = True
                break
    if user.secret_salt != token_data.secret or not session_exists or not user_session_exists:
        raise invalid_credentials_exception
    
    return user


async def get_current_active_user(
        current_user: User = Depends(get_current_user),
) -> User:
    """
    Get current active user
    :param current_user:
    :return User:
    """
    if not current_user.is_activated:
        raise inactivate_user_exception
    return current_user


async def get_admin_user(user: User = Depends(get_current_active_user)):
    if not user.is_superuser:
        raise not_admin_user_exception
    return user


async def get_application(
        security_scopes: SecurityScopes,
        token: str = Depends(AuthService.oauth2_scheme),
        access_token_service: JWTService = Depends(get_access_token_service),
        apps_service: AppService = Depends(get_app_service),
) -> Model:
    """
    Get application
    :param apps_service:
    :param users_service:
    :param security_scopes:
    :param token:
    :param access_token_service:
    :return dict:
    """
    try:
        token_data = access_token_service.decode(token)
        for scope in security_scopes.scopes:
            if scope not in token_data["scopes"]:
                raise no_permissions_exception
        application = await apps_service.get_one(
            id=int(token_data["sub"]),
            related=["scopes"],
        )
        if application.secret_key != token_data["secret"]:
            raise invalid_credentials_exception
        return application
    except JWTError as e:
        raise invalid_credentials_exception


async def get_activation_account_code_service(redis: Redis = Depends(get_redis)) -> CodeService:
    """
    Get activation account code service
    :param redis:
    :return CodeService:
    """
    return CodeService(redis=redis, key=RedisAuthKeyEnum.ACTIVATE_USER.value)


async def get_change_account_email_code_service(redis: Redis = Depends(get_redis)) -> CodeService:
    """
    Get change account email code service
    :param redis:
    :return CodeService:
    """
    return CodeService(redis=redis, key=RedisAuthKeyEnum.CHANGE_EMAIL.value)


async def get_reset_account_password_code_service(redis: Redis = Depends(get_redis)) -> CodeService:
    """
    Get reset account password code service
    :param redis:
    :return CodeService:
    """
    return CodeService(redis=redis, key=RedisAuthKeyEnum.RESET_PASSWORD.value)


async def get_steam_auth_service(
    users_service: UserService = Depends(get_users_service),
    players_service: PlayerService = Depends(get_players_service)
):
    return SteamAuthService(users_service, players_service)