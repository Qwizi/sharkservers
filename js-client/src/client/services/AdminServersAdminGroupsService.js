"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.AdminServersAdminGroupsService = void 0;
class AdminServersAdminGroupsService {
    constructor(httpRequest) {
        this.httpRequest = httpRequest;
    }
    /**
     * Admin Get Server Admins Groups
     * Retrieve the admins groups for a server.
     *
     * Args:
     * ----
     * params (Params): The parameters for the request.
     * server (Server): The server to retrieve the admins groups for.
     *
     * Returns:
     * -------
     * Page_GroupOut_: The paginated list of admins groups.
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
     * Create a new admin group for a server.
     *
     * Args:
     * ----
     * data (CreateGroupSchema): The data for creating the group.
     * server (Server): The server for which the group is being created.
     *
     * Returns:
     * -------
     * GroupOut: The created admin group.
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
     * Retrieve the admins group of a server by its group ID.
     *
     * Args:
     * ----
     * group_id (int): The ID of the admins group.
     * server (Server): The server object.
     *
     * Returns:
     * -------
     * GroupOut: The admins group information.
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
     * Delete an admin group from the server.
     *
     * Args:
     * ----
     * group_id (int): The ID of the admin group to delete.
     * server (Server): The server object.
     *
     * Returns:
     * -------
     * GroupOut: The deleted admin group.
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
