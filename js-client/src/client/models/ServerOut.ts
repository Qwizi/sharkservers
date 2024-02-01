/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Role_HSI } from './Role_HSI';

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
    admin_role?: Role_HSI;
    api_url: string;
};

