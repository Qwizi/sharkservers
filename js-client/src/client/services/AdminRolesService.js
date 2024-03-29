"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.AdminRolesService = void 0;
class AdminRolesService {
    constructor(httpRequest) {
        this.httpRequest = httpRequest;
    }
    /**
     * Admin Get Roles
     * Retrieve all roles with pagination.
     *
     * Args:
     * ----
     * params (Params, optional): The query parameters for pagination. Defaults to Depends().
     * admin_user (User, optional): The authenticated admin user. Defaults to Security(get_admin_user, scopes=["roles:all"]).
     * roles_service (RoleService, optional): The service for managing roles. Defaults to Depends(get_roles_service).
     *
     * Returns:
     * -------
     * Page[RoleOut]: The paginated list of roles.
     * @param page
     * @param size
     * @returns Page_RoleOut_ Successful Response
     * @throws ApiError
     */
    adminGetRoles(page = 1, size = 50) {
        return this.httpRequest.request({
            method: 'GET',
            url: '/v1/admin/roles',
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
     * Admin Create Role
     * Admin endpoint to create a new role.
     *
     * Args:
     * ----
     * role_data (CreateRoleSchema): The data for creating the role.
     * roles_service (RoleService, optional): The service for managing roles. Defaults to Depends(get_roles_service).
     * scopes_service (ScopeService, optional): The service for managing scopes. Defaults to Depends(get_scopes_service).
     *
     * Returns:
     * -------
     * The newly created role.
     * @param requestBody
     * @returns RoleOutWithScopes Successful Response
     * @throws ApiError
     */
    adminCreateRole(requestBody) {
        return this.httpRequest.request({
            method: 'POST',
            url: '/v1/admin/roles',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Admin Get Role
     * Retrieve the details of a role.
     *
     * Args:
     * ----
     * role (Role): The role object to retrieve details for.
     *
     * Returns:
     * -------
     * RoleOutWithScopes: The role object with associated scopes.
     * @param roleId
     * @returns RoleOutWithScopes Successful Response
     * @throws ApiError
     */
    adminGetRole(roleId) {
        return this.httpRequest.request({
            method: 'GET',
            url: '/v1/admin/roles/{role_id}',
            path: {
                'role_id': roleId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Admin Update Role
     * Update a role with the provided data.
     *
     * Args:
     * ----
     * update_role_data (UpdateRoleSchema): The data to update the role with.
     * role (Role): The role to be updated.
     * scopes_service (ScopeService): The service to handle scopes.
     *
     * Returns:
     * -------
     * Role: The updated role.
     * @param roleId
     * @param requestBody
     * @returns RoleOutWithScopes Successful Response
     * @throws ApiError
     */
    adminUpdateRole(roleId, requestBody) {
        return this.httpRequest.request({
            method: 'PUT',
            url: '/v1/admin/roles/{role_id}',
            path: {
                'role_id': roleId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Admin Delete Role
     * Delete a role.
     *
     * Args:
     * ----
     * role (Role): The role to be deleted.
     * roles_service (RoleService): The service used to delete the role.
     *
     * Returns:
     * -------
     * RoleOutWithScopes: The deleted role.
     * @param roleId
     * @returns RoleOutWithScopes Successful Response
     * @throws ApiError
     */
    adminDeleteRole(roleId) {
        return this.httpRequest.request({
            method: 'DELETE',
            url: '/v1/admin/roles/{role_id}',
            path: {
                'role_id': roleId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
exports.AdminRolesService = AdminRolesService;
