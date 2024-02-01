/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Ban_BMO } from './Ban_BMO';
import type { Like_KIF } from './Like_KIF';
import type { Player_ACX } from './Player_ACX';
import type { Post_YRC } from './Post_YRC';
import type { Role_KVI } from './Role_KVI';
import type { Thread_HXO } from './Thread_HXO';
import type { UserSession_YIF } from './UserSession_YIF';

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
    roles?: Array<Role_KVI>;
    display_role?: Role_KVI;
    last_login?: string;
    last_online?: string;
    threads_count?: number;
    posts_count?: number;
    likes_count?: number;
    player?: Player_ACX;
    sessions?: Array<UserSession_YIF>;
    banned_user?: Array<Ban_BMO>;
    banned_by?: Array<Ban_BMO>;
    user_reputation?: Array<Like_KIF>;
    user_posts?: Array<Post_YRC>;
    user_threads?: Array<Thread_HXO>;
};

