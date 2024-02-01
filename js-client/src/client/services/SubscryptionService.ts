/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CancelablePromise } from '../core/CancelablePromise';
import type { BaseHttpRequest } from '../core/BaseHttpRequest';

export class SubscryptionService {

    constructor(public readonly httpRequest: BaseHttpRequest) {}

    /**
     * Get Subscryption
     * @returns any Successful Response
     * @throws ApiError
     */
    public getSubscryption(): CancelablePromise<any> {
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
    public getWebhook(): CancelablePromise<any> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/v1/subscryption/webhook',
        });
    }

}
