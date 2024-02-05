/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Role_JUT } from './Role_JUT';
import type { Thread_BWB } from './Thread_BWB';

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
    admin_role?: Role_JUT;
    api_url: string;
    thread_server?: Array<Thread_BWB>;
};

