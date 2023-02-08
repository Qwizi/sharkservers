from pydantic import BaseModel, Field

from src.servers.models import Server

ServerOut = Server.get_pydantic()


class CreateServerSchema(BaseModel):
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
