/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

export type AdminUpdateUserSchema = {
    username?: string;
    email?: string;
    password?: string;
    is_activated?: boolean;
    is_superuser?: boolean;
    avatar?: string;
    roles?: Array<number>;
    display_role?: number;
    secret_salt?: string;
};

