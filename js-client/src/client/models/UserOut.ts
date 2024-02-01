/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Like_VMZ } from './Like_VMZ';
import type { Player_JQG } from './Player_JQG';
import type { Post_VJU } from './Post_VJU';
import type { Role_EIY } from './Role_EIY';
import type { Thread_FBF } from './Thread_FBF';
import type { UserSession_LRD } from './UserSession_LRD';

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
    roles?: Array<Role_EIY>;
    display_role?: Role_EIY;
    last_login?: string;
    last_online?: string;
    threads_count?: number;
    posts_count?: number;
    likes_count?: number;
    player?: Player_JQG;
    sessions?: Array<UserSession_LRD>;
    user_reputation?: Array<Like_VMZ>;
    user_posts?: Array<Post_VJU>;
    user_threads?: Array<Thread_FBF>;
};

