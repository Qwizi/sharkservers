import json
import os
import uuid
from io import BytesIO
from pathlib import Path

import httpx
from PIL import Image
from fastapi import HTTPException, UploadFile, Request
from fastapi_mail import FastMail, MessageSchema, MessageType
from fastapi_mail.email_utils import DefaultChecker
from pydantic import EmailStr
from starlette import status

from src.auth.schemas import RegisterUserSchema
from src.enums import ActivationEmailTypeEnum
from src.logger import logger, logger_with_filename
from src.settings import Settings
from src.users.models import User


class EmailService:
    mailer: FastMail
    checker: DefaultChecker

    def __init__(self, _mailer: FastMail, checker: DefaultChecker):
        self.mailer = _mailer
        self.checker = checker

    @staticmethod
    def activation_email_template(code: str):
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
    def change_email_template(code: str):
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

    async def _send_message(self, subject: str, recipients: list, body: str):
        if not await self.checker.check_mx_record(recipients[0].split("@")[1], False):
            logger.info(f"Email {recipients[0]} is invalid")
            return
        await self.mailer.send_message(message=MessageSchema(
            subject=subject,
            recipients=recipients,
            body=body,
            subtype=MessageType.html,
        ))

    async def send_confirmation_email(self, activation_type: ActivationEmailTypeEnum, email: EmailStr, code: str):
        subject = None
        body = None
        if activation_type == ActivationEmailTypeEnum.ACCOUNT:
            subject = "Twój kod aktywacyjny - Witamy na naszej stronie!"
            body = self.activation_email_template(code)
        elif activation_type == ActivationEmailTypeEnum.EMAIL:
            subject = "Twój kod weryfikacyjny - Zmiana adresu e-mail"
            body = self.change_email_template(code)
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
    ):
        logger_with_filename(filename=MainService.__name__, data="Step 0 - Install started")
        if create_file:
            if os.path.exists(file_path):
                raise HTTPException(detail="Its already installed", status_code=400)
        logger_with_filename(filename=MainService.__name__, data="Step 1 - Create default scopes")
        await MainService.create_default_scopes(scopes_service=scopes_service)
        logger_with_filename(filename=MainService.__name__, data="Step 2 - Create default roles")
        await roles_service.create_default_roles(scopes_service=scopes_service)
        logger_with_filename(filename=MainService.__name__, data="Step 2 - Default roles created")
        logger_with_filename(filename=MainService.__name__, data="Step 3 - Create admin user")
        admin_user: User = await auth_service.register(
            admin_user_data, is_activated=True, is_superuser=True
        )
        logger_with_filename(filename=MainService.__name__,
                             data=f"Step 3 - {admin_user.get_pydantic(exclude={'password', })} created")
        if create_file:
            open(file_path, "w+")

    @staticmethod
    async def generate_openapi_file():
        url = "http://localhost/openapi.json"
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
                    new_operation_id = operation_id[len(to_remove):]
                    print(operation_id)
                    operation["operationId"] = new_operation_id
                    print(new_operation_id)
            file_path.write_text(json.dumps(openapi_content))


class UploadService:
    ROOT_FOLDER = "static/uploads"
    AVATAR_FOLDER = "avatars"

    def __init__(self, settings: Settings):
        self.settings = settings
        self.avatars_upload_folder = Path.joinpath(Path(__file__).parent.parent, self.ROOT_FOLDER,
                                                   self.AVATAR_FOLDER)

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
        if not width:
            width = self.settings.AVATAR_WIDTH
        if not height:
            height = self.settings.AVATAR_HEIGHT
        resized_avatar = Image.open(file_path)
        resized_avatar.thumbnail((width, height))
        resized_avatar.save(file_path)

    async def upload_avatar(self, file: UploadFile):
        file_content = await file.read()
        if not self.is_valid_image_extension(file):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File extension is not allowed")
        if not self.is_valid_avatar_size(file_content):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File size is too big")
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
