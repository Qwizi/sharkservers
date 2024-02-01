"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.RootService = void 0;
class RootService {
    constructor(httpRequest) {
        this.httpRequest = httpRequest;
    }
    /**
     * Install
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
     * @returns any Successful Response
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
     * @returns any Successful Response
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
