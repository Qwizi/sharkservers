from fastapi import HTTPException
import httpx
from src.auth.schemas import SteamAuthSchema
from src.players.services import PlayerService
from src.users.services import UserService
from src.users.models import User


class SteamAuthService:
    def __init__(self, users_service: UserService, players_service: PlayerService):
        self.users_service = users_service
        self.players_service = players_service
        self.auth_url = "https://steamcommunity.com/openid/login"

    @staticmethod
    def get_steamid_from_url(url: str):
        return url.split("/")[-1]

    def format_params(self, params: SteamAuthSchema) -> dict:
        params_dict = {}
        #   'openid.ns': 'http://specs.openid.net/auth/2.0',
        #   'openid.mode': 'id_res',
        #   'openid.op_endpoint': 'https://steamcommunity.com/openid/login',
        #   'openid.claimed_id': 'https://steamcommunity.com/openid/id/76561198190469450',
        #   'openid.identity': 'https://steamcommunity.com/openid/id/76561198190469450',
        #   'openid.return_to': 'http://localhost:3000/settings/connected-accounts/steam/callback',
        #   'openid.response_nonce': '2023-09-29T09:28:05ZJJioTudsxVptILcRlbMrwrdreKk=',
        #   'openid.assoc_handle': '1234567890',
        #   'openid.signed': 'signed,op_endpoint,claimed_id,identity,return_to,response_nonce,assoc_handle',
        #   'openid.sig': 'VfzZNeWuJpFKdbXyRQytNS+anvE='
        params_dict["openid.ns"] = params.openid_ns
        params_dict["openid.mode"] = params.openid_mode
        params_dict["openid.op_endpoint"] = params.openid_op_endpoint
        params_dict["openid.claimed_id"] = params.openid_claimed_id
        params_dict["openid.identity"] = params.openid_identity
        params_dict["openid.return_to"] = params.openid_return_to
        params_dict["openid.response_nonce"] = params.openid_response_nonce
        params_dict["openid.assoc_handle"] = params.openid_assoc_handle
        params_dict["openid.signed"] = params.openid_signed
        params_dict["openid.sig"] = params.openid_sig
        return params_dict

    async def is_valid_params(self, params: SteamAuthSchema) -> bool:
        params_copy = params.copy()
        params_copy.openid_mode = "check_authentication"
        formatted_params = self.format_params(params_copy)
        async with httpx.AsyncClient() as client:
            response = await client.post(url=self.auth_url, data=formatted_params)
            return "is_valid:true" in response.text

    async def authenticate(self, user: User, params: SteamAuthSchema):
        if not await self.is_valid_params(params):
            raise HTTPException(400, "Cannot authenticate steam profile")
        steamid64 = self.get_steamid_from_url(params.openid_claimed_id)

        # check if player exists
        player_exists = await self.players_service.Meta.model.objects.filter(
            steamid64=steamid64
        ).exists()

        # if player exist check if user and player are connected
        if player_exists:
            if not user.player:
                player = await self.players_service.Meta.model.objects.get(
                    steamid64=steamid64
                )
                await user.update(player=user)
                return player
            else:
                raise HTTPException(400, "User have already connected profile")
        new_player = await self.players_service.create_player(
            steamid64=steamid64
        )
        await user.update(player=new_player)
        return new_player
