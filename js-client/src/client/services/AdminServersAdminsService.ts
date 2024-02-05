/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { AdminOut } from '../models/AdminOut';
import type { CreateAdminSchema } from '../models/CreateAdminSchema';
import type { Page_AdminOut_ } from '../models/Page_AdminOut_';
import type { UpdateAdminSchema } from '../models/UpdateAdminSchema';

import type { CancelablePromise } from '../core/CancelablePromise';
import type { BaseHttpRequest } from '../core/BaseHttpRequest';

export class AdminServersAdminsService {

    constructor(public readonly httpRequest: BaseHttpRequest) {}

    /**
     * Admin Get Server Admins
     * Retrieve the list of admins for a server.
     *
     * Args:
     * ----
     * params (Params): The query parameters for filtering and pagination.
     * server (Server): The server for which to retrieve the admins.
     *
     * Returns:
     * -------
     * Page_AdminOut_: The paginated list of admins for the server.
     * @param serverId
     * @param page
     * @param size
     * @returns Page_AdminOut_ Successful Response
     * @throws ApiError
     */
    public adminGetServerAdmins(
        serverId: string,
        page: number = 1,
        size: number = 50,
    ): CancelablePromise<Page_AdminOut_> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/v1/admin/servers/{server_id}/admins',
            path: {
                'server_id': serverId,
            },
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
     * Admin Create Server Admin
     * Create a server admin.
     *
     * Args:
     * ----
     * data (CreateAdminSchema): The data for creating the admin.
     * server (Server): The server instance.
     *
     * Returns:
     * -------
     * AdminOut: The created admin.
     * @param serverId
     * @param requestBody
     * @returns AdminOut Successful Response
     * @throws ApiError
     */
    public adminCreateServerAdmin(
        serverId: string,
        requestBody: CreateAdminSchema,
    ): CancelablePromise<AdminOut> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/v1/admin/servers/{server_id}/admins',
            path: {
                'server_id': serverId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Admin Get Server Admin
     * Retrieve the admin information for a specific server.
     *
     * Args:
     * ----
     * identity (str): The identity of the admin.
     * server (Server): The server object.
     *
     * Returns:
     * -------
     * AdminOut: The admin information.
     * @param identity
     * @param serverId
     * @returns AdminOut Successful Response
     * @throws ApiError
     */
    public adminGetServerAdmin(
        identity: string,
        serverId: string,
    ): CancelablePromise<AdminOut> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/v1/admin/servers/{server_id}/admins/{identity}',
            path: {
                'identity': identity,
                'server_id': serverId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Admin Update Server Admin
     * Update the server admin with the given identity using the provided data.
     *
     * Args:
     * ----
     * identity (str): The identity of the server admin to update.
     * data (UpdateAdminSchema): The updated admin data.
     * server (Server): The server instance.
     *
     * Returns:
     * -------
     * AdminOut: The updated server admin.
     * @param identity
     * @param serverId
     * @param requestBody
     * @returns AdminOut Successful Response
     * @throws ApiError
     */
    public adminUpdateServerAdmin(
        identity: string,
        serverId: string,
        requestBody: UpdateAdminSchema,
    ): CancelablePromise<AdminOut> {
        return this.httpRequest.request({
            method: 'PUT',
            url: '/v1/admin/servers/{server_id}/admins/{identity}',
            path: {
                'identity': identity,
                'server_id': serverId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Admin Delete Server Admin
     * Delete a server admin with the given identity from the server.
     *
     * Args:
     * ----
     * identity (str): The identity of the admin to be deleted.
     * server (Server): The server from which the admin should be deleted.
     *
     * Returns:
     * -------
     * AdminOut: The deleted admin.
     * @param identity
     * @param serverId
     * @returns AdminOut Successful Response
     * @throws ApiError
     */
    public adminDeleteServerAdmin(
        identity: string,
        serverId: string,
    ): CancelablePromise<AdminOut> {
        return this.httpRequest.request({
            method: 'DELETE',
            url: '/v1/admin/servers/{server_id}/admins/{identity}',
            path: {
                'identity': identity,
                'server_id': serverId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

}
