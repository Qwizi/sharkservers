/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { SteamRepProfile_NZC } from './SteamRepProfile_NZC';

/**
 * Player out schema.
 */
export type PlayerOut = {
    created_at?: string;
    updated_at?: string;
    id: string;
    steamrep_profile?: SteamRepProfile_NZC;
    username: string;
    steamid3: string;
    steamid32: string;
    steamid64: string;
    profile_url?: string;
    avatar?: string;
    country_code: string;
    reputation?: number;
};

