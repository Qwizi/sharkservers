/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Page_RoleOut_ } from '../models/Page_RoleOut_';
import type { RoleOutWithScopes } from '../models/RoleOutWithScopes';

import type { CancelablePromise } from '../core/CancelablePromise';
import type { BaseHttpRequest } from '../core/BaseHttpRequest';

export class RolesService {

    constructor(public readonly httpRequest: BaseHttpRequest) {}

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
    public getRoles(
        page: number = 1,
        size: number = 50,
    ): CancelablePromise<Page_RoleOut_> {
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
    public getRole(
        roleId: number,
    ): CancelablePromise<RoleOutWithScopes> {
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
