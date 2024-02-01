/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Category_NBA } from './Category_NBA';
import type { Post_IVP } from './Post_IVP';
import type { Server_LJL } from './Server_LJL';
import type { ThreadMeta_DJX } from './ThreadMeta_DJX';

export type Thread_JGW = {
    created_at?: string;
    updated_at?: string;
    id?: number;
    title: string;
    content: string;
    is_closed?: boolean;
    is_pinned?: boolean;
    status?: string;
    category?: Category_NBA;
    posts?: Array<Post_IVP>;
    meta_fields?: Array<ThreadMeta_DJX>;
    post_count?: number;
    server?: Server_LJL;
};

