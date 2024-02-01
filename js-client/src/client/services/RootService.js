"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.RootService = void 0;
class RootService {
    constructor(httpRequest) {
        this.httpRequest = httpRequest;
    }
    /**
     * Install
     * Endpoint for installing the SharkServers application.
     *
     * Args:
     * ----
     * - user_data: User data for the admin user.
     * - scopes_service: Service for managing scopes.
     * - roles_service: Service for managing roles.
     * - auth_service: Service for authentication.
     * - settings: Application settings.
     *
     * Returns:
     * -------
     * - A dictionary with a "msg" key indicating the success of the installation.
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    install(requestBody) {
        return this.httpRequest.request({
            method: 'POST',
            url: '/install',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Generate Openapi
     * Endpoint for generating the OpenAPI documentation.
     *
     * Returns
     * -------
     * - A dictionary with a "msg" key indicating the success of the generation.
     * @returns string Successful Response
     * @throws ApiError
     */
    generateOpenapi() {
        return this.httpRequest.request({
            method: 'GET',
            url: '/generate-openapi',
        });
    }
    /**
     * Generate Random Data
     * Endpoint for generating random data for testing purposes.
     *
     * Args:
     * ----
     * - auth_service: Service for authentication.
     * - roles_service: Service for managing roles.
     * - categories_service: Service for managing categories.
     * - threads_service: Service for managing threads.
     * - posts_service: Service for managing posts.
     * - servers_service: Service for managing servers.
     *
     * Returns:
     * -------
     * - A dictionary with a "msg" key indicating the success of the generation.
     * @returns string Successful Response
     * @throws ApiError
     */
    generateRandomData() {
        return this.httpRequest.request({
            method: 'GET',
            url: '/generate-random-data',
        });
    }
}
exports.RootService = RootService;
