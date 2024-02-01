/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Category_AIC } from './Category_AIC';
import type { Server_UYR } from './Server_UYR';
import type { ThreadMeta_AYW } from './ThreadMeta_AYW';
import type { User_OTX } from './User_OTX';

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
    category?: Category_AIC;
    author?: User_OTX;
    meta_fields?: Array<ThreadMeta_AYW>;
    post_count?: number;
    server?: Server_UYR;
};

