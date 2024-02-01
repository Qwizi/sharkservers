/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Category_CEN } from './Category_CEN';
import type { Server_PQY } from './Server_PQY';
import type { ThreadMeta_MHC } from './ThreadMeta_MHC';
import type { User_DFG } from './User_DFG';

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
    category?: Category_CEN;
    author?: User_DFG;
    meta_fields?: Array<ThreadMeta_MHC>;
    post_count?: number;
    server?: Server_PQY;
};

