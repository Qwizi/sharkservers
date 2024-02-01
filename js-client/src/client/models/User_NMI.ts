/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Like_EYR } from './Like_EYR';
import type { Player_TBD } from './Player_TBD';
import type { Role_MAJ } from './Role_MAJ';

export type User_NMI = {
    created_at?: string;
    updated_at?: string;
    id?: number;
    username: string;
    is_activated?: boolean;
    is_superuser?: boolean;
    avatar?: string;
    display_role?: Role_MAJ;
    last_login?: string;
    last_online?: string;
    threads_count?: number;
    posts_count?: number;
    likes_count?: number;
    player?: Player_TBD;
    user_reputation?: Array<Like_EYR>;
};

