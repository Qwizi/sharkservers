"""
Dependencies for auth.

Functions:
---------
    get_access_token_service: Get access token service
    get_refresh_token_service: Get refresh token service
    get_auth_service: Get auth service
    get_current_user: Get current user
    get_current_active_user: Get current active user
    get_admin_user: Get admin user
    get_application: Get application
    get_activation_account_code_service: Get activation account code service
    get_change_account_email_code_service: Get change account email code service
    get_reset_account_password_code_service: Get reset account password code service
    get_steam_auth_service: Get steam auth service
"""

from datetime import timedelta

from fastapi import Depends
from fastapi.security import SecurityScopes
from redis.client import Redis

from sharkservers.auth.enums import RedisAuthKeyEnum
from sharkservers.auth.exceptions import (
    inactivate_user_exception,
    invalid_credentials_exception,
    no_permissions_exception,
    not_admin_user_exception,
)
from sharkservers.auth.schemas import TokenDataSchema
from sharkservers.auth.services.auth import AuthService
from sharkservers.auth.services.code import CodeService
from sharkservers.auth.services.jwt import JWTService
from sharkservers.auth.services.steam import SteamAuthService
from sharkservers.db import get_redis
from sharkservers.logger import logger
from sharkservers.players.dependencies import get_players_service
from sharkservers.players.services import PlayerService
from sharkservers.roles.dependencies import get_roles_service
from sharkservers.roles.services import RoleService
from sharkservers.scopes.dependencies import get_scopes_service
from sharkservers.scopes.services import ScopeService
from sharkservers.settings import Settings, get_settings
from sharkservers.users.dependencies import (
    get_users_service,
)
from sharkservers.users.models import User
from sharkservers.users.services import UserService


async def get_access_token_service(
    settings: Settings = Depends(get_settings),
) -> JWTService:
    """
    Get the access token service.

    Args:
    ----
        settings (Settings): The application settings.

    Returns:
    -------
        JWTService: The access token service.

    """
    return JWTService(
        secret_key=settings.SECRET_KEY,
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES),
    )


async def get_refresh_token_service(
    settings: Settings = Depends(get_settings),
) -> JWTService:
    """
    # Retrieve the JWTService instance for handling refresh tokens.

    Args:
    ----
        settings (Settings): The application settings.

    Returns:
    -------
        JWTService: The JWTService instance for handling refresh tokens.
    """
    return JWTService(
        secret_key=settings.REFRESH_SECRET_KEY,
        expires_delta=timedelta(minutes=settings.REFRESH_TOKEN_EXPIRES),
    )


async def get_auth_service(
    users_service: UserService = Depends(get_users_service),
    roles_service: RoleService = Depends(get_roles_service),
    scopes_service: ScopeService = Depends(get_scopes_service),
) -> AuthService:
    """
    Get the authentication service with the required dependencies.

    Args:
    ----
        users_service (UserService): The user service dependency.
        roles_service (RoleService): The role service dependency.
        scopes_service (ScopeService): The scope service dependency.
        users_sessions_service (UserSessionService): The user session service dependency.

    Returns:
    -------
        AuthService: The authentication service instance.
    """
    return AuthService(
        users_service=users_service,
        roles_service=roles_service,
        scopes_service=scopes_service,
    )


async def get_current_user(
    security_scopes: SecurityScopes,
    token: str = Depends(AuthService.oauth2_scheme),
    access_token_service: JWTService = Depends(get_access_token_service),
    users_service: UserService = Depends(get_users_service),
) -> User:
    """
    Retrieve the current user based on the provided security scopes and token.

    Args:
    ----
        security_scopes (SecurityScopes): The security scopes required for the user.
        token (str): The access token used for authentication.
        access_token_service (JWTService): The service used for decoding the access token.
        users_service (UserService): The service used for retrieving user information.
        users_sessions_service (UserSessionService): The service used for retrieving user session information.

    Returns:
    -------
        User: The current user.

    Raises:
    ------
        InvalidCredentialsException: If the credentials are invalid.
        NoPermissionsException: If the user does not have the required permissions.
    """
    token_data: TokenDataSchema = access_token_service.decode_token(token)
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise no_permissions_exception
    logger.info(f"Token data: {token_data.user_id}")
    user: User = await users_service.get_one(
        id=token_data.user_id.uuid,
        related=[
            "roles",
            "display_role",
            "roles__scopes",
            "player",
            "player__steamrep_profile",
            "sessions",
        ],
    )
    if user.secret_salt != token_data.secret:
        raise invalid_credentials_exception

    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Retrieve the current active user.

    This function checks if the current user is activated. If not, it raises an exception.

    Args:
    ----
        current_user (User): The current user.

    Returns:
    -------
        User: The current active user.

    Raises:
    ------
        inactivate_user_exception: If the current user is not activated.
    """
    if not current_user.is_activated:
        raise inactivate_user_exception
    return current_user


async def get_admin_user(user: User = Depends(get_current_active_user)) -> User:
    """
    Retrieve the admin user.

    Args:
    ----
        user (User): The current user.

    Returns:
    -------
        User: The admin user.

    Raises:
    ------
        NotAdminUserException: If the user is not a superuser.
    """
    if not user.is_superuser:
        raise not_admin_user_exception
    return user


async def get_activation_account_code_service(
    redis: Redis = Depends(get_redis),
) -> CodeService:
    """
    Get the activation account code service.

    This function returns an instance of the CodeService class that is used for generating
    and validating activation codes for user accounts.

    Args:
    ----
        redis: The Redis connection object.

    Returns:
    -------
        The CodeService instance.

    """
    return CodeService(redis=redis, key=RedisAuthKeyEnum.ACTIVATE_USER.value)


async def get_change_account_email_code_service(
    redis: Redis = Depends(get_redis),
) -> CodeService:
    """
    Retrieves the CodeService instance for changing the account email.

    Args:
    ----
        redis (Redis): The Redis instance.

        CodeService: The CodeService instance for changing the account email.
    """  # noqa: D401
    return CodeService(redis=redis, key=RedisAuthKeyEnum.CHANGE_EMAIL.value)


async def get_reset_account_password_code_service(
    redis: Redis = Depends(get_redis),
) -> CodeService:
    """
    Retrieve the CodeService instance for resetting account password.

    Args:
    ----
        redis (Redis): The Redis instance used for storing the reset password code.

    Returns:
    -------
        CodeService: The CodeService instance for resetting account password.
    """
    return CodeService(redis=redis, key=RedisAuthKeyEnum.RESET_PASSWORD.value)


async def get_steam_auth_service(
    users_service: UserService = Depends(get_users_service),
    players_service: PlayerService = Depends(get_players_service),
) -> SteamAuthService:
    """
    Get the SteamAuthService instance with the provided dependencies.

    Args:
    ----
        users_service (UserService): The UserService instance.
        players_service (PlayerService): The PlayerSer>
    -------
        SteamAuthService: The SteamAuthService instance.
    """
    return SteamAuthService(users_service, players_service)
