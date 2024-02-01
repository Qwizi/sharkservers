/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Page_StaffRolesSchema_ } from '../models/Page_StaffRolesSchema_';
import type { Page_UserOut_ } from '../models/Page_UserOut_';
import type { UserOut } from '../models/UserOut';

import type { CancelablePromise } from '../core/CancelablePromise';
import type { BaseHttpRequest } from '../core/BaseHttpRequest';

export class UsersService {

    constructor(public readonly httpRequest: BaseHttpRequest) {}

    /**
     * Get Users
     * Get users
     * :param users_service:
     * :param params:
     * :return Page[UserOut]:
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
     * Get staff users
     * :param users_service:
     * :param params:
     * :return Page[UserOut]:
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
     * Get last logged users
     * :param users_service:
     * :param params:
     * :return Page[UserOut]:
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
     * Get user
     * :param user:
     * :return UserOut:
     * @param userId
     * @returns UserOut Successful Response
     * @throws ApiError
     */
    public getUser(
        userId: number,
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
     * Get user posts
     * :param posts_service:
     * :param params:
     * :param user:
     * :return AbstractPage:
     * @param userId
     * @param page
     * @param size
     * @param orderBy
     * @returns any Successful Response
     * @throws ApiError
     */
    public getUserPosts(
        userId: number,
        page: number = 1,
        size: number = 50,
        orderBy: string = '-id',
    ): CancelablePromise<any> {
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
     * Get user threads
     * :param threads_service:
     * :param params:
     * :param user:
     * :return AbstractPage:
     * @param userId
     * @param page
     * @param size
     * @param orderBy
     * @returns any Successful Response
     * @throws ApiError
     */
    public getUserThreads(
        userId: number,
        page: number = 1,
        size: number = 50,
        orderBy: string = '-id',
    ): CancelablePromise<any> {
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
