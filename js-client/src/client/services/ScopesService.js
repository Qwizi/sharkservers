"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.ScopesService = void 0;
class ScopesService {
    constructor(httpRequest) {
        this.httpRequest = httpRequest;
    }
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
     * @returns Page_ScopeOut_ Successful Response
     * @throws ApiError
     */
    getAllScopes(roleId, page = 1, size = 50) {
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
exports.ScopesService = ScopesService;
