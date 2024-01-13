"""
Steam auth service.

Steam auth service is a service that allows you to authenticate a user using Steam OpenID.

Classes:
--------
    SteamAuthService: Service class for authenticating users using Steam OpenID.

"""  # noqa: EXE002, E501

import httpx
from fastapi import HTTPException

from sharkservers.auth.schemas import SteamAuthSchema
from sharkservers.players.models import Player
from sharkservers.players.services import PlayerService
from sharkservers.users.models import User
from sharkservers.users.services import UserService


class SteamAuthService:
    """
    Service class for handling Steam authentication.

    Attributes
    ----------
        users_service (UserService): The user service.
        players_service (PlayerService): The player service.
        auth_url (str): The Steam authentication URL.

    Methods
    -------
        get_steamid_from_url: Get the Steam ID from a Steam profile URL.
        format_params: Format the Steam authentication parameters into a dict.
        is_valid_params: Check if the provided Steam authentication parameters are valid.
        authenticate: Authenticate a user using Steam authentication.
    """  # noqa: E501

    def __init__(
        self,
        users_service: UserService,
        players_service: PlayerService,
    ) -> None:
        """Initialize the SteamAuthService."""
        self.users_service = users_service
        self.players_service = players_service
        self.auth_url = "https://steamcommunity.com/openid/login"

    @staticmethod
    def get_steamid_from_url(url: str) -> str:
        """
        Extracts the SteamID from a given Steam profile URL.

        Args:
        ----
            url (str): The Steam profile URL.

        Returns:
        -------
            str: The extracted SteamID.
        """  # noqa: D401
        return url.split("/")[-1]

    def format_params(self, params: SteamAuthSchema) -> dict:
        """
        Format the Steam authentication parameters into a dict.

        Args:
        ----
            params (SteamAuthSchema): The Steam authentication parameters.

        Returns:
        -------
            dict: The formatted parameters.
        """
        params_dict = {}
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
        """
        Check if the provided Steam authentication parameters are valid.

        Args:
        ----
            params (SteamAuthSchema): The Steam authentication parameters.

        Returns:
        -------
            bool: True if the parameters are valid, False otherwise.
        """
        params_copy = params.copy()
        params_copy.openid_mode = "check_authentication"
        formatted_params = self.format_params(params_copy)
        async with httpx.AsyncClient() as client:
            response = await client.post(url=self.auth_url, data=formatted_params)
            return "is_valid:true" in response.text

    async def authenticate(self, user: User, params: SteamAuthSchema) -> Player:
        """
        Authenticate a user using Steam authentication.

        Args:
        ----
            user (User): The user to authenticate.
            params (SteamAuthSchema): The Steam authentication parameters.

        Returns:
        -------
            Player: The authenticated player.

        Raises:
        ------
            HTTPException: If the Steam profile cannot be authenticated or if the user is already connected to a profile.
        """  # noqa: E501
        if not await self.is_valid_params(params):
            raise HTTPException(400, "Cannot authenticate steam profile")
        steamid64 = self.get_steamid_from_url(params.openid_claimed_id)

        # check if player exists
        player_exists = await self.players_service.Meta.model.objects.filter(
            steamid64=steamid64,
        ).exists()

        # if player exist check if user and player are connected
        if player_exists:
            if user.player:
                raise HTTPException(400, "User have already connected profile")

            player = await self.players_service.Meta.model.objects.get(
                steamid64=steamid64,
            )
            await user.update(player=user)
            return player

        new_player = await self.players_service.create_player(steamid64=steamid64)
        await user.update(player=new_player)
        return new_player
