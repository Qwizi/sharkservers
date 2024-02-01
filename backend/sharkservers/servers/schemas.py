"""Schemas for the servers module."""
from __future__ import annotations

from pydantic import BaseModel

from sharkservers.servers.models import Server

server_out = Server.get_pydantic()


class ServerOut(server_out):
    """Schema for retrieving a server."""


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


class ServerStatusSchema(BaseModel):
    """Schema for retrieving a server's status."""

    id: int
    name: str
    ip: str
    port: int
    players: int
    max_players: int
    map: str
    game: str
