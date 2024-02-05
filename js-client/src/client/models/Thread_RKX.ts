/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Category_KOC } from './Category_KOC';
import type { Server_HAK } from './Server_HAK';
import type { ThreadMeta_RLM } from './ThreadMeta_RLM';

export type Thread_RKX = {
    created_at?: string;
    updated_at?: string;
    id?: string;
    title: string;
    content: string;
    is_closed?: boolean;
    is_pinned?: boolean;
    status?: string;
    category?: Category_KOC;
    meta_fields?: Array<ThreadMeta_RLM>;
    post_count?: number;
    server?: Server_HAK;
};

