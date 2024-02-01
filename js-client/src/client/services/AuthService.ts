/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ActivateUserCodeSchema } from '../models/ActivateUserCodeSchema';
import type { Body_auth_get_app_token } from '../models/Body_auth_get_app_token';
import type { Body_auth_login_user } from '../models/Body_auth_login_user';
import type { RefreshTokenSchema } from '../models/RefreshTokenSchema';
import type { RegisterUserSchema } from '../models/RegisterUserSchema';
import type { ResendActivationCodeSchema } from '../models/ResendActivationCodeSchema';
import type { ResetPasswordSchema } from '../models/ResetPasswordSchema';
import type { TokenSchema } from '../models/TokenSchema';
import type { UserActivatedSchema } from '../models/UserActivatedSchema';
import type { UserOut } from '../models/UserOut';

import type { CancelablePromise } from '../core/CancelablePromise';
import type { BaseHttpRequest } from '../core/BaseHttpRequest';

export class AuthService {

    constructor(public readonly httpRequest: BaseHttpRequest) {}

    /**
     * Register
     * @param requestBody
     * @returns UserOut Successful Response
     * @throws ApiError
     */
    public register(
        requestBody: RegisterUserSchema,
    ): CancelablePromise<UserOut> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/v1/auth/register',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Login User
     * Login user
     * :param auth_service:
     * :param refresh_token_service:
     * :param access_token_service:
     * :param form_data:
     * :return TokenSchema:
     * @param formData
     * @returns TokenSchema Successful Response
     * @throws ApiError
     */
    public loginUser(
        formData: Body_auth_login_user,
    ): CancelablePromise<TokenSchema> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/v1/auth/token',
            formData: formData,
            mediaType: 'application/x-www-form-urlencoded',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Access Token From Refresh Token
     * Get access token from refresh token
     * :param auth_service:
     * :param refresh_token_service:
     * :param access_token_service:
     * :param token_data:
     * :return TokenSchema:
     * @param requestBody
     * @returns TokenSchema Successful Response
     * @throws ApiError
     */
    public getAccessTokenFromRefreshToken(
        requestBody: RefreshTokenSchema,
    ): CancelablePromise<TokenSchema> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/v1/auth/token/refresh',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Logout User
     * Logout user
     * :param auth_service:
     * :param user:
     * :return:
     * @returns UserOut Successful Response
     * @throws ApiError
     */
    public logoutUser(): CancelablePromise<UserOut> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/v1/auth/logout',
        });
    }

    /**
     * Activate User
     * Activate user
     * :param activate_code_service:
     * :param auth_service:
     * :param activate_code_data:
     * :return bool:
     * @param requestBody
     * @returns UserActivatedSchema Successful Response
     * @throws ApiError
     */
    public activateUser(
        requestBody: ActivateUserCodeSchema,
    ): CancelablePromise<UserActivatedSchema> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/v1/auth/activate',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Resend Activate Code
     * Resend activate code
     * :param code_service:
     * :param background_tasks:
     * :param email_service:
     * :param auth_service:
     * :param data:
     * :return bool:
     * @param requestBody
     * @returns string Successful Response
     * @throws ApiError
     */
    public resendActivateCode(
        requestBody: ResendActivationCodeSchema,
    ): CancelablePromise<Record<string, string>> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/v1/auth/activate/resend',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * @deprecated
     * Connect Steam Profile
     * @returns any Successful Response
     * @throws ApiError
     */
    public connectSteamProfile(): CancelablePromise<any> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/v1/auth/connect/steam',
        });
    }

    /**
     * @deprecated
     * Steam Profile Callback
     * @returns any Successful Response
     * @throws ApiError
     */
    public steamProfileCallback(): CancelablePromise<any> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/v1/auth/callback/steam',
        });
    }

    /**
     * Get App Token
     * Get app token
     * :param auth_service:
     * :param access_token_service:
     * :param form_data:
     * :return TokenSchema:
     * @param formData
     * @returns TokenSchema Successful Response
     * @throws ApiError
     */
    public getAppToken(
        formData?: Body_auth_get_app_token,
    ): CancelablePromise<TokenSchema> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/v1/auth/apps/token',
            formData: formData,
            mediaType: 'application/x-www-form-urlencoded',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Forgot Password Request
     * Forgot password request
     * :param code_service:
     * :param background_tasks:
     * :param email_service:
     * :param auth_service:
     * :param data:
     * :return bool:
     * @param requestBody
     * @returns string Successful Response
     * @throws ApiError
     */
    public forgotPasswordRequest(
        requestBody: ResendActivationCodeSchema,
    ): CancelablePromise<Record<string, string>> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/v1/auth/forgot-password',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Reset Password
     * Reset password
     * :param code_service:
     * :param auth_service:
     * :param data:
     * :return bool:
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public resetPassword(
        requestBody: ResetPasswordSchema,
    ): CancelablePromise<Record<string, any>> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/v1/auth/reset-password',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

}
