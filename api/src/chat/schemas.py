# chat schemas
from fastapi_pagination import Page
from pydantic import BaseModel, Field
from src.chat.enums import WebsocketEventEnum
from src.chat.models import Chat

ChatOut = Chat.get_pydantic(
    exclude={
        "author__password",
        "author__email",
        "author__secret_salt",
        "author__roles",
        "author__banned_user",
        "author__banned_by",
        "author__apps",
        "author__last_login",
        "author__players",
    }
)


class CreateChatMessageSchema(BaseModel):
    message: str = Field(min_length=1, max_length=500)


class UpdateChatSchema(BaseModel):
    pass


class ChatEventSchema(BaseModel):
    event: WebsocketEventEnum
    data: Page[ChatOut] | ChatOut
