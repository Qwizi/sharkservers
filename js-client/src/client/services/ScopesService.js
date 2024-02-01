"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.ScopesService = void 0;
class ScopesService {
    constructor(httpRequest) {
        this.httpRequest = httpRequest;
    }
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
