/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Like_KIF } from './Like_KIF';
import type { Player_ACX } from './Player_ACX';
import type { Post_YRC } from './Post_YRC';
import type { Role_FDU } from './Role_FDU';
import type { Thread_HXO } from './Thread_HXO';
import type { UserSession_YIF } from './UserSession_YIF';

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
    roles?: Array<Role_FDU>;
    display_role?: Role_FDU;
    last_login?: string;
    last_online?: string;
    threads_count?: number;
    posts_count?: number;
    likes_count?: number;
    player?: Player_ACX;
    sessions?: Array<UserSession_YIF>;
    user_reputation?: Array<Like_KIF>;
    user_posts?: Array<Post_YRC>;
    user_threads?: Array<Thread_HXO>;
};

