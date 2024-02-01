"use server";
import { z } from "zod";
import {
  RegisterUserInputs,
  registerFormSchema,
} from "@/components/auth/register-form";
import { sharkApi } from "@/lib/server-api";
import { action, authAction } from "@/lib/action";
import {
  RegisterUserSchema,
  ActivationCodeSchema,
  ActivationCodeSchemaInputs,
  LoginUserSchema,
  LoginUserSchemaInputs,
  ChangeUsernameSchema,
  ChangeUsernameSchemaInputs,
  changeAvatarSchema,
  ChangeAvatarSchemaInputs,
  emailSchema,
  EmailSchemaInputs,
  CreateUserSchemaInputs,
  CreateUserSchema,
  UserIdSchema,
  UserIdSchemaInputs,
  UpdateUserSchema,
  UpdateUserSchemaInputs,
  CreateRoleSchema,
  CreateRoleSchemaInputs,
  CreateServerSchema,
  CreateServerSchemaInputs,
  UpdateServerSchema,
  UpdateServerSchemaInputs,
  CreateForumCategorySchema,
  CreateForumCategorySchemaInputs,
  CreateThreadSchema,
  CreateNormalThreadSchema,
  CreateApplicationThreadFormSchema,
} from "@/schemas";
import { revalidatePath } from "next/cache";

const HOME_PATH = "/";
const USERS_PATH = "/users";
const FORUM_PATH = "/forum";
const ADMIN_USERS_PATH = "/admin/users";
const ADMIN_ROLE_PATH = "/admin/roles";
const ADMIN_SERVERS_PATH = "/admin/servers";

export const registerUserAction = action(
  RegisterUserSchema,
  async (data: RegisterUserInputs) => {
    const api = await sharkApi();
    const responseData = await api.auth.register({
      username: data.username,
      email: data.email,
      password: data.password,
      password2: data.password2,
    });
    revalidatePath(HOME_PATH);
    revalidatePath(USERS_PATH);
    return responseData;
  },
);

export const activateUserAction = action(
  ActivationCodeSchema,
  async (data: ActivationCodeSchemaInputs) => {
    const api = await sharkApi();
    const responseData = await api.auth.activateUser({
      code: data.code,
    });
    return responseData;
  },
);

export const changeUsernameAction = authAction(
  ChangeUsernameSchema,
  async ({ ...data }: ChangeUsernameSchemaInputs, { session }) => {
    const api = await sharkApi();
    console.log(data);
    const response = await api.usersMe.changeUserUsername({
      username: data.username,
    });
    revalidatePath(HOME_PATH);
    revalidatePath(USERS_PATH);
    return response;
  },
);

export const changeAvatarAction = authAction(
  changeAvatarSchema,
  async ({ ...data }: ChangeAvatarSchemaInputs, { session }) => {
    console.log(data);
    const api = await sharkApi();
    const response = await api.usersMe.uploadUserAvatar({
      avatar: data.avatar,
    });
    revalidatePath(HOME_PATH);
    revalidatePath(USERS_PATH);
    return { test: true };
  },
);

export const requestChangeEmailAction = authAction(
  emailSchema,
  async ({ ...data }: EmailSchemaInputs, { session, api }) => {
    return await api.usersMe.requestChangeUserEmail({
      email: data.email,
    });
  },
);

export const confirmChangeEmailAction = authAction(
  ActivationCodeSchema,
  async (data: ActivationCodeSchemaInputs, { session, api }) => {
    return await api.usersMe.confirmChangeUserEmail({
      code: data.code,
    });
  },
);

export const adminCreateUserAction = authAction(
  CreateUserSchema,
  async (data: CreateUserSchemaInputs, { session, api }) => {
    const response = await api.adminUsers.adminCreateUser({
      username: data.username,
      email: data.email,
      password: data.password,
      is_activated: data.is_activated,
      is_superuser: data.is_superuser,
    });
    revalidatePath(ADMIN_USERS_PATH);
    return response;
  },
);

export const adminDeleteUserAction = authAction(
  UserIdSchema,
  async (data: UserIdSchemaInputs, { session, api }) => {
    const response = await api.adminUsers.adminDeleteUser(data.id);
    revalidatePath(ADMIN_USERS_PATH);
    return response;
  },
);

export const adminUpdateUserAction = authAction(
  UpdateUserSchema,
  async (data: UpdateUserSchemaInputs, { session, api }) => {
    let updatedData = {
      username: data.username,
      email: data.email,
      is_activated: data.is_activated,
      is_superuser: data.is_superuser,
      display_role: Number(data.display_role),
      password: data.password,
    };
    if (data?.roles && data.roles.length > 0) {
      const roles = data.roles?.map((role) => {
        return Number(role);
      });
      updatedData = { ...updatedData, roles: roles };
    }
    console.log(updatedData);
    const response = await api.adminUsers.adminUpdateUser(data.id, updatedData);
    revalidatePath(ADMIN_USERS_PATH);
    revalidatePath(USERS_PATH);
    revalidatePath(HOME_PATH);
    return response;
  },
);

export const adminDeleteRoleAction = authAction(
  UserIdSchema,
  async (data: UserIdSchemaInputs, { session, api }) => {
    const response = await api.adminRoles.adminDeleteRole(data.id);
    revalidatePath(ADMIN_ROLE_PATH);
    return response;
  },
);

export const adminCreateRoleAction = authAction(
  CreateRoleSchema,
  async (data: CreateRoleSchemaInputs, { session, api }) => {
    const scopes = data.scopes.map((scope) => {
      return Number(scope);
    });
    const response = await api.adminRoles.adminCreateRole({
      tag: data.tag,
      name: data.name,
      color: data.color,
      is_staff: data.is_staff,
      scopes: scopes,
    });
    console.log(response);
    revalidatePath(ADMIN_ROLE_PATH);
    return response;
  },
);

export const adminDeleteServerAction = authAction(
  UserIdSchema,
  async (data: UserIdSchemaInputs, { session, api }) => {
    const response = await api.adminServers.adminDeleteServer(data.id);
    revalidatePath(ADMIN_SERVERS_PATH);
    return response;
  },
);

export const adminCreateServerAction = authAction(
  CreateServerSchema,
  async (data: CreateServerSchemaInputs, { session, api }) => {
    const response = await api.adminServers.adminCreateServer({
      tag: data.tag,
      name: data.name,
      ip: data.ip,
      port: Number(data.port),
      api_url: data.api_url,
    });
    console.log(response);
    revalidatePath(ADMIN_SERVERS_PATH);
    return response;
  },
);

export const adminUpdateServerAction = authAction(
  UpdateServerSchema,
  async (data: UpdateServerSchemaInputs, { session, api }) => {
    const response = await api.adminServers.adminUpdateServer(data.id, {
      tag: data.tag,
      name: data.name,
      ip: data.ip,
      port: Number(data.port),
      api_url: data.api_url,
    });
    console.log(response);
    revalidatePath(ADMIN_SERVERS_PATH);
    return response;
  },
);

export const adminCreateForumCategoryAction = authAction(
  CreateForumCategorySchema,
  async (data: CreateForumCategorySchemaInputs, { session, api }) => {
    const response = await api.adminForum.adminCreateCategory({
      name: data.name,
      description: data.description,
      type: data.type,
    });
    console.log(response);
    revalidatePath(ADMIN_SERVERS_PATH);
    return response;
  },
);

export const createNormalThreadAction = authAction(
  CreateNormalThreadSchema,
  async (data, { session, api }) => {
    const response = await api.forum.createThread({
      title: data.title,
      content: data.content,
      category: Number(data.category),
    });
    console.log(response);
    revalidatePath(HOME_PATH);
    revalidatePath(FORUM_PATH);
    return response;
  },
);

export const createApplicantThreadAction = authAction(
  CreateApplicationThreadFormSchema,
  async (data, { session, api }) => {
    const response = await api.forum.createThread({
      title: data.title,
      content: data.content,
      server_id: Number(data.server_id),
      category: Number(data.category),
      question_age: Number(data.question_age),
      question_experience: data.question_experience,
      question_reason: data.question_reason,
    });
    console.log(response);
    revalidatePath(HOME_PATH);
    revalidatePath(FORUM_PATH);
    return response;
  },
);
