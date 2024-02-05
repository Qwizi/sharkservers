/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Ban_YPL } from './Ban_YPL';
import type { Like_UUM } from './Like_UUM';
import type { Player_AHL } from './Player_AHL';
import type { Post_EWP } from './Post_EWP';
import type { RoleOut } from './RoleOut';
import type { RoleOutWithScopes } from './RoleOutWithScopes';
import type { Thread_XFJ } from './Thread_XFJ';
import type { UserSession_IVK } from './UserSession_IVK';

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
    player?: Player_AHL;
    sessions?: Array<UserSession_IVK>;
    banned_user?: Array<Ban_YPL>;
    banned_by?: Array<Ban_YPL>;
    user_reputation?: Array<Like_UUM>;
    user_posts?: Array<Post_EWP>;
    user_threads?: Array<Thread_XFJ>;
};

