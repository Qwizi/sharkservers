"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.AdminRolesService = void 0;
class AdminRolesService {
    constructor(httpRequest) {
        this.httpRequest = httpRequest;
    }
    /**
     * Admin Get Roles
     * Admin get all roles.
     * :param roles_service:
     * :param params:
     * :param admin_user:
     * :return AbstractPag[RoleOut]:
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
     * Admin create role.
     * :param role_data:
     * :param admin_user:
     * :param roles_service:
     * :param scopes_service:
     * :return:
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
     * Admin get role by id.
     * :param role:
     * :param role_id:
     * :param user:
     * :return:
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
     * Admin update role.
     * :param update_role_data:
     * :param scopes_service:
     * :param role:
     * :param admin_user:
     * :return:
     * @param roleId
     * @param requestBody
     * @returns any Successful Response
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
     * Admin delete role.
     * :param role:
     * :param user:
     * :return:
     * @param roleId
     * @returns any Successful Response
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
    /**
     * Admin Add Scopes To Role
     * @param roleId
     * @param requestBody
     * @returns RoleOut Successful Response
     * @throws ApiError
     */
    adminAddScopesToRole(roleId, requestBody) {
        return this.httpRequest.request({
            method: 'POST',
            url: '/v1/admin/roles/{role_id}/scopes/add',
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
}
exports.AdminRolesService = AdminRolesService;
