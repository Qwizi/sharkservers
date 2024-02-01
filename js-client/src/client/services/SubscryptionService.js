"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.SubscryptionService = void 0;
class SubscryptionService {
    constructor(httpRequest) {
        this.httpRequest = httpRequest;
    }
    /**
     * Get Subscryption
     * @returns any Successful Response
     * @throws ApiError
     */
    getSubscryption() {
        return this.httpRequest.request({
            method: 'GET',
            url: '/v1/subscryption/',
        });
    }
    /**
     * Get Webhook
     * @returns any Successful Response
     * @throws ApiError
     */
    getWebhook() {
        return this.httpRequest.request({
            method: 'POST',
            url: '/v1/subscryption/webhook',
        });
    }
}
exports.SubscryptionService = SubscryptionService;
