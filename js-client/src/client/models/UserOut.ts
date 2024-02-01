/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Like_OTE } from './Like_OTE';
import type { Player_HQF } from './Player_HQF';
import type { Post_QKB } from './Post_QKB';
import type { Role_VFC } from './Role_VFC';
import type { Thread_NTR } from './Thread_NTR';
import type { UserSession_QAA } from './UserSession_QAA';

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
    roles?: Array<Role_VFC>;
    display_role?: Role_VFC;
    last_login?: string;
    last_online?: string;
    threads_count?: number;
    posts_count?: number;
    likes_count?: number;
    player?: Player_HQF;
    sessions?: Array<UserSession_QAA>;
    user_reputation?: Array<Like_OTE>;
    user_posts?: Array<Post_QKB>;
    user_threads?: Array<Thread_NTR>;
};

