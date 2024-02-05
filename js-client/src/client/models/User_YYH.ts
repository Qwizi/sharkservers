/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Ban_BGT } from './Ban_BGT';
import type { Like_ZYX } from './Like_ZYX';
import type { Player_GYQ } from './Player_GYQ';
import type { Post_STX } from './Post_STX';
import type { Role_BTL } from './Role_BTL';
import type { UserSession_KAN } from './UserSession_KAN';

export type User_YYH = {
    created_at?: string;
    updated_at?: string;
    id?: string;
    username: string;
    email: string;
    password: string;
    is_activated?: boolean;
    is_superuser?: boolean;
    avatar?: string;
    roles?: Array<Role_BTL>;
    display_role?: Role_BTL;
    last_login?: string;
    last_online?: string;
    secret_salt: string;
    threads_count?: number;
    posts_count?: number;
    likes_count?: number;
    player?: Player_GYQ;
    sessions?: Array<UserSession_KAN>;
    banned_user?: Array<Ban_BGT>;
    banned_by?: Array<Ban_BGT>;
    user_reputation?: Array<Like_ZYX>;
    user_posts?: Array<Post_STX>;
};

