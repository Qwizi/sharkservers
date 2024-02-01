/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CreatePlayerSchema } from '../models/CreatePlayerSchema';
import type { Page_PlayerOut_ } from '../models/Page_PlayerOut_';
import type { PlayerOut } from '../models/PlayerOut';

import type { CancelablePromise } from '../core/CancelablePromise';
import type { BaseHttpRequest } from '../core/BaseHttpRequest';

export class AdminPlayersService {

    constructor(public readonly httpRequest: BaseHttpRequest) {}

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
    public adminGetSteamProfiles(
        page: number = 1,
        size: number = 50,
    ): CancelablePromise<Page_PlayerOut_> {
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
    public adminCreatePlayer(
        requestBody: CreatePlayerSchema,
    ): CancelablePromise<Record<string, any>> {
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
    public adminGetSteamProfile(
        profileId: number,
    ): CancelablePromise<PlayerOut> {
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
    public adminDeleteSteamProfile(
        profileId: number,
    ): CancelablePromise<PlayerOut> {
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
