"use client";

import {
  adminCreateForumCategoryAction,
  adminCreateRoleAction,
  adminCreateServerAction,
  adminCreateUserAction,
} from "@/actions";
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
import {
  CreateForumCategorySchema,
  CreateRoleSchema,
  CreateServerSchema,
  CreateUserSchema,
} from "@/schemas";
import { zodResolver } from "@hookform/resolvers/zod";
import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { CategoryTypeEnum, Page_Scope_GGF_ } from "sharkservers-sdk";
import { z } from "zod";

export default function CreateForumCategoryForm() {
  const categoryTypes = [
    CategoryTypeEnum.PUBLIC,
    CategoryTypeEnum.PRIVATE,
    CategoryTypeEnum.APPLICATION,
  ];
  const form = useForm<z.infer<typeof CreateForumCategorySchema>>({
    resolver: zodResolver(CreateForumCategorySchema),
    defaultValues: {
      name: "",
      description: "",
      type: CategoryTypeEnum.PUBLIC,
    },
  });
  const router = useRouter();

  async function onSubmit(data: z.infer<typeof CreateForumCategorySchema>) {
    const response = await adminCreateForumCategoryAction(data);
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
        description: "Pomyslnie utworzono kategorie",
      });
      form.reset();
      router.push("/admin/forum-categories");
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
          name="description"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Opis</FormLabel>
              <FormControl>
                <Input {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="type"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Typ</FormLabel>
              <Select onValueChange={field.onChange} defaultValue={field.value}>
                <FormControl>
                  <SelectTrigger>
                    <SelectValue placeholder="Select a verified email to display" />
                  </SelectTrigger>
                </FormControl>
                <SelectContent>
                  {Object.values(CategoryTypeEnum).map((value, i) => (
                    <SelectItem key={i} value={value}>
                      {value}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              <FormMessage />
            </FormItem>
          )}
        />

        <Button type="submit">Dodaj</Button>
      </form>
    </Form>
  );
}
