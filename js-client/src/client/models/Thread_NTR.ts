/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Category_AJS } from './Category_AJS';
import type { Post_QKB } from './Post_QKB';
import type { Server_CYF } from './Server_CYF';
import type { ThreadMeta_ZJN } from './ThreadMeta_ZJN';

export type Thread_NTR = {
    created_at?: string;
    updated_at?: string;
    id?: number;
    title: string;
    content: string;
    is_closed?: boolean;
    is_pinned?: boolean;
    status?: string;
    category?: Category_AJS;
    posts?: Array<Post_QKB>;
    meta_fields?: Array<ThreadMeta_ZJN>;
    post_count?: number;
    server?: Server_CYF;
};

