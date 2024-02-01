"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.AdminServersAdminGroupsService = void 0;
class AdminServersAdminGroupsService {
    constructor(httpRequest) {
        this.httpRequest = httpRequest;
    }
    /**
     * Admin Get Server Admins Groups
     * Get server admins groups
     * :param servers_service:
     * :param server:
     * :return:
     * @param serverId
     * @param page
     * @param size
     * @returns Page_GroupOut_ Successful Response
     * @throws ApiError
     */
    adminGetServerAdminsGroups(serverId, page = 1, size = 50) {
        return this.httpRequest.request({
            method: 'GET',
            url: '/v1/admin/servers/{server_id}/admins/groups',
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
     * Admin Create Server Admins Groups
     * Create server admins groups
     * :param servers_service:
     * :param server:
     * :return:
     * @param serverId
     * @param requestBody
     * @returns GroupOut Successful Response
     * @throws ApiError
     */
    adminCreateServerAdminsGroups(serverId, requestBody) {
        return this.httpRequest.request({
            method: 'POST',
            url: '/v1/admin/servers/{server_id}/admins/groups',
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
     * Admin Get Server Admins Group
     * Get server admins group
     * :param servers_service:
     * :param server:
     * :return:
     * @param groupId
     * @param serverId
     * @returns GroupOut Successful Response
     * @throws ApiError
     */
    adminGetServerAdminsGroup(groupId, serverId) {
        return this.httpRequest.request({
            method: 'GET',
            url: '/v1/admin/servers/{server_id}/admins/groups/{group_id}',
            path: {
                'group_id': groupId,
                'server_id': serverId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Admin Delete Server Admins Group
     * Delete server admins group
     * :param servers_service:
     * :param server:
     * :return:
     * @param groupId
     * @param serverId
     * @returns GroupOut Successful Response
     * @throws ApiError
     */
    adminDeleteServerAdminsGroup(groupId, serverId) {
        return this.httpRequest.request({
            method: 'DELETE',
            url: '/v1/admin/servers/{server_id}/admins/groups/{group_id}',
            path: {
                'group_id': groupId,
                'server_id': serverId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
exports.AdminServersAdminGroupsService = AdminServersAdminGroupsService;
