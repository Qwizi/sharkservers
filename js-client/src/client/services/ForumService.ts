/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CategoryOut } from '../models/CategoryOut';
import type { CreatePostSchema } from '../models/CreatePostSchema';
import type { CreateThreadSchema } from '../models/CreateThreadSchema';
import type { Page_CategoryOut_ } from '../models/Page_CategoryOut_';
import type { Page_LikeOut_ } from '../models/Page_LikeOut_';
import type { Page_PostOut_ } from '../models/Page_PostOut_';
import type { Page_ThreadOut_ } from '../models/Page_ThreadOut_';
import type { PostOut } from '../models/PostOut';
import type { ThreadOut } from '../models/ThreadOut';
import type { UpdatePostSchema } from '../models/UpdatePostSchema';
import type { UpdateThreadSchema } from '../models/UpdateThreadSchema';

import type { CancelablePromise } from '../core/CancelablePromise';
import type { BaseHttpRequest } from '../core/BaseHttpRequest';

export class ForumService {

    constructor(public readonly httpRequest: BaseHttpRequest) {}

    /**
     * Get Categories
     * Get all categories.
     * :param categories_service:
     * :param params:
     * :return:
     * @param page
     * @param size
     * @param orderBy
     * @returns Page_CategoryOut_ Successful Response
     * @throws ApiError
     */
    public getCategories(
        page: number = 1,
        size: number = 50,
        orderBy: string = '-id',
    ): CancelablePromise<Page_CategoryOut_> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/v1/forum/categories',
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
     * Get Category
     * Get category
     * :param category:
     * :return:
     * @param categoryId
     * @returns CategoryOut Successful Response
     * @throws ApiError
     */
    public getCategory(
        categoryId: number,
    ): CancelablePromise<CategoryOut> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/v1/forum/categories/{category_id}',
            path: {
                'category_id': categoryId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Threads
     * Get all threads.
     * :param threads_service:
     * :param category_id:
     * :param params:
     * :return:
     * @param page
     * @param size
     * @param orderBy
     * @param category
     * @param server
     * @param status
     * @param closed
     * @returns Page_ThreadOut_ Successful Response
     * @throws ApiError
     */
    public getThreads(
        page: number = 1,
        size: number = 50,
        orderBy: string = '-id',
        category?: number,
        server?: number,
        status?: string,
        closed?: boolean,
    ): CancelablePromise<Page_ThreadOut_> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/v1/forum/threads',
            query: {
                'page': page,
                'size': size,
                'order_by': orderBy,
                'category': category,
                'server': server,
                'status': status,
                'closed': closed,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Create Thread
     * Create new thread.
     * :param thread_meta_service:
     * :param categories_service:
     * :param threads_service:
     * :param thread_data:
     * :param user:
     * :return:
     * @param requestBody
     * @returns ThreadOut Successful Response
     * @throws ApiError
     */
    public createThread(
        requestBody: CreateThreadSchema,
    ): CancelablePromise<ThreadOut> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/v1/forum/threads',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Thread
     * Get thread by id.
     * :param thread:
     * :return:
     * @param threadId
     * @returns ThreadOut Successful Response
     * @throws ApiError
     */
    public getThread(
        threadId: number,
    ): CancelablePromise<ThreadOut> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/v1/forum/threads/{thread_id}',
            path: {
                'thread_id': threadId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Update Thread
     * Update thread by id.
     * :param thread_data:
     * :param thread:
     * :return:
     * @param threadId
     * @param requestBody
     * @returns ThreadOut Successful Response
     * @throws ApiError
     */
    public updateThread(
        threadId: number,
        requestBody: UpdateThreadSchema,
    ): CancelablePromise<ThreadOut> {
        return this.httpRequest.request({
            method: 'PUT',
            url: '/v1/forum/threads/{thread_id}',
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
     * Get Posts
     * Get all posts by thread id.
     * :param posts_service:
     * :param thread_id:
     * :param params:
     * :return:
     * @param threadId
     * @param page
     * @param size
     * @param orderBy
     * @returns Page_PostOut_ Successful Response
     * @throws ApiError
     */
    public getPosts(
        threadId?: number,
        page: number = 1,
        size: number = 50,
        orderBy: string = '-id',
    ): CancelablePromise<Page_PostOut_> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/v1/forum/posts',
            query: {
                'thread_id': threadId,
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
     * Create Post
     * :param threads_service:
     * :param posts_service:
     * :param post_data:
     * :param user:
     * :return:
     * @param requestBody
     * @returns PostOut Successful Response
     * @throws ApiError
     */
    public createPost(
        requestBody: CreatePostSchema,
    ): CancelablePromise<PostOut> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/v1/forum/posts',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Post By Id
     * Get post by id.
     * :param post:
     * :return:
     * @param postId
     * @returns PostOut Successful Response
     * @throws ApiError
     */
    public getPostById(
        postId: number,
    ): CancelablePromise<PostOut> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/v1/forum/posts/{post_id}',
            path: {
                'post_id': postId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Update Post
     * @param postId
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public updatePost(
        postId: number,
        requestBody: UpdatePostSchema,
    ): CancelablePromise<any> {
        return this.httpRequest.request({
            method: 'PUT',
            url: '/v1/forum/posts/{post_id}',
            path: {
                'post_id': postId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Post Likes
     * Get all post likes.
     * :param post:
     * :param likes_service:
     * :return:
     * @param postId
     * @param page
     * @param size
     * @returns Page_LikeOut_ Successful Response
     * @throws ApiError
     */
    public getPostLikes(
        postId: number,
        page: number = 1,
        size: number = 50,
    ): CancelablePromise<Page_LikeOut_> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/v1/forum/posts/{post_id}/likes',
            path: {
                'post_id': postId,
            },
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
     * Like Post
     * Like post.
     * :param post:
     * :param user:
     * :param likes_service:
     * :return:
     * @param postId
     * @returns any Successful Response
     * @throws ApiError
     */
    public likePost(
        postId: number,
    ): CancelablePromise<any> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/v1/forum/posts/{post_id}/like',
            path: {
                'post_id': postId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Dislike Post
     * Dislike post.
     * :param post:
     * :param user:
     * :param likes_service:
     * :return:
     * @param postId
     * @returns any Successful Response
     * @throws ApiError
     */
    public dislikePost(
        postId: number,
    ): CancelablePromise<any> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/v1/forum/posts/{post_id}/dislike',
            path: {
                'post_id': postId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

}
