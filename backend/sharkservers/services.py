"""Services module."""

import json
import os
import uuid
from pathlib import Path

import httpx
from fastapi import HTTPException, UploadFile
from fastapi_mail.email_utils import DefaultChecker
from PIL import Image, UnidentifiedImageError
from pydantic import EmailStr
from starlette import status

from sharkservers.auth.schemas import RegisterUserSchema
from sharkservers.enums import ActivationEmailTypeEnum
from sharkservers.logger import logger, logger_with_filename
from sharkservers.roles.services import RoleService
from sharkservers.scopes.services import ScopeService
from sharkservers.settings import Settings
from sharkservers.users.models import User



class EmailService:
    """Email service class."""

    def __init__(self, resend, checker: DefaultChecker) -> None:
        """Initialize EmailService class."""
        self.resend = resend
        self.checker = checker
        self.params = {
            "from": "No-Reply <no-reply@sharkservers.pl>",
        }

    async def send_confirmation_email(self, activation_type: ActivationEmailTypeEnum, email: EmailStr, code: str) -> None:
        """
        Send a confirmation email.

        Args:
        ----
            activation_type (ActivationEmailTypeEnum): The type of the activation email.
            email (EmailStr): The email address of the recipient.
            code (str): The activation code.

        Returns:
        -------
            None
        """

        if not await self.checker.check_mx_record(email.split("@")[1]):
            logger.error(f"Email {email} mx record is invalid")
            return

        try:
            subject = None
            body = None
            if activation_type == ActivationEmailTypeEnum.ACCOUNT:
                subject = "Witamy na naszej stronie!"
            elif activation_type == ActivationEmailTypeEnum.EMAIL:
                subject = "Zmiana adresu e-mail"
            elif activation_type == ActivationEmailTypeEnum.PASSWORD:
                subject = "Reset hasła"

            html = "Twój kod to: " + code + "<br><br> Pozdrawiamy, <br> Administracja SharkServers.pl"
            params = {
                "from": self.params["from"],
                "to": email,
                "subject": subject,
                "html": html,
            }
            self.resend.Emails.send(params)
            logger.info(f"Activation email sent to {email} with subject <{subject}> data <{html}'>")
        except Exception as e:
            logger.error(f"E-mail sending error: {e}")


class MainService:
    @staticmethod
    async def create_default_scopes(scopes_service):
        await scopes_service.create_default_scopes(
            applications=[
                "users",
                "roles",
                "scopes",
                "players",
                "categories",
                "tags",
                "threads",
                "posts",
                "apps",
            ],
            additional=[
                ("users", "me", "Get my profile"),
                ("users", "me:username", "Update my username"),
                ("users", "me:password", "Update my password"),
                ("users", "me:display-role", "Update my display role"),
                ("threads", "open", "Open a thread"),
                ("threads", "close", "Close a thread"),
            ],
        )

    @staticmethod
    async def install(
        file_path,
        admin_user_data: RegisterUserSchema,
        scopes_service: ScopeService,
        roles_service: RoleService,
        auth_service,
        create_file: bool = True,
        settings: Settings = None,
    ):
        logger_with_filename(
            filename=MainService.__name__,
            data="Step 0 - Install started",
        )
        if create_file:
            if os.path.exists(file_path):
                raise HTTPException(detail="Its already installed", status_code=400)
        logger_with_filename(
            filename=MainService.__name__,
            data="Step 1 - Create default scopes",
        )
        await MainService.create_default_scopes(scopes_service=scopes_service)
        logger_with_filename(
            filename=MainService.__name__,
            data="Step 2 - Create default roles",
        )
        await roles_service.create_default_roles(scopes_service=scopes_service)
        logger_with_filename(
            filename=MainService.__name__,
            data="Step 2 - Default roles created",
        )
        logger_with_filename(
            filename=MainService.__name__,
            data="Step 3 - Create admin user",
        )
        admin_user: User = await auth_service.register(
            admin_user_data,
            is_activated=True,
            is_superuser=True,
            settings=settings,
        )
        bot_password = auth_service.generate_secret_salt()
        bot_user: User = await auth_service.register(
            RegisterUserSchema(
                username="Bot",
                email="bot@sharkservers.pl",
                password=bot_password,
                password2=bot_password,
            ),
            is_activated=True,
            settings=settings,
        )
        logger_with_filename(
            filename=MainService.__name__,
            data=f"Step 3 - {admin_user.get_pydantic(exclude={'password' })} created",
        )
        if create_file:
            open(file_path, "w+")

    @staticmethod
    async def generate_openapi_file():
        url = "http://localhost:8080/openapi.json"
        async with httpx.AsyncClient() as client:
            r = await client.get(url)
            with open("openapi.json", "wb") as f:
                f.write(r.content)
            file_path = Path("./openapi.json")
            openapi_content = json.loads(file_path.read_text())

            for path_data in openapi_content["paths"].values():
                for operation in path_data.values():
                    tag = operation["tags"][0]
                    operation_id = operation["operationId"]
                    to_remove = f"{tag}-"
                    new_operation_id = operation_id[len(to_remove) :]
                    print(operation_id)
                    operation["operationId"] = new_operation_id
                    print(new_operation_id)
            file_path.write_text(json.dumps(openapi_content))


class UploadService:
    ROOT_FOLDER = "static/uploads"
    AVATAR_FOLDER = "avatars"

    def __init__(self, settings: Settings):
        self.settings = settings
        self.avatars_upload_folder = Path.joinpath(
            Path(__file__).parent.parent,
            self.ROOT_FOLDER,
            self.AVATAR_FOLDER,
        )

    def is_valid_content_type(self, file: UploadFile):
        return file.content_type in self.settings.IMAGE_ALLOWED_CONTENT_TYPES

    def is_valid_image_extension(self, file: UploadFile):
        file_suffix = Path(file.filename).suffix
        if file_suffix not in self.settings.IMAGE_ALLOWED_EXTENSIONS:
            return False
        return True

    def is_valid_avatar_size(self, file_bytes: bytes):
        return len(file_bytes) <= self.settings.AVATAR_MAX_SIZE

    def get_avatar_path(self, file_name: str) -> Path:
        return Path.joinpath(self.avatars_upload_folder, file_name)

    @staticmethod
    def create_avatar_file_name(suffix: str):
        return f"{uuid.uuid4()}{suffix}"

    @staticmethod
    def create_file(file_path: Path, file_content):
        with open(file_path, "wb") as f:
            f.write(file_content)

    def resize_image(self, file_path: Path, width: int = None, height: int = None):
        try:
            if not width:
                width = self.settings.AVATAR_WIDTH
            if not height:
                height = self.settings.AVATAR_HEIGHT
            resized_avatar = Image.open(file_path)
            resized_avatar.thumbnail((width, height))
            resized_avatar.save(file_path)
        except UnidentifiedImageError:
            if file_path.exists():
                file_path.unlink()
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="File is not an image",
            )

    async def upload_avatar(self, file: UploadFile):
        file_content = await file.read()
        if not self.is_valid_content_type(file):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="File extension is not allowed",
            )
        if not self.is_valid_avatar_size(file_content):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="File size is too big",
            )
        file_name = self.create_avatar_file_name(Path(file.filename).suffix)
        avatar_full_path = self.get_avatar_path(file_name)
        # create avatar file
        self.create_file(avatar_full_path, file_content)
        # resize avatar
        self.resize_image(avatar_full_path)
        return {
            "file_name": file_name,
            "avatar_full_path": str(avatar_full_path),
        }

    def delete_avatar(self, file_name: str):
        avatar_full_path = self.get_avatar_path(file_name)
        if avatar_full_path.exists():
            avatar_full_path.unlink()
            return True
        return False
