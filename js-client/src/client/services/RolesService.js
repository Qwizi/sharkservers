"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.RolesService = void 0;
class RolesService {
    constructor(httpRequest) {
        this.httpRequest = httpRequest;
    }
    /**
     * Get Roles
     * Retrieve all roles based on the provided parameters.
     *
     * Args:
     * ----
     * params (Params): The parameters for filtering and pagination.
     * roles_service (RoleService): The service for retrieving roles.
     *
     * Returns:
     * -------
     * Page[RoleOut]: A paginated list of RoleOut objects.
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
     * Retrieve a role by its ID.
     *
     * Args:
     * ----
     * role (Role): The role object.
     *
     * Returns:
     * -------
     * RoleOutWithScopes: The role object with associated scopes.
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
