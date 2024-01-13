"""
Module contains the API endpoints related to admin users.

Functions:
- admin_get_users: Retrieves a paginated list of users.
- admin_get_user: Retrieves a specific user.
- admin_create_user: Creates a user.
- admin_delete_user: Deletes a user.
- admin_update_user: Updates a user.


"""
from __future__ import annotations

from fastapi import APIRouter, Depends, Security
from fastapi_events.dispatcher import dispatch
from fastapi_pagination import Page, Params

from sharkservers.auth.dependencies import get_admin_user, get_auth_service
from sharkservers.auth.schemas import RegisterUserSchema
from sharkservers.auth.services.auth import AuthService
from sharkservers.auth.utils import get_password_hash
from sharkservers.roles.dependencies import get_roles_service
from sharkservers.roles.services import RoleService
from sharkservers.settings import Settings, get_settings
from sharkservers.users.dependencies import get_users_service, get_valid_user
from sharkservers.users.enums import UsersAdminEventsEnum
from sharkservers.users.models import User
from sharkservers.users.schemas import (
    AdminUpdateUserSchema,
    CreateUserSchema,
    UserOutWithEmail,
)
from sharkservers.users.services import UserService

router = APIRouter()


@router.get(
    "",
    response_model_exclude_none=True,
    dependencies=[Security(get_admin_user, scopes=["users:all"])],
)
async def admin_get_users(
    params: Params = Depends(),
    users_service: UserService = Depends(get_users_service),
) -> Page[UserOutWithEmail]:
    """
    Retrieve all users with their associated data.

    Args:
    ----
        params (Params, optional): The parameters for filtering and pagination. Defaults to Depends().
        users_service (UserService, optional): The service for retrieving user data. Defaults to Depends(get_users_service).

    Returns:
    -------
        Page[UserOutWithEmail]: The paginated list of users with their associated data.
    """
    users = await users_service.get_all(
        params=params,
        related=["display_role", "player", "player__steamrep_profile"],
    )
    dispatch(UsersAdminEventsEnum.GET_ALL, payload={"data": users})
    return users


@router.get(
    "/{user_id}",
    dependencies=[Security(get_admin_user, scopes=["users:retrieve"])],
)
async def admin_get_user(
    user: User = Depends(get_valid_user),
) -> UserOutWithEmail:
    """
    Retrieve the user information for an admin user.

    Args:
    ----
        user (User): The admin user object.

    Returns:
    -------
        UserOutWithEmail: The user information with email.

    """
    return user


@router.post(
    "",
    response_model=UserOutWithEmail,
    dependencies=[Security(get_admin_user, scopes=["users:create"])],
)
async def admin_create_user(
    user_data: CreateUserSchema,
    auth_service: AuthService = Depends(get_auth_service),
    settings: Settings = Depends(get_settings),
) -> UserOutWithEmail:
    """
    Create a new user with the provi    print(roles)
    ded user data.


    Args:
    ----
        user_data (CreateUserSchema): The data for creating a new user.
        auth_service (AuthService, optional): The authentication service. Defaults to Depends(get_auth_service).
        settings (Settings, optional): The application settings. Defaults to Depends(get_settings).

    Returns:
    -------
        UserOutWithEmail: The created user with email.
    """  # noqa: D205
    return await auth_service.register(
        RegisterUserSchema(
            username=user_data.username,
            email=user_data.email,
            password=user_data.password,
            password2=user_data.password,
        ),
        is_activated=user_data.is_activated,
        is_superuser=user_data.is_superuser,
        settings=settings,
    )


@router.delete(
    "/{user_id}",
    dependencies=[Security(get_admin_user, scopes=["users:delete"])],
)
async def admin_delete_user(
    validate_user: User = Depends(get_valid_user),
    users_service: UserService = Depends(get_users_service),
) -> UserOutWithEmail:
    """
    Deletes a user from the system.

    Args:
    ----
        validate_user (User): The user to be deleted.
        users_service (UserService): The service responsible for user operations.

    Returns:
    -------
        UserOutWithEmail: The deleted user with email.
    """  # noqa: D401
    return await users_service.delete(_id=validate_user.id)


@router.put(
    "/{user_id}",
    dependencies=[Security(get_admin_user, scopes=["users:update"])],
)
async def admin_update_user(
    update_user_data: AdminUpdateUserSchema,
    validate_user: User = Depends(get_valid_user),
    roles_service: RoleService = Depends(get_roles_service),
) -> UserOutWithEmail:
    """
    Admin function to update a user's information.

    Args:
    ----
        update_user_data (AdminUpdateUserSchema): The updated user data.
        validate_user (User): The user to be updated.
        roles_service (RoleService): The service for managing roles.

    Returns:
    -------
        UserOutWithEmail: The updated user with email.

    """
    update_user_data_dict = update_user_data.dict()
    filtered = {k: v for k, v in update_user_data_dict.items() if v is not None}
    update_user_data_dict.clear()
    update_user_data_dict.update(filtered)
    password = update_user_data_dict.pop("password", None)
    if password:
        password_hash = get_password_hash(password)
        update_user_data_dict.update(password=password_hash)
    roles_ids: list[int] | None = update_user_data_dict.pop("roles", None)
    display_role_id: int | None = update_user_data_dict.pop("display_role", None)
    roles = []
    if roles_ids:
        for role_id in roles_ids:
            role = await roles_service.get_one(id=role_id)
            roles.append(role)
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
