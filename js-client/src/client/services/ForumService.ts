/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CategoryOut } from '../models/CategoryOut';
import type { CreatePostSchema } from '../models/CreatePostSchema';
import type { CreateThreadSchema } from '../models/CreateThreadSchema';
import type { LikeOut } from '../models/LikeOut';
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
     *
     * Args:
     * ----
     * params (Params, optional): The params. Defaults to Depends().
     * queries (OrderQuery, optional): The queries. Defaults to Depends().
     * categories_service (CategoryService, optional): The categories service. Defaults to Depends(get_categories_service).
     *
     * Returns:
     * -------
     * Page[CategoryOut]: The categories.
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
     * Get a category.
     *
     * Args:
     * ----
     * category (Category, optional): The category. Defaults to Depends(get_valid_category).
     *
     * Returns:
     * -------
     * CategoryOut: The category.
     * @param categoryId
     * @returns CategoryOut Successful Response
     * @throws ApiError
     */
    public getCategory(
        categoryId: string,
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
     *
     * Args:
     * ----
     * params (Params, optional): The params. Defaults to Depends().
     * queries (ThreadQuery, optional): The queries. Defaults to Depends().
     * threads_service (ThreadService, optional): The threads service. Defaults to Depends(get_threads_service).
     *
     * Returns:
     * -------
     * Page[ThreadOut]: The threads.
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
     * Create thread.
     *
     * Args:
     * ----
     * thread_data (CreateThreadSchema): The thread data.
     * user (User, optional): The user. Defaults to Security(get_current_active_user, scopes=["threads:create"]).
     * threads_service (ThreadService, optional): The threads service. Defaults to Depends(get_threads_service).
     * categories_service (CategoryService, optional): The categories service. Defaults to Depends(get_categories_service).
     * thread_meta_service (ThreadMetaService, optional): The thread meta service. Defaults to Depends(get_thread_meta_service).
     * servers_service (ServerService, optional): The servers service. Defaults to Depends(get_servers_service).
     *
     *
     * Returns:
     * -------
     * ThreadOut: The thread.
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
     *
     * Args:
     * ----
     * thread (Thread, optional): The thread. Defaults to Depends(get_valid_thread).
     *
     * Returns:
     * -------
     * ThreadOut: The thread.
     * @param threadId
     * @returns ThreadOut Successful Response
     * @throws ApiError
     */
    public getThread(
        threadId: string,
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
     *
     * Args:
     * ----
     * thread_data (UpdateThreadSchema): The thread data.
     * thread (Thread, optional): The thread. Defaults to Depends(get_valid_thread_with_author).
     *
     * Returns:
     * -------
     * ThreadOut: The thread.
     * @param threadId
     * @param requestBody
     * @returns ThreadOut Successful Response
     * @throws ApiError
     */
    public updateThread(
        threadId: string,
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
     * Get all posts.
     *
     * Args:
     * ----
     * thread_id (int, optional): The thread ID. Defaults to None.
     * params (Params, optional): The params. Defaults to Depends().
     * queries (PostQuery, optional): The queries. Defaults to Depends().
     * posts_service (PostService, optional): The posts service. Defaults to Depends(get_posts_service).
     *
     * Returns:
     * -------
     * Page[PostOut]: The posts.
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
     * Create post.
     *
     * Args:
     * ----
     * post_data (CreatePostSchema): The post data.
     * user (User, optional): The user. Defaults to Security(get_current_active_user, scopes=["posts:create"]).
     * posts_service (PostService, optional): The posts service. Defaults to Depends(get_posts_service).
     * threads_service (ThreadService, optional): The threads service. Defaults to Depends(get_threads_service).
     *
     * Raises:
     * ------
     * thread_is_closed_exception: The thread is closed exception.
     *
     * Returns:
     * -------
     * PostOut: The post.
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
     * Get post by ID.
     *
     * Args:
     * ----
     * post (Post): The post. Defaults to Depends(get_valid_post).
     *
     * Returns:
     * -------
     * Post: The post.
     * @param postId
     * @returns PostOut Successful Response
     * @throws ApiError
     */
    public getPostById(
        postId: string,
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
     * Update post.
     *
     * Args:
     * ----
     * post_data (UpdatePostSchema): The post data.
     * post (Post, optional): The post. Defaults to Depends(get_valid_post_author).
     *
     * Returns:
     * -------
     * Post: The post.
     * @param postId
     * @param requestBody
     * @returns PostOut Successful Response
     * @throws ApiError
     */
    public updatePost(
        postId: string,
        requestBody: UpdatePostSchema,
    ): CancelablePromise<PostOut> {
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
     * Get post likes.
     *
     * Args:
     * ----
     * post (Post, optional): The post. Defaults to Depends(get_valid_post).
     * likes_service (LikeService, optional): The likes service. Defaults to Depends(get_likes_service).
     * params (Params, optional): The params. Defaults to Depends().
     *
     * Returns:
     * -------
     * Page[LikeOut]: The likes.
     * @param postId
     * @param page
     * @param size
     * @returns Page_LikeOut_ Successful Response
     * @throws ApiError
     */
    public getPostLikes(
        postId: string,
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
     *
     * Args:
     * ----
     * post (Post, optional): The post. Defaults to Depends(get_valid_post).
     * user (User, optional): The user. Defaults to Security(get_current_active_user, scopes=["posts:create"]).
     * likes_service (LikeService, optional): The likes service. Defaults to Depends(get_likes_service).
     *
     * Returns:
     * -------
     * LikeOut: The like.
     * @param postId
     * @returns LikeOut Successful Response
     * @throws ApiError
     */
    public likePost(
        postId: string,
    ): CancelablePromise<LikeOut> {
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
     *
     * Args:
     * ----
     * post (Post, optional): The post. Defaults to Depends(get_valid_post).
     * user (User, optional): The user. Defaults to Security(get_current_active_user, scopes=["posts:create"]).
     * likes_service (LikeService, optional): The likes service. Defaults to Depends(get_likes_service).
     *
     * Returns:
     * -------
     * dict: The response.
     * @param postId
     * @returns any Successful Response
     * @throws ApiError
     */
    public dislikePost(
        postId: string,
    ): CancelablePromise<Record<string, any>> {
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
