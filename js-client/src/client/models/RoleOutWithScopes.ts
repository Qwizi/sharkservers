/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { ScopeOut } from './ScopeOut';

/**
 * RoleOutWithScopes schema.
 */
export type RoleOutWithScopes = {
    created_at?: string;
    updated_at?: string;
    id: string;
    tag: string;
    name: string;
    color?: string;
    scopes: Array<ScopeOut>;
    is_staff?: boolean;
};

