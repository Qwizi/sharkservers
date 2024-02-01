/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { ChatColorModule_IZG } from './ChatColorModule_IZG';
import type { Role_AJC } from './Role_AJC';

export type ServerOut = {
    created_at?: string;
    updated_at?: string;
    id?: number;
    name: string;
    tag: string;
    ip: string;
    port: number;
    admin_role?: Role_AJC;
    api_url: string;
    server_chat_color_module?: Array<ChatColorModule_IZG>;
};

