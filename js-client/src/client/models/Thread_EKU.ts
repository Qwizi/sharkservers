/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Category_AHN } from './Category_AHN';
import type { Post_EHQ } from './Post_EHQ';
import type { Server_CLM } from './Server_CLM';
import type { ThreadMeta_TNX } from './ThreadMeta_TNX';

export type Thread_EKU = {
    created_at?: string;
    updated_at?: string;
    id?: number;
    title: string;
    content: string;
    is_closed?: boolean;
    is_pinned?: boolean;
    status?: string;
    category?: Category_AHN;
    posts?: Array<Post_EHQ>;
    meta_fields?: Array<ThreadMeta_TNX>;
    post_count?: number;
    server?: Server_CLM;
};

