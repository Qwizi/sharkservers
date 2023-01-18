import random
import string
from datetime import timedelta, datetime
from enum import Enum
from sqlite3 import IntegrityError as SQLIntegrityError
from urllib import parse

import httpx
from asyncpg import UniqueViolationError
from cryptography.fernet import Fernet
from fastapi import Depends, Security
from fastapi.security import OAuth2PasswordBearer, SecurityScopes, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from ormar import NoMatch
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import RedirectResponse

from src.auth.enums import RedisAuthKeyEnum
from src.auth.exceptions import invalid_credentials_exception, incorrect_username_password_exception, \
    no_permissions_exception, inactivate_user_exception, not_admin_user_exception, user_exists_exception, \
    invalid_activation_code_exception, user_activated_exception
from src.auth.schemas import TokenDataSchema, RegisterUserSchema, ActivateUserCodeSchema, TokenSchema, \
    RefreshTokenSchema
from src.roles.models import Role
from src.scopes.utils import get_scopesv3
from src.settings import Settings, get_settings
from src.steamprofile.models import SteamProfile
from src.steamprofile.schemas import SteamPlayer
from src.steamprofile.utils import get_steam_user_info
from src.users.exceptions import UserNotFound
from src.users.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

crypto_key = Fernet.generate_key()

fernet = Fernet(crypto_key)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(plain_password):
    return pwd_context.hash(plain_password)


async def authenticate_user(username: str, password: str) -> User | bool:
    try:
        user = await User.objects.select_related(["roles", "roles__scopes"]).get(username=username)
        secret_salt = generate_secret_salt()
        await user.update(secret_salt=secret_salt)
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
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise invalid_credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenDataSchema(user_id=int(user_id), scopes=token_scopes, secret=payload.get("secret"))
        try:
            user = await User.objects.select_related(["roles", "display_role", "roles__scopes", "steamprofile"]).get(
                id=int(token_data.user_id))
        except UserNotFound:
            raise incorrect_username_password_exception
        if user.secret_salt != token_data.secret:
            raise invalid_credentials_exception
    except JWTError as e:
        raise invalid_credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise no_permissions_exception
    return user


async def get_current_active_user(current_user: User = Security(get_current_user, scopes=["users:me"])):
    if not current_user.is_activated:
        raise inactivate_user_exception
    return current_user


async def get_admin_user(user: User = Depends(get_current_active_user)):
    if not user.is_superuser:
        raise not_admin_user_exception
    return user


async def register_user(user_data: RegisterUserSchema) -> User:
    password = get_password_hash(user_data.password)
    try:
        user_role = await Role.objects.get(id=2)
        secret_salt = generate_secret_salt()
        created_user = await User.objects.create(
            username=user_data.username,
            email=user_data.email,
            password=password,
            display_role=user_role,
            avatar="/static/images/default_avatar.png",
            secret_salt=secret_salt
        )

        await created_user.roles.add(user_role)
    except (IntegrityError, SQLIntegrityError, UniqueViolationError) as e:
        raise user_exists_exception
    return created_user


async def _login_user(form_data: OAuth2PasswordRequestForm, settings: Settings):
    user = await authenticate_user(username=form_data.username, password=form_data.password)
    if not user:
        raise incorrect_username_password_exception

    scopes = await get_scopesv3(user.roles)
    access_token = create_access_token(settings, data={
        'sub': str(user.id),
        "scopes": scopes,
        "secret": user.secret_salt
    })
    refresh_token = create_refresh_token(settings, data={'sub': str(user.id), "secret": user.secret_salt})
    await user.update(last_login=datetime.utcnow())
    return TokenSchema(access_token=access_token, refresh_token=refresh_token, token_type="bearer"), user


async def _get_access_token_from_refresh_token(token_data: RefreshTokenSchema, settings: Settings):
    try:
        payload = jwt.decode(token_data.refresh_token, settings.REFRESH_SECRET_KEY, algorithms=[settings.ALGORITHM])
        if datetime.utcfromtimestamp(payload["exp"]) > datetime.utcnow():
            user_id: str = payload.get("sub")
            secret: str = payload.get("secret")
            user = await User.objects.select_related(["roles", "roles__scopes"]).get(id=int(user_id))
            if secret != user.secret_salt:
                raise invalid_credentials_exception
            if user:
                await user.update(last_login=datetime.utcnow())
                scopes = await get_scopesv3(user.roles)
                access_token = create_access_token(settings, data={'sub': str(user.id), "scopes": scopes})
                return TokenSchema(access_token=access_token, refresh_token=token_data.refresh_token,
                                   token_type="bearer"), user
    except JWTError as e:
        raise invalid_credentials_exception


async def _logout_user(user: User = Depends(get_current_active_user)):
    secret = generate_secret_salt()
    await user.update(secret_salt=secret)
    return {"message": "Successfully logged out"}


async def create_admin_user(user_data: RegisterUserSchema):
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


def generate_secret_salt():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32))


def create_activate_code_redis_key(code: str):
    return f"{RedisAuthKeyEnum.ACTIVATE_USER.value}:{code}"


def create_token_blacklist_redis_key(token: str):
    return f"{RedisAuthKeyEnum.TOKEN_BLACKLIST.value}:{token}"


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


async def _activate_user(activate_code: ActivateUserCodeSchema, redis):
    code = activate_code.code
    user_id = await get_user_id_by_code(code, redis)
    if not user_id:
        raise invalid_activation_code_exception
    try:
        user = await User.objects.get(id=user_id)
        if user.is_activated:
            await delete_activate_code(code, redis)
            raise user_activated_exception
        await user.update(is_activated=True)
        await delete_activate_code(code, redis)
        return True, user
    except NoMatch:
        raise invalid_activation_code_exception


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


async def get_user_agent(request: Request):
    user_agent = request.headers.get("User-Agent")
    if not user_agent:
        return None
    return user_agent
