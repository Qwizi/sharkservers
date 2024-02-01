/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Category_IHZ } from './Category_IHZ';
import type { Post_VJU } from './Post_VJU';
import type { Server_WIO } from './Server_WIO';
import type { ThreadMeta_SKI } from './ThreadMeta_SKI';

export type Thread_FBF = {
    created_at?: string;
    updated_at?: string;
    id?: number;
    title: string;
    content: string;
    is_closed?: boolean;
    is_pinned?: boolean;
    status?: string;
    category?: Category_IHZ;
    posts?: Array<Post_VJU>;
    meta_fields?: Array<ThreadMeta_SKI>;
    post_count?: number;
    server?: Server_WIO;
};

