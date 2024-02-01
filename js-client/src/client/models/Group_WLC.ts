/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { GroupOverride_PVT } from './GroupOverride_PVT';

/**
 * Group_WLC model
 */
export type Group_WLC = {
    created_at?: string;
    updated_at?: string;
    id?: number;
    flags: string;
    name: string;
    immunity_level: number;
    groupoverrides?: Array<GroupOverride_PVT>;
};

