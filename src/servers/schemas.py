from pydantic import BaseModel

from src.servers.models import Server

ServerOut = Server.get_pydantic()


class CreateServerSchema(BaseModel):
    name: str
    ip: str
    port: int
