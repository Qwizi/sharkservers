/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Like_EYR } from './Like_EYR';
import type { Player_TBD } from './Player_TBD';
import type { Post_ZBH } from './Post_ZBH';
import type { Role_MAJ } from './Role_MAJ';
import type { Thread_IDL } from './Thread_IDL';
import type { UserSession_QNT } from './UserSession_QNT';

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
    roles?: Array<Role_MAJ>;
    display_role?: Role_MAJ;
    last_login?: string;
    last_online?: string;
    threads_count?: number;
    posts_count?: number;
    likes_count?: number;
    player?: Player_TBD;
    sessions?: Array<UserSession_QNT>;
    user_reputation?: Array<Like_EYR>;
    user_posts?: Array<Post_ZBH>;
    user_threads?: Array<Thread_IDL>;
};

