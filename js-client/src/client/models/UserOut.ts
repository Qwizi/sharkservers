/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Like_LHM } from './Like_LHM';
import type { Player_YFV } from './Player_YFV';
import type { Post_IVP } from './Post_IVP';
import type { Role_LDV } from './Role_LDV';
import type { Thread_JGW } from './Thread_JGW';
import type { UserSession_YLT } from './UserSession_YLT';

/**
 * Represents the output schema for a user.
 */
export type UserOut = {
    created_at?: string;
    updated_at?: string;
    id?: number;
    username: string;
    is_activated?: boolean;
    is_superuser?: boolean;
    avatar?: string;
    roles?: Array<Role_LDV>;
    display_role?: Role_LDV;
    last_login?: string;
    last_online?: string;
    threads_count?: number;
    posts_count?: number;
    likes_count?: number;
    player?: Player_YFV;
    sessions?: Array<UserSession_YLT>;
    user_reputation?: Array<Like_LHM>;
    user_posts?: Array<Post_IVP>;
    user_threads?: Array<Thread_JGW>;
};

