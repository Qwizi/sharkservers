from fastapi import APIRouter, Depends, Security
from fastapi_pagination import Page, Params, paginate
from fastapi_pagination.ext.ormar import paginate
from ormar import NoMatch

from app.auth.schemas import RegisterUser
from app.auth.utils import register_user, get_current_active_user, get_admin_user
from app.roles.exceptions import RoleNotFound
from app.roles.models import Role
from app.users.exceptions import UserNotFound
from app.users.models import User
from app.users.schemas import UserOutWithEmail, CreateUser

router = APIRouter()


@router.get("", response_model=Page[UserOutWithEmail], response_model_exclude_none=True)
async def admin_get_users(params: Params = Depends(),
                          user: User = Security(get_admin_user, scopes=["users:get_all"])):
    users = User.objects.select_related("display_role")
    return await paginate(users, params)


@router.get("/{user_id}", response_model=UserOutWithEmail)
async def admin_get_user(user_id: int, user: User = Security(get_admin_user, scopes=["users:retrieve"])):
    try:
        user = await User.objects.select_related(["display_role", "roles", "steamprofile"]).get(id=user_id)
    except NoMatch:
        raise UserNotFound
    return user


@router.post("", response_model=UserOutWithEmail)
async def admin_create_user(user_data: CreateUser,
                            user: User = Security(get_admin_user, scopes=["users:create"])):
    register_user_schema = RegisterUser(
        username=user_data.username,
        email=user_data.email,
        password=user_data.password,
        password2=user_data.password
    )
    created_user = await register_user(register_user_schema)
    if user_data.is_activated:
        await created_user.update(is_activated=True)
    if user_data.display_role:
        try:
            role = await Role.objects.get(id=user_data.display_role)
            await created_user.update(display_role=role)
            await created_user.roles.add(role)
        except NoMatch:
            raise RoleNotFound()
    return created_user


@router.delete("/{user_id}")
async def admin_delete_user(user_id: int, user: User = Security(get_admin_user, scopes=["users:delete"])):
    try:
        user = await User.objects.get(id=user_id)
        await user.delete()
    except NoMatch:
        raise UserNotFound
    return {"msg": "Successfully deleted user"}
