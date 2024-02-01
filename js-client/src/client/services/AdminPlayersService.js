"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.AdminPlayersService = void 0;
class AdminPlayersService {
    constructor(httpRequest) {
        this.httpRequest = httpRequest;
    }
    /**
     * Admin Get Steam Profiles
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
