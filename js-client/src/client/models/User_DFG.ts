/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Like_KIF } from './Like_KIF';
import type { Player_ACX } from './Player_ACX';
import type { Role_FDU } from './Role_FDU';

export type User_DFG = {
    created_at?: string;
    updated_at?: string;
    id?: number;
    username: string;
    is_activated?: boolean;
    is_superuser?: boolean;
    avatar?: string;
    display_role?: Role_FDU;
    last_login?: string;
    last_online?: string;
    threads_count?: number;
    posts_count?: number;
    likes_count?: number;
    player?: Player_ACX;
    user_reputation?: Array<Like_KIF>;
};

