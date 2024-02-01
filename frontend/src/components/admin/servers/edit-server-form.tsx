"use client";

import { adminUpdateServerAction, adminUpdateUserAction } from "@/actions";
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
import { UpdateServerSchema, UpdateUserSchema } from "@/schemas";
import { zodResolver } from "@hookform/resolvers/zod";
import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { Page_RoleOut_, ServerOut, UserOutWithEmail } from "sharkservers-sdk";
import { z } from "zod";

interface EditServerFormProps {
  server: ServerOut;
}

export default function EditServerForm({ server }: EditServerFormProps) {
  const form = useForm<z.infer<typeof UpdateServerSchema>>({
    resolver: zodResolver(UpdateServerSchema),
    defaultValues: {
      id: server.id,
      name: server.name,
      tag: server.tag,
      ip: server.ip,
      port: String(server.port),
      api_url: server.api_url,
    },
  });
  const router = useRouter();

  async function onSubmit(data: z.infer<typeof UpdateServerSchema>) {
    console.log(data);
    const updatedData = data;

    const response = await adminUpdateServerAction(updatedData);
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
        description: "Pomyslnie zaktualizowano server",
      });
      router.push("/admin/servers");
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
          name="ip"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Ip</FormLabel>
              <FormControl>
                <Input {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="api_url"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Api url</FormLabel>
              <FormControl>
                <Input {...field} />
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
