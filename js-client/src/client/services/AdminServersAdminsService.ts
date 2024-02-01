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
    public adminGetServerAdmins(
        serverId: number,
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
     * Create server admin
     * :param servers_service:
     * :param server:
     * :return:
     * @param serverId
     * @param requestBody
     * @returns AdminOut Successful Response
     * @throws ApiError
     */
    public adminCreateServerAdmin(
        serverId: number,
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
     * Get server admin
     * :param servers_service:
     * :param server:
     * :return:
     * @param identity
     * @param serverId
     * @returns AdminOut Successful Response
     * @throws ApiError
     */
    public adminGetServerAdmin(
        identity: string,
        serverId: number,
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
    public adminUpdateServerAdmin(
        identity: string,
        serverId: number,
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
     * Delete server admin
     * :param servers_service:
     * :param server:
     * :return:
     * @param identity
     * @param serverId
     * @returns AdminOut Successful Response
     * @throws ApiError
     */
    public adminDeleteServerAdmin(
        identity: string,
        serverId: number,
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
