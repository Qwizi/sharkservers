import json

from broadcaster import Broadcast
from fastapi.encoders import jsonable_encoder
from fastapi_pagination import Params

from sharkservers.chat.enums import WebsocketEventEnum
from sharkservers.chat.schemas import ChatEventSchema
from sharkservers.chat.services import ChatService
from sharkservers.forum.services import PostService, ThreadService
from sharkservers.users.services import UserService


class Bot:
    broadcast: None | Broadcast

    def __init__(
        self,
        users_service: UserService,
        threads_service: ThreadService,
        posts_service: PostService,
        chat_service: ChatService,
        user_id: int = 2,
    ):
        self.user_id = user_id
        self.users_service = users_service
        self.threads_service = threads_service
        self.post_service = posts_service
        self.chat_service = chat_service
        self.bot_user = None

    async def init_bot_user(self):
        self.bot_user = await self.users_service.get_one(
            id=self.user_id,
            related=["display_role"],
        )

    def set_broadcast(self, broadcast: Broadcast):
        self.broadcast = broadcast

    async def send_message(self, message: str):
        new_message = await self.chat_service.create(
            author=self.bot_user,
            message=message,
        )
        new_message_schema = ChatEventSchema(
            event=WebsocketEventEnum.GET_MESSAGE,
            data=new_message,
        )
        messages = await self.chat_service.get_all(
            params=Params(size=10),
            related=["author", "author__display_role"],
            order_by="-id",
        )
        messages_schema = ChatEventSchema(
            event=WebsocketEventEnum.GET_MESSAGES,
            data=messages,
        )
        # await websocket.send_json(jsonable_encoder(messages_schema))
        await self.broadcast.publish(
            channel="chat",
            message=json.dumps(jsonable_encoder(messages_schema)),
        )
