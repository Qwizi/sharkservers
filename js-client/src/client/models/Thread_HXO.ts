/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Category_CEN } from './Category_CEN';
import type { Post_YRC } from './Post_YRC';
import type { Server_CMD } from './Server_CMD';
import type { ThreadMeta_MHC } from './ThreadMeta_MHC';

export type Thread_HXO = {
    created_at?: string;
    updated_at?: string;
    id?: number;
    title: string;
    content: string;
    is_closed?: boolean;
    is_pinned?: boolean;
    status?: string;
    category?: Category_CEN;
    posts?: Array<Post_YRC>;
    meta_fields?: Array<ThreadMeta_MHC>;
    post_count?: number;
    server?: Server_CMD;
};

