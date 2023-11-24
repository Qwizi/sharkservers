import json
from datetime import timedelta
from sqlite3 import IntegrityError as SQLIntegrityError

from asyncpg import UniqueViolationError
from fastapi import Request, HTTPException, UploadFile
from fastapi_pagination import Params, Page
from psycopg2 import IntegrityError
from pydantic import EmailStr
from src.forum.services import PostService, ThreadService

from src.auth.exceptions import invalid_activation_code_exception
from src.auth.services.code import CodeService
from src.auth.utils import now_datetime, verify_password, get_password_hash
from src.db import BaseService
from src.services import UploadService
from src.settings import Settings
from src.users.exceptions import (
    user_not_found_exception,
    username_not_available_exception,
    invalid_current_password_exception,
    cannot_change_display_role_exception,
    user_email_is_the_same_exception,
)
from src.users.models import User, UserSession
from src.users.schemas import (
    UserOut,
    ChangeUsernameSchema,
    ChangePasswordSchema,
    ChangeDisplayRoleSchema,
)
from src.logger import logger


class UserService(BaseService):
    class Meta:
        model = User
        not_found_exception = user_not_found_exception

    async def get_last_online_users(self, params: Params) -> Page[UserOut]:
        filter_after = now_datetime() - timedelta(minutes=15)
        return await self.get_all(
            params=params, related=["display_role", "player", "player__steamrep_profile"], last_online__gt=filter_after
        )

    @staticmethod
    async def change_username(user: User, change_username_data: ChangeUsernameSchema):
        """
        Change username
        :param user:
        :param change_username_data:
        :return:
        """
        try:
            await user.update(username=change_username_data.username)
            return user
        except (UniqueViolationError, IntegrityError, SQLIntegrityError):
            raise username_not_available_exception

    @staticmethod
    async def change_password(user: User, change_password_data: ChangePasswordSchema):
        """
        Change user password
        :param user:
        :param change_password_data:
        :return:
        """
        if not verify_password(change_password_data.current_password, user.password):
            raise invalid_current_password_exception
        new_password = get_password_hash(change_password_data.new_password)
        await user.update(password=new_password)
        return user

    @staticmethod
    async def change_display_role(
        user: User, change_display_role_data: ChangeDisplayRoleSchema
    ) -> (User, int):
        display_role_exists_in_user_roles = False
        old_user_display_role = user.display_role.id
        for role in user.roles:
            if role.id == change_display_role_data.role_id:
                display_role_exists_in_user_roles = True
                break
        if not display_role_exists_in_user_roles:
            raise cannot_change_display_role_exception
        await user.update(display_role=change_display_role_data.role_id)
        return user, old_user_display_role

    @staticmethod
    async def create_confirm_email_code(
        code_service: CodeService, user: User, new_email: EmailStr
    ):
        if user.email == new_email:
            raise user_email_is_the_same_exception
        redis_data = {
            "user_id": user.id,
            "new_email": new_email,
        }
        confirm_code, _data = await code_service.create(
            data=json.dumps(redis_data), code_len=5, expire=900
        )
        return confirm_code, new_email

    async def confirm_change_email(self, code_service: CodeService, code: str):
        user_data = await code_service.get(code)
        if user_data is None:
            raise invalid_activation_code_exception
        user_data = json.loads(user_data)
        user_id = user_data.get("user_id", None)
        new_email = user_data.get("new_email", None)
        user_id = int(user_id)

        user = await self.get_one(id=user_id, related=["display_role", "roles"])
        await user.update(email=new_email)
        await code_service.delete(code)
        return user

    async def upload_avatar(
        self,
        user: User,
        avatar: UploadFile,
        request: Request,
        upload_service: UploadService,
        settings: Settings,
    ) -> dict:
        try:
            file_data = await upload_service.upload_avatar(file=avatar)
            file_name = file_data.get("file_name")
            default_avatar_url = request.url_for(
                "static", path="images/default_avatar.png"
            )
            avatar_url = request.url_for("static", path=f"uploads/avatars/{file_name}")
            old_avatar_url = user.avatar
            await user.update(avatar=str(avatar_url))
            if old_avatar_url != default_avatar_url:
                old_avatar_filename = old_avatar_url.split("/")[-1]
                upload_service.delete_avatar(old_avatar_filename)

            if settings.TESTING:
                upload_service.delete_avatar(file_name)
            return {
                "old_avatar_url": old_avatar_url,
                "avatar_url": avatar_url,
            }
        except HTTPException as e:
            raise e

    async def sync_counters(self, threads_service: ThreadService, posts_service: PostService):
        try:
            users = await self.Meta.model.objects.select_related(
                ["user_threads", "user_posts", "user_reputation"]
            ).all()
            for user in users:
                threads_count = await threads_service.Meta.model.objects.select_related("posts").filter(author=user).count()
                posts_count = await posts_service.Meta.model.objects.select_related("likes").filter(author=user).count()
                await user.update(threads_count=threads_count, posts_count=posts_count)
            logger.info(f"Finished sync counters to users -> {len(users)}")
        except Exception as e:
            logger.error(e.message)

class UserSessionService(BaseService):
    class Meta:
        model = UserSession
        not_found_exception = user_not_found_exception