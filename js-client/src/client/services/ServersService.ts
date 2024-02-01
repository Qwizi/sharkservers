/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Page_ServerOut_ } from '../models/Page_ServerOut_';
import type { ServerOut } from '../models/ServerOut';

import type { CancelablePromise } from '../core/CancelablePromise';
import type { BaseHttpRequest } from '../core/BaseHttpRequest';

export class ServersService {

    constructor(public readonly httpRequest: BaseHttpRequest) {}

    /**
     * Get Servers
     * Get all servers
     * :return:
     * @param ip
     * @param port
     * @param page
     * @param size
     * @returns Page_ServerOut_ Successful Response
     * @throws ApiError
     */
    public getServers(
        ip?: string,
        port?: number,
        page: number = 1,
        size: number = 50,
    ): CancelablePromise<Page_ServerOut_> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/v1/servers/',
            query: {
                'ip': ip,
                'port': port,
                'page': page,
                'size': size,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Servers Status
     * Get all servers' status
     * :return:
     * @returns any Successful Response
     * @throws ApiError
     */
    public getServersStatus(): CancelablePromise<any> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/v1/servers/status',
        });
    }

    /**
     * Get Server
     * Get server by id
     * :param server:
     * :param server_id:
     * :return:
     * @param serverId
     * @returns ServerOut Successful Response
     * @throws ApiError
     */
    public getServer(
        serverId: number,
    ): CancelablePromise<ServerOut> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/v1/servers/{server_id}',
            path: {
                'server_id': serverId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

}
