from typing import List

from fastapi import APIRouter, Depends
from fastapi_pagination import Page, paginate, Params
from ormar import NoMatch

from app.users.exceptions import UserNotFound
from app.users.models import User
from app.users.schemas import UserOut

router = APIRouter()


@router.get("", response_model=Page[UserOut])
async def get_users(params: Params = Depends()):
    users = await User.objects.all()
    return paginate(users, params)


@router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: int):
    try:
        user = await User.objects.get(id=user_id)
        return user
    except NoMatch as e:
        raise UserNotFound()
