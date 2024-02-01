/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Like_FNC } from './Like_FNC';
import type { Player_LPL } from './Player_LPL';
import type { Role_KXR } from './Role_KXR';

export type User_PRS = {
    created_at?: string;
    updated_at?: string;
    id?: number;
    username: string;
    is_activated?: boolean;
    is_superuser?: boolean;
    avatar?: string;
    display_role?: Role_KXR;
    last_login?: string;
    last_online?: string;
    threads_count?: number;
    posts_count?: number;
    likes_count?: number;
    player?: Player_LPL;
    user_reputation?: Array<Like_FNC>;
};

