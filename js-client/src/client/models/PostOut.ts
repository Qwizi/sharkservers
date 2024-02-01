/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { User_PRS } from './User_PRS';

/**
 * Post output schema.
 */
export type PostOut = {
    created_at?: string;
    updated_at?: string;
    id?: number;
    author?: User_PRS;
    content: string;
    likes_count?: number;
};

