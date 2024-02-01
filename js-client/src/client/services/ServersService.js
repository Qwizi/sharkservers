"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.ServersService = void 0;
class ServersService {
    constructor(httpRequest) {
        this.httpRequest = httpRequest;
    }
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
     * Get all servers' status
     * :return:
     * @returns any Successful Response
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
     * Get server by id
     * :param server:
     * :param server_id:
     * :return:
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
