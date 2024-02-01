/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Page_Scope_YVN_ } from '../models/Page_Scope_YVN_';

import type { CancelablePromise } from '../core/CancelablePromise';
import type { BaseHttpRequest } from '../core/BaseHttpRequest';

export class ScopesService {

    constructor(public readonly httpRequest: BaseHttpRequest) {}

    /**
     * Get All Scopes
     * Get all scopes
     *
     * :param scopes_service:
     * :param params:
     * :param role_id:
     * :return:
     * @param roleId
     * @param page
     * @param size
     * @returns Page_Scope_YVN_ Successful Response
     * @throws ApiError
     */
    public getAllScopes(
        roleId?: number,
        page: number = 1,
        size: number = 50,
    ): CancelablePromise<Page_Scope_YVN_> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/v1/scopes',
            query: {
                'role_id': roleId,
                'page': page,
                'size': size,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

}
