"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.PlayersService = void 0;
class PlayersService {
    constructor(httpRequest) {
        this.httpRequest = httpRequest;
    }
    /**
     * Get Players
     * Retrieve a list of players based on the provided parameters.
     *
     * Args:
     * ----
     * params (Params): The parameters for filtering and pagination.
     * players_service (PlayerService): The service for retrieving player data.
     *
     * Returns:
     * -------
     * Page[PlayerOut]: A paginated list of player data.
     * @param page
     * @param size
     * @returns Page_PlayerOut_ Successful Response
     * @throws ApiError
     */
    getPlayers(page = 1, size = 50) {
        return this.httpRequest.request({
            method: 'GET',
            url: '/v1/players',
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
     * Create Player
     * Create a new player.
     *
     * Args:
     * ----
     * player_data (CreatePlayerSchema): The data for creating a player.
     * players_service (PlayerService): The service for managing players.
     *
     * Returns:
     * -------
     * PlayerOut: The created player.
     * @param requestBody
     * @returns PlayerOut Successful Response
     * @throws ApiError
     */
    createPlayer(requestBody) {
        return this.httpRequest.request({
            method: 'POST',
            url: '/v1/players',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Player
     * Retrieve a player by their Steam ID.
     *
     * Args:
     * ----
     * player (Player): The player object obtained from the `get_valid_player_by_steamid` dependency.
     *
     * Returns:
     * -------
     * Player: The retrieved player object.
     * @param steamid64
     * @returns PlayerOut Successful Response
     * @throws ApiError
     */
    getPlayer(steamid64) {
        return this.httpRequest.request({
            method: 'GET',
            url: '/v1/players/{steamid64}',
            path: {
                'steamid64': steamid64,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
exports.PlayersService = PlayersService;
