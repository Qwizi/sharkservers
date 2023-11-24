from fastapi_events.dispatcher import dispatch
from fastapi_events.handlers.local import local_handler
from fastapi_events.typing import Event

from src.players.enums import PlayerEventEnum
from src.players.services import player_service


@local_handler.register(event_name=PlayerEventEnum.CREATE)
async def create_player(event: Event):
    event_name, payload = event
    steamid64 = payload.get("steamid64")
    player = await player_service.create_player(steamid64=steamid64)
    dispatch(event_name=PlayerEventEnum.CREATED, payload={"player": player})
