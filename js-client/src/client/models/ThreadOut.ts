/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { CategoryOut } from './CategoryOut';
import type { ServerOut } from './ServerOut';
import type { ThreadMetaOut } from './ThreadMetaOut';
import type { UserOut } from './UserOut';

/**
 * Thread output schema.
 */
export type ThreadOut = {
    created_at?: string;
    updated_at?: string;
    id: string;
    title: string;
    content: string;
    is_closed?: boolean;
    is_pinned?: boolean;
    status?: string;
    category: CategoryOut;
    author: UserOut;
    meta_fields?: Array<ThreadMetaOut>;
    post_count?: number;
    server?: ServerOut;
};

