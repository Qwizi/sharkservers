/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Ban_MXS } from './Ban_MXS';
import type { Like_LAQ } from './Like_LAQ';
import type { Player_LPF } from './Player_LPF';
import type { Post_YIT } from './Post_YIT';
import type { Role_QRS } from './Role_QRS';
import type { Thread_SET } from './Thread_SET';
import type { UserSession_JIN } from './UserSession_JIN';

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
    roles?: Array<Role_QRS>;
    display_role?: Role_QRS;
    last_login?: string;
    last_online?: string;
    threads_count?: number;
    posts_count?: number;
    likes_count?: number;
    player?: Player_LPF;
    sessions?: Array<UserSession_JIN>;
    banned_user?: Array<Ban_MXS>;
    banned_by?: Array<Ban_MXS>;
    user_reputation?: Array<Like_LAQ>;
    user_posts?: Array<Post_YIT>;
    user_threads?: Array<Thread_SET>;
};

