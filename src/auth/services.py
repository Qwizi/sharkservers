import json
import random
import string
from datetime import timedelta, datetime
from sqlite3 import IntegrityError as SQLIntegrityError
from urllib import parse

import httpx
from aioredis import Redis
from asyncpg import UniqueViolationError
from cryptography.fernet import Fernet
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from ormar import NoMatch
from passlib.context import CryptContext
from pydantic import EmailStr
from sqlalchemy.exc import IntegrityError
from starlette.requests import Request
from starlette.responses import RedirectResponse

from src.auth.enums import RedisAuthKeyEnum
from src.auth.exceptions import (
    invalid_credentials_exception,
    incorrect_username_password_exception,
    user_exists_exception,
    user_activated_exception,
)
from src.auth.schemas import (
    TokenDataSchema,
    TokenSchema,
    RefreshTokenSchema,
    RegisterUserSchema,
)
from src.auth.utils import crypto_key
from src.logger import logger
from src.players.models import Player
from src.players.services import PlayerService
from src.roles.enums import ProtectedDefaultRolesEnum
from src.roles.services import roles_service
from src.scopes.utils import get_scopesv3
from src.services import EmailService
from src.users.exceptions import user_not_found_exception
from src.users.models import User
from src.users.services import UserService, users_service


class JWTService:
    def __init__(
        self,
        secret_key: str,
        algorithm: str = "HS256",
        expires_delta: timedelta = timedelta(minutes=15),
    ):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expires_delta = expires_delta

    def encode(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + self.expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def decode(self, token: str) -> dict:
        return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])

    def decode_token(self, token: str) -> TokenDataSchema:
        try:
            payload = self.decode(token)
            user_id: str = payload.get("sub")
            if user_id is None:
                raise invalid_credentials_exception
            token_scopes = payload.get("scopes", [])
            secret = payload.get("secret")

            return TokenDataSchema(
                user_id=int(user_id), scopes=token_scopes, secret=secret
            )
        except JWTError as e:
            raise invalid_credentials_exception


class CodeService:
    redis: Redis
    key: str

    def __init__(self, redis: Redis, key: str):
        self.redis = redis
        self.key = key

    @staticmethod
    def generate(number: int = 8):
        """
        Generate code
        :param number:
        :return:
        """
        return "".join(random.choice(string.digits) for _ in range(number))

    def get_redis_key(self, code: str):
        return f"{self.key}:{code}"

    async def create(self, data: any, code_len: int = 8, expire: int = 60 * 60):
        """
        Create code
        :param code_len:
        :param data:
        :param expire:
        :return:
        """
        code = self.generate(number=code_len)
        redis_key = self.get_redis_key(code)
        if await self.redis.exists(redis_key):
            await self.redis.delete(redis_key)
        await self.redis.set(redis_key, data)
        await self.redis.expire(redis_key, expire)
        return redis_key.split(":")[1], await self.redis.get(redis_key)

    async def get(self, code: str):
        return await self.redis.get(self.get_redis_key(code))

    async def delete(self, code: str):
        return await self.redis.delete(self.get_redis_key(code))


class AuthService:
    def __init__(self, _users_service: UserService):
        self.users_service = _users_service
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.crypto_key = Fernet.generate_key()
        self.fernet = Fernet(crypto_key)
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

    def verify_password(self, plain_password, hashed_password):
        """

        :param plain_password:
        :param hashed_password:
        :return:
        """
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        """
        Hash password
        :param password:
        :return:
        """
        return self.pwd_context.hash(password)

    async def authenticate_user(self, username: str, password: str):
        """
        Authenticate user
        :param username:
        :param password:
        :return:
        """
        try:
            user = await self.users_service.get_one(
                username=username, related=["roles", "roles__scopes"]
            )
            secret_salt = self.generate_secret_salt()
            await user.update(secret_salt=secret_salt)
            if not self.verify_password(password, user.password):
                return False
        except NoMatch:
            return False
        return user

    async def register(
        self,
        user_data: RegisterUserSchema,
        is_activated: bool = False,
        is_superuser: bool = False,
    ) -> User:
        """
        Register new user
        :param is_superuser:
        :param is_activated:
        :param user_data:
        :return:
        """
        password = self.get_password_hash(user_data.password)
        try:
            secret_salt = self.generate_secret_salt()

            user_role = await roles_service.get_one(
                id=ProtectedDefaultRolesEnum.USER.value
            )
            role = user_role
            if is_superuser:
                role = await roles_service.get_one(
                    id=ProtectedDefaultRolesEnum.ADMIN.value
                )
            registered_user = await self.users_service.create(
                username=user_data.username,
                email=user_data.email,
                password=password,
                display_role=role,
                avatar="/static/images/default_avatar.png",
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
        except (IntegrityError, SQLIntegrityError, UniqueViolationError) as e:
            raise user_exists_exception

    async def login(
        self,
        form_data: OAuth2PasswordRequestForm,
        jwt_access_token_service: JWTService,
        jwt_refresh_token_service: JWTService,
    ) -> (TokenSchema, User):
        """
        Login user
        :param form_data:
        :param jwt_access_token_service:
        :param jwt_refresh_token_service:
        :return:
        """
        user = await self.authenticate_user(form_data.username, form_data.password)
        if not user:
            raise incorrect_username_password_exception
        # TODO must be change
        scopes = await get_scopesv3(user.roles)
        access_token = jwt_access_token_service.encode(
            data={"sub": str(user.id), "scopes": scopes, "secret": user.secret_salt}
        )
        refresh_token = jwt_refresh_token_service.encode(
            data={"sub": str(user.id), "secret": user.secret_salt}
        )
        await user.update(last_login=datetime.utcnow())
        return (
            TokenSchema(
                access_token=access_token,
                token_type="bearer",
                refresh_token=refresh_token,
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
        payload = jwt_refresh_token_service.decode(token_data.refresh_token)
        exp = payload.get("exp", None)
        if datetime.utcfromtimestamp(exp) < datetime.utcnow():
            raise invalid_credentials_exception
        user_id = int(payload.get("sub"))
        secret: str = payload.get("secret")
        user = await self.users_service.get_one(
            id=user_id, related=["roles", "roles__scopes"]
        )
        if not user or user.secret_salt != secret:
            raise invalid_credentials_exception
        scopes = await get_scopesv3(user.roles)
        access_token = jwt_access_token_service.encode(
            data={"sub": str(user.id), "scopes": scopes, "secret": user.secret_salt}
        )
        await user.update(last_login=datetime.utcnow())
        return (
            TokenSchema(
                access_token=access_token,
                refresh_token=token_data.refresh_token,
                token_type="bearer",
            ),
            user,
        )

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
            await email_service.send_activation_email(email=email, code=code)
            logger.info(f"Activation code: {code}")
            return msg
        except Exception as e:
            return msg

    async def activate_user(self, code: str, code_service: CodeService):
        user_id = await code_service.get(code)
        if not user_id:
            return False, False
        user = await users_service.get_one(id=int(user_id))
        if user.is_activated:
            await code_service.delete(code)
            raise user_activated_exception
        await user.update(is_activated=True)
        return True, user

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


auth_service = AuthService(_users_service=users_service)
