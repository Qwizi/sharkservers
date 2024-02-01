/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Role_ZTD } from './Role_ZTD';

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
    admin_role?: Role_ZTD;
    api_url: string;
};

