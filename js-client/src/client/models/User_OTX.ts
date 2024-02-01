/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Like_LAQ } from './Like_LAQ';
import type { Player_LPF } from './Player_LPF';
import type { Role_KPW } from './Role_KPW';

export type User_OTX = {
    created_at?: string;
    updated_at?: string;
    id?: number;
    username: string;
    is_activated?: boolean;
    is_superuser?: boolean;
    avatar?: string;
    display_role?: Role_KPW;
    last_login?: string;
    last_online?: string;
    threads_count?: number;
    posts_count?: number;
    likes_count?: number;
    player?: Player_LPF;
    user_reputation?: Array<Like_LAQ>;
};

