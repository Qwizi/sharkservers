from fastapi import WebSocket
from fastapi.encoders import jsonable_encoder

from src.chat.schemas import ChatEventSchema


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, chat_schema: ChatEventSchema, websocket: WebSocket):
        await websocket.send_json(jsonable_encoder(chat_schema))

    async def broadcast(self, chat_schema: ChatEventSchema):
        for connection in self.active_connections:
            await connection.send_json(jsonable_encoder(chat_schema))


manager = ConnectionManager()