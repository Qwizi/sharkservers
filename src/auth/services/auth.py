import random
import string
from datetime import datetime
from sqlite3 import IntegrityError
from sqlite3 import IntegrityError as SQLIntegrityError
from typing import Optional
from urllib import parse

import httpx
from asyncpg import UniqueViolationError
from fastapi import HTTPException, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError
from ormar import NoMatch
from pydantic import EmailStr
from starlette.requests import Request
from starlette.responses import RedirectResponse
from src.settings import Settings

from src.apps.services import AppService
from src.auth.exceptions import (
    inactivate_user_exception,
    user_exists_exception,
    incorrect_username_password_exception,
    token_expired_exception,
    invalid_credentials_exception,
    user_activated_exception,
    invalid_activation_code_exception,
)
from src.auth.schemas import (
    RegisterUserSchema,
    TokenSchema,
    TokenDetailsSchema,
    RefreshTokenSchema,
    ResetPasswordSchema,
)
from src.auth.services.code import CodeService
from src.auth.services.jwt import JWTService
from src.auth.utils import now_datetime, verify_password, get_password_hash
from src.enums import ActivationEmailTypeEnum
from src.logger import logger
from src.players.services import PlayerService
from src.roles.enums import ProtectedDefaultRolesEnum, ProtectedDefaultRolesTagEnum
from src.roles.services import RoleService
from src.scopes.services import ScopeService
from src.services import EmailService
from src.users.exceptions import (
    username_not_available_exception,
    invalid_current_password_exception,
    cannot_change_display_role_exception,
)
from src.users.models import User
from src.users.schemas import (
    ChangeUsernameSchema,
    ChangePasswordSchema,
    ChangeDisplayRoleSchema,
)
from src.users.services import UserService, UserSessionService


class OAuth2ClientSecretRequestForm:
    def __init__(
        self,
        client_id: Optional[str] = Form(default=None),
        client_secret: Optional[str] = Form(default=None),
    ):
        self.client_id = client_id
        self.client_secret = client_secret


class AuthService:
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/token")

    def __init__(
        self,
        users_service: UserService,
        roles_service: RoleService,
        scopes_service: ScopeService,
        users_sessions_service: UserSessionService,
    ):
        self.users_service = users_service
        self.roles_service = roles_service
        self.scopes_service = scopes_service
        self.users_sessions_service = users_sessions_service

    async def authenticate_user(
        self, username: str, password: str, user_ip: str, user_agent: str
    ):
        """
        Authenticate user
        :param username:
        :param password:
        :return:
        """
        try:
            user = await self.users_service.get_one(
                username=username, related=["roles", "roles__scopes", "sessions"]
            )
            # secret_salt = self.generate_secret_salt()
            # await user.update(secret_salt=secret_salt)
            if not user.is_activated:
                raise inactivate_user_exception
            if not verify_password(password, user.password) or not user.is_activated:
                return False
        except NoMatch:
            return False
        return user

    async def register(
        self,
        user_data: RegisterUserSchema,
        is_activated: bool = False,
        is_superuser: bool = False,
        request: Request = None,
        settings: Settings = None,
    ) -> User:
        """
        Register new user
        :param server_url:
        :param is_superuser:
        :param is_activated:
        :param user_data:
        :return:
        """

        try:
            password = get_password_hash(user_data.password)
            secret_salt = self.generate_secret_salt()

            user_role = await self.roles_service.get_one(
                tag=ProtectedDefaultRolesTagEnum.USER.value
            )
            role = user_role
            if is_superuser:
                role = await self.roles_service.get_one(
                    tag=ProtectedDefaultRolesTagEnum.ADMIN.value
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
            return registered_user
        except (
            IntegrityError,
            SQLIntegrityError,
            UniqueViolationError,
            HTTPException,
        ) as e:
            raise user_exists_exception

    async def login(
        self,
        form_data: OAuth2PasswordRequestForm,
        jwt_access_token_service: JWTService,
        jwt_refresh_token_service: JWTService,
        user_ip: str,
        user_agent: str,
    ) -> (TokenSchema, User):
        """
        Login user
        :param form_data:
        :param jwt_access_token_service:
        :param jwt_refresh_token_service:
        :return:
        """
        user = await self.authenticate_user(
            form_data.username,
            form_data.password,
            user_ip=user_ip,
            user_agent=user_agent,
        )
        if not user:
            raise incorrect_username_password_exception
        user_session_exists = (
            await self.users_sessions_service.Meta.model.objects.filter(
                user_ip=user_ip, user_agent=user_agent
            ).exists()
        )
        if user_session_exists:
            user_session = await self.users_sessions_service.Meta.model.objects.get(
                user_ip=user_ip, user_agent=user_agent
            )
            exists_in_relation = False
            for session in user.sessions:
                if session.id == user_session.id:
                    exists_in_relation = True
            if not exists_in_relation:
                await user.sessions.add(user_session)
        else:
            user_session = await self.users_sessions_service.create(
                user_ip=user_ip, user_agent=user_agent
            )
            logger.info(user_session)
            await user.sessions.add(user_session)
            logger.info(user.sessions)

        scopes = await self.scopes_service.get_scopes_list(user.roles)
        access_token, access_token_exp = jwt_access_token_service.encode(
            data={
                "sub": str(user.id),
                "scopes": scopes,
                "secret": user.secret_salt,
                "session_id": str(user_session.id),
            }
        )
        refresh_token, refresh_toke_exp = jwt_refresh_token_service.encode(
            data={"sub": str(user.id), "secret": user.secret_salt}
        )
        await user.update(last_online=now_datetime())
        return (
            TokenSchema(
                access_token=TokenDetailsSchema(
                    token=access_token, exp=access_token_exp, token_type="bearer"
                ),
                refresh_token=TokenDetailsSchema(
                    token=refresh_token, exp=refresh_toke_exp, token_type="bearer"
                ),
            ),
            user,
        )

    async def create_access_token_from_refresh_token(
        self,
        token_data: RefreshTokenSchema,
        jwt_access_token_service: JWTService,
        jwt_refresh_token_service: JWTService,
    ):
        """

        :param token_data:
        :param jwt_access_token_service:
        :param jwt_refresh_token_service:
        :return:
        """
        try:
            payload = jwt_refresh_token_service.decode(token_data.refresh_token)
            refresh_token_exp = payload.get("exp", None)
            if datetime.fromtimestamp(refresh_token_exp) < now_datetime():
                raise token_expired_exception
            user_id = int(payload.get("sub"))
            secret: str = payload.get("secret")
            user = await self.users_service.get_one(
                id=user_id, related=["roles", "roles__scopes"]
            )
            if not user or user.secret_salt != secret:
                raise invalid_credentials_exception
            scopes = await self.scopes_service.get_scopes_list(user.roles)
            access_token, access_token_exp = jwt_access_token_service.encode(
                data={"sub": str(user.id), "scopes": scopes, "secret": user.secret_salt}
            )
            await user.update(last_login=datetime.utcnow())
            return (
                TokenSchema(
                    access_token=TokenDetailsSchema(
                        token=access_token, exp=access_token_exp, token_type="bearer"
                    ),
                    refresh_token=TokenDetailsSchema(
                        token=token_data.refresh_token,
                        exp=refresh_token_exp,
                        token_type="bearer",
                    ),
                ),
                user,
            )
        except JWTError as e:
            raise invalid_credentials_exception

    async def logout(self, user: User):
        """
        Logout user
        :param user:
        :return:
        """
        secret = self.generate_secret_salt()
        await user.update(secret_salt=secret)
        return user

    @staticmethod
    def generate_code(number: int = 8):
        """
        Generate code
        :param number:
        :return:
        """
        return "".join(random.choice(string.digits) for _ in range(number))

    @staticmethod
    def generate_secret_salt():
        """
        Generate secret salt
        :return:
        """
        return "".join(
            random.choice(string.ascii_letters + string.digits) for _ in range(32)
        )

    async def resend_activation_code(
        self, email: EmailStr, code_service: CodeService, email_service: EmailService
    ):
        """
        Activate user
        :param email_service:
        :param code_service:
        :param email:
        :return:
        """
        msg = {
            "msg": "If email is correct, you will receive an email with activation code"
        }
        try:
            user = await self.users_service.get_one(email=email, is_activated=False)
            code, code_data = await code_service.create(
                data=int(user.id), code_len=5, expire=900
            )
            await email_service.send_confirmation_email(
                ActivationEmailTypeEnum.ACCOUNT, user.email, code
            )

            logger.info(f"Activation code: {code}")
            return msg
        except Exception as e:
            return msg

    async def activate_user(self, code: str, code_service: CodeService):
        user_id = await code_service.get(code)
        if not user_id:
            return False, False
        user = await self.users_service.get_one(id=int(user_id))
        if user.is_activated:
            await code_service.delete(code)
            raise user_activated_exception
        await user.update(is_activated=True)
        return True, user

    async def confirm_change_email(self, code_service: CodeService, code: str):
        user_data: dict = await code_service.get(code)
        if not user_data:
            raise invalid_activation_code_exception
        user_id = int(user_data.get("user_id"))
        email = user_data.get("email")
        user = await self.users_service.get_one(id=user_id)
        await user.update(email=email)
        return user

    @staticmethod
    def redirect_to_steam():
        steam_openid_url = "https://steamcommunity.com/openid/login"
        u = {
            "openid.ns": "http://specs.openid.net/auth/2.0",
            "openid.identity": "http://specs.openid.net/auth/2.0/identifier_select",
            "openid.claimed_id": "http://specs.openid.net/auth/2.0/identifier_select",
            "openid.mode": "checkid_setup",
            "openid.return_to": "http://localhost:80/auth/callback/steam/",
            "openid.realm": "http://localhost:80",
        }
        query_string = parse.urlencode(u)
        auth_url = steam_openid_url + "?" + query_string
        return RedirectResponse(auth_url)

    async def authenticate_steam_user(
        self, request: Request, user: User, player_service: PlayerService
    ):
        steam_login_url_base = "https://steamcommunity.com/openid/login"

        signed_params = request.query_params
        params_dict = {}
        for key, value in signed_params.items():
            params_dict[key] = value

        params_dict["openid.mode"] = "check_authentication"
        async with httpx.AsyncClient() as client:
            r = await client.post(url=steam_login_url_base, data=params_dict)
        if "is_valid:true" not in r.text:
            raise HTTPException(detail="Cannot validate steam profile", status_code=400)
        steamid64 = params_dict["openid.claimed_id"].split("/")[-1]
        player = await player_service.create_player(steamid64=steamid64)
        return player

    @staticmethod
    async def change_username(
        user: User, change_username_data: ChangeUsernameSchema
    ) -> User:
        """
        Change user username
        :param change_username_data:
        :param user:
        :return:
        """
        try:
            await user.update(
                username=change_username_data.username, updated_date=now_datetime()
            )
            return user
        except (UniqueViolationError, IntegrityError, SQLIntegrityError):
            raise username_not_available_exception

    async def change_password(
        self, user: User, change_password_data: ChangePasswordSchema
    ) -> User:
        """
        Change user password
        :param user:
        :param change_password_data:
        :return:
        """
        if not self.verify_password(
            change_password_data.current_password, user.password
        ):
            raise invalid_current_password_exception
        new_password = self.get_password_hash(change_password_data.new_password)
        await user.update(password=new_password, updated_date=now_datetime())
        return user

    @staticmethod
    async def change_display_role(
        user: User, change_display_role_data: ChangeDisplayRoleSchema
    ) -> (User, int):
        display_role_exists_in_user_roles = False
        old_user_display_role = user.display_role.id
        for role in user.roles:
            if role.id == change_display_role_data.role_id:
                display_role_exists_in_user_roles = True
                break
        if not display_role_exists_in_user_roles:
            raise cannot_change_display_role_exception
        await user.update(
            display_role=change_display_role_data.role_id,
            updated_date=now_datetime(),
        )
        return user, old_user_display_role

    @staticmethod
    async def validate_app(
        client_id: str, client_secret: str, apps_service: AppService
    ):
        """
        Validate app
        :param apps_service:
        :param client_id:
        :param client_secret:
        :return:
        """
        app = await apps_service.get_one(
            client_id=client_id, client_secret=client_secret, related=["scopes"]
        )
        if not app:
            return False
        return app

    async def get_app_token(
        self,
        form_data: OAuth2ClientSecretRequestForm,
        apps_service: AppService,
        jwt_access_token_service: JWTService,
        jwt_refresh_token_service: JWTService,
    ) -> TokenSchema:
        """
        Get app token
        :param form_data:
        :return:
        """
        app = await AuthService.validate_app(
            client_id=form_data.client_id,
            client_secret=form_data.client_secret,
            apps_service=apps_service,
        )

        if not app:
            raise invalid_credentials_exception
        scopes_list = []

        for scope in app.scopes:
            scopes_list.append(scope.get_string())

        access_token = jwt_access_token_service.encode(
            data={
                "sub": str(app.id),
                "name": app.name,
                "scopes": scopes_list,
                "secret": app.secret_key,
            }
        )
        refresh_token = jwt_refresh_token_service.encode(
            data={
                "sub": str(app.id),
                "name": app.name,
                "scopes": scopes_list,
                "secret": app.secret_key,
            }
        )
        return TokenSchema(
            access_token=access_token,
            token_type="bearer",
            refresh_token=refresh_token,
        )

    async def confirm_change_email(
        self, user: User, code: str, code_service: CodeService
    ) -> User:
        """
        Confirm change email
        :param code:
        :param code_service:
        :param user:
        :return:
        """
        data = await code_service.get(code)
        if not data:
            raise invalid_activation_code_exception
        return user

    async def reset_password(
        self, reset_password_data: ResetPasswordSchema, code_service: CodeService
    ):
        """
        Confirm change password
        :param reset_password_data:
        :param code_service:
        :return:
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

    async def get_user_agent(request: Request):
        return request.headers.get("User-Agent", None)
