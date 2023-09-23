# chat dependencies
from fastapi import Depends, WebSocketException, status
from src.chat.bot import Bot
from src.forum.dependencies import get_posts_service, get_threads_service
from src.forum.services import PostService, ThreadService
from src.auth.dependencies import get_access_token_service
from src.auth.services.jwt import JWTService
from src.chat.services import ChatService
from src.users.dependencies import get_users_service
from src.users.services import UserService


async def get_chat_service():
    return ChatService()


async def ws_get_current_user(
    token: str = None,
    access_token_service: JWTService = Depends(get_access_token_service),
    users_service: UserService = Depends(get_users_service),
):
    if not token:
        return None
    token_data = access_token_service.decode_token(token)
    user = await users_service.get_one(
        id=token_data.user_id,
        related=["roles", "display_role", "roles__scopes", "players"],
    )
    if user.secret_salt != token_data.secret:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    return user


async def get_bot(
    users_service: UserService = Depends(get_users_service),
    threads_service: ThreadService = Depends(get_threads_service),
    posts_service: PostService = Depends(get_posts_service),
    chat_service: ChatService = Depends(get_chat_service)
):
    bot = Bot(
        user_id=2,
        users_service=users_service,
        threads_service=threads_service,
        posts_service=posts_service,
        chat_service=chat_service
    )
    await bot.init_bot_user()
    return bot
