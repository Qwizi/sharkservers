/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CreateServerSchema } from '../models/CreateServerSchema';
import type { ServerOut } from '../models/ServerOut';
import type { UpdateServerSchema } from '../models/UpdateServerSchema';

import type { CancelablePromise } from '../core/CancelablePromise';
import type { BaseHttpRequest } from '../core/BaseHttpRequest';

export class AdminServersService {

    constructor(public readonly httpRequest: BaseHttpRequest) {}

    /**
     * Admin Get Servers
     * Get all servers
     * :return:
     * @returns ServerOut Successful Response
     * @throws ApiError
     */
    public adminGetServers(): CancelablePromise<ServerOut> {
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
    public adminCreateServer(
        requestBody: CreateServerSchema,
    ): CancelablePromise<ServerOut> {
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
    public adminGetServer(
        serverId: number,
    ): CancelablePromise<ServerOut> {
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
    public adminUpdateServer(
        serverId: number,
        requestBody: UpdateServerSchema,
    ): CancelablePromise<ServerOut> {
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
    public adminDeleteServer(
        serverId: number,
    ): CancelablePromise<any> {
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
