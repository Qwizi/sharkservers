/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CreateScopeSchema } from '../models/CreateScopeSchema';
import type { Page_Scope_YVN_ } from '../models/Page_Scope_YVN_';
import type { Scope_YVN } from '../models/Scope_YVN';
import type { UpdateScopeSchema } from '../models/UpdateScopeSchema';

import type { CancelablePromise } from '../core/CancelablePromise';
import type { BaseHttpRequest } from '../core/BaseHttpRequest';

export class AdminScopesService {

    constructor(public readonly httpRequest: BaseHttpRequest) {}

    /**
     * Admin Get Scopes
     * Admin get scopes.
     * :param scopes_service:
     * :param params:
     * :param     admin_user:
     * :return:
     * @param page
     * @param size
     * @returns Page_Scope_YVN_ Successful Response
     * @throws ApiError
     */
    public adminGetScopes(
        page: number = 1,
        size: number = 50,
    ): CancelablePromise<Page_Scope_YVN_> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/v1/admin/scopes',
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
     * Admin Create Scope
     * Admin create scope.
     * :param scope_data:
     * :param admin_user:
     * :return:
     * @param requestBody
     * @returns Scope_YVN Successful Response
     * @throws ApiError
     */
    public adminCreateScope(
        requestBody: CreateScopeSchema,
    ): CancelablePromise<Scope_YVN> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/v1/admin/scopes',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Admin Get Scope
     * @param scopeId
     * @returns Scope_YVN Successful Response
     * @throws ApiError
     */
    public adminGetScope(
        scopeId: number,
    ): CancelablePromise<Scope_YVN> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/v1/admin/scopes/{scope_id}',
            path: {
                'scope_id': scopeId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Admin Update Scope
     * Admin update scope.
     * :param update_scope_data:
     * :param scopes_service:
     * :param scope:
     * :param admin_user:
     * :return:
     * @param scopeId
     * @param requestBody
     * @returns Scope_YVN Successful Response
     * @throws ApiError
     */
    public adminUpdateScope(
        scopeId: number,
        requestBody: UpdateScopeSchema,
    ): CancelablePromise<Scope_YVN> {
        return this.httpRequest.request({
            method: 'PUT',
            url: '/v1/admin/scopes/{scope_id}',
            path: {
                'scope_id': scopeId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Admin Delete Scope
     * Admin delete scope.
     * :param scope:
     * :param admin_user:
     * :return:
     * @param scopeId
     * @returns Scope_YVN Successful Response
     * @throws ApiError
     */
    public adminDeleteScope(
        scopeId: number,
    ): CancelablePromise<Scope_YVN> {
        return this.httpRequest.request({
            method: 'DELETE',
            url: '/v1/admin/scopes/{scope_id}',
            path: {
                'scope_id': scopeId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

}
