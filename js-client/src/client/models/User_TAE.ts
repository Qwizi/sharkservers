/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Like_VMZ } from './Like_VMZ';
import type { Player_JQG } from './Player_JQG';
import type { Role_EIY } from './Role_EIY';

export type User_TAE = {
    created_at?: string;
    updated_at?: string;
    id?: number;
    username: string;
    is_activated?: boolean;
    is_superuser?: boolean;
    avatar?: string;
    display_role?: Role_EIY;
    last_login?: string;
    last_online?: string;
    threads_count?: number;
    posts_count?: number;
    likes_count?: number;
    player?: Player_JQG;
    user_reputation?: Array<Like_VMZ>;
};

