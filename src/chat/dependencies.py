# chat dependencies
from src.chat.models import Chat
from src.chat.services import chat_service


async def get_valid_chat(chat_id: int) -> Chat:
    """
    Get valid chat
    :param chat_id:
    :return Chat:
    """
    return await chat_service.get_one(id=chat_id)


