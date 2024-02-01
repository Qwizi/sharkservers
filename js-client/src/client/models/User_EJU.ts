/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Like_NZF } from './Like_NZF';
import type { Player_EWH } from './Player_EWH';
import type { Post_CSI } from './Post_CSI';
import type { Role_FKG } from './Role_FKG';

export type User_EJU = {
    created_at?: string;
    updated_at?: string;
    id?: number;
    username: string;
    is_activated?: boolean;
    is_superuser?: boolean;
    avatar?: string;
    display_role?: Role_FKG;
    last_login?: string;
    last_online?: string;
    threads_count?: number;
    posts_count?: number;
    likes_count?: number;
    player?: Player_EWH;
    user_reputation?: Array<Like_NZF>;
    user_posts?: Array<Post_CSI>;
};

