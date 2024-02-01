import { CategoryTypeEnum } from "sharkservers-sdk";
import { z } from "zod";
const MAX_FILE_SIZE = 1024 * 1024 * 2;
function checkFileType(file: File) {
  // file type checking
  if (file?.name) {
    const fileType = file.name.split(".").pop();
    if (["gif", "png", "jpg", "jpeg"].includes(fileType)) return true;
  }
  return false;
}

export const RegisterUserSchema = z
  .object({
    username: z
      .string()
      .min(2)
      .max(32)
      .regex(
        new RegExp("^[a-zA-Z0-9_-]+$"),
        "Nazwa użytkownika musi zawierac tylko litery, cyfry oraz znaki specjalne - _",
      ),
    email: z.coerce.string().email(),
    password: z.string().min(8),
    password2: z.string().min(8),
  })
  .refine((data) => data.password === data.password2, {
    message: "Hasła nie sa takie same",
    path: ["password"],
  });

export const LoginUserSchema = z.object({
  username: z
    .string()
    .min(2)
    .max(32)
    .regex(
      new RegExp("^[a-zA-Z0-9_-]+$"),
      "Nazwa użytkownika musi zawierac tylko litery, cyfry oraz znaki specjalne - _",
    ),
  password: z.string().min(8),
});

export const ActivationCodeSchema = z.object({
  code: z.string().min(5).max(5),
});

export const ChangeUsernameSchema = z.object({
  username: z
    .string()
    .min(2)
    .max(32)
    .regex(
      new RegExp("^[a-zA-Z0-9_-]+$"),
      "Nazwa użytkownika musi zawierac tylko litery, cyfry oraz znaki specjalne - _",
    ),
});

export const changeAvatarSchema = z.object({
  avatar: z.any(),
});

export const emailSchema = z.object({
  email: z.coerce.string().email(),
});

export const CreateUserSchema = z.object({
  username: z
    .string()
    .min(2)
    .max(32)
    .regex(
      new RegExp("^[a-zA-Z0-9_-]+$"),
      "Nazwa użytkownika musi zawierac tylko litery, cyfry oraz znaki specjalne - _",
    ),
  email: z.coerce.string().email(),
  password: z.string().min(8),
  is_activated: z.boolean().optional(),
  is_superuser: z.boolean().optional(),
});

export const UpdateUserSchema = z.object({
  id: z.number().int(),
  username: z
    .string()
    .min(2)
    .max(32)
    .regex(
      new RegExp("^[a-zA-Z0-9_-]+$"),
      "Nazwa użytkownika musi zawierac tylko litery, cyfry oraz znaki specjalne - _",
    )
    .optional(),
  password: z.string().min(8).optional(),
  email: z.coerce.string().email().optional(),
  is_activated: z.boolean().optional(),
  is_superuser: z.boolean().optional(),
  roles: z.array(z.string()).optional(),
  display_role: z.string().optional(),
  avatar: z.any().optional(),
});

export const UserIdSchema = z.object({
  id: z.number().int(),
});

function isValidColor(value: string): boolean {
  const regex = /^#(?:[0-9a-fA-F]{3}){1,2}$/;
  return regex.test(value);
}

const colorSchema = z.string().refine(isValidColor, {
  message: "Invalid color",
});

export const CreateRoleSchema = z.object({
  name: z.string().min(2).max(32),
  tag: z.string().min(2).max(32),
  color: colorSchema,
  is_staff: z.boolean(),
  scopes: z.array(z.string()),
});

export const CreateServerSchema = z.object({
  tag: z.string().min(2).max(32),
  name: z.string().min(2).max(32),
  ip: z.string().min(2).max(32),
  port: z.string(),
  api_url: z.string().min(2).max(256),
});

export const UpdateServerSchema = z.object({
  id: z.number().int(),
  tag: z.string().min(2).max(32).optional(),
  name: z.string().min(2).max(32).optional(),
  ip: z.string().min(2).max(32).optional(),
  port: z.string().optional(),
  api_url: z.string().min(2).max(256).optional(),
});

export const CreateForumCategorySchema = z.object({
  name: z.string().min(2).max(32),
  description: z.string().min(2).max(32),
  type: z
    .string()
    .refine(
      (value) =>
        Object.values(CategoryTypeEnum).includes(value as CategoryTypeEnum),
      {
        message: "Invalid category type",
      },
    ),
});

export const CreateNormalThreadSchema = z.object({
  title: z.string().min(2).max(64),
  content: z.string().min(2),
  category: z.string().min(1),
});

export const CreateThreadSchema = z.object({
  title: z.string().min(2).max(64),
  content: z.string().min(2),
  category: z.string().min(1),
  server_id: z.string().min(1).optional(),
  question_experience: z.string().min(2).optional(),
  question_age: z.number().int().optional(),
  question_reason: z.string().min(2).optional(),
});

export const CreateApplicationThreadFormSchema = z.object({
  title: z.string().min(2).max(64),
  content: z.string().min(2),
  category: z.string().min(1),
  server_id: z.string().min(1),
  question_experience: z.string().min(2),
  question_age: z.number().int(),
  question_reason: z.string().min(2),
});

export type RegisterUserSchemaInputs = z.infer<typeof RegisterUserSchema>;
export type ActivationCodeSchemaInputs = z.infer<typeof ActivationCodeSchema>;
export type LoginUserSchemaInputs = z.infer<typeof LoginUserSchema>;
export type ChangeUsernameSchemaInputs = z.infer<typeof ChangeUsernameSchema>;
export type ChangeAvatarSchemaInputs = z.infer<typeof changeAvatarSchema>;
export type EmailSchemaInputs = z.infer<typeof emailSchema>;
export type CreateUserSchemaInputs = z.infer<typeof CreateUserSchema>;
export type UserIdSchemaInputs = z.infer<typeof UserIdSchema>;
export type UpdateUserSchemaInputs = z.infer<typeof UpdateUserSchema>;
export type CreateRoleSchemaInputs = z.infer<typeof CreateRoleSchema>;
export type CreateServerSchemaInputs = z.infer<typeof CreateServerSchema>;
export type UpdateServerSchemaInputs = z.infer<typeof UpdateServerSchema>;
export type CreateForumCategorySchemaInputs = z.infer<
  typeof CreateForumCategorySchema
>;
export type CreateThreadSchemaInputs = z.infer<typeof CreateThreadSchema>;
export type CreateNormalThreadSchemaInputs = z.infer<
  typeof CreateNormalThreadSchema
>;
export type CreateApplicationThreadFormSchemaInputs = z.infer<
  typeof CreateApplicationThreadFormSchema
>;
