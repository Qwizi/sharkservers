from datetime import timedelta

from fastapi import Depends
from fastapi.security import SecurityScopes
from ormar import NoMatch

from src.auth.exceptions import no_permissions_exception, invalid_credentials_exception, inactivate_user_exception, \
    not_admin_user_exception
from src.auth.services import JWTService, auth_service
from src.settings import Settings, get_settings
from src.users.models import User
from src.users.services import users_service


async def get_access_token_service(settings: Settings = Depends(get_settings)) -> JWTService:
    """
    Get access token service
    :param settings:
    :return JWTService:
    """
    return JWTService(secret_key=settings.SECRET_KEY, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES))


async def get_refresh_token_service(settings: Settings = Depends(get_settings)) -> JWTService:
    """
    Get refresh token service
    :param settings:
    :return JWTService:
    """
    return JWTService(secret_key=settings.REFRESH_SECRET_KEY,
                      expires_delta=timedelta(minutes=settings.REFRESH_TOKEN_EXPIRES))


async def get_current_user(security_scopes: SecurityScopes, token: str = Depends(auth_service.oauth2_scheme),
                           access_token_service: JWTService = Depends(get_access_token_service)) -> User:
    """
    Get current user
    :param security_scopes:
    :param token:
    :param access_token_service:
    :return dict:
    """
    token_data = access_token_service.decode_token(token)
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise no_permissions_exception
    user = await users_service.get_one(id=token_data.user_id,
                                       related=["roles", "display_role", "roles__scopes", "players"])
    if user.secret_salt != token_data.secret:
        raise invalid_credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
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
