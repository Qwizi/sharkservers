/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

/**
 * Schema for creating a user.
 */
export type CreateUserSchema = {
    username: string;
    email: string;
    password: string;
    is_activated?: boolean;
    is_superuser?: boolean;
};

