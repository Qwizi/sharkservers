/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Ban_XZP } from './Ban_XZP';
import type { Like_EYR } from './Like_EYR';
import type { Player_TBD } from './Player_TBD';
import type { Post_ZBH } from './Post_ZBH';
import type { Role_CHQ } from './Role_CHQ';
import type { Thread_IDL } from './Thread_IDL';
import type { UserSession_QNT } from './UserSession_QNT';

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
    roles?: Array<Role_CHQ>;
    display_role?: Role_CHQ;
    last_login?: string;
    last_online?: string;
    threads_count?: number;
    posts_count?: number;
    likes_count?: number;
    player?: Player_TBD;
    sessions?: Array<UserSession_QNT>;
    banned_user?: Array<Ban_XZP>;
    banned_by?: Array<Ban_XZP>;
    user_reputation?: Array<Like_EYR>;
    user_posts?: Array<Post_ZBH>;
    user_threads?: Array<Thread_IDL>;
};

