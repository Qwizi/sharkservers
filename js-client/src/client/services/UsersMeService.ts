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
import type { Page_PostOut_ } from '../models/Page_PostOut_';
import type { Page_ThreadOut_ } from '../models/Page_ThreadOut_';
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
     * Retrieve the currently logged-in user.
     *
     * Args:
     * ----
     * user (User): The currently logged-in user.
     *
     * Returns:
     * -------
     * UserOutWithEmail: The logged-in user with email.
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
     * Retrieves all posts created by the logged-in user.
     *
     * Args:
     * ----
     * params (Params, optional): The parameters for pagination and filtering. Defaults to Depends().
     * queries (OrderQuery, optional): The query parameters for ordering the posts. Defaults to Depends().
     * user (User, optional): The logged-in user. Defaults to Security(get_current_active_user, scopes=["users:me"]).
     * posts_service (PostService, optional): The service for retrieving posts. Defaults to Depends(get_posts_service).
     *
     * Returns:
     * -------
     * List[Post]: The list of posts created by the logged-in user.
     * @param page
     * @param size
     * @param orderBy
     * @returns Page_PostOut_ Successful Response
     * @throws ApiError
     */
    public getLoggedUserPosts(
        page: number = 1,
        size: number = 50,
        orderBy: string = '-id',
    ): CancelablePromise<Page_PostOut_> {
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
     * Retrieve all threads for the logged-in user.
     *
     * Args:
     * ----
     * params (Params): The parameters for filtering and pagination.
     * queries (OrderQuery): The query parameters for ordering.
     * user (User): The logged-in user.
     * threads_service (ThreadService): The service for handling threads.
     *
     * Returns:
     * -------
     * List[Thread]: The list of threads for the logged-in user.
     * @param page
     * @param size
     * @param orderBy
     * @returns Page_ThreadOut_ Successful Response
     * @throws ApiError
     */
    public getLoggedUserThreads(
        page: number = 1,
        size: number = 50,
        orderBy: string = '-id',
    ): CancelablePromise<Page_ThreadOut_> {
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
     * Change User Username
     * Change the username of the current user.
     *
     * Args:
     * ----
     * change_username_data (ChangeUsernameSchema): The data containing the new username.
     * user (User): The current authenticated user.
     * users_service (UserService): The service responsible for handling user-related operations.
     *
     * Returns:
     * -------
     * SuccessChangeUsernameSchema: The response containing the old and new usernames.
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
     * Change the password of the current user.
     *
     * Args:
     * ----
     * change_password_data (ChangePasswordSchema): The new password data.
     * user (User): The current user.
     * users_service (UserService): The service for managing users.
     *
     * Returns:
     * -------
     * dict: A dictionary with a success message.
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
     * Request a change of user email.
     *
     * Args:
     * ----
     * change_email_data (ChangeEmailSchema): The data for the email change request.
     * background_tasks (BackgroundTasks): The background tasks manager.
     * user (User): The current authenticated user.
     * email_service (EmailService): The email service.
     * code_service (CodeService): The code service for email confirmation codes.
     * users_service (UserService): The user service.
     *
     * Returns:
     * -------
     * dict: A dictionary with a success message indicating that the request for email change was sent.
     * @param requestBody
     * @returns string Successful Response
     * @throws ApiError
     */
    public requestChangeUserEmail(
        requestBody: ChangeEmailSchema,
    ): CancelablePromise<Record<string, string>> {
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
     * Confirm the change of user's email address using the activation code.
     *
     * Args:
     * ----
     * activate_code_data (ActivateUserCodeSchema): The activation code data.
     * code_service (CodeService, optional): The code service dependency. Defaults to Depends(get_change_account_email_code_service).
     * users_service (UserService, optional): The users service dependency. Defaults to Depends(get_users_service).
     *
     * Returns:
     * -------
     * UserOutWithEmail: The updated user with the new email address.
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
     * Change the display role of the current user.
     *
     * Args:
     * ----
     * change_display_role_data (ChangeDisplayRoleSchema): The data for changing the display role.
     * user (User): The current user.
     * users_service (UserService): The service for managing users.
     *
     * Returns:
     * -------
     * UserOutWithEmail: The updated user object.
     * @param requestBody
     * @returns UserOutWithEmail Successful Response
     * @throws ApiError
     */
    public changeUserDisplayRole(
        requestBody: ChangeDisplayRoleSchema,
    ): CancelablePromise<UserOutWithEmail> {
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
     * Upload the user's avatar.
     * sharkservers.
     *
     * Returns
     * -------
     * dict: A dictionary with a success message.
     * @param formData
     * @returns string Successful Response
     * @throws ApiError
     */
    public uploadUserAvatar(
        formData: Body_users_me_upload_user_avatar,
    ): CancelablePromise<Record<string, string>> {
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
     * Connect a Steam profile to the user's account.
     *
     * Args:
     * ----
     * params (SteamAuthSchema): The parameters for Steam authentication.
     * user (User, optional): The authenticated user. Defaults to the current active user.
     * steam_auth_service (SteamAuthService, optional): The Steam authentication service. Defaults to the injected service.
     *
     * Returns:
     * -------
     * None: Nothing.
     * @param requestBody
     * @returns null Successful Response
     * @throws ApiError
     */
    public connectSteamProfile(
        requestBody: SteamAuthSchema,
    ): CancelablePromise<null> {
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
     * Retrieve the sessions of the current user.
     *
     * Args:
     * ----
     * user (User): The current user.
     *
     * Returns:
     * -------
     * list[UserSessionOut]: A list of user sessions.
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
     * Delete the user session.
     *
     * Args:
     * ----
     * user_session (UserSession): The user session to be deleted.
     *
     * Returns:
     * -------
     * UserSession: The deleted user session.
     * @param sessionId
     * @returns UserSessionOut Successful Response
     * @throws ApiError
     */
    public deleteUserSession(
        sessionId: string,
    ): CancelablePromise<UserSessionOut> {
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
