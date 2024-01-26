"""
Auth service.

Module responsible for authentication and authorization.

Classes:
- OAuth2ClientSecretRequestForm: Represents a form for requesting OAuth2 client secret.
- AuthService: Represents the service responsible for authentication and authorization operations.
"""
from __future__ import annotations

import random
import string
from datetime import datetime
from sqlite3 import IntegrityError
from sqlite3 import IntegrityError as SQLIntegrityError

from asyncpg import UniqueViolationError
from fastapi import Form, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError
from ormar import NoMatch
from pydantic import EmailStr

from sharkservers.auth.exceptions import (
    incorrect_username_password_exception,
    invalid_activation_code_exception,
    invalid_credentials_exception,
    token_expired_exception,
    user_activated_exception,
    user_exists_exception,
)
from sharkservers.auth.schemas import (
    RefreshTokenSchema,
    RegisterUserSchema,
    ResetPasswordSchema,
    TokenDetailsSchema,
    TokenSchema,
)
from sharkservers.auth.services.code import CodeService
from sharkservers.auth.services.jwt import JWTService
from sharkservers.auth.utils import get_password_hash, now_datetime, verify_password
from sharkservers.enums import ActivationEmailTypeEnum
from sharkservers.logger import logger
from sharkservers.roles.enums import ProtectedDefaultRolesTagEnum
from sharkservers.roles.services import RoleService
from sharkservers.scopes.services import ScopeService
from sharkservers.services import EmailService
from sharkservers.settings import Settings
from sharkservers.users.models import User
from sharkservers.users.services import UserService


class OAuth2ClientSecretRequestForm:
    """
    Represents a form for requesting OAuth2 client secret.

    Args:
    ----
        client_id (str, optional): The client ID. Defaults to None.
        client_secret (str, optional): The client secret. Defaults to None.
    """

    def __init__(
        self,
        client_id: str | None = Form(default=None),
        client_secret: str | None = Form(default=None),
    ) -> None:
        """Initializes an instance of the Auth class."""  # noqa: D401
        self.client_id = client_id
        self.client_secret = client_secret


class AuthService:
    """
    Service class for authentication-related operations.

    Attributes
    ----------
        users_service (UserService): The service for managing user-related operations.
        roles_service (RoleService): The service for managing role-related operations.
        scopes_service (ScopeService): The service for managing scope-related operations.
        users_sessions_service (UserSessionService): The service for managing user session-related operations.

    Methods
    -------
        authenticate_user: Authenticates a user based on the provided username and password.
        register: Register a new user.
        login: Authenticate a user and generates access and refresh tokens.
        create_access_token_from_refresh_token: Create an access token from a refresh token.
        logout: Log out the specified user by generating a new secret salt and updating it in the user's record.
        generate_code: Generate a random code consisting of digits.
        generate_secret_salt: Generate a secret salt consisting of random alphanumeric characters.
        resend_activation_code: Resend the activation code to the specified email address.
        activate_user: Activate a user based on the provided activation code.
        confirm_change_email: Confirm the change of email for a user.
        reset_password: Reset the password for a user.
        get_user_agent: Get the User-Agent header from the request.
    """

    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/token")

    def __init__(
        self,
        users_service: UserService,
        roles_service: RoleService,
        scopes_service: ScopeService,
    ) -> None:
        """
        Initialize the Auth service.

        Args:
        ----
            users_service (UserService): The service for managing users.
            roles_service (RoleService): The service for managing roles.
            scopes_service (ScopeService): The service for managing scopes.
            users_sessions_service (UserSessionService): The service for managing user sessions.
        """
        self.users_service = users_service
        self.roles_service = roles_service
        self.scopes_service = scopes_service

    async def authenticate_user(
        self,
        username: str,
        password: str,
        user_ip: str | None,  # noqa: ARG002
        user_agent: str | None,  # noqa: ARG002
    ) -> User | bool:
        """
        Authenticates a user based on the provided username and password.

        Args:
        ----
            username (str): The username of the user.
            password (str): The password of the user.
            user_ip (str): The IP address of the user.
            user_agent (str): The user agent string of the user's browser.

        Returns:
        -------
            Union[User, bool]: The authenticated user object if successful, False otherwise.
        """  # noqa: D401
        try:
            user: User = await self.users_service.get_one(
                username=username,
                related=["roles", "roles__scopes", "sessions"],
            )
            if not verify_password(password, user.password) or not user.is_activated:
                return False
        except NoMatch:
            return False
        return user

    async def register(  # noqa: PLR0913
        self,
        user_data: RegisterUserSchema,
        is_activated: bool = False,  # noqa: FBT001, FBT002
        is_superuser: bool = False,  # noqa: FBT001, FBT002
        request: Request = None,  # noqa: ARG002
        settings: Settings = None,
    ) -> User:
        """
        Register a new user.

        Args:
        ----
            user_data (RegisterUserSchema): The user data for registration.
            is_activated (bool, optional): Whether the user is activated. Defaults to False.
            is_superuser (bool, optional): Whether the user is a superuser. Defaults to False.
            request (Request, optional): The request object. Defaults to None.
            settings (Settings, optional): The settings object. Defaults to None.

        Returns:
        -------
            User: The registered user.

        Raises:
        ------
            user_exists_exception: If the user already exists.
        """
        try:
            password = get_password_hash(user_data.password)
            secret_salt = self.generate_secret_salt()

            user_role = await self.roles_service.get_one(
                tag=ProtectedDefaultRolesTagEnum.USER.value,
            )
            role = user_role
            if is_superuser:
                role = await self.roles_service.get_one(
                    tag=ProtectedDefaultRolesTagEnum.ADMIN.value,
                )

            avatar_url = (
                f"{settings.SITE_URL}/static/images/default_avatar.png"
                if settings
                else "http://localhost/static/images/default_avatar.png"
            )
            registered_user = await self.users_service.create(
                username=user_data.username,
                email=user_data.email,
                password=password,
                display_role=role,
                avatar=str(avatar_url),
                secret_salt=secret_salt,
                is_activated=is_activated,
                is_superuser=is_superuser,
            )
            if not is_superuser:
                await registered_user.roles.add(role)
            else:
                await registered_user.roles.add(user_role)
                await registered_user.roles.add(role)
            return registered_user  # noqa: TRY300
        except (
            IntegrityError,
            SQLIntegrityError,
            UniqueViolationError,
            HTTPException,
        ) as err:
            raise user_exists_exception from err

    async def login(  # noqa: PLR0913
        self,
        form_data: OAuth2PasswordRequestForm,
        jwt_access_token_service: JWTService,
        jwt_refresh_token_service: JWTService,
        user_ip: str | None = None,
        user_agent: str | None = None,
    ) -> tuple[TokenSchema, User]:
        """
        Authenticate a user and generates access and refresh tokens.

        Args:
        ----
            form_data (OAuth2PasswordRequestForm): The form data containing the username and password.
            jwt_access_token_service (JWTService): The service used to encode the access token.
            jwt_refresh_token_service (JWTService): The service used to encode the refresh token.
            user_ip (str): The IP address of the user.
            user_agent (str): The user agent string.

        Returns:
        -------
            tuple[TokenSchema, User]: A tuple containing the access and refresh tokens, and the authenticated user.
        """
        user = await self.authenticate_user(
            form_data.username,
            form_data.password,
            user_ip=user_ip,
            user_agent=user_agent,
        )
        if not user:
            raise incorrect_username_password_exception

        scopes = await self.scopes_service.get_scopes_list(user.roles)
        access_token, access_token_exp = jwt_access_token_service.encode(
            data={
                "sub": str(user.id),
                "scopes": scopes,
                "secret": user.secret_salt,
            },
        )
        refresh_token, refresh_toke_exp = jwt_refresh_token_service.encode(
            data={"sub": str(user.id), "secret": user.secret_salt},
        )
        await user.update(last_online=now_datetime())
        return (
            TokenSchema(
                access_token=TokenDetailsSchema(
                    token=access_token,
                    exp=access_token_exp,
                    token_type="bearer",  # noqa: S106
                ),
                refresh_token=TokenDetailsSchema(
                    token=refresh_token,
                    exp=refresh_toke_exp,
                    token_type="bearer",  # noqa: S106
                ),
            ),
            user,
        )

    async def create_access_token_from_refresh_token(
        self,
        token_data: RefreshTokenSchema,
        jwt_access_token_service: JWTService,
        jwt_refresh_token_service: JWTService,
    ) -> tuple[TokenSchema, User]:
        """
        Create an access token from a refresh token.

        Args:
        ----
            token_data (RefreshTokenSchema): The refresh token data.
            jwt_access_token_service (JWTService): The JWT service for access tokens.
            jwt_refresh_token_service (JWTService): The JWT service for refresh tokens.

        Returns:
        -------
            tuple[TokenSchema, User]: A tuple containing the access token schema and the user object.
        """
        try:
            payload = jwt_refresh_token_service.decode(token_data.refresh_token)
            refresh_token_exp = payload.get("exp", None)
            # TODO(Qwizi): replace with timezone  # noqa: TD003
            if (
                datetime.fromtimestamp(refresh_token_exp)
                < now_datetime()  # noqa: DTZ006
            ):
                raise token_expired_exception
            user_id = int(payload.get("sub"))
            secret: str = payload.get("secret")
            user = await self.users_service.get_one(
                id=user_id,
                related=["roles", "roles__scopes"],
            )
            if not user or user.secret_salt != secret:
                raise invalid_credentials_exception
            scopes = await self.scopes_service.get_scopes_list(user.roles)
            access_token, access_token_exp = jwt_access_token_service.encode(
                data={
                    "sub": str(user.id),
                    "scopes": scopes,
                    "secret": user.secret_salt,
                },
            )
            # TODO(Qwizi): replace with timezone  # noqa: TD003
            await user.update(last_login=datetime.utcnow())  # noqa: DTZ003
            return (
                TokenSchema(
                    access_token=TokenDetailsSchema(
                        token=access_token,
                        exp=access_token_exp,
                        token_type="bearer",  # noqa: S106
                    ),
                    refresh_token=TokenDetailsSchema(
                        token=token_data.refresh_token,
                        exp=refresh_token_exp,
                        token_type="bearer",  # noqa: S106
                    ),
                ),
                user,
            )
        except JWTError as err:
            raise invalid_credentials_exception from err

    async def logout(self, user: User) -> User:
        """
        Log out the specified user by generating a new secret salt and updating it in the user's record.

        Args:
        ----
            user (User): The user to log out.

        Returns:
        -------
            User: The updated user object.
        """
        secret = self.generate_secret_salt()
        await user.update(secret_salt=secret)
        return user

    @staticmethod
    def generate_code(number: int = 8) -> str:
        """
        Generate a random code consisting of digits.

        Args:
        ----
            number (int): The length of the generated code. Default is 8.

        Returns:
        -------
            str: The generated code.
        """
        # TODO(Qwizi): replace with secrets (secrets.token_hex(number)[:number])  # noqa: TD003
        return "".join(
            random.choice(string.digits) for _ in range(number)
        )  # noqa: S311

    @staticmethod
    def generate_secret_salt() -> str:
        """
        Generate a secret salt consisting of random alphanumeric characters.

        Returns
        -------
            str: The generated secret salt.
        """
        # TODO(Qwizi): replace with secrets (secrets.token_hex(number)[:number])  # noqa: TD003
        return "".join(
            random.choice(string.ascii_letters + string.digits)  # noqa: S311
            for _ in range(32)
        )

    async def resend_activation_code(
        self,
        email: EmailStr,
        code_service: CodeService,
        email_service: EmailService,
    ) -> dict[str, str]:
        """
        Resend the activation code to the specified email address.

        Args:
        ----
            email (EmailStr): The email address to send the activation code to.
            code_service (CodeService): The code service used to create the activation code.
            email_service (EmailService): The email service used to send the activation email.

        Returns:
        -------
            dict: A dictionary with a message indicating that the activation code will be sent if the email is correct.
        """
        msg = {
            "msg": "If email is correct, you will receive an email with activation code",
        }
        try:
            user = await self.users_service.get_one(email=email, is_activated=False)
            code, code_data = await code_service.create(
                data=int(user.id),
                code_len=5,
                expire=900,
            )
            await email_service.send_confirmation_email(
                ActivationEmailTypeEnum.ACCOUNT,
                user.email,
                code,
            )

            logger.info(f"Activation code: {code}")
            return msg  # noqa: TRY300
        except Exception:  # noqa: BLE001
            return msg

    async def activate_user(
        self,
        code: str,
        code_service: CodeService,
    ) -> tuple[bool, User]:
        """
        Activate a user based on the provided activation code.

        Args:
        ----
            code (str): The activation code.
            code_service (CodeService): The code service used to retrieve the user ID.

        Returns:
        -------
            Tuple[bool, Union[bool, User]]: A tuple containing a boolean indicating the success of the activation,
            and either a boolean indicating if the user was already activated or the activated user object.
        """
        user_id = await code_service.get(code)
        if not user_id:
            return False, False
        user = await self.users_service.get_one(id=int(user_id))
        if user.is_activated:
            await code_service.delete(code)
            raise user_activated_exception
        await user.update(is_activated=True)
        return True, user

    async def confirm_change_email(self, code_service: CodeService, code: str) -> User:
        """
        Confirm the change of email for a user.

        Args:
        ----
            code_service (CodeService): The code service used to retrieve the user data.
            code (str): The activation code.

        Returns:
        -------
            User: The updated user object.

        Raises:
        ------
            InvalidActivationCodeException: If the activation code is invalid.
        """
        user_data: dict = await code_service.get(code)
        if not user_data:
            raise invalid_activation_code_exception
        user_id = int(user_data.get("user_id"))
        email = user_data.get("email")
        user = await self.users_service.get_one(id=user_id)
        await user.update(email=email)
        return user

    async def reset_password(
        self,
        reset_password_data: ResetPasswordSchema,
        code_service: CodeService,
    ) -> bool:
        """
        Reset the password for a user.

        Args:
        ----
            reset_password_data (ResetPasswordSchema): The data required to reset the password.
            code_service (CodeService): The service used to validate the activation code.

        Returns:
        -------
            bool: True if the password was successfully reset, False otherwise.
        """
        email = await code_service.get(reset_password_data.code)
        if not email:
            raise invalid_activation_code_exception
        user = await self.users_service.get_one(email=email)
        new_password = get_password_hash(reset_password_data.password)
        await user.update(
            password=new_password,
            secret_salt=self.generate_secret_salt(),
        )
        await code_service.delete(reset_password_data.code)
        return True

    async def get_user_agent(self, request: Request) -> str:
        """
        Get the User-Agent header from the request.

        Args:
        ----
            request (Request): The incoming request.

        Returns:
        -------
            str: The User-Agent header value, or None if not found.
        """
        return request.headers.get("User-Agent", None)
