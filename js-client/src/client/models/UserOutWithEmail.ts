/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Ban_SKU } from './Ban_SKU';
import type { Like_NZF } from './Like_NZF';
import type { Player_EWH } from './Player_EWH';
import type { Post_CSI } from './Post_CSI';
import type { Role_QIO } from './Role_QIO';
import type { Thread_LZY } from './Thread_LZY';
import type { UserSession_IDD } from './UserSession_IDD';

export type UserOutWithEmail = {
    created_at?: string;
    updated_at?: string;
    id?: number;
    username: string;
    email: string;
    is_activated?: boolean;
    is_superuser?: boolean;
    avatar?: string;
    roles?: Array<Role_QIO>;
    display_role?: Role_QIO;
    last_login?: string;
    last_online?: string;
    threads_count?: number;
    posts_count?: number;
    likes_count?: number;
    player?: Player_EWH;
    sessions?: Array<UserSession_IDD>;
    banned_user?: Array<Ban_SKU>;
    banned_by?: Array<Ban_SKU>;
    user_reputation?: Array<Like_NZF>;
    user_posts?: Array<Post_CSI>;
    user_threads?: Array<Thread_LZY>;
};

