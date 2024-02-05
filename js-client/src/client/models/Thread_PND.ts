/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Category_GQC } from './Category_GQC';
import type { Post_STX } from './Post_STX';
import type { ThreadMeta_WQV } from './ThreadMeta_WQV';
import type { User_YYH } from './User_YYH';

export type Thread_PND = {
    created_at?: string;
    updated_at?: string;
    id?: string;
    title: string;
    content: string;
    is_closed?: boolean;
    is_pinned?: boolean;
    status?: string;
    category?: Category_GQC;
    author?: User_YYH;
    posts?: Array<Post_STX>;
    meta_fields?: Array<ThreadMeta_WQV>;
    post_count?: number;
};

