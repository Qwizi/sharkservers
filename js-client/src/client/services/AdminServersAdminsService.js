"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.AdminServersAdminsService = void 0;
class AdminServersAdminsService {
    constructor(httpRequest) {
        this.httpRequest = httpRequest;
    }
    /**
     * Admin Get Server Admins
     * Get server admins
     * :param servers_service:
     * :param server:
     * :return:
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
     * Create server admin
     * :param servers_service:
     * :param server:
     * :return:
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
     * Get server admin
     * :param servers_service:
     * :param server:
     * :return:
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
     * Update server admin
     * :param servers_service:
     * :param server:
     * :return:
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
     * Delete server admin
     * :param servers_service:
     * :param server:
     * :return:
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
