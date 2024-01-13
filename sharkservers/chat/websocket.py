import json

from fastapi.encoders import jsonable_encoder
from fastapi_pagination import Params
from sharkservers.chat.enums import WebsocketEventEnum
from sharkservers.chat.schemas import ChatEventSchema
from sharkservers.chat.services import ChatService
from sharkservers.logger import logger
from sharkservers.users.models import User
from sharkservers.utils import broadcast
from starlette.websockets import WebSocket


async def chatroom_ws_receiver(
    websocket,
    chat_service: ChatService,
    author: User | None = None,
):
    async for message in websocket.iter_json():
        message_event = message.get("event", None)
        message_data = message.get("data", None)
        if message_event == WebsocketEventEnum.SEND_MESSAGE:
            if message_data is None:
                return

            new_message = await chat_service.create(author=author, message=message_data)
            logger.info(new_message)
            new_message_schema = ChatEventSchema(
                event=WebsocketEventEnum.GET_MESSAGE,
                data=new_message,
            )
            messages = await chat_service.get_all(
                params=Params(size=10),
                related=[
                    "author",
                    "author__display_role",
                    "author__player",
                    "author__player__steamrep_profile",
                ],
                order_by="-id",
            )
            messages_schema = ChatEventSchema(
                event=WebsocketEventEnum.GET_MESSAGES,
                data=messages,
            )
            # await websocket.send_json(jsonable_encoder(messages_schema))
            await broadcast.publish(
                channel="chat",
                message=json.dumps(jsonable_encoder(messages_schema)),
            )

        await broadcast.publish(channel="chat", message=json.dumps(message))


async def chatroom_ws_sender(
    websocket: WebSocket,
    chat_service: ChatService,
    author: User = None,
):
    async with broadcast.subscribe(channel="chat") as subscriber:
        async for event in subscriber:
            message = json.loads(event.message)
            message_event = message.get("event", None)
            message_data = message.get("data", None)
            logger.info(message_event)
            if message_event == WebsocketEventEnum.GET_MESSAGES:
                messages = await chat_service.get_all(
                    params=Params(size=10),
                    related=[
                        "author",
                        "author__display_role",
                        "author__player",
                        "author__player__steamrep_profile",
                    ],
                    order_by="-id",
                )
                messages_schema = ChatEventSchema(
                    event=WebsocketEventEnum.GET_MESSAGES,
                    data=messages,
                )
                await websocket.send_json(jsonable_encoder(messages_schema))
