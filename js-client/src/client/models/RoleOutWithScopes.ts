/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Scope_OUE } from './Scope_OUE';

/**
 * RoleOutWithScopes schema.
 */
export type RoleOutWithScopes = {
    created_at?: string;
    updated_at?: string;
    id?: number;
    tag: string;
    name: string;
    color?: string;
    scopes?: Array<Scope_OUE>;
    is_staff?: boolean;
};

