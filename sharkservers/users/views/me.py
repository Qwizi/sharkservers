"""
Module contains the API endpoints related to the currently logged-in user.

Functions:
- get_logged_user: Retrieves the currently logged-in user.
- get_logged_user_posts: Retrieves all posts created by the logged-in user.
- get_logged_user_threads: Retrieves all threads created by the logged-in user.
- change_user_username: Changes the username of the current user.
- change_user_password: Changes the password of the current user.
- request_change_user_email: Requests a change of user email.
- confirm_change_user_email: Confirms the change of user email.
- change_user_display_role: Changes the display role of the current user.
- upload_user_avatar: Uploads the user's avatar.
- connect_steam_profile: Connects a Steam profile to the user's account.
- get_user_sessions: Retrieves the sessions of the current user.
- delete_user_session: Deletes the user session.

"""
from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    File,
    Request,
    Security,
    UploadFile,
)
from fastapi_limiter.depends import RateLimiter

from sharkservers.auth.dependencies import (
    get_change_account_email_code_service,
    get_current_active_user,
    get_steam_auth_service,
)
from sharkservers.dependencies import get_email_service, get_upload_service
from sharkservers.enums import ActivationEmailTypeEnum
from sharkservers.forum.dependencies import get_posts_service, get_threads_service
from sharkservers.settings import Settings, get_settings
from sharkservers.users.dependencies import get_users_service, get_valid_user_session
from sharkservers.users.schemas import (
    ChangeDisplayRoleSchema,
    ChangeEmailSchema,
    ChangePasswordSchema,
    ChangeUsernameSchema,
    SuccessChangeUsernameSchema,
    UserOutWithEmail,
    UserSessionOut,
)


from fastapi_pagination import Page, Params

from sharkservers.auth.schemas import ActivateUserCodeSchema, SteamAuthSchema
from sharkservers.auth.services.code import CodeService
from sharkservers.auth.services.steam import SteamAuthService
from sharkservers.forum.schemas import PostOut, ThreadOut
from sharkservers.forum.services import PostService, ThreadService
from sharkservers.schemas import OrderQuery
from sharkservers.services import EmailService, UploadService
from sharkservers.users.models import User, UserSession
from sharkservers.users.services import UserService

limiter = RateLimiter(times=1, seconds=60)

router = APIRouter()


@router.get(
    "",
)
async def get_logged_user(
    user: User = Security(get_current_active_user, scopes=["users:me"]),  # noqa: B008
) -> UserOutWithEmail:
    """
    Retrieve the currently logged-in user.

    Args:
    ----
        user (User): The currently logged-in user.

    Returns:
    -------
        UserOutWithEmail: The logged-in user with email.

    """
    return user


@router.get("/posts")
async def get_logged_user_posts(
    params: Params = Depends(),  # noqa: B008
    queries: OrderQuery = Depends(),  # noqa: B008
    user: User = Security(get_current_active_user, scopes=["users:me"]),  # noqa: B008
    posts_service: PostService = Depends(get_posts_service),  # noqa: B008
) -> Page[PostOut]:
    """
    Retrieves all posts created by the logged-in user.

    Args:
    ----
        params (Params, optional): The parameters for pagination and filtering. Defaults to Depends().
        queries (OrderQuery, optional): The query parameters for ordering the posts. Defaults to Depends().
        user (User, optional): The logged-in user. Defaults to Security(get_current_active_user, scopes=["users:me"]).
        posts_service (PostService, optional): The service for retrieving posts. Defaults to Depends(get_posts_service).

    Returns:
    -------
        List[Post]: The list of posts created by the logged-in user.
    """  # noqa: D401, E501
    return await posts_service.get_all(
        params=params,
        author__id=user.id,
        order_by=queries.order_by,
    )


@router.get("/threads")
async def get_logged_user_threads(
    params: Params = Depends(),  # noqa: B008
    queries: OrderQuery = Depends(),  # noqa: B008
    user: User = Security(get_current_active_user, scopes=["users:me"]),  # noqa: B008
    threads_service: ThreadService = Depends(get_threads_service),  # noqa: B008
) -> Page[ThreadOut]:
    """
    Retrieve all threads for the logged-in user.

    Args:
    ----
        params (Params): The parameters for filtering and pagination.
        queries (OrderQuery): The query parameters for ordering.
        user (User): The logged-in user.
        threads_service (ThreadService): The service for handling threads.

    Returns:
    -------
        List[Thread]: The list of threads for the logged-in user.
    """
    return await threads_service.get_all(
        params=params,
        author__id=user.id,
        order_by=queries.order_by,
    )


@router.post("/username")
async def change_user_username(
    change_username_data: ChangeUsernameSchema,
    user: User = Security(get_current_active_user, scopes=["users:me:username"]),  # noqa: B008
    users_service: UserService = Depends(get_users_service),  # noqa: B008
) -> SuccessChangeUsernameSchema:
    """
    Change the username of the current user.

    Args:
    ----
        change_username_data (ChangeUsernameSchema): The data containing the new username.
        user (User): The current authenticated user.
        users_service (UserService): The service responsible for handling user-related operations.

    Returns:
    -------
        SuccessChangeUsernameSchema: The response containing the old and new usernames.
    """  # noqa: E501
    old_username = user.username
    user = await users_service.change_username(user, change_username_data)
    return SuccessChangeUsernameSchema(
        old_username=old_username,
        new_username=change_username_data.username,
    )


@router.post("/password")
async def change_user_password(
    change_password_data: ChangePasswordSchema,
    user: User = Security(get_current_active_user, scopes=["users:me:password"]),  # noqa: B008
    users_service: UserService = Depends(get_users_service),  # noqa: B008
) -> dict:
    """
    Change the password of the current user.

    Args:
    ----
        change_password_data (ChangePasswordSchema): The new password data.
        user (User): The current user.
        users_service (UserService): The service for managing users.

    Returns:
    -------
        dict: A dictionary with a success message.
    """
    user = await users_service.change_password(user, change_password_data)
    return {"msg": "Successfully changed password"}


@router.post("/email", dependencies=[Depends(limiter)])
async def request_change_user_email(  # noqa: PLR0913
    change_email_data: ChangeEmailSchema,
    background_tasks: BackgroundTasks,
    user: User = Security(get_current_active_user, scopes=["users:me"]),  # noqa: B008
    email_service: EmailService = Depends(get_email_service),  # noqa: B008
    code_service: CodeService = Depends(get_change_account_email_code_service),  # noqa: B008
    users_service: UserService = Depends(get_users_service),  # noqa: B008
) -> dict[str, str]:
    """
    Request a change of user email.

    Args:
    ----
        change_email_data (ChangeEmailSchema): The data for the email change request.
        background_tasks (BackgroundTasks): The background tasks manager.
        user (User): The current authenticated user.
        email_service (EmailService): The email service.
        code_service (CodeService): The code service for email confirmation codes.
        users_service (UserService): The user service.

    Returns:
    -------
        dict: A dictionary with a success message indicating that the request for email change was sent.
    """  # noqa: E501
    confirm_code, _data = await users_service.create_confirm_email_code(
        code_service=code_service,
        user=user,
        new_email=change_email_data.email,
    )
    background_tasks.add_task(
        email_service.send_confirmation_email,
        ActivationEmailTypeEnum.EMAIL,
        change_email_data.email,
        confirm_code,
    )
    return {"msg": "Request for change email was sent"}


@router.post(
    "/email/confirm",
    dependencies=[Security(get_current_active_user, scopes=["users:me"])],
)
async def confirm_change_user_email(
    activate_code_data: ActivateUserCodeSchema,
    code_service: CodeService = Depends(get_change_account_email_code_service),  # noqa: B008
    users_service: UserService = Depends(get_users_service),  # noqa: B008
) -> UserOutWithEmail:
    """
    Confirm the change of user's email address using the activation code.

    Args:
    ----
        activate_code_data (ActivateUserCodeSchema): The activation code data.
        code_service (CodeService, optional): The code service dependency. Defaults to Depends(get_change_account_email_code_service).
        users_service (UserService, optional): The users service dependency. Defaults to Depends(get_users_service).

    Returns:
    -------
        UserOutWithEmail: The updated user with the new email address.
    """  # noqa: E501
    return await users_service.confirm_change_email(
        code_service=code_service,
        code=activate_code_data.code,
    )


@router.post("/display-role")
async def change_user_display_role(
    change_display_role_data: ChangeDisplayRoleSchema,
    user: User = Security(get_current_active_user, scopes=["users:me:display-role"]),  # noqa: B008
    users_service: UserService = Depends(get_users_service),  # noqa: B008
) -> UserOutWithEmail:
    """
    Change the display role of the current user.

    Args:
    ----
        change_display_role_data (ChangeDisplayRoleSchema): The data for changing the display role.
        user (User): The current user.
        users_service (UserService): The service for managing users.

    Returns:
    -------
        UserOutWithEmail: The updated user object.
    """  # noqa: E501
    user, old_user_display_role = await users_service.change_display_role(
        user,
        change_display_role_data,
    )
    return user


@router.post("/avatar")
async def upload_user_avatar(  # noqa: PLR0913
    request: Request,
    avatar: UploadFile = File(...),  # noqa: B008
    user: User = Security(get_current_active_user, scopes=["users:me"]),  # noqa: B008
    users_service: UserService = Depends(get_users_service),  # noqa: B008
    upload_service: UploadService = Depends(get_upload_service),  # noqa: B008
    settings: Settings = Depends(get_settings),  # noqa: B008
) -> dict[str, str]:
    """
    Upload the user's avatar.
    sharkservers.

    Returns
    -------
        dict: A dictionary with a success message.

    """  # noqa: D205
    await users_service.upload_avatar(
        user,
        avatar,
        request,
        upload_service,
        settings,
    )
    return {"msg": "Avatar was uploaded"}


@router.post("/connect/steam")
async def connect_steam_profile(
    params: SteamAuthSchema,
    user: User = Security(get_current_active_user, scopes=["users:me"]),  # noqa: B008
    steam_auth_service: SteamAuthService = Depends(get_steam_auth_service),  # noqa: B008
) -> None:
    """
    Connect a Steam profile to the user's account.

    Args:
    ----
        params (SteamAuthSchema): The parameters for Steam authentication.
        user (User, optional): The authenticated user. Defaults to the current active user.
        steam_auth_service (SteamAuthService, optional): The Steam authentication service. Defaults to the injected service.

    Returns:
    -------
        None: Nothing.
    """  # noqa: E501
    return await steam_auth_service.authenticate(user, params)


@router.get("/sessions")
async def get_user_sessions(
    user: User = Security(get_current_active_user, scopes=["users:me"]),  # noqa: B008
) -> list[UserSessionOut]:
    """
    Retrieve the sessions of the current user.

    Args:
    ----
        user (User): The current user.

    Returns:
    -------
        list[UserSessionOut]: A list of user sessions.
    """
    return user.sessions


@router.delete("/sessions/{session_id}")
async def delete_user_session(
    user_session: UserSession = Depends(get_valid_user_session),  # noqa: B008
) -> UserSessionOut:
    """
    Delete the user session.

    Args:
    ----
        user_session (UserSession): The user session to be deleted.

    Returns:
    -------
        UserSession: The deleted user session.
    """
    await user_session.delete()
    return user_session
