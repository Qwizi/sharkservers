"""Services module."""

import json
import os
import uuid
from pathlib import Path
from typing import TYPE_CHECKING

import httpx
from fastapi import HTTPException, UploadFile
from fastapi_mail import FastMail, MessageSchema, MessageType
from fastapi_mail.email_utils import DefaultChecker
from PIL import Image, UnidentifiedImageError
from pydantic import EmailStr
from starlette import status

from sharkservers.auth.schemas import RegisterUserSchema
from sharkservers.enums import ActivationEmailTypeEnum
from sharkservers.logger import logger, logger_with_filename
from sharkservers.settings import Settings
from sharkservers.users.models import User


class EmailService:
    """
    Email service class.

    Attributes
    ----------
        mailer: FastMail instance.
        checker: DefaultChecker instance.

    Methods
    -------
        activation_email_template: Returns an activation email template.
        change_email_template: Returns a change email template.
        password_reset_email_template: Returns a password reset email template.
        _send_message: Sends an email message.
        send_confirmation_email: Sends a confirmation email.
    """

    mailer: FastMail
    checker: DefaultChecker

    def __init__(self, _mailer: FastMail, checker: DefaultChecker) -> None:
        """Initialize EmailService class."""
        self.mailer = _mailer
        self.checker = checker

    @staticmethod
    def activation_email_template(code: str) -> str:
        """
        Return an activation email template.

        Args:
        ----
            code (str): Activation code.

        Returns:
        -------
            str: Activation email template.
        """
        return f"""
        Drogi(a) Użytkowniku, <br>

Dziękujemy za dołączenie do naszej społeczności! Jesteśmy podekscytowani, że jesteś z nami.<br>

Aby dokończyć proces rejestracji i aktywować swoje konto, proszę skorzystać z poniższego kodu aktywacyjnego: <br>

Kod aktywacyjny: {code} <br>

Pamiętaj, że kod aktywacyjny może wygasnąć po pewnym czasie, więc zalecamy, abyś aktywował/a swoje konto jak najszybciej. <br>

Pozdrawiamy, <br>
Administracja SharkServers.pl
        """

    @staticmethod
    def change_email_template(code: str) -> str:
        """
        Return a change email template.

        Args:
        ----
            code (str): Verification code.

        Returns:
        -------
            str: Change email template.
        """
        return f"""
Drogi(a) Użytkowniku,<br>

Otrzymujesz tę wiadomość, ponieważ zażądałeś/aś zmiany adresu e-mail powiązanego z Twoim kontem na SharkServers.pl.<br>

Proszę skorzystać z poniższego kodu weryfikacyjnego, aby potwierdzić tę zmianę:<br>

Kod weryfikacyjny: {code}<br>

Prosimy o wprowadzenie powyższego kodu w odpowiednie pole na naszej stronie w celu potwierdzenia zmiany adresu e-mail. Jeśli nie żądałeś/aś tej zmiany, prosimy o natychmiastowy kontakt z naszym zespołem wsparcia pod adresem [Adres e-mail zespołu wsparcia] lub za pośrednictwem formularza kontaktowego na naszej stronie.<br>

Pamiętaj, że ten kod weryfikacyjny wygaśnie po pewnym czasie w celu zabezpieczenia Twojego konta. Prosimy o jego użycie jak najszybciej.<br>

Jeśli potrzebujesz pomocy lub masz pytania, zawsze możesz skontaktować się z naszym zespołem obsługi klienta.<br>

Z poważaniem,<br>
Administracja SharkServers.pl

        """

    @staticmethod
    def password_reset_email_template(code: str) -> str:
        """
        Password reset email template.

        Args:
        ----
            code (str): Verification code.

        Returns:
        -------
            str: Password reset email template.
        """
        return f"""
        Drogi(a) Użytkowniku,<br><br>

Otrzymujesz tę wiadomość, ponieważ zażądałeś/aś zresetowania hasła powiązanego z Twoim kontem na SharkServers.pl.<br><br>

Proszę skorzystać z poniższego kodu weryfikacyjnego, aby zresetować hasło:<br><br>

Kod weryfikacyjny: {code}<br><br>

Proszę wprowadzić powyższy kod w odpowiednie pole na naszej stronie w celu zresetowania hasła. Jeśli to nie Ty zażądałeś/aś resetowania hasła, zignoruj tę wiadomość.<br><br>

Kod weryfikacyjny wygasa po ograniczonym czasie w celu zabezpieczenia Twojego konta. Proszę o użycie go jak najszybciej.<br><br>

Jeśli potrzebujesz pomocy lub masz pytania, zawsze możesz skontaktować się z naszym zespołem obsługi klienta.<br><br>

Z poważaniem,<br>
Administracja SharkServers.pl
        """

    async def _send_message(self, subject: str, recipients: list, body: str) -> None:
        """
        Sends an email message to the specified recipients.

        Args:
        ----
            subject (str): The subject of the email.
            recipients (list): A list of email addresses of the recipients.
            body (str): The body of the email.

        Returns:
        -------
            None
        """  # noqa: D401
        if not await self.checker.check_mx_record(recipients[0].split("@")[1]):
            logger.info(f"Email {recipients[0]} is invalid")
            return
        await self.mailer.send_message(
            message=MessageSchema(
                subject=subject,
                recipients=recipients,
                body=body,
                subtype=MessageType.html,
            ),
        )

    async def send_confirmation_email(
        self,
        activation_type: ActivationEmailTypeEnum,
        email: EmailStr,
        code: str,
    ) -> None:
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
        subject = None
        body = None
        if activation_type == ActivationEmailTypeEnum.ACCOUNT:
            subject = "Twój kod aktywacyjny - Witamy na naszej stronie!"
            body = self.activation_email_template(code)
        elif activation_type == ActivationEmailTypeEnum.EMAIL:
            subject = "Twój kod weryfikacyjny - Zmiana adresu e-mail"
            body = self.change_email_template(code)
        elif activation_type == ActivationEmailTypeEnum.PASSWORD:
            subject = "Twój kod weryfikacyjny - Reset hasła"
            body = self.password_reset_email_template(code)
        await self._send_message(subject, [email], body)
        logger.info(f"Activation email sent to {email} with code {code}")


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
        scopes_service,
        roles_service,
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