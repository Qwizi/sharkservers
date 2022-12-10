from fastapi import APIRouter, Depends
from fastapi_pagination import Page, paginate, Params
from ormar import NoMatch

from app.auth.utils import get_current_active_user
from app.users.exceptions import UserNotFound
from app.users.models import User
from app.users.schemas import UserOut, UserOutWithEmail

router = APIRouter()


@router.get("", response_model=Page[UserOut])
async def get_users(params: Params = Depends()):
    users = await User.objects.select_related(["roles", "display_role"]).all()
    return paginate(users, params)


@router.get("/me", response_model=UserOutWithEmail)
async def get_logged_user(user: User = Depends(get_current_active_user)):
    return user


@router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: int):
    try:
        user = await User.objects.select_related(["roles", "display_role"]).get(id=user_id)
        return user
    except NoMatch as e:
        raise UserNotFound()
