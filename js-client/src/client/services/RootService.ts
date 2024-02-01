/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { RegisterUserSchema } from '../models/RegisterUserSchema';

import type { CancelablePromise } from '../core/CancelablePromise';
import type { BaseHttpRequest } from '../core/BaseHttpRequest';

export class RootService {

    constructor(public readonly httpRequest: BaseHttpRequest) {}

    /**
     * Install
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public install(
        requestBody: RegisterUserSchema,
    ): CancelablePromise<any> {
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
    public generateOpenapi(): CancelablePromise<any> {
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
    public generateRandomData(): CancelablePromise<any> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/generate-random-data',
        });
    }

}
