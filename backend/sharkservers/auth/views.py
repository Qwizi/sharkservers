"""Module contains the API endpoints related to authentication."""
from __future__ import annotations

from fastapi import APIRouter, BackgroundTasks, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_limiter.depends import RateLimiter

from sharkservers.auth.dependencies import (
    get_access_token_service,
    get_activation_account_code_service,
    get_auth_service,
    get_current_active_user,
    get_refresh_token_service,
    get_reset_account_password_code_service,
)
from sharkservers.auth.exceptions import invalid_activation_code_exception
from sharkservers.auth.schemas import (
    ActivateUserCodeSchema,
    RefreshTokenSchema,
    RegisterUserSchema,
    ResendActivationCodeSchema,
    ResetPasswordSchema,
    TokenSchema,
    UserActivatedSchema,
)
from sharkservers.auth.services.auth import AuthService
from sharkservers.auth.services.code import CodeService
from sharkservers.auth.services.jwt import JWTService
from sharkservers.dependencies import get_email_service
from sharkservers.enums import ActivationEmailTypeEnum
from sharkservers.logger import logger
from sharkservers.services import EmailService
from sharkservers.settings import Settings, get_settings
from sharkservers.users.models import User
from sharkservers.users.schemas import UserOut

router = APIRouter()

settings = get_settings()
limiter = RateLimiter(
    times=999 if settings.TESTING else 10,
    minutes=60 if settings.TESTING else 5,
)
refresh_token_limiter = RateLimiter(times=3, minutes=60)


@router.post("/register", dependencies=[Depends(limiter)])
async def register(  # noqa: PLR0913
    user_data: RegisterUserSchema,
    background_tasks: BackgroundTasks,
    request: Request,
    auth_service: AuthService = Depends(get_auth_service),
    code_service: CodeService = Depends(
        get_activation_account_code_service,
    ),
    email_service: EmailService = Depends(get_email_service),
    settings: Settings = Depends(get_settings),
) -> UserOut:
    """
    Register a new user.

    Args:
    ----
        user_data (RegisterUserSchema): The user data to register.
        background_tasks (BackgroundTasks): The background tasks object.
        request (Request): The request object.
        auth_service (AuthService, optional): The authentication service. Defaults to Depends(get_auth_service).
        code_service (CodeService, optional): The code service. Defaults to Depends(get_activation_account_code_service).
        email_service (EmailService, optional): The email service. Defaults to Depends(get_email_service).
        settings (Settings, optional): The settings object. Defaults to Depends(get_settings).

    Returns:
    -------
        UserOut: The registered user.
    """
    registered_user: User = await auth_service.register(
        user_data=user_data,
        request=request,
        settings=settings,
    )
    activation_code, _user_id = await code_service.create(
        data=registered_user.id,
        code_len=5,
        expire=900,
    )
    logger.info(f"Activation code: {activation_code}")
    # Send activation email only if not testing
    if not settings.TESTING:
        background_tasks.add_task(
            email_service.send_confirmation_email,
            ActivationEmailTypeEnum.ACCOUNT,
            registered_user.email,
            activation_code,
        )
    return registered_user


@router.post("/token", dependencies=[Depends(limiter)])
async def login_user(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    access_token_service: JWTService = Depends(get_access_token_service),
    refresh_token_service: JWTService = Depends(
        get_refresh_token_service,
    ),
    auth_service: AuthService = Depends(get_auth_service),
) -> TokenSchema:
    """
    Log in a user and returns a token.

    Args:
    ----
        request (Request): The incoming request object.
        form_data (OAuth2PasswordRequestForm, optional): The form data containing the user's credentials. Defaults to Depends().
        access_token_service (JWTService, optional): The service for generating access tokens. Defaults to Depends(get_access_token_service).
        refresh_token_service (JWTService, optional): The service for generating refresh tokens. Defaults to Depends(get_refresh_token_service).
        auth_service (AuthService, optional): The service for handling authentication. Defaults to Depends(get_auth_service).

    Returns:
    -------
        TokenSchema: The token schema containing the access token.
    """
    user_ip = request.client.host
    user_agent = request.headers.get("User-Agent", None)
    token, user = await auth_service.login(
        form_data,
        jwt_access_token_service=access_token_service,
        jwt_refresh_token_service=refresh_token_service,
        user_ip=user_ip,
        user_agent=user_agent,
    )
    return token


@router.post("/token/refresh")
async def get_access_token_from_refresh_token(
    token_data: RefreshTokenSchema,
    access_token_service: JWTService = Depends(get_access_token_service),
    refresh_token_service: JWTService = Depends(
        get_refresh_token_service,
    ),
    auth_service: AuthService = Depends(get_auth_service),
) -> TokenSchema:
    """
    Retrieve an access token from a refresh token.

    Args:
    ----
        token_data (RefreshTokenSchema): The refresh token data.
        access_token_service (JWTService, optional): The access token service. Defaults to Depends(get_access_token_service).
        refresh_token_service (JWTService, optional): The refresh token service. Defaults to Depends(get_refresh_token_service).
        auth_service (AuthService, optional): The authentication service. Defaults to Depends(get_auth_service).

    Returns:
    -------
        TokenSchema: The access token.
    """
    token, user = await auth_service.create_access_token_from_refresh_token(
        token_data,
        jwt_access_token_service=access_token_service,
        jwt_refresh_token_service=refresh_token_service,
    )
    return token


@router.post("/logout")
async def logout_user(
    user: User = Depends(get_current_active_user),
    auth_service: AuthService = Depends(get_auth_service),
) -> UserOut:
    """
    Log out the user.

    Args:
    ----
        user (User): The user to be logged out.
        auth_service (AuthService): The authentication service.

    Returns:
    -------
        UserOut: The logged out user.
    """
    return await auth_service.logout(user)


@router.post("/activate", dependencies=[Depends(limiter)])
async def activate_user(
    activate_code_data: ActivateUserCodeSchema,
    auth_service: AuthService = Depends(get_auth_service),
    activate_code_service: CodeService = Depends(
        get_activation_account_code_service,
    ),
) -> UserActivatedSchema:
    """
    Activate a user account using the provided activation code.

    Args:
    ----
        activate_code_data (ActivateUserCodeSchema): The activation code data.
        auth_service (AuthService): The authentication service.
        activate_code_service (CodeService): The activation code service.

    Returns:
    -------
        UserActivatedSchema: The activated user data.

    Raises:
    ------
        invalid_activation_code_exception: If the activation code is invalid.
    """
    user_activated, user = await auth_service.activate_user(
        code=activate_code_data.code,
        code_service=activate_code_service,
    )
    if not user_activated:
        raise invalid_activation_code_exception
    return user


@router.post("/activate/resend", dependencies=[Depends(limiter)])
async def resend_activate_code(
    data: ResendActivationCodeSchema,
    background_tasks: BackgroundTasks,
    auth_service: AuthService = Depends(get_auth_service),
    code_service: CodeService = Depends(
        get_activation_account_code_service,
    ),
    email_service: EmailService = Depends(get_email_service),
) -> dict[str, str]:
    """
    Resends the activation code to the specified email address.

    Args:
    ----
        data (ResendActivationCodeSchema): The data containing the email address.
        background_tasks (BackgroundTasks): The background tasks manager.
        auth_service (AuthService): The authentication service.
        code_service (CodeService): The activation code service.
        email_service (EmailService): The email service.

    Returns:
    -------
        dict[str, str]: A dictionary with a message indicating if the email is correct and an email with the activation code will be sent.
    """
    background_tasks.add_task(
        auth_service.resend_activation_code,
        data.email,
        code_service=code_service,
        email_service=email_service,
    )
    return {
        "msg": "If email is correct, you will receive an email with activation code",
    }


@router.post("/forgot-password", dependencies=[Depends(limiter)])
async def forgot_password_request(
    data: ResendActivationCodeSchema,
    background_tasks: BackgroundTasks,
    email_service: EmailService = Depends(get_email_service),
    code_service: CodeService = Depends(
        get_reset_account_password_code_service,
    ),
) -> dict[str, str]:
    """
    Send a request to reset the account password.

    Args:
    ----
        data (ResendActivationCodeSchema): The data containing the email address.
        background_tasks (BackgroundTasks): The background tasks manager.
        auth_service (AuthService): The authentication service.
        email_service (EmailService): The email service.
        code_service (CodeService): The code service for resetting the account password.

    Returns:
    -------
        dict[str, str]: A dictionary with a message indicating that an email with the reset code will be sent if the email is correct.
    """
    code, _data = await code_service.create(data.email, code_len=5, expire=900)
    background_tasks.add_task(
        email_service.send_confirmation_email,
        ActivationEmailTypeEnum.PASSWORD,
        data.email,
        code,
    )
    return {"msg": "If email is correct, you will receive an email with reset code"}


@router.post("/reset-password", dependencies=[Depends(limiter)])
async def reset_password(
    data: ResetPasswordSchema,
    auth_service: AuthService = Depends(get_auth_service),
    code_service: CodeService = Depends(
        get_reset_account_password_code_service,
    ),
) -> dict:
    """
    Reset the password for a user account.

    Args:
    ----
        data (ResetPasswordSchema): The data containing the password reset information.
        auth_service (AuthService): The authentication service.
        code_service (CodeService): The code service for resetting the account password.

    Returns:
    -------
        dict: A dictionary with a message indicating that the password has been reset.
    """
    await auth_service.reset_password(
        reset_password_data=data,
        code_service=code_service,
    )
    return {"msg": "Password has been reset"}
