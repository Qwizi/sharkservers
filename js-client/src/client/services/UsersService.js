"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.UsersService = void 0;
class UsersService {
    constructor(httpRequest) {
        this.httpRequest = httpRequest;
    }
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
    getUsers(page = 1, size = 50, orderBy = '-id', username) {
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
    getStaffUsers(page = 1, size = 50) {
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
    getLastOnlineUsers(page = 1, size = 50) {
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
    getUser(userId) {
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
    getUserPosts(userId, page = 1, size = 50, orderBy = '-id') {
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
    getUserThreads(userId, page = 1, size = 50, orderBy = '-id') {
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
exports.UsersService = UsersService;
