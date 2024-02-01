/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Ban_OBO } from './Ban_OBO';
import type { Like_OTE } from './Like_OTE';
import type { Player_HQF } from './Player_HQF';
import type { Post_QKB } from './Post_QKB';
import type { Role_JTG } from './Role_JTG';
import type { Thread_NTR } from './Thread_NTR';
import type { UserSession_QAA } from './UserSession_QAA';

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
    roles?: Array<Role_JTG>;
    display_role?: Role_JTG;
    last_login?: string;
    last_online?: string;
    threads_count?: number;
    posts_count?: number;
    likes_count?: number;
    player?: Player_HQF;
    sessions?: Array<UserSession_QAA>;
    banned_user?: Array<Ban_OBO>;
    banned_by?: Array<Ban_OBO>;
    user_reputation?: Array<Like_OTE>;
    user_posts?: Array<Post_QKB>;
    user_threads?: Array<Thread_NTR>;
};

