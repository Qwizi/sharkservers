"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.ForumService = void 0;
class ForumService {
    constructor(httpRequest) {
        this.httpRequest = httpRequest;
    }
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
    getCategories(page = 1, size = 50, orderBy = '-id') {
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
    getCategory(categoryId) {
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
    getThreads(page = 1, size = 50, orderBy = '-id', category, server, status, closed) {
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
    createThread(requestBody) {
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
    getThread(threadId) {
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
    updateThread(threadId, requestBody) {
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
    getPosts(threadId, page = 1, size = 50, orderBy = '-id') {
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
    createPost(requestBody) {
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
    getPostById(postId) {
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
    updatePost(postId, requestBody) {
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
    getPostLikes(postId, page = 1, size = 50) {
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
    likePost(postId) {
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
    dislikePost(postId) {
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
exports.ForumService = ForumService;
