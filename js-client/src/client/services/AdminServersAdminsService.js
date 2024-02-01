"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.AdminServersAdminsService = void 0;
class AdminServersAdminsService {
    constructor(httpRequest) {
        this.httpRequest = httpRequest;
    }
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
    adminGetServerAdmins(serverId, page = 1, size = 50) {
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
    adminCreateServerAdmin(serverId, requestBody) {
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
    adminGetServerAdmin(identity, serverId) {
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
    adminUpdateServerAdmin(identity, serverId, requestBody) {
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
    adminDeleteServerAdmin(identity, serverId) {
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
exports.AdminServersAdminsService = AdminServersAdminsService;
