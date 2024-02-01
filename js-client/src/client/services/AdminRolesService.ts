/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CreateRoleSchema } from '../models/CreateRoleSchema';
import type { Page_RoleOut_ } from '../models/Page_RoleOut_';
import type { RoleOutWithScopes } from '../models/RoleOutWithScopes';
import type { UpdateRoleSchema } from '../models/UpdateRoleSchema';

import type { CancelablePromise } from '../core/CancelablePromise';
import type { BaseHttpRequest } from '../core/BaseHttpRequest';

export class AdminRolesService {

    constructor(public readonly httpRequest: BaseHttpRequest) {}

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
    public adminGetRoles(
        page: number = 1,
        size: number = 50,
    ): CancelablePromise<Page_RoleOut_> {
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
    public adminCreateRole(
        requestBody: CreateRoleSchema,
    ): CancelablePromise<RoleOutWithScopes> {
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
    public adminGetRole(
        roleId: number,
    ): CancelablePromise<RoleOutWithScopes> {
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
    public adminUpdateRole(
        roleId: number,
        requestBody: UpdateRoleSchema,
    ): CancelablePromise<RoleOutWithScopes> {
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
    public adminDeleteRole(
        roleId: number,
    ): CancelablePromise<RoleOutWithScopes> {
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
