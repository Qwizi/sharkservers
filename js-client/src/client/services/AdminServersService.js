"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.AdminServersService = void 0;
class AdminServersService {
    constructor(httpRequest) {
        this.httpRequest = httpRequest;
    }
    /**
     * Admin Get Servers
     * Get all servers
     * :return:
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
     * Create a new server
     * :param servers_service:
     * :param server_data:
     * :return:
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
     * Get server by id
     * :param servers_service:
     * :param server:
     * :return:
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
     * Update a server
     * :param servers_service:
     * :param server:
     * :param server_data:
     * :return:
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
     * Delete a server
     * :param servers_service:
     * :param server:
     * :return:
     * @param serverId
     * @returns any Successful Response
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
