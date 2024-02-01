/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Group_WLC } from './Group_WLC';

/**
 * AdminOut model
 */
export type AdminOut = {
    created_at?: string;
    updated_at?: string;
    id?: number;
    authtype?: string;
    identity: string;
    password?: string;
    flags: string;
    name: string;
    immunity: number;
    groups?: Array<Group_WLC>;
};

