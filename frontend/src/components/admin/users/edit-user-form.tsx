"use client";

import { adminUpdateUserAction } from "@/actions";
import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { MultiSelect } from "@/components/ui/multi-select";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { toast } from "@/components/ui/use-toast";
import { cn } from "@/lib/utils";
import { UpdateUserSchema } from "@/schemas";
import { zodResolver } from "@hookform/resolvers/zod";
import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { Page_RoleOut_, UserOutWithEmail } from "sharkservers-sdk";
import { z } from "zod";

interface EditUserFormProps {
  user: UserOutWithEmail;
  roles: Page_RoleOut_;
}

export default function EditUserForm({ user, roles }: EditUserFormProps) {
  const roles_options = roles.items.map((role) => {
    return {
      value: String(role.id),
      label: role.name,
    };
  });
  const user_roles_options = user?.roles?.map((role) => {
    return String(role.id);
  });
  const form = useForm<z.infer<typeof UpdateUserSchema>>({
    resolver: zodResolver(UpdateUserSchema),
    defaultValues: {
      id: user.id,
      username: user.username,
      email: user.email,
      is_activated: user.is_activated,
      is_superuser: user.is_superuser,
      roles: user_roles_options,
      display_role: String(user?.display_role?.id),
    },
  });
  const router = useRouter();

  async function onSubmit(data: z.infer<typeof UpdateUserSchema>) {
    console.log(data);
    const updatedData = data;

    const response = await adminUpdateUserAction(updatedData);
    console.log(response);
    if (response.serverError) {
      toast({
        variant: "destructive",
        title: "Oh nie. Wystapil bład",
        description: response.serverError,
      });
    } else if (response.validationError) {
      toast({
        variant: "destructive",
        title: "Oh nie. Wystapil bład",
        description: "Wystapil bład walidacji",
      });
    } else {
      toast({
        variant: "success",
        title: "Sukces!",
        description: "Pomyslnie zaktualizowano użytkownika",
      });
      router.push("/admin/users");
    }
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
        <FormField
          control={form.control}
          name="id"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Id</FormLabel>
              <FormControl>
                <Input {...field} readOnly />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="username"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Nazwa użytkownika</FormLabel>
              <FormControl>
                <Input {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="email"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Email</FormLabel>
              <FormControl>
                <Input {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="password"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Hasło</FormLabel>
              <FormControl>
                <Input {...field} type="password" />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="display_role"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Wyświetlana rola</FormLabel>
              <Select onValueChange={field.onChange} defaultValue={field.value}>
                <FormControl>
                  <SelectTrigger>
                    <SelectValue placeholder="Select a verified email to display" />
                  </SelectTrigger>
                </FormControl>
                <SelectContent>
                  {roles &&
                    roles.items.map((role, i) => (
                      <SelectItem key={i} value={String(role.id)}>
                        {role.name}
                      </SelectItem>
                    ))}
                </SelectContent>
              </Select>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="roles"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Role</FormLabel>
              <MultiSelect
                selected={field.value}
                options={roles_options}
                {...field}
                className="sm:w-[510px]"
              />
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="is_activated"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Aktywowany</FormLabel>
              <FormControl className="ml-2">
                <Input
                  className={cn(
                    "peer h-4 w-4 shrink-0 rounded-sm border border-primary ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 data-[state=checked]:bg-primary data-[state=checked]:text-primary-foreground",
                  )}
                  type="checkbox"
                  {...field}
                  defaultChecked={user.is_activated}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="is_superuser"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Superużytkownik</FormLabel>
              <FormControl className="ml-2">
                <Input
                  className={cn(
                    "peer h-4 w-4 shrink-0 rounded-sm border border-primary ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 data-[state=checked]:bg-primary data-[state=checked]:text-primary-foreground",
                  )}
                  type="checkbox"
                  {...field}
                  defaultChecked={user.is_superuser}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit">Aktualizuj</Button>
      </form>
    </Form>
  );
}
