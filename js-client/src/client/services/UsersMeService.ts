/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ActivateUserCodeSchema } from '../models/ActivateUserCodeSchema';
import type { Body_users_me_upload_user_avatar } from '../models/Body_users_me_upload_user_avatar';
import type { ChangeDisplayRoleSchema } from '../models/ChangeDisplayRoleSchema';
import type { ChangeEmailSchema } from '../models/ChangeEmailSchema';
import type { ChangePasswordSchema } from '../models/ChangePasswordSchema';
import type { ChangeUsernameSchema } from '../models/ChangeUsernameSchema';
import type { CreateAppSchema } from '../models/CreateAppSchema';
import type { SteamAuthSchema } from '../models/SteamAuthSchema';
import type { SuccessChangeUsernameSchema } from '../models/SuccessChangeUsernameSchema';
import type { UserOutWithEmail } from '../models/UserOutWithEmail';
import type { UserSessionOut } from '../models/UserSessionOut';

import type { CancelablePromise } from '../core/CancelablePromise';
import type { BaseHttpRequest } from '../core/BaseHttpRequest';

export class UsersMeService {

    constructor(public readonly httpRequest: BaseHttpRequest) {}

    /**
     * Get Logged User
     * Get logged user
     * :param user:
     * :return UserOutWithEmail:
     * @returns UserOutWithEmail Successful Response
     * @throws ApiError
     */
    public getLoggedUser(): CancelablePromise<UserOutWithEmail> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/v1/users/me',
        });
    }

    /**
     * Get Logged User Posts
     * Get user posts
     * :param params:
     * :param posts_service:
     * :param user:
     * :return AbstractPage:
     * @param page
     * @param size
     * @param orderBy
     * @returns any Successful Response
     * @throws ApiError
     */
    public getLoggedUserPosts(
        page: number = 1,
        size: number = 50,
        orderBy: string = '-id',
    ): CancelablePromise<any> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/v1/users/me/posts',
            query: {
                'page': page,
                'size': size,
                'order_by': orderBy,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Logged User Threads
     * Get user threads
     * :param threads_service:
     * :param params:
     * :param user:
     * :return AbstractPage:
     * @param page
     * @param size
     * @param orderBy
     * @returns any Successful Response
     * @throws ApiError
     */
    public getLoggedUserThreads(
        page: number = 1,
        size: number = 50,
        orderBy: string = '-id',
    ): CancelablePromise<any> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/v1/users/me/threads',
            query: {
                'page': page,
                'size': size,
                'order_by': orderBy,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * @deprecated
     * Get User Apps
     * Get user apps
     * :param apps_service:
     * :param user:
     * :return dict:
     * @param page
     * @param size
     * @returns any Successful Response
     * @throws ApiError
     */
    public getUserApps(
        page: number = 1,
        size: number = 50,
    ): CancelablePromise<Record<string, any>> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/v1/users/me/apps',
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
     * @deprecated
     * Create User App
     * Create user app
     * :param scopes_service:
     * :param apps_service:
     * :param app_data:
     * :param user:
     * :return dict:
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public createUserApp(
        requestBody: CreateAppSchema,
    ): CancelablePromise<Record<string, any>> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/v1/users/me/apps',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Change User Username
     * Change user username
     * :param change_username_data:
     * :param user:
     * :return UserOut:
     * @param requestBody
     * @returns SuccessChangeUsernameSchema Successful Response
     * @throws ApiError
     */
    public changeUserUsername(
        requestBody: ChangeUsernameSchema,
    ): CancelablePromise<SuccessChangeUsernameSchema> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/v1/users/me/username',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Change User Password
     * Change user password
     * :param change_password_data:
     * :param user:
     * :return dict:
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public changeUserPassword(
        requestBody: ChangePasswordSchema,
    ): CancelablePromise<Record<string, any>> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/v1/users/me/password',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Request Change User Email
     * Request change user email
     * :param email_service:
     * :param users_service:
     * :param background_tasks:
     * :param code_service:
     * :param change_email_data:
     * :param user:
     * :return dict:
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public requestChangeUserEmail(
        requestBody: ChangeEmailSchema,
    ): CancelablePromise<any> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/v1/users/me/email',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Confirm Change User Email
     * Confirm change user email
     * :param users_service:
     * :param code_service:
     * :param activate_code_data:
     * :return dict:
     * @param requestBody
     * @returns UserOutWithEmail Successful Response
     * @throws ApiError
     */
    public confirmChangeUserEmail(
        requestBody: ActivateUserCodeSchema,
    ): CancelablePromise<UserOutWithEmail> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/v1/users/me/email/confirm',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Change User Display Role
     * Change user display role
     * :param auth_service:
     * :param change_display_role_data:
     * :param user:
     * :return dict:
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public changeUserDisplayRole(
        requestBody: ChangeDisplayRoleSchema,
    ): CancelablePromise<any> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/v1/users/me/display-role',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Upload User Avatar
     * Upload user avatar
     * :return:
     * @param formData
     * @returns any Successful Response
     * @throws ApiError
     */
    public uploadUserAvatar(
        formData: Body_users_me_upload_user_avatar,
    ): CancelablePromise<any> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/v1/users/me/avatar',
            formData: formData,
            mediaType: 'multipart/form-data',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Connect Steam Profile
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public connectSteamProfile(
        requestBody: SteamAuthSchema,
    ): CancelablePromise<any> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/v1/users/me/connect/steam',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get User Sessions
     * @returns UserSessionOut Successful Response
     * @throws ApiError
     */
    public getUserSessions(): CancelablePromise<Array<UserSessionOut>> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/v1/users/me/sessions',
        });
    }

    /**
     * Delete User Session
     * @param sessionId
     * @returns any Successful Response
     * @throws ApiError
     */
    public deleteUserSession(
        sessionId: string,
    ): CancelablePromise<any> {
        return this.httpRequest.request({
            method: 'DELETE',
            url: '/v1/users/me/sessions/{session_id}',
            path: {
                'session_id': sessionId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

}
