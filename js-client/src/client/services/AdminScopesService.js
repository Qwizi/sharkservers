"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.AdminScopesService = void 0;
class AdminScopesService {
    constructor(httpRequest) {
        this.httpRequest = httpRequest;
    }
    /**
     * Admin Get Scopes
     * Retrieve all scopes for admin users.
     *
     * Args:
     * ----
     * params (Params): The parameters for filtering and pagination.
     * scopes_service (ScopeService): The service for retrieving scopes.
     *
     * Returns:
     * -------
     * Page[ScopeOut]: A paginated list of ScopeOut objects.
     * @param page
     * @param size
     * @returns Page_Scope_CXR_ Successful Response
     * @throws ApiError
     */
    adminGetScopes(page = 1, size = 50) {
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
     * Create a new scope.
     *
     * Args:
     * ----
     * scope_data (CreateScopeSchema): The data for creating the scope.
     * scopes_service (ScopeService, optional): The service for managing scopes. Defaults to Depends(get_scopes_service).
     *
     * Returns:
     * -------
     * ScopeOut: The created scope.
     * @param requestBody
     * @returns Scope_CXR Successful Response
     * @throws ApiError
     */
    adminCreateScope(requestBody) {
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
     * Retrieve a scope for admin users.
     *
     * Args:
     * ----
     * scope (Scope): The scope to retrieve.
     *
     * Returns:
     * -------
     * ScopeOut: The retrieved scope.
     * @param scopeId
     * @returns Scope_CXR Successful Response
     * @throws ApiError
     */
    adminGetScope(scopeId) {
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
     * Update the given scope with the provided data.
     *
     * Args:
     * ----
     * update_scope_data (UpdateScopeSchema): The data to update the scope with.
     * scope (Scope): The scope to be updated.
     *
     * Returns:
     * -------
     * ScopeOut: The updated scope.
     * @param scopeId
     * @param requestBody
     * @returns Scope_CXR Successful Response
     * @throws ApiError
     */
    adminUpdateScope(scopeId, requestBody) {
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
     * Deletes a scope from the system.
     *
     * Args:
     * ----
     * scope (Scope): The scope to be deleted.
     * scopes_service (ScopeService): The service responsible for managing scopes.
     *
     * Returns:
     * -------
     * ScopeOut: The deleted scope.
     * @param scopeId
     * @returns Scope_CXR Successful Response
     * @throws ApiError
     */
    adminDeleteScope(scopeId) {
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
exports.AdminScopesService = AdminScopesService;
