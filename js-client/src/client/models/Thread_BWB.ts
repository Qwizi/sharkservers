/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Category_GNK } from './Category_GNK';
import type { Post_YMB } from './Post_YMB';
import type { ThreadMeta_PXJ } from './ThreadMeta_PXJ';
import type { User_BBX } from './User_BBX';

export type Thread_BWB = {
    created_at?: string;
    updated_at?: string;
    id?: string;
    title: string;
    content: string;
    is_closed?: boolean;
    is_pinned?: boolean;
    status?: string;
    category?: Category_GNK;
    author?: User_BBX;
    posts?: Array<Post_YMB>;
    meta_fields?: Array<ThreadMeta_PXJ>;
    post_count?: number;
};

