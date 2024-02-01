/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Like_OTE } from './Like_OTE';
import type { Player_HQF } from './Player_HQF';
import type { Role_VFC } from './Role_VFC';

export type User_WTM = {
    created_at?: string;
    updated_at?: string;
    id?: number;
    username: string;
    is_activated?: boolean;
    is_superuser?: boolean;
    avatar?: string;
    display_role?: Role_VFC;
    last_login?: string;
    last_online?: string;
    threads_count?: number;
    posts_count?: number;
    likes_count?: number;
    player?: Player_HQF;
    user_reputation?: Array<Like_OTE>;
};

