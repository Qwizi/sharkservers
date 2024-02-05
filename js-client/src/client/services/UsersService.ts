/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Page_PostOut_ } from '../models/Page_PostOut_';
import type { Page_StaffRolesSchema_ } from '../models/Page_StaffRolesSchema_';
import type { Page_ThreadOut_ } from '../models/Page_ThreadOut_';
import type { Page_UserOut_ } from '../models/Page_UserOut_';
import type { UserOut } from '../models/UserOut';

import type { CancelablePromise } from '../core/CancelablePromise';
import type { BaseHttpRequest } from '../core/BaseHttpRequest';

export class UsersService {

    constructor(public readonly httpRequest: BaseHttpRequest) {}

    /**
     * Get Users
     * Retrieve a list of users based on the provided parameters and queries.
     *
     * Args:
     * ----
     * params (Params, optional): The parameters for pagination and filtering. Defaults to Depends().
     * queries (UserQuery, optional): The queries for filtering and ordering. Defaults to Depends().
     * users_service (UserService, optional): The service for retrieving user data. Defaults to Depends(get_users_service).
     *
     * Returns:
     * -------
     * Page[UserOut]: The paginated list of users.
     * @param page
     * @param size
     * @param orderBy
     * @param username
     * @returns Page_UserOut_ Successful Response
     * @throws ApiError
     */
    public getUsers(
        page: number = 1,
        size: number = 50,
        orderBy: string = '-id',
        username?: string,
    ): CancelablePromise<Page_UserOut_> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/v1/users',
            query: {
                'page': page,
                'size': size,
                'order_by': orderBy,
                'username': username,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Staff Users
     * Retrieve staff users based on the provided parameters.
     *
     * Args:
     * ----
     * params (Params): The parameters for filtering and pagination.
     * roles_service (RoleService): The service for retrieving staff roles.
     *
     * Returns:
     * -------
     * Page[StaffRolesSchema]: A paginated list of staff roles.
     * @param page
     * @param size
     * @returns Page_StaffRolesSchema_ Successful Response
     * @throws ApiError
     */
    public getStaffUsers(
        page: number = 1,
        size: number = 50,
    ): CancelablePromise<Page_StaffRolesSchema_> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/v1/users/staff',
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
     * Get Last Online Users
     * Retrieve the last online users based on the provided parameters.
     *
     * Args:
     * ----
     * params (Params): The parameters for filtering the users.
     * users_service (UserService): The service for retrieving user data.
     *
     * Returns:
     * -------
     * Page[UserOut]: A paginated list of UserOut objects representing the last online users.
     * @param page
     * @param size
     * @returns Page_UserOut_ Successful Response
     * @throws ApiError
     */
    public getLastOnlineUsers(
        page: number = 1,
        size: number = 50,
    ): CancelablePromise<Page_UserOut_> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/v1/users/online',
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
     * Get User
     * Retrieve the authenticated user.
     *
     * Args:
     * ----
     * user (User): The authenticated user.
     *
     * Returns:
     * -------
     * UserOut: The user object with restricted information.
     * @param userId
     * @returns UserOut Successful Response
     * @throws ApiError
     */
    public getUser(
        userId: string,
    ): CancelablePromise<UserOut> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/v1/users/{user_id}',
            path: {
                'user_id': userId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get User Posts
     * Retrieve all posts authored by a specific user.
     *
     * Args:
     * ----
     * params (Params, optional): The parameters for pagination and filtering. Defaults to Depends().
     * queries (OrderQuery, optional): The query parameters for ordering. Defaults to Depends().
     * user (User, optional): The authenticated user. Defaults to Depends(get_valid_user).
     * posts_service (PostService, optional): The service for retrieving posts. Defaults to Depends(get_posts_service).
     *
     * Returns:
     * -------
     * Page[PostOut]: A paginated list of PostOut objects.
     * @param userId
     * @param page
     * @param size
     * @param orderBy
     * @returns Page_PostOut_ Successful Response
     * @throws ApiError
     */
    public getUserPosts(
        userId: string,
        page: number = 1,
        size: number = 50,
        orderBy: string = '-id',
    ): CancelablePromise<Page_PostOut_> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/v1/users/{user_id}/posts',
            path: {
                'user_id': userId,
            },
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
     * Get User Threads
     * Retrieves all threads belonging to a specific user.
     *
     * Args:
     * ----
     * params (Params): The parameters for pagination and filtering.
     * queries (OrderQuery): The query parameters for ordering.
     * user (User): The authenticated user.
     * threads_service (ThreadService): The service for managing threads.
     *
     * Returns:
     * -------
     * Page[ThreadOut]: A paginated list of threads belonging to the user.
     * @param userId
     * @param page
     * @param size
     * @param orderBy
     * @returns Page_ThreadOut_ Successful Response
     * @throws ApiError
     */
    public getUserThreads(
        userId: string,
        page: number = 1,
        size: number = 50,
        orderBy: string = '-id',
    ): CancelablePromise<Page_ThreadOut_> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/v1/users/{user_id}/threads',
            path: {
                'user_id': userId,
            },
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

}
