/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

/**
 * Schema for changing password.
 *
 * Attributes
 * ----------
 * current_password (str): The current password.
 * new_password (str): The new password.
 * new_password2 (str): The confirmation of the new password.
 *
 * Raises
 * ------
 * ValueError: If the new_password2 does not match the new_password.
 */
export type ChangePasswordSchema = {
    current_password: string;
    new_password: string;
    new_password2: string;
};

