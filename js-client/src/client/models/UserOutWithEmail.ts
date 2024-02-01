/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Ban_XLQ } from './Ban_XLQ';
import type { Like_VMZ } from './Like_VMZ';
import type { Player_JQG } from './Player_JQG';
import type { Post_VJU } from './Post_VJU';
import type { Role_HZZ } from './Role_HZZ';
import type { Thread_FBF } from './Thread_FBF';
import type { UserSession_LRD } from './UserSession_LRD';

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
    roles?: Array<Role_HZZ>;
    display_role?: Role_HZZ;
    last_login?: string;
    last_online?: string;
    threads_count?: number;
    posts_count?: number;
    likes_count?: number;
    player?: Player_JQG;
    sessions?: Array<UserSession_LRD>;
    banned_user?: Array<Ban_XLQ>;
    banned_by?: Array<Ban_XLQ>;
    user_reputation?: Array<Like_VMZ>;
    user_posts?: Array<Post_VJU>;
    user_threads?: Array<Thread_FBF>;
};

