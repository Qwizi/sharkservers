import json
import uuid
from datetime import timedelta
from pathlib import Path
from sqlite3 import IntegrityError as SQLIntegrityError

from PIL import Image
from asyncpg import UniqueViolationError
from fastapi import File, Request, HTTPException
from fastapi_pagination import Params, Page
from psycopg2 import IntegrityError
from pydantic import EmailStr
from starlette import status

from src.auth.exceptions import invalid_activation_code_exception
from src.auth.services.code import CodeService
from src.auth.utils import now_datetime, verify_password, get_password_hash
from src.db import BaseService
from src.users.exceptions import (
    user_not_found_exception, username_not_available_exception, invalid_current_password_exception,
    cannot_change_display_role_exception, user_email_is_the_same_exception,
)
from src.users.models import User
from src.users.schemas import UserOut, ChangeUsernameSchema, ChangePasswordSchema, ChangeDisplayRoleSchema


class UserService(BaseService):
    class Meta:
        model = User
        not_found_exception = user_not_found_exception

    async def get_last_online_users(self, params: Params) -> Page[UserOut]:
        filter_after = now_datetime() - timedelta(minutes=15)
        return await self.get_all(params=params, related=["display_role"], last_online__gt=filter_after)

    @staticmethod
    async def change_username(user: User, change_username_data: ChangeUsernameSchema):
        """
        Change username
        :param user:
        :param change_username_data:
        :return:
        """
        try:
            await user.update(
                username=change_username_data.username, updated_date=now_datetime()
            )
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
        if not verify_password(
                change_password_data.current_password, user.password
        ):
            raise invalid_current_password_exception
        new_password = get_password_hash(change_password_data.new_password)
        await user.update(password=new_password, updated_date=now_datetime())
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
        await user.update(
            display_role=change_display_role_data.role_id,
            updated_date=now_datetime(),
        )
        return user, old_user_display_role

    @staticmethod
    async def create_confirm_email_code(code_service: CodeService, user: User, new_email: EmailStr):
        if user.email == new_email:
            raise user_email_is_the_same_exception
        redis_data = {
            "user_id": user.id,
            "new_email": new_email,
        }
        confirm_code, _data = await code_service.create(data=json.dumps(redis_data), code_len=5, expire=900)
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
        await user.update(email=new_email, updated_date=now_datetime())
        await code_service.delete(code)
        return user

    async def upload_avatar(self, user: User, avatar: File, request: Request):
        uploads_files_path = "static/uploads/avatars"
        available_extensions = [".jpg", ".jpeg", ".png"]
        file_suffix = Path(avatar.filename).suffix
        if file_suffix not in available_extensions:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File extension is not allowed", )
        file_name = f"{uuid.uuid4()}{file_suffix}"
        full_path = Path.joinpath(Path(__file__).parent.parent.parent, uploads_files_path, file_name)
        file_content = await avatar.read()
        with open(full_path, "wb") as f:
            f.write(file_content)

        # resize image
        resized_avatar = Image.open(full_path)
        resized_avatar.thumbnail((100, 100))
        resized_avatar.save(full_path)
        default_avatar_url = request.url_for("static", path="images/default_avatar.png")
        avatar_url = request.url_for("static", path=f"uploads/avatars/{file_name}")
        old_avatar_url = user.avatar
        await user.update(avatar=str(avatar_url))
        # delete old avatar if it is not default
        if old_avatar_url != default_avatar_url:
            old_avatar_filename = old_avatar_url.split("/")[-1]
            old_avatar_path = Path.joinpath(Path(__file__).parent.parent.parent, uploads_files_path,
                                            old_avatar_filename)
            if old_avatar_path.exists():
                old_avatar_path.unlink()
        return {
            "old_avatar_url": old_avatar_url,
            "avatar_url": avatar_url,
        }
