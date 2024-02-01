/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Category_VSL } from './Category_VSL';
import type { Server_TRD } from './Server_TRD';
import type { ThreadMeta_CSQ } from './ThreadMeta_CSQ';
import type { User_NMI } from './User_NMI';

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
    category?: Category_VSL;
    author?: User_NMI;
    meta_fields?: Array<ThreadMeta_CSQ>;
    post_count?: number;
    server?: Server_TRD;
};

