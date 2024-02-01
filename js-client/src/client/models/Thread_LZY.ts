/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Category_UYW } from './Category_UYW';
import type { Post_CSI } from './Post_CSI';
import type { Server_MTQ } from './Server_MTQ';
import type { ThreadMeta_XDD } from './ThreadMeta_XDD';

export type Thread_LZY = {
    created_at?: string;
    updated_at?: string;
    id?: number;
    title: string;
    content: string;
    is_closed?: boolean;
    is_pinned?: boolean;
    status?: string;
    category?: Category_UYW;
    posts?: Array<Post_CSI>;
    meta_fields?: Array<ThreadMeta_XDD>;
    post_count?: number;
    server?: Server_MTQ;
};

