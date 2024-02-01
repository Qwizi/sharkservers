"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.AdminScopesService = void 0;
class AdminScopesService {
    constructor(httpRequest) {
        this.httpRequest = httpRequest;
    }
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
     * Admin create scope.
     * :param scope_data:
     * :param admin_user:
     * :return:
     * @param requestBody
     * @returns Scope_YVN Successful Response
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
     * @param scopeId
     * @returns Scope_YVN Successful Response
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
     * Admin delete scope.
     * :param scope:
     * :param admin_user:
     * :return:
     * @param scopeId
     * @returns Scope_YVN Successful Response
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
