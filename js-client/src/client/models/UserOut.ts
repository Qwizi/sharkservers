/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Like_ATB } from './Like_ATB';
import type { Player_FPT } from './Player_FPT';
import type { Post_KHL } from './Post_KHL';
import type { RoleOut } from './RoleOut';
import type { RoleOutWithScopes } from './RoleOutWithScopes';
import type { Thread_RKX } from './Thread_RKX';
import type { UserSession_IZE } from './UserSession_IZE';

/**
 * Represents the output schema for a user.
 */
export type UserOut = {
    created_at?: string;
    updated_at?: string;
    id: string;
    username: string;
    is_activated?: boolean;
    is_superuser?: boolean;
    avatar?: string;
    roles: Array<RoleOutWithScopes>;
    display_role: RoleOut;
    last_login?: string;
    last_online?: string;
    threads_count?: number;
    posts_count?: number;
    likes_count?: number;
    player?: Player_FPT;
    sessions?: Array<UserSession_IZE>;
    user_reputation?: Array<Like_ATB>;
    user_posts?: Array<Post_KHL>;
    user_threads?: Array<Thread_RKX>;
};

