"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.RolesService = void 0;
class RolesService {
    constructor(httpRequest) {
        this.httpRequest = httpRequest;
    }
    /**
     * Get Roles
     * Get roles
     * :param roles_service:
     * :param params:
     * :return AbstractPage:
     * @param page
     * @param size
     * @returns Page_RoleOut_ Successful Response
     * @throws ApiError
     */
    getRoles(page = 1, size = 50) {
        return this.httpRequest.request({
            method: 'GET',
            url: '/v1/roles',
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
     * Get Role
     * Get role by id
     * :param role:
     * :return:
     * @param roleId
     * @returns RoleOutWithScopes Successful Response
     * @throws ApiError
     */
    getRole(roleId) {
        return this.httpRequest.request({
            method: 'GET',
            url: '/v1/roles/{role_id}',
            path: {
                'role_id': roleId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
exports.RolesService = RolesService;
