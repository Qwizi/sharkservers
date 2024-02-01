/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Category_UYW } from './Category_UYW';
import type { Server_JUE } from './Server_JUE';
import type { ThreadMeta_XDD } from './ThreadMeta_XDD';
import type { User_EJU } from './User_EJU';

export type ThreadOut = {
    created_at?: string;
    updated_at?: string;
    id?: number;
    title: string;
    content: string;
    is_closed?: boolean;
    is_pinned?: boolean;
    status?: string;
    category?: Category_UYW;
    author?: User_EJU;
    meta_fields?: Array<ThreadMeta_XDD>;
    post_count?: number;
    server?: Server_JUE;
};

