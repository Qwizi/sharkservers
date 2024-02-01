/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { ChatColorModule_IRN } from './ChatColorModule_IRN';
import type { Role_QIO } from './Role_QIO';

export type Server_MTQ = {
    created_at?: string;
    updated_at?: string;
    id?: number;
    name: string;
    tag: string;
    ip: string;
    port: number;
    admin_role?: Role_QIO;
    api_url: string;
    server_chat_color_module?: Array<ChatColorModule_IRN>;
};

