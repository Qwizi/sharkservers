/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { User_WTM } from './User_WTM';

/**
 * Post output schema.
 */
export type PostOut = {
    created_at?: string;
    updated_at?: string;
    id?: number;
    author?: User_WTM;
    content: string;
    likes_count?: number;
};

