"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.AdminForumService = void 0;
class AdminForumService {
    constructor(httpRequest) {
        this.httpRequest = httpRequest;
    }
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
    adminGetCategories(page = 1, size = 50) {
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
    adminCreateCategory(requestBody) {
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
    adminGetCategory(categoryId) {
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
    adminDeleteCategory(categoryId) {
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
    adminUpdateThread(threadId, requestBody) {
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
    adminDeleteThread(threadId) {
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
    adminCloseThread(threadId) {
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
    adminOpenThread(threadId) {
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
    runThreadAction(threadId, requestBody) {
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
    adminCreatePost(requestBody) {
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
    adminUpdatePost(requestBody) {
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
    adminDeletePost(postId) {
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
exports.AdminForumService = AdminForumService;
