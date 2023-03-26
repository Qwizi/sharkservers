# chat schemas
from pydantic import BaseModel, Field
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
    }
)


class CreateChatMessageSchema(BaseModel):
    message: str = Field(min_length=1, max_length=500)


class UpdateChatSchema(BaseModel):
    pass
