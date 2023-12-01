from typing import Optional

from pydantic import BaseModel, Field
from pydantic.color import Color

from src.servers.models import Server

serverOut = Server.get_pydantic()


class ServerOut(serverOut):
    pass


class CreateServerSchema(BaseModel):
    tag: str
    name: str
    ip: str
    port: int = Field(gt=0, lt=65536)


class ServerStatusSchema(BaseModel):
    id: int
    name: str
    ip: str
    port: int
    players: int
    max_players: int
    map: str
    game: str


class CreatePlayerChatColorSchema(BaseModel):
    steamid64: Optional[str] = Field(max_length=17)
    tag: str = Field(min_length=3, max_length=32)
    flag: Optional[str] = Field(max_length=1)
    tag_color: Color
    name_color: Color
    text_color: Color


class UpdatePlayerChatColorSchema(BaseModel):
    steamid64: Optional[str] = Field(max_length=17)
    tag: Optional[str] = Field(min_length=3, max_length=32)
    flag: Optional[str] = Field(max_length=1)
    tag_color: Optional[Color]
    name_color: Optional[Color]
    text_color: Optional[Color]
