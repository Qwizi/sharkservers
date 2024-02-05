/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Ban_PAN } from './Ban_PAN';
import type { Like_ATB } from './Like_ATB';
import type { Player_FPT } from './Player_FPT';
import type { Post_KHL } from './Post_KHL';
import type { RoleOut } from './RoleOut';
import type { RoleOutWithScopes } from './RoleOutWithScopes';
import type { Thread_RKX } from './Thread_RKX';
import type { UserSession_IZE } from './UserSession_IZE';

/**
 * Represents the output schema for a user with email.
 */
export type UserOutWithEmail = {
    created_at?: string;
    updated_at?: string;
    id: string;
    username: string;
    email: string;
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
    banned_user?: Array<Ban_PAN>;
    banned_by?: Array<Ban_PAN>;
    user_reputation?: Array<Like_ATB>;
    user_posts?: Array<Post_KHL>;
    user_threads?: Array<Thread_RKX>;
};

