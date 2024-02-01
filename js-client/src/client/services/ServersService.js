"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.ServersService = void 0;
class ServersService {
    constructor(httpRequest) {
        this.httpRequest = httpRequest;
    }
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
    getServers(ip, port, page = 1, size = 50) {
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
    getServersStatus() {
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
    getServer(serverId) {
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
exports.ServersService = ServersService;
