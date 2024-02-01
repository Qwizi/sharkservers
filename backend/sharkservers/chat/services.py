# chat services
from sharkservers.chat.exceptions import chat_not_found_exception
from sharkservers.chat.models import Chat
from sharkservers.db import BaseService


class ChatService(BaseService):
    class Meta:
        model = Chat
        not_found_exception = chat_not_found_exception
