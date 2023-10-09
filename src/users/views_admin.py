from fastapi import APIRouter, Depends, Security
from fastapi_events.dispatcher import dispatch
from fastapi_pagination import Page, Params
from src.settings import Settings, get_settings

from src.auth.dependencies import get_admin_user, get_auth_service
from src.auth.schemas import RegisterUserSchema
from src.auth.services.auth import AuthService
from src.roles.dependencies import get_roles_service
from src.roles.services import RoleService
from src.users.dependencies import get_valid_user, get_users_service
from src.users.enums import UsersAdminEventsEnum
from src.users.models import User
from src.users.schemas import UserOutWithEmail, CreateUserSchema, BanUserSchema, AdminUpdateUserSchema
from src.users.services import UserService

router = APIRouter()


@router.get("", response_model=Page[UserOutWithEmail], response_model_exclude_none=True)
async def admin_get_users(
        params: Params = Depends(),
        users_service: UserService = Depends(get_users_service),
        admin_user: User = Security(get_admin_user, scopes=["users:all"]),
) -> Page[UserOutWithEmail]:
    """
    Admin route to get users list
    :param admin_user:
    :param users_service:
    :param params:
    :return Page[UserOutWithEmail]:
    """
    users = await users_service.get_all(params=params, related=["display_role"])
    dispatch(UsersAdminEventsEnum.GET_ALL, payload={"data": users})
    return users


@router.get("/{user_id}", response_model=UserOutWithEmail)
async def admin_get_user(
        user: User = Depends(get_valid_user),
        admin_users: User = Security(get_admin_user, scopes=["users:retrieve"]),
) -> UserOutWithEmail:
    """
    Admin route to get user
    :param admin_users:
    :param user:
    :return UserOutWithEmail:
    """
    # emit event
    dispatch(UsersAdminEventsEnum.GET_ONE, payload={"data": user})
    return user



@router.post("", response_model=UserOutWithEmail)
async def admin_create_user(
        user_data: CreateUserSchema,
        auth_service: AuthService = Depends(get_auth_service),
        admin_user: User = Security(get_admin_user, scopes=["users:create"]),
        settings: Settings = Depends(get_settings)
) -> UserOutWithEmail:
    """
    Admin create user
    :param user_data:
    :param user:
    :return UserOutWithEmail:
    """
    created_user = await auth_service.register(RegisterUserSchema(
        username=user_data.username,
        email=user_data.email,
        password=user_data.password,
        password2=user_data.password
    ),
        is_activated=user_data.is_activated,
        is_superuser=user_data.is_superuser,
        settings=settings
    )
    dispatch(UsersAdminEventsEnum.CREATE, payload={"data": created_user})
    return created_user


@router.delete("/{user_id}")
async def admin_delete_user(
        validate_user: User = Depends(get_valid_user),
        admin_user: User = Security(get_admin_user, scopes=["users:delete"]),
        users_service: UserService = Depends(get_users_service),
) -> dict:
    """
    Admin delete user
    :param users_service:
    :param validate_user:
    :param user_id:
    :param admin_user:
    :return dict:
    """
    user_deleted = await users_service.delete(_id=validate_user.id)
    dispatch(UsersAdminEventsEnum.DELETE, payload={"data": user_deleted})
    return {"detail": f"User with id {validate_user.id} was deleted"}


@router.put("/{user_id}")
async def admin_update_user(
        update_user_data: AdminUpdateUserSchema,
        admin_user: User = Security(get_admin_user, scopes=["users:update"]),
        validate_user: User = Depends(get_valid_user),
        roles_service: RoleService = Depends(get_roles_service)

) -> UserOutWithEmail:
    update_user_data_dict = update_user_data.dict()
    filtered = {k: v for k, v in update_user_data_dict.items() if v is not None}
    update_user_data_dict.clear()
    update_user_data_dict.update(filtered)
    roles_ids: list[int] | None = update_user_data_dict.pop("roles", None)
    display_role_id: int | None = update_user_data_dict.pop("display_role", None)
    print(roles_ids)
    roles = []
    if roles_ids:
        for role_id in roles_ids:
            role = await roles_service.get_one(id=role_id)
            roles.append(role)
    print(roles)
    if roles:
        for _role in validate_user.roles:
            await validate_user.roles.remove(_role)
        for role in roles:
            await validate_user.roles.add(role)
    if display_role_id:
        display_role = await roles_service.get_one(id=display_role_id)
        await validate_user.update(display_role=display_role)
    await validate_user.update(**update_user_data_dict)
    return validate_user
