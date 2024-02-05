/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Page_ServerOut_ } from '../models/Page_ServerOut_';
import type { ServerOut } from '../models/ServerOut';
import type { ServerStatusSchema } from '../models/ServerStatusSchema';

import type { CancelablePromise } from '../core/CancelablePromise';
import type { BaseHttpRequest } from '../core/BaseHttpRequest';

export class ServersService {

    constructor(public readonly httpRequest: BaseHttpRequest) {}

    /**
     * Get Servers
     * Retrieve servers based on the provided parameters.
     *
     * Args:
     * ----
     * params (Params, optional): The query parameters for filtering and pagination. Defaults to Depends().
     * ip (str, optional): The IP address of the server to retrieve. Defaults to None.
     * port (int, optional): The port of the server to retrieve. Defaults to None.
     * servers_service (ServerService, optional): The server service dependency. Defaults to Depends(get_servers_service).
     *
     * Returns:
     * -------
     * Page[ServerOut]: A paginated list of server objects.
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
     * Retrieve the status of servers.
     *
     * Args:
     * ----
     * servers_service (ServerService): The server service instance used to retrieve server status.
     *
     * Returns:
     * -------
     * list[ServerStatusSchema]: A list of server status objects.
     *
     * Raises:
     * ------
     * ConnectionRefusedError: If there is an error retrieving the server status.
     * @returns ServerStatusSchema Successful Response
     * @throws ApiError
     */
    public getServersStatus(): CancelablePromise<Array<ServerStatusSchema>> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/v1/servers/status',
        });
    }

    /**
     * Get Server
     * Retrieve a server based on the provided server model.
     *
     * Args:
     * ----
     * server (Model): The server model to retrieve.
     *
     * Returns:
     * -------
     * ServerOut: The retrieved server.
     * @param serverId
     * @returns ServerOut Successful Response
     * @throws ApiError
     */
    public getServer(
        serverId: string,
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
