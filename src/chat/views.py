# chat views
from fastapi import APIRouter, Depends, Security
from fastapi_events.dispatcher import dispatch
from fastapi_pagination import Page, Params
from fastapi_pagination.bases import AbstractPage

from src.auth.dependencies import get_current_active_user
from src.users.models import User

from src.chat.schemas import ChatOut, CreateChatMessageSchema, UpdateChatSchema
from src.chat.services import chat_service
from src.chat.models import Chat
from src.chat.enums import ChatEventsEnum
from src.chat.dependencies import get_valid_chat

router = APIRouter()


@router.get("", response_model_exclude_none=True)
async def get_chat_messages(params: Params = Depends()) -> Page[ChatOut]:
    """
    Get chats
    :param params:
    :return AbstractPage:
    """
    chats = await chat_service.get_all(
        params=params,
        order_by=["-created_date"],
        related=["author", "author__display_role"],
    )
    dispatch(event_name=ChatEventsEnum.GET_ALL, payload={"data": chats})
    return chats


@router.post("", response_model_exclude_none=True)
async def create_chat_message(
    chat: CreateChatMessageSchema, user: User = Security(get_current_active_user)
):
    """
    Create chat message
    :param chat:
    :param user:
    :return ChatOut:
    """
    chat = await chat_service.create(message=chat.message, author=user)
    dispatch(event_name=ChatEventsEnum.CREATE, payload={"data": chat})
    return chat
