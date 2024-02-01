/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { BaseHttpRequest } from './core/BaseHttpRequest';
import type { OpenAPIConfig } from './core/OpenAPI';
import { AxiosHttpRequest } from './core/AxiosHttpRequest';

import { AdminForumService } from './services/AdminForumService';
import { AdminPlayersService } from './services/AdminPlayersService';
import { AdminRolesService } from './services/AdminRolesService';
import { AdminScopesService } from './services/AdminScopesService';
import { AdminServersService } from './services/AdminServersService';
import { AdminServersAdminGroupsService } from './services/AdminServersAdminGroupsService';
import { AdminServersAdminsService } from './services/AdminServersAdminsService';
import { AdminUsersService } from './services/AdminUsersService';
import { AuthService } from './services/AuthService';
import { ForumService } from './services/ForumService';
import { PlayersService } from './services/PlayersService';
import { RolesService } from './services/RolesService';
import { RootService } from './services/RootService';
import { ScopesService } from './services/ScopesService';
import { ServersService } from './services/ServersService';
import { SubscryptionService } from './services/SubscryptionService';
import { UsersService } from './services/UsersService';
import { UsersMeService } from './services/UsersMeService';

type HttpRequestConstructor = new (config: OpenAPIConfig) => BaseHttpRequest;

export class ApiClient {

    public readonly adminForum: AdminForumService;
    public readonly adminPlayers: AdminPlayersService;
    public readonly adminRoles: AdminRolesService;
    public readonly adminScopes: AdminScopesService;
    public readonly adminServers: AdminServersService;
    public readonly adminServersAdminGroups: AdminServersAdminGroupsService;
    public readonly adminServersAdmins: AdminServersAdminsService;
    public readonly adminUsers: AdminUsersService;
    public readonly auth: AuthService;
    public readonly forum: ForumService;
    public readonly players: PlayersService;
    public readonly roles: RolesService;
    public readonly root: RootService;
    public readonly scopes: ScopesService;
    public readonly servers: ServersService;
    public readonly subscryption: SubscryptionService;
    public readonly users: UsersService;
    public readonly usersMe: UsersMeService;

    public readonly request: BaseHttpRequest;

    constructor(config?: Partial<OpenAPIConfig>, HttpRequest: HttpRequestConstructor = AxiosHttpRequest) {
        this.request = new HttpRequest({
            BASE: config?.BASE ?? '',
            VERSION: config?.VERSION ?? '1.1.0',
            WITH_CREDENTIALS: config?.WITH_CREDENTIALS ?? false,
            CREDENTIALS: config?.CREDENTIALS ?? 'include',
            TOKEN: config?.TOKEN,
            USERNAME: config?.USERNAME,
            PASSWORD: config?.PASSWORD,
            HEADERS: config?.HEADERS,
            ENCODE_PATH: config?.ENCODE_PATH,
        });

        this.adminForum = new AdminForumService(this.request);
        this.adminPlayers = new AdminPlayersService(this.request);
        this.adminRoles = new AdminRolesService(this.request);
        this.adminScopes = new AdminScopesService(this.request);
        this.adminServers = new AdminServersService(this.request);
        this.adminServersAdminGroups = new AdminServersAdminGroupsService(this.request);
        this.adminServersAdmins = new AdminServersAdminsService(this.request);
        this.adminUsers = new AdminUsersService(this.request);
        this.auth = new AuthService(this.request);
        this.forum = new ForumService(this.request);
        this.players = new PlayersService(this.request);
        this.roles = new RolesService(this.request);
        this.root = new RootService(this.request);
        this.scopes = new ScopesService(this.request);
        this.servers = new ServersService(this.request);
        this.subscryption = new SubscryptionService(this.request);
        this.users = new UsersService(this.request);
        this.usersMe = new UsersMeService(this.request);
    }
}

