/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Category_AJS } from './Category_AJS';
import type { Server_ZBO } from './Server_ZBO';
import type { ThreadMeta_ZJN } from './ThreadMeta_ZJN';
import type { User_WTM } from './User_WTM';

/**
 * Thread output schema.
 */
export type ThreadOut = {
    created_at?: string;
    updated_at?: string;
    id?: number;
    title: string;
    content: string;
    is_closed?: boolean;
    is_pinned?: boolean;
    status?: string;
    category?: Category_AJS;
    author?: User_WTM;
    meta_fields?: Array<ThreadMeta_ZJN>;
    post_count?: number;
    server?: Server_ZBO;
};

