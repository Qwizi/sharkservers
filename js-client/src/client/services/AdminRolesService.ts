/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CreateRoleSchema } from '../models/CreateRoleSchema';
import type { Page_RoleOut_ } from '../models/Page_RoleOut_';
import type { RoleOut } from '../models/RoleOut';
import type { RoleOutWithScopes } from '../models/RoleOutWithScopes';
import type { UpdateRoleSchema } from '../models/UpdateRoleSchema';

import type { CancelablePromise } from '../core/CancelablePromise';
import type { BaseHttpRequest } from '../core/BaseHttpRequest';

export class AdminRolesService {

    constructor(public readonly httpRequest: BaseHttpRequest) {}

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
     * Admin get role by id.
     * :param role:
     * :param role_id:
     * :param user:
     * :return:
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
    public adminUpdateRole(
        roleId: number,
        requestBody: UpdateRoleSchema,
    ): CancelablePromise<any> {
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
    public adminDeleteRole(
        roleId: number,
    ): CancelablePromise<any> {
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
    public adminAddScopesToRole(
        roleId: number,
        requestBody: Array<number>,
    ): CancelablePromise<RoleOut> {
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
