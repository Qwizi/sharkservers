"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.PlayersService = void 0;
class PlayersService {
    constructor(httpRequest) {
        this.httpRequest = httpRequest;
    }
    /**
     * Get Players
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
     * Create player
     * :param app:
     * :param player_data:
     * :param players_service:
     * :return:
     * @param requestBody
     * @returns any Successful Response
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
     * @param steamid64
     * @returns any Successful Response
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
