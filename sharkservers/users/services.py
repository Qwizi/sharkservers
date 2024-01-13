"""
Module contains the services for managing user-related operations.

It includes the following classes:
- UserService: Provides methods for managing user data, such as changing username, password, and display role.
- UserSessionService: Provides methods for managing user session data.

"""  # noqa: E501

import json
from datetime import timedelta
from sqlite3 import IntegrityError as SQLIntegrityError

from asyncpg import UniqueViolationError
from fastapi import HTTPException, Request, UploadFile
from fastapi_pagination import Page, Params
from psycopg2 import IntegrityError
from pydantic import EmailStr

from sharkservers.auth.exceptions import invalid_activation_code_exception
from sharkservers.auth.services.code import CodeService
from sharkservers.auth.utils import get_password_hash, now_datetime, verify_password
from sharkservers.db import BaseService
from sharkservers.forum.services import PostService, ThreadService
from sharkservers.logger import logger
from sharkservers.services import UploadService
from sharkservers.settings import Settings
from sharkservers.users.exceptions import (
    cannot_change_display_role_exception,
    invalid_current_password_exception,
    user_email_is_the_same_exception,
    user_not_found_exception,
    username_not_available_exception,
)
from sharkservers.users.models import User, UserSession
from sharkservers.users.schemas import (
    ChangeDisplayRoleSchema,
    ChangePasswordSchema,
    ChangeUsernameSchema,
    UserOut,
)


class UserService(BaseService):
    """Service class for managing user-related operations."""

    class Meta:
        """Meta class for defining metadata options for the User model."""

        model = User
        not_found_exception = user_not_found_exception

    async def get_last_online_users(self, params: Params) -> Page[UserOut]:
        """
        Get the last online users.

        Args:
        ----
            params (Params): Pagination parameters.

        Returns:
        -------
            Page[UserOut]: A paginated list of UserOut objects.

        """
        filter_after = now_datetime() - timedelta(minutes=15)
        return await self.get_all(
            params=params,
            related=["display_role", "player", "player__steamrep_profile"],
            last_online__gt=filter_after,
        )

    @staticmethod
    async def change_username(
        user: User,
        change_username_data: ChangeUsernameSchema,
    ) -> User:
        """
        Change the username of a user.

        Args:
        ----
            user (User): The user object.
            change_username_data (ChangeUsernameSchema): The new username.

        Returns:
        -------
            User: The updated user object.

        Raises:
        ------
            username_not_available_exception: If the new username is not available.

        """
        try:
            await user.update(username=change_username_data.username)
        except (UniqueViolationError, IntegrityError, SQLIntegrityError) as err:
            raise username_not_available_exception from err
        else:
            return user

    @staticmethod
    async def change_password(
        user: User,
        change_password_data: ChangePasswordSchema,
    ) -> User:
        """
        Change the password of a user.

        Args:
        ----
            user (User): The user object.
            change_password_data (ChangePasswordSchema): The new password.

        Returns:
        -------
            User: The updated user object.

        Raises:
        ------
            invalid_current_password_exception: If the current password is invalid.

        """
        if not verify_password(change_password_data.current_password, user.password):
            raise invalid_current_password_exception
        new_password = get_password_hash(change_password_data.new_password)
        await user.update(password=new_password)
        return user

    @staticmethod
    async def change_display_role(
        user: User,
        change_display_role_data: ChangeDisplayRoleSchema,
    ) -> (User, int):
        """
        Change the display role of a user.

        Args:
        ----
            user (User): The user object.
            change_display_role_data (ChangeDisplayRoleSchema): The new display role.

        Returns:
        -------
            Tuple[User, int]: The updated user object and the old display role ID.

        Raises:
        ------
            cannot_change_display_role_exception: If the new display role is not available.

        """  # noqa: E501
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
        code_service: CodeService,
        user: User,
        new_email: EmailStr,
    ) -> (str, EmailStr):
        """
        Create a confirmation code for changing the user's email.

        Args:
        ----
            code_service (CodeService): The code service object.
            user (User): The user object.
            new_email (EmailStr): The new email address.

        Returns:
        -------
            Tuple[str, EmailStr]: The confirmation code and the new email address.

        Raises:
        ------
            user_email_is_the_same_exception: If the new email is the same as the current email.

        """  # noqa: E501
        if user.email == new_email:
            raise user_email_is_the_same_exception
        redis_data = {
            "user_id": user.id,
            "new_email": new_email,
        }
        confirm_code, _data = await code_service.create(
            data=json.dumps(redis_data),
            code_len=5,
            expire=900,
        )
        return confirm_code, new_email

    async def confirm_change_email(self, code_service: CodeService, code: str) -> User:
        """
        Confirm the change of the user's email.

        Args:
        ----
            code_service (CodeService): The code service object.
            code (str): The confirmation code.

        Returns:
        -------
            User: The updated user object.

        Raises:
        ------
            invalid_activation_code_exception: If the activation code is invalid.

        """
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

    async def upload_avatar(  # noqa: PLR0913
        self,
        user: User,
        avatar: UploadFile,
        request: Request,
        upload_service: UploadService,
        settings: Settings,
    ) -> dict:
        """
        Upload and update the user's avatar.

        Args:
        ----
            user (User): The user object.
            avatar (UploadFile): The avatar file to upload.
            request (Request): The request object.
            upload_service (UploadService): The upload service object.
            settings (Settings): The application settings.

        Returns:
        -------
            dict: A dictionary containing the old and new avatar URLs.

        Raises:
        ------
            HTTPException: If there is an error during the avatar upload.

        """
        try:
            file_data = await upload_service.upload_avatar(file=avatar)
            file_name = file_data.get("file_name")
            default_avatar_url = request.url_for(
                "static",
                path="images/default_avatar.png",
            )
            avatar_url = request.url_for("static", path=f"uploads/avatars/{file_name}")
            old_avatar_url = user.avatar
            await user.update(avatar=str(avatar_url))
            if old_avatar_url != default_avatar_url:
                old_avatar_filename = old_avatar_url.split("/")[-1]
                upload_service.delete_avatar(old_avatar_filename)

            if settings.TESTING:
                upload_service.delete_avatar(file_name)
            else:
                return {
                    "old_avatar_url": old_avatar_url,
                    "avatar_url": avatar_url,
                }
        except HTTPException:  # noqa: TRY302
            raise

    async def sync_counters(
        self,
        threads_service: ThreadService,
        posts_service: PostService,
    ) -> None:
        """
        Synchronize the thread and post counters for all users.

        Args:
        ----
            threads_service (ThreadService): The thread service object.
            posts_service (PostService): The post service object.

        """
        try:
            users = await self.Meta.model.objects.select_related(
                ["user_threads", "user_posts", "user_reputation"],
            ).all()
            for user in users:
                threads_count = (
                    await threads_service.Meta.model.objects.select_related("posts")
                    .filter(author=user)
                    .count()
                )
                posts_count = (
                    await posts_service.Meta.model.objects.select_related("likes")
                    .filter(author=user)
                    .count()
                )
                await user.update(threads_count=threads_count, posts_count=posts_count)
            logger.info(f"Finished sync counters to users -> {len(users)}")
        except Exception as e:  # noqa: BLE001
            logger.error(e.message)


class UserSessionService(BaseService):
    """Service class for managing user session-related operations."""

    class Meta:
        """Meta class for defining metadata options for the UserSession model."""

        model = UserSession
        not_found_exception = user_not_found_exception
