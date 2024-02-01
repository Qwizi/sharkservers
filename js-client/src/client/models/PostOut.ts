/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { User_DFG } from './User_DFG';

/**
 * Post output schema.
 */
export type PostOut = {
    created_at?: string;
    updated_at?: string;
    id?: number;
    author?: User_DFG;
    content: string;
    likes_count?: number;
};

