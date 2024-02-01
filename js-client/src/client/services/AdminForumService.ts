/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { AdminCreatePostSchema } from '../models/AdminCreatePostSchema';
import type { AdminThreadActionSchema } from '../models/AdminThreadActionSchema';
import type { AdminUpdatePostSchema } from '../models/AdminUpdatePostSchema';
import type { AdminUpdateThreadSchema } from '../models/AdminUpdateThreadSchema';
import type { CategoryOut } from '../models/CategoryOut';
import type { CreateCategorySchema } from '../models/CreateCategorySchema';
import type { Page_CategoryOut_ } from '../models/Page_CategoryOut_';

import type { CancelablePromise } from '../core/CancelablePromise';
import type { BaseHttpRequest } from '../core/BaseHttpRequest';

export class AdminForumService {

    constructor(public readonly httpRequest: BaseHttpRequest) {}

    /**
     * Admin Get Categories
     * Get all categories.
     * :param categories_service:
     * :param params:
     * :return:
     * @param page
     * @param size
     * @returns Page_CategoryOut_ Successful Response
     * @throws ApiError
     */
    public adminGetCategories(
        page: number = 1,
        size: number = 50,
    ): CancelablePromise<Page_CategoryOut_> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/v1/admin/forum/categories',
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
     * Admin Create Category
     * Create category
     * :param categories_service:
     * :param category_data:
     * :return:
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public adminCreateCategory(
        requestBody: CreateCategorySchema,
    ): CancelablePromise<any> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/v1/admin/forum/categories',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Admin Get Category
     * Get category
     * :param category:
     * :return:
     * @param categoryId
     * @returns CategoryOut Successful Response
     * @throws ApiError
     */
    public adminGetCategory(
        categoryId: number,
    ): CancelablePromise<CategoryOut> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/v1/admin/forum/categories/{category_id}',
            path: {
                'category_id': categoryId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Admin Delete Category
     * Delete category
     * :param categories_service:
     * :param user:
     * :param category:
     * :return:
     * @param categoryId
     * @returns any Successful Response
     * @throws ApiError
     */
    public adminDeleteCategory(
        categoryId: number,
    ): CancelablePromise<any> {
        return this.httpRequest.request({
            method: 'DELETE',
            url: '/v1/admin/forum/categories/{category_id}',
            path: {
                'category_id': categoryId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Admin Update Thread
     * @param threadId
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public adminUpdateThread(
        threadId: number,
        requestBody: AdminUpdateThreadSchema,
    ): CancelablePromise<any> {
        return this.httpRequest.request({
            method: 'PUT',
            url: '/v1/admin/forum/threads/{thread_id}',
            path: {
                'thread_id': threadId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Admin Delete Thread
     * @param threadId
     * @returns any Successful Response
     * @throws ApiError
     */
    public adminDeleteThread(
        threadId: number,
    ): CancelablePromise<any> {
        return this.httpRequest.request({
            method: 'DELETE',
            url: '/v1/admin/forum/threads/{thread_id}',
            path: {
                'thread_id': threadId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Admin Close Thread
     * @param threadId
     * @returns any Successful Response
     * @throws ApiError
     */
    public adminCloseThread(
        threadId: number,
    ): CancelablePromise<any> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/v1/admin/forum/threads/{thread_id}/close',
            path: {
                'thread_id': threadId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Admin Open Thread
     * @param threadId
     * @returns any Successful Response
     * @throws ApiError
     */
    public adminOpenThread(
        threadId: number,
    ): CancelablePromise<any> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/v1/admin/forum/threads/{thread_id}/open',
            path: {
                'thread_id': threadId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Run Thread Action
     * Run thread action
     * :return:
     * @param threadId
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public runThreadAction(
        threadId: number,
        requestBody: AdminThreadActionSchema,
    ): CancelablePromise<any> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/v1/admin/forum/threads/{thread_id}/action',
            path: {
                'thread_id': threadId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Admin Create Post
     * Create post
     * :param posts_service:
     * :param post_data:
     * :param thread:
     * :param user:
     * :return:
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public adminCreatePost(
        requestBody: AdminCreatePostSchema,
    ): CancelablePromise<any> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/v1/admin/forum/posts/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Admin Update Post
     * Update post
     * :param posts_service:
     * :param post:
     * :param post_data:
     * :param user:
     * :return:
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public adminUpdatePost(
        requestBody: AdminUpdatePostSchema,
    ): CancelablePromise<any> {
        return this.httpRequest.request({
            method: 'PUT',
            url: '/v1/admin/forum/posts/{post_id}',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Admin Delete Post
     * Delete post
     * :param posts_service:
     * :param post:
     * :param user:
     * :return:
     * @param postId
     * @returns any Successful Response
     * @throws ApiError
     */
    public adminDeletePost(
        postId: number,
    ): CancelablePromise<any> {
        return this.httpRequest.request({
            method: 'DELETE',
            url: '/v1/admin/forum/posts/{post_id}',
            path: {
                'post_id': postId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

}
