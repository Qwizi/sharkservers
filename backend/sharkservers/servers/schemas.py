"""Schemas for the servers module."""
from __future__ import annotations

from pydantic import BaseModel
from uuidbase62 import (
    UUIDBase62ModelMixin,
    con_uuidbase62,
)

from sharkservers.servers.models import Server

server_out = Server.get_pydantic()


class ServerOut(UUIDBase62ModelMixin, server_out):
    """Schema for retrieving a server."""

    id: con_uuidbase62(prefix="server")


class CreateServerSchema(BaseModel):
    """Schema for creating a server."""

    tag: str
    name: str
    ip: str
    port: int
    api_url: str


class UpdateServerSchema(BaseModel):
    """Schema for updating server information."""

    tag: str | None
    name: str | None
    ip: str | None
    port: int | None
    api_url: str | None


class ServerStatusSchema(UUIDBase62ModelMixin, BaseModel):
    """Schema for retrieving a server's status."""

    id: con_uuidbase62(prefix="server")
    name: str
    ip: str
    port: int
    players: int
    max_players: int
    map: str
    game: str
