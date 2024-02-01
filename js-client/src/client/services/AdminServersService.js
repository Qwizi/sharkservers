"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.AdminServersService = void 0;
class AdminServersService {
    constructor(httpRequest) {
        this.httpRequest = httpRequest;
    }
    /**
     * Admin Get Servers
     * Retrieve all servers with their associated admin role.
     *
     * Args:
     * ----
     * servers_service (ServerService): The server service instance.
     *
     * Returns:
     * -------
     * ServerOut: The server data with the associated admin role.
     * @returns ServerOut Successful Response
     * @throws ApiError
     */
    adminGetServers() {
        return this.httpRequest.request({
            method: 'GET',
            url: '/v1/admin/servers',
        });
    }
    /**
     * Admin Create Server
     * Create a new server using the provided server data.
     *
     * Args:
     * ----
     * server_data (CreateServerSchema): The data for creating the server.
     * servers_service (ServerService): The server service instance.
     *
     * Returns:
     * -------
     * ServerOut: The created server.
     * @param requestBody
     * @returns ServerOut Successful Response
     * @throws ApiError
     */
    adminCreateServer(requestBody) {
        return this.httpRequest.request({
            method: 'POST',
            url: '/v1/admin/servers',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Admin Get Server
     * Retrieve the details of a server for admin purposes.
     *
     * Args:
     * ----
     * server (Server): The server object to retrieve details for.
     *
     * Returns:
     * -------
     * ServerOut: The server details.
     * @param serverId
     * @returns ServerOut Successful Response
     * @throws ApiError
     */
    adminGetServer(serverId) {
        return this.httpRequest.request({
            method: 'GET',
            url: '/v1/admin/servers/{server_id}',
            path: {
                'server_id': serverId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Admin Update Server
     * Update the server with the provided data.
     *
     * Args:
     * ----
     * server_data (UpdateServerSchema): The data to update the server with.
     * server (Server): The server to be updated.
     *
     * Returns:
     * -------
     * ServerOut: The updated server.
     * @param serverId
     * @param requestBody
     * @returns ServerOut Successful Response
     * @throws ApiError
     */
    adminUpdateServer(serverId, requestBody) {
        return this.httpRequest.request({
            method: 'PUT',
            url: '/v1/admin/servers/{server_id}',
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
     * Admin Delete Server
     * Delete the specified server.
     *
     * Args:
     * ----
     * server (Server): The server to be deleted.
     * servers_service (ServerService): The server service instance.
     *
     * Returns:
     * -------
     * bool: True if the server is successfully deleted, False otherwise.
     * @param serverId
     * @returns boolean Successful Response
     * @throws ApiError
     */
    adminDeleteServer(serverId) {
        return this.httpRequest.request({
            method: 'DELETE',
            url: '/v1/admin/servers/{server_id}',
            path: {
                'server_id': serverId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
exports.AdminServersService = AdminServersService;
