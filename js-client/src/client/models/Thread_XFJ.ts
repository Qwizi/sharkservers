/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Category_ESQ } from './Category_ESQ';
import type { Server_FUT } from './Server_FUT';
import type { ThreadMeta_NFV } from './ThreadMeta_NFV';

export type Thread_XFJ = {
    created_at?: string;
    updated_at?: string;
    id?: string;
    title: string;
    content: string;
    is_closed?: boolean;
    is_pinned?: boolean;
    status?: string;
    category?: Category_ESQ;
    meta_fields?: Array<ThreadMeta_NFV>;
    post_count?: number;
    server?: Server_FUT;
};

