/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Page_Scope_DBV_ } from '../models/Page_Scope_DBV_';

import type { CancelablePromise } from '../core/CancelablePromise';
import type { BaseHttpRequest } from '../core/BaseHttpRequest';

export class ScopesService {

    constructor(public readonly httpRequest: BaseHttpRequest) {}

    /**
     * Get All Scopes
     * Retrieve all scopes.
     *
     * Args:
     * ----
     * params (Params, optional): The request parameters. Defaults to Depends().
     * scopes_service (ScopeService, optional): The scope service. Defaults to Depends(get_scopes_service).
     * role_id (int | None, optional): The role ID. Defaults to None.
     *
     * Returns:
     * -------
     * Page[ScopeOut]: The list of scopes.
     * @param roleId
     * @param page
     * @param size
     * @returns Page_Scope_DBV_ Successful Response
     * @throws ApiError
     */
    public getAllScopes(
        roleId?: number,
        page: number = 1,
        size: number = 50,
    ): CancelablePromise<Page_Scope_DBV_> {
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
