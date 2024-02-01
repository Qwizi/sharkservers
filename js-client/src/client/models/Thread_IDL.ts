/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Category_VSL } from './Category_VSL';
import type { Post_ZBH } from './Post_ZBH';
import type { Server_UVD } from './Server_UVD';
import type { ThreadMeta_CSQ } from './ThreadMeta_CSQ';

export type Thread_IDL = {
    created_at?: string;
    updated_at?: string;
    id?: number;
    title: string;
    content: string;
    is_closed?: boolean;
    is_pinned?: boolean;
    status?: string;
    category?: Category_VSL;
    posts?: Array<Post_ZBH>;
    meta_fields?: Array<ThreadMeta_CSQ>;
    post_count?: number;
    server?: Server_UVD;
};

