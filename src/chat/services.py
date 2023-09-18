# chat services
from src.db import BaseService
from src.chat.models import Chat
from src.chat.exceptions import chat_not_found_exception


class ChatService(BaseService):
    class Meta:
        model = Chat
        not_found_exception = chat_not_found_exception
