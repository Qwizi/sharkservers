/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CreateGroupSchema } from '../models/CreateGroupSchema';
import type { GroupOut } from '../models/GroupOut';
import type { Page_GroupOut_ } from '../models/Page_GroupOut_';

import type { CancelablePromise } from '../core/CancelablePromise';
import type { BaseHttpRequest } from '../core/BaseHttpRequest';

export class AdminServersAdminGroupsService {

    constructor(public readonly httpRequest: BaseHttpRequest) {}

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
    public adminGetServerAdminsGroups(
        serverId: number,
        page: number = 1,
        size: number = 50,
    ): CancelablePromise<Page_GroupOut_> {
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
    public adminCreateServerAdminsGroups(
        serverId: number,
        requestBody: CreateGroupSchema,
    ): CancelablePromise<GroupOut> {
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
    public adminGetServerAdminsGroup(
        groupId: number,
        serverId: number,
    ): CancelablePromise<GroupOut> {
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
    public adminDeleteServerAdminsGroup(
        groupId: number,
        serverId: number,
    ): CancelablePromise<GroupOut> {
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
