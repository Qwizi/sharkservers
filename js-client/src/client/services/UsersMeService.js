"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.UsersMeService = void 0;
class UsersMeService {
    constructor(httpRequest) {
        this.httpRequest = httpRequest;
    }
    /**
     * Get Logged User
     * Get logged user
     * :param user:
     * :return UserOutWithEmail:
     * @returns UserOutWithEmail Successful Response
     * @throws ApiError
     */
    getLoggedUser() {
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
    getLoggedUserPosts(page = 1, size = 50, orderBy = '-id') {
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
    getLoggedUserThreads(page = 1, size = 50, orderBy = '-id') {
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
    getUserApps(page = 1, size = 50) {
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
    createUserApp(requestBody) {
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
    changeUserUsername(requestBody) {
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
    changeUserPassword(requestBody) {
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
    requestChangeUserEmail(requestBody) {
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
    confirmChangeUserEmail(requestBody) {
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
    changeUserDisplayRole(requestBody) {
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
    uploadUserAvatar(formData) {
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
    connectSteamProfile(requestBody) {
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
    getUserSessions() {
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
    deleteUserSession(sessionId) {
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
exports.UsersMeService = UsersMeService;
