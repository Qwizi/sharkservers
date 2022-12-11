import datetime

from asyncpg import UniqueViolationError
from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi_pagination import Page, paginate, Params
from ormar import NoMatch
from psycopg2 import IntegrityError

from app.auth.utils import get_current_active_user, verify_password, get_password_hash
from app.users.exceptions import UserNotFound
from app.users.models import User
from app.users.schemas import UserOut, UserOutWithEmail, ChangeUsername, ChangePassword

router = APIRouter()


@router.get("", response_model=Page[UserOut])
async def get_users(params: Params = Depends()):
    users = await User.objects.select_related(["roles", "display_role"]).all()
    return paginate(users, params)


@router.get("/me", response_model=UserOutWithEmail)
async def get_logged_user(user: User = Depends(get_current_active_user)):
    return user


@router.post("/me/username", response_model=UserOut)
async def change_logged_user_username(change_username: ChangeUsername,
                                      user: User = Security(get_current_active_user, scopes=["users:me:username"])):
    try:
        await user.update(username=change_username.username, updated_date=datetime.datetime.utcnow())
    except UniqueViolationError:
        raise HTTPException(detail="Username is not available", status_code=400)
    return user


@router.post("/me/password")
async def change_logged_user_password(change_password: ChangePassword,
                                      user: User = Security(get_current_active_user, scopes=["users:me:password"])):
    if not verify_password(change_password.current_password, user.password):
        raise HTTPException(detail="Invalid current password", status_code=400)
    new_password = get_password_hash(change_password.new_password)
    await user.update(password=new_password, updated_date=datetime.datetime.utcnow())
    return {"msg": "Successfully changed password"}


@router.get("/online", response_model=Page[UserOut])
async def get_last_logged_users(params: Params = Depends()):
    filter_after = datetime.datetime.utcnow() - datetime.timedelta(minutes=15)
    users = await User.objects.select_related("display_role").filter(
        last_login__gt=filter_after).all()
    return paginate(users, params)


@router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: int):
    try:
        user = await User.objects.select_related(["roles", "display_role"]).get(id=user_id)
        return user
    except NoMatch as e:
        raise UserNotFound()
