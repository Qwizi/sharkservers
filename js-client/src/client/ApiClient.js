"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.ApiClient = void 0;
const AxiosHttpRequest_1 = require("./core/AxiosHttpRequest");
const AdminForumService_1 = require("./services/AdminForumService");
const AdminPlayersService_1 = require("./services/AdminPlayersService");
const AdminRolesService_1 = require("./services/AdminRolesService");
const AdminScopesService_1 = require("./services/AdminScopesService");
const AdminServersService_1 = require("./services/AdminServersService");
const AdminServersAdminGroupsService_1 = require("./services/AdminServersAdminGroupsService");
const AdminServersAdminsService_1 = require("./services/AdminServersAdminsService");
const AdminUsersService_1 = require("./services/AdminUsersService");
const AuthService_1 = require("./services/AuthService");
const ForumService_1 = require("./services/ForumService");
const PlayersService_1 = require("./services/PlayersService");
const RolesService_1 = require("./services/RolesService");
const RootService_1 = require("./services/RootService");
const ScopesService_1 = require("./services/ScopesService");
const ServersService_1 = require("./services/ServersService");
const SubscryptionService_1 = require("./services/SubscryptionService");
const UsersService_1 = require("./services/UsersService");
const UsersMeService_1 = require("./services/UsersMeService");
class ApiClient {
    constructor(config, HttpRequest = AxiosHttpRequest_1.AxiosHttpRequest) {
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
        this.adminForum = new AdminForumService_1.AdminForumService(this.request);
        this.adminPlayers = new AdminPlayersService_1.AdminPlayersService(this.request);
        this.adminRoles = new AdminRolesService_1.AdminRolesService(this.request);
        this.adminScopes = new AdminScopesService_1.AdminScopesService(this.request);
        this.adminServers = new AdminServersService_1.AdminServersService(this.request);
        this.adminServersAdminGroups = new AdminServersAdminGroupsService_1.AdminServersAdminGroupsService(this.request);
        this.adminServersAdmins = new AdminServersAdminsService_1.AdminServersAdminsService(this.request);
        this.adminUsers = new AdminUsersService_1.AdminUsersService(this.request);
        this.auth = new AuthService_1.AuthService(this.request);
        this.forum = new ForumService_1.ForumService(this.request);
        this.players = new PlayersService_1.PlayersService(this.request);
        this.roles = new RolesService_1.RolesService(this.request);
        this.root = new RootService_1.RootService(this.request);
        this.scopes = new ScopesService_1.ScopesService(this.request);
        this.servers = new ServersService_1.ServersService(this.request);
        this.subscryption = new SubscryptionService_1.SubscryptionService(this.request);
        this.users = new UsersService_1.UsersService(this.request);
        this.usersMe = new UsersMeService_1.UsersMeService(this.request);
    }
}
exports.ApiClient = ApiClient;
