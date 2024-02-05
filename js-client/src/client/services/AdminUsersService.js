"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.AdminUsersService = void 0;
class AdminUsersService {
    constructor(httpRequest) {
        this.httpRequest = httpRequest;
    }
    /**
     * Admin Get Users
     * Retrieve all users with their associated data.
     *
     * Args:
     * ----
     * params (Params, optional): The parameters for filtering and pagination. Defaults to Depends().
     * users_service (UserService, optional): The service for retrieving user data. Defaults to Depends(get_users_service).
     *
     * Returns:
     * -------
     * Page[UserOutWithEmail]: The paginated list of users with their associated data.
     * @param page
     * @param size
     * @returns Page_UserOutWithEmail_ Successful Response
     * @throws ApiError
     */
    adminGetUsers(page = 1, size = 50) {
        return this.httpRequest.request({
            method: 'GET',
            url: '/v1/admin/users',
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
     * Admin Create User
     * Create a new user with the provi    print(roles)
     * ded user data.
     *
     *
     * Args:
     * ----
     * user_data (CreateUserSchema): The data for creating a new user.
     * auth_service (AuthService, optional): The authentication service. Defaults to Depends(get_auth_service).
     * settings (Settings, optional): The application settings. Defaults to Depends(get_settings).
     *
     * Returns:
     * -------
     * UserOutWithEmail: The created user with email.
     * @param requestBody
     * @returns UserOutWithEmail Successful Response
     * @throws ApiError
     */
    adminCreateUser(requestBody) {
        return this.httpRequest.request({
            method: 'POST',
            url: '/v1/admin/users',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Admin Get User
     * Retrieve the user information for an admin user.
     *
     * Args:
     * ----
     * user (User): The admin user object.
     *
     * Returns:
     * -------
     * UserOutWithEmail: The user information with email.
     * @param userId
     * @returns UserOutWithEmail Successful Response
     * @throws ApiError
     */
    adminGetUser(userId) {
        return this.httpRequest.request({
            method: 'GET',
            url: '/v1/admin/users/{user_id}',
            path: {
                'user_id': userId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Admin Update User
     * Admin function to update a user's information.
     *
     * Args:
     * ----
     * update_user_data (AdminUpdateUserSchema): The updated user data.
     * validate_user (User): The user to be updated.
     * roles_service (RoleService): The service for managing roles.
     *
     * Returns:
     * -------
     * UserOutWithEmail: The updated user with email.
     * @param userId
     * @param requestBody
     * @returns UserOutWithEmail Successful Response
     * @throws ApiError
     */
    adminUpdateUser(userId, requestBody) {
        return this.httpRequest.request({
            method: 'PUT',
            url: '/v1/admin/users/{user_id}',
            path: {
                'user_id': userId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Admin Delete User
     * Deletes a user from the system.
     *
     * Args:
     * ----
     * validate_user (User): The user to be deleted.
     * users_service (UserService): The service responsible for user operations.
     *
     * Returns:
     * -------
     * UserOutWithEmail: The deleted user with email.
     * @param userId
     * @returns UserOutWithEmail Successful Response
     * @throws ApiError
     */
    adminDeleteUser(userId) {
        return this.httpRequest.request({
            method: 'DELETE',
            url: '/v1/admin/users/{user_id}',
            path: {
                'user_id': userId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
exports.AdminUsersService = AdminUsersService;
