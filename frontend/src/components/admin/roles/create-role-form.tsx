"use client";

import { adminCreateRoleAction, adminCreateUserAction } from "@/actions";
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
import { toast } from "@/components/ui/use-toast";
import { cn } from "@/lib/utils";
import { CreateRoleSchema, CreateUserSchema } from "@/schemas";
import { zodResolver } from "@hookform/resolvers/zod";
import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { Page_Scope_GGF_ } from "sharkservers-sdk";
import { z } from "zod";

interface CreateRoleFormProps {
  scopes: Page_Scope_GGF_;
}

export default function CreateRoleForm({ scopes }: CreateRoleFormProps) {
  const scopes_options = scopes.items.map((scope) => {
    return {
      value: String(scope.id),
      label: `${scope.app_name}:${scope.value}`,
    };
  });
  const form = useForm<z.infer<typeof CreateRoleSchema>>({
    resolver: zodResolver(CreateRoleSchema),
    defaultValues: {
      name: "",
      color: "",
      is_staff: true,
      scopes: [],
    },
  });
  const router = useRouter();

  async function onSubmit(data: z.infer<typeof CreateRoleSchema>) {
    const response = await adminCreateRoleAction(data);
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
        description: "Pomyslnie utworzono użytkownika",
      });
      form.reset();
      router.push("/admin/roles");
    }
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
        <FormField
          control={form.control}
          name="name"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Nazwa</FormLabel>
              <FormControl>
                <Input {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="tag"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Tag</FormLabel>
              <FormControl>
                <Input {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="color"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Kolor</FormLabel>
              <FormControl>
                <Input {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="is_staff"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Is staff?</FormLabel>
              <FormControl className="ml-2">
                <Input
                  className={cn(
                    "peer h-4 w-4 shrink-0 rounded-sm border border-primary ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 data-[state=checked]:bg-primary data-[state=checked]:text-primary-foreground",
                  )}
                  type="checkbox"
                  {...field}
                  {...field}
                  defaultChecked={true}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="scopes"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Scopes</FormLabel>
              <MultiSelect
                selected={field.value}
                options={scopes_options}
                {...field}
                className="sm:w-[510px]"
              />
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit">Dodaj</Button>
      </form>
    </Form>
  );
}
