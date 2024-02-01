/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { AdminThreadActionSchema } from '../models/AdminThreadActionSchema';
import type { AdminUpdatePostSchema } from '../models/AdminUpdatePostSchema';
import type { AdminUpdateThreadSchema } from '../models/AdminUpdateThreadSchema';
import type { CategoryOut } from '../models/CategoryOut';
import type { CreateCategorySchema } from '../models/CreateCategorySchema';
import type { PostOut } from '../models/PostOut';
import type { ThreadOut } from '../models/ThreadOut';

import type { CancelablePromise } from '../core/CancelablePromise';
import type { BaseHttpRequest } from '../core/BaseHttpRequest';

export class AdminForumService {

    constructor(public readonly httpRequest: BaseHttpRequest) {}

    /**
     * Admin Create Category
     * Admin create category.
     *
     * Args:
     * ----
     * category_data (CreateCategorySchema): The category data.
     * categories_service (CategoryService, optional): The categories service. Defaults to Depends(get_categories_service).
     *
     * Returns:
     * -------
     * Category: The category.
     * @param requestBody
     * @returns CategoryOut Successful Response
     * @throws ApiError
     */
    public adminCreateCategory(
        requestBody: CreateCategorySchema,
    ): CancelablePromise<CategoryOut> {
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
     * Admin Delete Category
     * Delete category.
     *
     * Args:
     * ----
     * category (Category, optional): The category. Defaults to Depends(get_valid_category).
     *
     * Returns:
     * -------
     * Category: The category.
     * @param categoryId
     * @returns CategoryOut Successful Response
     * @throws ApiError
     */
    public adminDeleteCategory(
        categoryId: number,
    ): CancelablePromise<CategoryOut> {
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
     * Update thread.
     *
     * Args:
     * ----
     * update_thread_data (AdminUpdateThreadSchema): The update thread data.
     * thread (Thread, optional): The thread. Defaults to Depends(get_valid_thread).
     * threads_service (ThreadService, optional): The threads service. Defaults to Depends(get_threads_service).
     * users_service (UserService, optional): The users service. Defaults to Depends(get_users_service).
     * categories_service (CategoryService, optional): The categories service. Defaults to Depends(get_categories_service).
     *
     * Returns:
     * -------
     * Thread: The thread.
     * @param threadId
     * @param requestBody
     * @returns ThreadOut Successful Response
     * @throws ApiError
     */
    public adminUpdateThread(
        threadId: number,
        requestBody: AdminUpdateThreadSchema,
    ): CancelablePromise<ThreadOut> {
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
     * Delete thread.
     *
     * Args:
     * ----
     * thread (Thread, optional): The thread. Defaults to Depends(get_valid_thread).
     *
     * Returns:
     * -------
     * Thread: The thread.
     * @param threadId
     * @returns ThreadOut Successful Response
     * @throws ApiError
     */
    public adminDeleteThread(
        threadId: number,
    ): CancelablePromise<ThreadOut> {
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
     * Run Thread Action
     * Run thread action.
     *
     * Args:
     * ----
     * data (AdminThreadActionSchema): The data.
     * thread (Thread, optional): The thread. Defaults to Depends(get_valid_thread).
     * threads_service (ThreadService, optional): The threads service. Defaults to Depends(get_threads_service).
     * categories_service (CategoryService, optional): The categories service. Defaults to Depends(get_categories_service).
     *
     * Raises:
     * ------
     * HTTPException: The HTTP exception.
     *
     * Returns:
     * -------
     * ThreadOut: The thread.
     * @param threadId
     * @param requestBody
     * @returns ThreadOut Successful Response
     * @throws ApiError
     */
    public runThreadAction(
        threadId: number,
        requestBody: AdminThreadActionSchema,
    ): CancelablePromise<ThreadOut> {
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
     * Admin Update Post
     * Admin update post.
     *
     * Args:
     * ----
     * post_data (AdminUpdatePostSchema): The post data.
     * posts_service (PostService, optional): The posts service. Defaults to Depends(get_posts_service).
     * threads_service (ThreadService, optional): The threads service. Defaults to Depends(get_threads_service).
     * users_service (UserService, optional): The users service. Defaults to Depends(get_users_service).
     *
     * Returns:
     * -------
     * PostOut: The post.
     * @param requestBody
     * @returns PostOut Successful Response
     * @throws ApiError
     */
    public adminUpdatePost(
        requestBody: AdminUpdatePostSchema,
    ): CancelablePromise<PostOut> {
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
     * Admin delete post.
     *
     * Args:
     * ----
     * post (Post, optional): The post. Defaults to Depends(get_valid_post).
     *
     * Returns:
     * -------
     * Post: The post.
     * @param postId
     * @returns PostOut Successful Response
     * @throws ApiError
     */
    public adminDeletePost(
        postId: number,
    ): CancelablePromise<PostOut> {
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
