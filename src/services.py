import json
import os
from pathlib import Path

import httpx
from fastapi import HTTPException
from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
from pydantic import EmailStr

from src.logger import logger
from src.auth.schemas import RegisterUserSchema
from src.settings import get_settings


class EmailService:
    mailer: FastMail

    def __init__(self, _mailer: FastMail):
        self.mailer = _mailer

    @staticmethod
    def activation_email_template(code: str):
        return f"""
        Witaj twój kod aktywacyjny to: {code}
        """

    async def send_activation_email(self, email: EmailStr, code: str):
        await self.mailer.send_message(
            message=MessageSchema(
                subject="Aktywacja konta",
                recipients=[email],
                body=self.activation_email_template(code),
                subtype=MessageType.html,
            )
        )


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
        logger.info("Step 0 - Install started")
        if create_file:
            if os.path.exists(file_path):
                raise HTTPException(detail="Its already installed", status_code=400)
        logger.info("Step 1 - Create default scopes")
        await MainService.create_default_scopes(scopes_service=scopes_service)
        logger.info("Step 2 - Create default roles")
        await roles_service.create_default_roles(scopes_service=scopes_service)
        logger.info("Step 3 - Create admin user")
        await auth_service.register(
            admin_user_data, is_activated=True, is_superuser=True
        )
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
                    new_operation_id = operation_id[len(to_remove) :]
                    print(operation_id)
                    operation["operationId"] = new_operation_id
                    print(new_operation_id)
            file_path.write_text(json.dumps(openapi_content))


settings = get_settings()

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
    USE_CREDENTIALS=settings.USE_CREDENTIALS,
    VALIDATE_CERTS=settings.VALIDATE_CERTS,
)

mailer = FastMail(conf)
email_service = EmailService(_mailer=mailer)
