/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Role_TFE } from './Role_TFE';

/**
 * Schema for retrieving a server.
 */
export type ServerOut = {
    created_at?: string;
    updated_at?: string;
    id?: number;
    name: string;
    tag: string;
    ip: string;
    port: number;
    admin_role?: Role_TFE;
    api_url: string;
};

