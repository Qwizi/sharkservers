from fastapi import (
    APIRouter,
    Depends,
    Security,
    BackgroundTasks,
    UploadFile,
    File,
    Request,
)
from fastapi_events.dispatcher import dispatch
from fastapi_limiter.depends import RateLimiter
from fastapi_pagination import Page, Params
from src.schemas import OrderQuery

from src.apps.dependencies import get_app_service
from src.apps.schemas import CreateAppSchema
from src.apps.services import AppService
from src.auth.dependencies import (
    get_current_active_user,
    get_auth_service,
    get_change_account_email_code_service,
)
from src.auth.schemas import ActivateUserCodeSchema
from src.auth.services.auth import AuthService
from src.auth.services.code import CodeService
from src.dependencies import get_email_service, get_upload_service
from src.enums import ActivationEmailTypeEnum
from src.forum.dependencies import get_posts_service, get_threads_service
from src.forum.services import PostService, ThreadService
from src.roles.dependencies import get_roles_service
from src.roles.schemas import StaffRolesSchema
from src.roles.services import RoleService
from src.scopes.dependencies import get_scopes_service
from src.scopes.services import ScopeService
from src.services import EmailService, UploadService
from src.settings import Settings, get_settings
from src.users.dependencies import get_valid_user, get_users_service
from src.users.enums import UsersEventsEnum
from src.users.models import User
from src.users.schemas import (
    UserOut,
    UserOutWithEmail,
    ChangeUsernameSchema,
    ChangePasswordSchema,
    ChangeDisplayRoleSchema,
    SuccessChangeUsernameSchema,
    ChangeEmailSchema,
)
from src.users.services import UserService

router = APIRouter()

limiter = RateLimiter(times=1, seconds=60)


@router.get("", response_model=Page[UserOut])
async def get_users(
    params: Params = Depends(),
    queries: OrderQuery = Depends(),
    users_service: UserService = Depends(get_users_service),
) -> Page[UserOut]:
    """
    Get users
    :param users_service:
    :param params:
    :return Page[UserOut]:
    """
    dispatch(UsersEventsEnum.GET_ALL_PRE, payload={"data": params})
    users = await users_service.get_all(
        params=params, related=["display_role"], order_by=queries.order_by
    )
    dispatch(UsersEventsEnum.GET_ALL_POST, payload={"data": users})
    return users


@router.get("/staff")
async def get_staff_users(
    params: Params = Depends(), roles_service: RoleService = Depends(get_roles_service)
) -> Page[StaffRolesSchema]:
    """
    Get staff users
    :param users_service:
    :param params:
    :return Page[UserOut]:
    """
    return await roles_service.get_staff_roles(params)


@router.get("/online")
async def get_last_online_users(
    params: Params = Depends(), users_service: UserService = Depends(get_users_service)
) -> Page[UserOut]:
    """
    Get last logged users
    :param users_service:
    :param params:
    :return Page[UserOut]:
    """
    return await users_service.get_last_online_users(params=params)


@router.get(
    "/me",
)
async def get_logged_user(
    user: User = Security(get_current_active_user, scopes=["users:me"])
) -> UserOutWithEmail:
    """
    Get logged user
    :param user:
    :return UserOutWithEmail:
    """
    dispatch(UsersEventsEnum.ME_PRE, payload={"user": user})
    dispatch(UsersEventsEnum.ME_POST, payload={"user": user})
    return user


@router.get("/me/posts")
async def get_logged_user_posts(
    params: Params = Depends(),
    queries: OrderQuery = Depends(),
    user: User = Security(get_current_active_user, scopes=["users:me"]),
    posts_service: PostService = Depends(get_posts_service),
):
    """
    Get user posts
    :param params:
    :param posts_service:
    :param user:
    :return AbstractPage:
    """
    return await posts_service.get_all(
        params=params, author__id=user.id, order_by=queries.order_by
    )


@router.get("/me/threads")
async def get_logged_user_threads(
    params: Params = Depends(),
    queries: OrderQuery = Depends(),
    user: User = Security(get_current_active_user, scopes=["users:me"]),
    threads_service: ThreadService = Depends(get_threads_service),
):
    """
    Get user threads
    :param threads_service:
    :param params:
    :param user:
    :return AbstractPage:
    """
    return await threads_service.get_all(
        params=params, author__id=user.id, order_by=queries.order_by
    )


@router.get("/me/apps")
async def get_user_apps(
    params: Params = Depends(),
    user: User = Security(get_current_active_user, scopes=["apps:all"]),
    apps_service: AppService = Depends(get_app_service),
) -> dict:
    """
    Get user apps
    :param apps_service:
    :param user:
    :return dict:
    """
    apps = await apps_service.get_all(params=params, owner__id=user.id)
    return apps


@router.post("/me/username")
async def change_user_username(
    change_username_data: ChangeUsernameSchema,
    user: User = Security(get_current_active_user, scopes=["users:me:username"]),
    users_service: UserService = Depends(get_users_service),
) -> SuccessChangeUsernameSchema:
    """
    Change user username
    :param change_username_data:
    :param user:
    :return UserOut:
    """
    dispatch(
        UsersEventsEnum.CHANGE_USERNAME_PRE, payload={"data": change_username_data}
    )
    old_username = user.username
    user = await users_service.change_username(user, change_username_data)
    dispatch(UsersEventsEnum.CHANGE_USERNAME_POST, payload={"data": user})
    return SuccessChangeUsernameSchema(
        old_username=old_username, new_username=change_username_data.username
    )


@router.post("/me/password")
async def change_user_password(
    change_password_data: ChangePasswordSchema,
    user: User = Security(get_current_active_user, scopes=["users:me:password"]),
    users_service: UserService = Depends(get_users_service),
) -> dict:
    """
    Change user password
    :param change_password_data:
    :param user:
    :return dict:
    """
    dispatch(
        UsersEventsEnum.CHANGE_PASSWORD_PRE, payload={"data": change_password_data}
    )
    user = await users_service.change_password(user, change_password_data)
    dispatch(UsersEventsEnum.CHANGE_PASSWORD_POST, payload={"data": user})
    return {"msg": "Successfully changed password"}


@router.post("/me/email", dependencies=[Depends(limiter)])
async def request_change_user_email(
    change_email_data: ChangeEmailSchema,
    background_tasks: BackgroundTasks,
    user: User = Security(get_current_active_user, scopes=["users:me"]),
    email_service: EmailService = Depends(get_email_service),
    code_service: CodeService = Depends(get_change_account_email_code_service),
    users_service: UserService = Depends(get_users_service),
):
    """
    Request change user email
    :param email_service:
    :param users_service:
    :param background_tasks:
    :param code_service:
    :param change_email_data:
    :param user:
    :return dict:
    """
    confirm_code, _data = await users_service.create_confirm_email_code(
        code_service=code_service, user=user, new_email=change_email_data.email
    )
    background_tasks.add_task(
        email_service.send_confirmation_email,
        ActivationEmailTypeEnum.EMAIL,
        change_email_data.email,
        confirm_code,
    )
    return {"msg": "Request for change email was sent"}


@router.post(
    "/me/email/confirm",
    dependencies=[Security(get_current_active_user, scopes=["users:me"])],
)
async def confirm_change_user_email(
    activate_code_data: ActivateUserCodeSchema,
    code_service: CodeService = Depends(get_change_account_email_code_service),
    users_service: UserService = Depends(get_users_service),
) -> UserOutWithEmail:
    """
    Confirm change user email
    :param users_service:
    :param code_service:
    :param activate_code_data:
    :return dict:
    """
    updated_user = await users_service.confirm_change_email(
        code_service=code_service, code=activate_code_data.code
    )
    return updated_user


@router.post("/me/display-role")
async def change_user_display_role(
    change_display_role_data: ChangeDisplayRoleSchema,
    user: User = Security(get_current_active_user, scopes=["users:me:display-role"]),
    users_service: UserService = Depends(get_users_service),
):
    """
    Change user display role
    :param auth_service:
    :param change_display_role_data:
    :param user:
    :return dict:
    """
    user, old_user_display_role = await users_service.change_display_role(
        user, change_display_role_data
    )
    return user


@router.get("/me/apps")
async def get_user_apps(
    params: Params = Depends(),
    user: User = Security(get_current_active_user, scopes=["apps:all"]),
    apps_service: AppService = Depends(get_app_service),
) -> dict:
    """
    Get user apps
    :param apps_service:
    :param user:
    :return dict:
    """
    apps = await apps_service.get_all(params=params, owner__id=user.id)
    return apps


@router.post("/me/apps")
async def create_user_app(
    app_data: CreateAppSchema,
    user: User = Security(get_current_active_user, scopes=["apps:create"]),
    apps_service: AppService = Depends(get_app_service),
    scopes_service: ScopeService = Depends(get_scopes_service),
    settings: Settings = Depends(get_settings),
) -> dict:
    """
    Create user app
    :param scopes_service:
    :param apps_service:
    :param app_data:
    :param user:
    :return dict:
    """
    app = await apps_service.create(
        name=app_data.name,
        description=app_data.description,
        owner=user,
    )
    if settings.DEBUG:
        scopes = await scopes_service.Meta.model.objects.all()
    else:
        scopes = await scopes_service.Meta.model.filter(id__in=app_data.scopes)
    for scope in scopes:
        await app.scopes.add(scope)
    return app


@router.post("/me/avatar")
async def upload_user_avatar(
    request: Request,
    avatar: UploadFile = File(...),
    user: User = Security(get_current_active_user, scopes=["users:me"]),
    users_service: UserService = Depends(get_users_service),
    upload_service: UploadService = Depends(get_upload_service),
    settings: Settings = Depends(get_settings),
):
    """
    Upload user avatar
    :return:
    """
    data = await users_service.upload_avatar(
        user, avatar, request, upload_service, settings
    )
    print(data)
    return {"msg": "Avatar was uploaded"}


@router.get("/{user_id}", response_model=UserOut)
async def get_user(user: User = Depends(get_valid_user)) -> UserOut:
    """
    Get user
    :param user:
    :return UserOut:
    """
    dispatch(UsersEventsEnum.GET_ONE_PRE, payload={"user_id": user.id})
    dispatch(UsersEventsEnum.GET_ONE_POST, payload={"user": user})
    return user


@router.get("/{user_id}/posts")
async def get_user_posts(
    params: Params = Depends(),
    queries: OrderQuery = Depends(),
    user: User = Depends(get_valid_user),
    posts_service: PostService = Depends(get_posts_service),
):
    """
    Get user posts
    :param posts_service:
    :param params:
    :param user:
    :return AbstractPage:
    """
    return await posts_service.get_all(
        params=params, author__id=user.id, order_by=queries.order_by
    )


@router.get("/{user_id}/threads")
async def get_user_threads(
    params: Params = Depends(),
    queries: OrderQuery = Depends(),
    user: User = Depends(get_valid_user),
    threads_service: ThreadService = Depends(get_threads_service),
):
    """
    Get user threads
    :param threads_service:
    :param params:
    :param user:
    :return AbstractPage:
    """
    return await threads_service.get_all(
        params=params, author__id=user.id, order_by=queries.order_by
    )
