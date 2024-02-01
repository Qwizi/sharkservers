/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { User_NMI } from './User_NMI';

/**
 * Post output schema.
 */
export type PostOut = {
    created_at?: string;
    updated_at?: string;
    id?: number;
    author?: User_NMI;
    content: string;
    likes_count?: number;
};

