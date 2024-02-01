/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Category_NBA } from './Category_NBA';
import type { Server_DXQ } from './Server_DXQ';
import type { ThreadMeta_DJX } from './ThreadMeta_DJX';
import type { User_MZB } from './User_MZB';

/**
 * Thread output schema.
 */
export type ThreadOut = {
    created_at?: string;
    updated_at?: string;
    id?: number;
    title: string;
    content: string;
    is_closed?: boolean;
    is_pinned?: boolean;
    status?: string;
    category?: Category_NBA;
    author?: User_MZB;
    meta_fields?: Array<ThreadMeta_DJX>;
    post_count?: number;
    server?: Server_DXQ;
};

