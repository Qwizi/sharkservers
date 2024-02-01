/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Ban_VLY } from './Ban_VLY';
import type { Like_LHM } from './Like_LHM';
import type { Player_YFV } from './Player_YFV';
import type { Post_IVP } from './Post_IVP';
import type { Role_WEK } from './Role_WEK';
import type { Thread_JGW } from './Thread_JGW';
import type { UserSession_YLT } from './UserSession_YLT';

/**
 * Represents the output schema for a user with email.
 */
export type UserOutWithEmail = {
    created_at?: string;
    updated_at?: string;
    id?: number;
    username: string;
    email: string;
    is_activated?: boolean;
    is_superuser?: boolean;
    avatar?: string;
    roles?: Array<Role_WEK>;
    display_role?: Role_WEK;
    last_login?: string;
    last_online?: string;
    threads_count?: number;
    posts_count?: number;
    likes_count?: number;
    player?: Player_YFV;
    sessions?: Array<UserSession_YLT>;
    banned_user?: Array<Ban_VLY>;
    banned_by?: Array<Ban_VLY>;
    user_reputation?: Array<Like_LHM>;
    user_posts?: Array<Post_IVP>;
    user_threads?: Array<Thread_JGW>;
};

