"""Module contains the ConnectionManager class, which manages WebSocket connections and provides methods for sending messages."""  # noqa: E501
from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi.encoders import jsonable_encoder

if TYPE_CHECKING:
    from fastapi import WebSocket

    from sharkservers.chat.schemas import ChatEventSchema


class ConnectionManager:
    """Manages WebSocket connections and provides methods for sending messages."""

    def __init__(self) -> None:
        """Initialize the ConnectionManager class."""
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket) -> None:
        """
        Accepts a WebSocket connection and adds it to the list of active connections.

        Args:
        ----
            websocket (WebSocket): The WebSocket connection to be added.

        """  # noqa: D401
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        """
        Removes a WebSocket connection from the list of active connections.

        Args:
        ----
            websocket (WebSocket): The WebSocket connection to be removed.

        Returns:
        -------
            None
        """  # noqa: D401
        self.active_connections.remove(websocket)

    async def send_personal_message(
        self,
        chat_schema: ChatEventSchema,
        websocket: WebSocket,
    ) -> None:
        """
        Send a personal message to a specific WebSocket connection.

        Args:
        ----
            chat_schema (ChatEventSchema): The chat event schema to be sent.
            websocket (WebSocket): The WebSocket connection to send the message to.

        Returns:
        -------
            None
        """
        await websocket.send_json(jsonable_encoder(chat_schema))

    async def broadcast(self, chat_schema: ChatEventSchema) -> None:
        """
        Send a message to all active WebSocket connections.

        Args:
        ----
            chat_schema (ChatEventSchema): The chat event schema to be sent.

        Returns:
        -------
            None
        """
        for connection in self.active_connections:
            await connection.send_json(jsonable_encoder(chat_schema))


manager = ConnectionManager()
