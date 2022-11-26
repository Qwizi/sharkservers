from typing import List

from fastapi import APIRouter
from ormar import NoMatch

from app.users.exceptions import UserNotFound
from app.users.models import User
from app.users.schemas import UserOut

router = APIRouter()


@router.get("", response_model=list[UserOut])
async def get_users():
    return await User.objects.all()


@router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: int):
    try:
        user = await User.objects.get(id=user_id)
        return user
    except NoMatch as e:
        raise UserNotFound()
