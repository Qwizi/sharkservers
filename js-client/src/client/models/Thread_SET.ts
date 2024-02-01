/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Category_AIC } from './Category_AIC';
import type { Post_YIT } from './Post_YIT';
import type { Server_XXZ } from './Server_XXZ';
import type { ThreadMeta_AYW } from './ThreadMeta_AYW';

export type Thread_SET = {
    created_at?: string;
    updated_at?: string;
    id?: number;
    title: string;
    content: string;
    is_closed?: boolean;
    is_pinned?: boolean;
    status?: string;
    category?: Category_AIC;
    posts?: Array<Post_YIT>;
    meta_fields?: Array<ThreadMeta_AYW>;
    post_count?: number;
    server?: Server_XXZ;
};

