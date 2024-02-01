"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.AuthService = void 0;
class AuthService {
    constructor(httpRequest) {
        this.httpRequest = httpRequest;
    }
    /**
     * Register
     * Register a new user.
     *
     * Args:
     * ----
     * user_data (RegisterUserSchema): The user data to register.
     * background_tasks (BackgroundTasks): The background tasks object.
     * request (Request): The request object.
     * auth_service (AuthService, optional): The authentication service. Defaults to Depends(get_auth_service).
     * code_service (CodeService, optional): The code service. Defaults to Depends(get_activation_account_code_service).
     * email_service (EmailService, optional): The email service. Defaults to Depends(get_email_service).
     * settings (Settings, optional): The settings object. Defaults to Depends(get_settings).
     *
     * Returns:
     * -------
     * UserOut: The registered user.
     * @param requestBody
     * @returns UserOut Successful Response
     * @throws ApiError
     */
    register(requestBody) {
        return this.httpRequest.request({
            method: 'POST',
            url: '/v1/auth/register',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Login User
     * Log in a user and returns a token.
     *
     * Args:
     * ----
     * request (Request): The incoming request object.
     * form_data (OAuth2PasswordRequestForm, optional): The form data containing the user's credentials. Defaults to Depends().
     * access_token_service (JWTService, optional): The service for generating access tokens. Defaults to Depends(get_access_token_service).
     * refresh_token_service (JWTService, optional): The service for generating refresh tokens. Defaults to Depends(get_refresh_token_service).
     * auth_service (AuthService, optional): The service for handling authentication. Defaults to Depends(get_auth_service).
     *
     * Returns:
     * -------
     * TokenSchema: The token schema containing the access token.
     * @param formData
     * @returns TokenSchema Successful Response
     * @throws ApiError
     */
    loginUser(formData) {
        return this.httpRequest.request({
            method: 'POST',
            url: '/v1/auth/token',
            formData: formData,
            mediaType: 'application/x-www-form-urlencoded',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Access Token From Refresh Token
     * Retrieve an access token from a refresh token.
     *
     * Args:
     * ----
     * token_data (RefreshTokenSchema): The refresh token data.
     * access_token_service (JWTService, optional): The access token service. Defaults to Depends(get_access_token_service).
     * refresh_token_service (JWTService, optional): The refresh token service. Defaults to Depends(get_refresh_token_service).
     * auth_service (AuthService, optional): The authentication service. Defaults to Depends(get_auth_service).
     *
     * Returns:
     * -------
     * TokenSchema: The access token.
     * @param requestBody
     * @returns TokenSchema Successful Response
     * @throws ApiError
     */
    getAccessTokenFromRefreshToken(requestBody) {
        return this.httpRequest.request({
            method: 'POST',
            url: '/v1/auth/token/refresh',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Logout User
     * Log out the user.
     *
     * Args:
     * ----
     * user (User): The user to be logged out.
     * auth_service (AuthService): The authentication service.
     *
     * Returns:
     * -------
     * UserOut: The logged out user.
     * @returns UserOut Successful Response
     * @throws ApiError
     */
    logoutUser() {
        return this.httpRequest.request({
            method: 'POST',
            url: '/v1/auth/logout',
        });
    }
    /**
     * Activate User
     * Activate a user account using the provided activation code.
     *
     * Args:
     * ----
     * activate_code_data (ActivateUserCodeSchema): The activation code data.
     * auth_service (AuthService): The authentication service.
     * activate_code_service (CodeService): The activation code service.
     *
     * Returns:
     * -------
     * UserActivatedSchema: The activated user data.
     *
     * Raises:
     * ------
     * invalid_activation_code_exception: If the activation code is invalid.
     * @param requestBody
     * @returns UserActivatedSchema Successful Response
     * @throws ApiError
     */
    activateUser(requestBody) {
        return this.httpRequest.request({
            method: 'POST',
            url: '/v1/auth/activate',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Resend Activate Code
     * Resends the activation code to the specified email address.
     *
     * Args:
     * ----
     * data (ResendActivationCodeSchema): The data containing the email address.
     * background_tasks (BackgroundTasks): The background tasks manager.
     * auth_service (AuthService): The authentication service.
     * code_service (CodeService): The activation code service.
     * email_service (EmailService): The email service.
     *
     * Returns:
     * -------
     * dict[str, str]: A dictionary with a message indicating if the email is correct and an email with the activation code will be sent.
     * @param requestBody
     * @returns string Successful Response
     * @throws ApiError
     */
    resendActivateCode(requestBody) {
        return this.httpRequest.request({
            method: 'POST',
            url: '/v1/auth/activate/resend',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Forgot Password Request
     * Send a request to reset the account password.
     *
     * Args:
     * ----
     * data (ResendActivationCodeSchema): The data containing the email address.
     * background_tasks (BackgroundTasks): The background tasks manager.
     * auth_service (AuthService): The authentication service.
     * email_service (EmailService): The email service.
     * code_service (CodeService): The code service for resetting the account password.
     *
     * Returns:
     * -------
     * dict[str, str]: A dictionary with a message indicating that an email with the reset code will be sent if the email is correct.
     * @param requestBody
     * @returns string Successful Response
     * @throws ApiError
     */
    forgotPasswordRequest(requestBody) {
        return this.httpRequest.request({
            method: 'POST',
            url: '/v1/auth/forgot-password',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Reset Password
     * Reset the password for a user account.
     *
     * Args:
     * ----
     * data (ResetPasswordSchema): The data containing the password reset information.
     * auth_service (AuthService): The authentication service.
     * code_service (CodeService): The code service for resetting the account password.
     *
     * Returns:
     * -------
     * dict: A dictionary with a message indicating that the password has been reset.
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    resetPassword(requestBody) {
        return this.httpRequest.request({
            method: 'POST',
            url: '/v1/auth/reset-password',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
exports.AuthService = AuthService;
