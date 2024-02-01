"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.AdminPlayersService = void 0;
class AdminPlayersService {
    constructor(httpRequest) {
        this.httpRequest = httpRequest;
    }
    /**
     * Admin Get Steam Profiles
     * Retrieve all player profiles with their associated SteamRep profiles.
     *
     * Args:
     * ----
     * params (Params): The parameters for filtering and pagination.
     * players_service (PlayerService): The service for retrieving player profiles.
     *
     * Returns:
     * -------
     * Page[PlayerOut]: A paginated list of player profiles with their associated SteamRep profiles.
     * @param page
     * @param size
     * @returns Page_PlayerOut_ Successful Response
     * @throws ApiError
     */
    adminGetSteamProfiles(page = 1, size = 50) {
        return this.httpRequest.request({
            method: 'GET',
            url: '/v1/admin/players',
            query: {
                'page': page,
                'size': size,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Admin Create Player
     * Admin endpoint to create a player.
     *
     * Args:
     * ----
     * profile_data (CreatePlayerSchema): The data for creating a player.
     * background_tasks (BackgroundTasks): The background tasks object.
     * players_service (PlayerService, optional): The player service dependency. Defaults to Depends(get_players_service).
     *
     * Returns:
     * -------
     * dict: A dictionary with a message indicating that the player was created.
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    adminCreatePlayer(requestBody) {
        return this.httpRequest.request({
            method: 'POST',
            url: '/v1/admin/players',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Admin Get Steam Profile
     * Retrieve the Steam profile of a player with the given profile ID.
     *
     * Args:
     * ----
     * profile_id (int): The ID of the player's Steam profile.
     *
     * Returns:
     * -------
     * PlayerOut: The player's Steam profile.
     *
     * Raises:
     * ------
     * player_not_found_exception: If the player's profile is not found.
     * @param profileId
     * @returns PlayerOut Successful Response
     * @throws ApiError
     */
    adminGetSteamProfile(profileId) {
        return this.httpRequest.request({
            method: 'GET',
            url: '/v1/admin/players/{profile_id}',
            path: {
                'profile_id': profileId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Admin Delete Steam Profile
     * Delete a Steam profile with the given profile ID.
     *
     * Args:
     * ----
     * profile_id (int): The ID of the profile to delete.
     *
     * Returns:
     * -------
     * PlayerOut: The deleted player profile.
     *
     * Raises:
     * ------
     * player_not_found_exception: If the player profile with the given ID is not found.
     * @param profileId
     * @returns PlayerOut Successful Response
     * @throws ApiError
     */
    adminDeleteSteamProfile(profileId) {
        return this.httpRequest.request({
            method: 'DELETE',
            url: '/v1/admin/players/{profile_id}',
            path: {
                'profile_id': profileId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
exports.AdminPlayersService = AdminPlayersService;
