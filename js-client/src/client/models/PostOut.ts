/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { LikeOut } from './LikeOut';
import type { UserOut } from './UserOut';

/**
 * Post output schema.
 */
export type PostOut = {
    created_at?: string;
    updated_at?: string;
    id: string;
    author: UserOut;
    content: string;
    likes_count?: number;
    likes?: Array<LikeOut>;
};

