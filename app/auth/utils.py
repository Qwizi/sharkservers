import asyncio
import random
import string
from datetime import timedelta, datetime
from enum import Enum
from sqlite3 import IntegrityError as SQLIntegrityError
from typing import Optional, Dict
from urllib import parse

import httpx
from asyncpg import UniqueViolationError
from cryptography.fernet import Fernet
from fastapi import Depends, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2, SecurityScopes
from fastapi.security.utils import get_authorization_scheme_param
from fastapi_events.dispatcher import dispatch
from jose import jwt, JWTError
from ormar import NoMatch
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError
from starlette import status
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.auth.exceptions import credentials_exception, invalid_username_password_exception, inactive_user_exception, \
    InvalidActivateCode, UserIsAlreadyActivated, admin_user_exception
from app.auth.schemas import TokenData, RegisterUser, ActivateUserCode
from app.roles.models import Role
from app.settings import Settings, get_settings
from app.steamprofile.models import SteamProfile
from app.steamprofile.schemas import SteamPlayer
from app.steamprofile.utils import get_steam_user_info
from app.users.exceptions import UserNotFound
from app.users.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

crypto_key = Fernet.generate_key()

fernet = Fernet(crypto_key)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


class RedisKey(Enum):
    ACTIVATE_USER = "activate-user-code"


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(plain_password):
    return pwd_context.hash(plain_password)


async def authenticate_user(username: str, password: str) -> User | bool:
    try:
        user = await User.objects.select_related(["roles", "roles__scopes"]).get(username=username)
        if not verify_password(password, user.password):
            return False
    except NoMatch as e:
        return False
    return user


def create_access_token(settings: Settings = Depends(get_settings), data: dict = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def create_refresh_token(settings: Settings = Depends(get_settings), data: dict = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=
                                           settings.REFRESH_TOKEN_EXPIRES)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, settings.REFRESH_SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def get_current_user(security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme),
                           settings: Settings = Depends(get_settings)):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(user_id=user_id, scopes=token_scopes)
    except JWTError as e:
        raise credentials_exception
    try:
        user = await User.objects.select_related(["roles", "display_role", "roles__scopes", "steamprofile"]).get(
            id=int(token_data.user_id))
    except UserNotFound:
        raise invalid_username_password_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user


async def get_current_active_user(current_user: User = Security(get_current_user, scopes=["users:me"])):
    if not current_user.is_activated:
        raise inactive_user_exception
    return current_user


async def get_admin_user(user: User = Depends(get_current_active_user)):
    if not user.is_superuser:
        raise admin_user_exception
    return user


async def register_user(user_data: RegisterUser) -> User:
    password = get_password_hash(user_data.password)
    try:
        user_role = await Role.objects.get(id=2)
        created_user = await User.objects.create(
            username=user_data.username,
            email=user_data.email,
            password=password,
            display_role=user_role,
            avatar="/static/images/default_avatar.png"
        )

        await created_user.roles.add(user_role)
    except (IntegrityError, SQLIntegrityError, UniqueViolationError) as e:
        raise HTTPException(status_code=422, detail=f"Email or username already exists")
    return created_user


async def create_admin_user(user_data: RegisterUser):
    registered_user = await register_user(user_data)
    admin_role = await Role.objects.get(id=1)
    await registered_user.roles.add(admin_role)
    await registered_user.update(
        is_activated=True,
        is_superuser=True,
        display_role=admin_role
    )
    print(registered_user)
    return registered_user


def generate_code(number: int = 8):
    return ''.join(random.choice(string.digits) for _ in range(number))


def create_activate_code_redis_key(code: str):
    return f"{RedisKey.ACTIVATE_USER.value}:{code}"


async def create_activate_code(user_id: int, redis):
    code = generate_code(5)
    redis_key = create_activate_code_redis_key(code)
    if await redis.exists(redis_key):
        await redis.delete(redis_key)
    await redis.set(redis_key, user_id)
    await redis.expire(redis_key, 900)
    return redis_key.split(":")[1], await redis.get(redis_key),


async def get_user_id_by_code(code: str, redis):
    redis_key = create_activate_code_redis_key(code)
    code = await redis.get(redis_key)
    if code:
        return int(code)
    return None


async def delete_activate_code(code, redis):
    return await redis.delete(create_activate_code_redis_key(code))


async def activate_user(activate_code: ActivateUserCode, redis):
    code = activate_code.code
    user_id = await get_user_id_by_code(code, redis)
    if not user_id:
        raise InvalidActivateCode
    try:
        user = await User.objects.get(id=user_id)
        if user.is_activated:
            await delete_activate_code(code, redis)
            raise UserIsAlreadyActivated()
        await user.update(is_activated=True)
        await delete_activate_code(code, redis)
        return True
    except NoMatch:
        raise InvalidActivateCode


async def redirect_to_steam():
    steam_openid_url = "https://steamcommunity.com/openid/login"
    u = {
        'openid.ns': "http://specs.openid.net/auth/2.0",
        'openid.identity': "http://specs.openid.net/auth/2.0/identifier_select",
        'openid.claimed_id': "http://specs.openid.net/auth/2.0/identifier_select",
        'openid.mode': 'checkid_setup',
        'openid.return_to': 'http://localhost:80/callback/steam/',
        'openid.realm': 'http://localhost:80'
    }
    query_string = parse.urlencode(u)
    auth_url = steam_openid_url + "?" + query_string
    return RedirectResponse(auth_url)


async def validate_steam_callback(request: Request, user: User):
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
    steam_player_info: SteamPlayer = get_steam_user_info(steamid64)

    player, _created = await SteamProfile.objects.get_or_create(
        steamid64=steam_player_info.steamid64,
        _defaults={
            "user": user,
            "username": steam_player_info.username,
            "steamid32": steam_player_info.steamid32,
            "steamid3": steam_player_info.steamid3,
            "avatar": steam_player_info.avatar,
            "profile_url": steam_player_info.profile_url,
            "country_code": steam_player_info.country_code
        }
    )

    print(player)

    # this fucntion should always return false if the payload is not valid
    return steam_player_info
