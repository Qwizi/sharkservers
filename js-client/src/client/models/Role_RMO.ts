/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Scope_SBW } from './Scope_SBW';

export type Role_RMO = {
    created_at?: string;
    updated_at?: string;
    id?: number;
    tag: string;
    name: string;
    color?: string;
    scopes?: Array<Scope_SBW>;
    is_staff?: boolean;
};

