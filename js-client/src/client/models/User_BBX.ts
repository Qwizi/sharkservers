/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Ban_WIB } from './Ban_WIB';
import type { Like_XMW } from './Like_XMW';
import type { Player_EUH } from './Player_EUH';
import type { Post_YMB } from './Post_YMB';
import type { Role_JUT } from './Role_JUT';
import type { UserSession_AQF } from './UserSession_AQF';

export type User_BBX = {
    created_at?: string;
    updated_at?: string;
    id?: string;
    username: string;
    email: string;
    password: string;
    is_activated?: boolean;
    is_superuser?: boolean;
    avatar?: string;
    roles?: Array<Role_JUT>;
    display_role?: Role_JUT;
    last_login?: string;
    last_online?: string;
    secret_salt: string;
    threads_count?: number;
    posts_count?: number;
    likes_count?: number;
    player?: Player_EUH;
    sessions?: Array<UserSession_AQF>;
    banned_user?: Array<Ban_WIB>;
    banned_by?: Array<Ban_WIB>;
    user_reputation?: Array<Like_XMW>;
    user_posts?: Array<Post_YMB>;
};

