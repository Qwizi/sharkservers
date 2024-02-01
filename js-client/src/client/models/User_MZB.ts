/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Like_LHM } from './Like_LHM';
import type { Player_YFV } from './Player_YFV';
import type { Role_LDV } from './Role_LDV';

export type User_MZB = {
    created_at?: string;
    updated_at?: string;
    id?: number;
    username: string;
    is_activated?: boolean;
    is_superuser?: boolean;
    avatar?: string;
    display_role?: Role_LDV;
    last_login?: string;
    last_online?: string;
    threads_count?: number;
    posts_count?: number;
    likes_count?: number;
    player?: Player_YFV;
    user_reputation?: Array<Like_LHM>;
};

