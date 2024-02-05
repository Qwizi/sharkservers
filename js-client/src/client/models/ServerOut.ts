/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Role_BTL } from './Role_BTL';
import type { Thread_PND } from './Thread_PND';

/**
 * Schema for retrieving a server.
 */
export type ServerOut = {
    created_at?: string;
    updated_at?: string;
    id: string;
    name: string;
    tag: string;
    ip: string;
    port: number;
    admin_role?: Role_BTL;
    api_url: string;
    thread_server?: Array<Thread_PND>;
};

