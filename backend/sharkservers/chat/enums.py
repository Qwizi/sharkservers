# chat enums
from enum import Enum


class ChatExceptionEnum(str, Enum):
    NOT_FOUND = "Chat not found"


class ChatEventsEnum(str, Enum):
    """RChat events enum."""

    GET_ALL = "CHAT_GET_ALL"
    GET_ONE = "CHAT_GET_ONE"
    CREATE = "CHAT_CREATE"
    UPDATE = "CHAT_UPDATE"
    DELETE = "CHAT_DELETE"
    ADMIN_GET_ALL = "CHAT_ADMIN_GET_ALL"
    ADMIN_GET_ONE = "CHAT_ADMIN_GET_ONE"
    ADMIN_CREATE = "CHAT_ADMIN_CREATE"
    ADMIN_UPDATE = "CHAT_ADMIN_UPDATE"
    ADMIN_DELETE = "CHAT_ADMIN_DELETE"


class WebsocketEventEnum(str, Enum):
    GET_MESSAGES = "get_messages"
    GET_MESSAGE = "get_message"
    SEND_MESSAGE = "send_message"
