"use clinet";

import { createApplicantThreadAction } from "@/actions";
import { Button } from "@/components/ui/button";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { toast } from "@/components/ui/use-toast";
import useUser from "@/hooks/user";
import {
  CreateApplicationThreadFormSchema,
  CreateApplicationThreadFormSchemaInputs,
} from "@/schemas";
import { zodResolver } from "@hookform/resolvers/zod";
import MarkdownEditor from "@uiw/react-markdown-editor";
import { useRouter } from "next/navigation";
import { use, useEffect } from "react";
import { useForm } from "react-hook-form";
import { CategoryOut, Page_ServerOut_ } from "sharkservers-sdk";
import slugify from "slugify";

interface CreateApplicationThreadFormProps {
  category: CategoryOut;
  servers: Page_ServerOut_ | undefined;
}

export default function CreateApplicationThreadForm({
  category,
  servers,
}: CreateApplicationThreadFormProps) {
  const router = useRouter();
  const { user } = useUser();
  const content = `
# Podanie na Administratora {username}\n
**SteamID:** {steamid32}\n
**Serwer:** {serverName}\n
**Wiek:** {age}\n
**Doświadczenie:** {experience}\n
**Dlaczego chcesz zostać administratorem?:** {reason}\n
`;

  const form = useForm<CreateApplicationThreadFormSchemaInputs>({
    resolver: zodResolver(CreateApplicationThreadFormSchema),
    defaultValues: {
      title: ``,
      content: content,
      server_id: undefined,
      category: category?.id ? String(category.id) : undefined,
      question_age: undefined,
      question_experience: undefined,
      question_reason: undefined,
    },
  });

  const serverIdWatch = form.watch("server_id");
  const ageWatch = form.watch("question_age");
  const experienceWatch = form.watch("question_experience");
  const reasonWatch = form.watch("question_reason");

  useEffect(() => {
    if (category) {
      form.setValue("category", String(category.id));
    }
    let replacedContent = content;

    if (user) {
      form.setValue("title", `Podanie na Administratora ${user.username}`);

      replacedContent = replacedContent.replace("{username}", user.username);

      if (user?.player) {
        replacedContent = replacedContent.replace(
          "{steamid32}",
          user.player.steamid32,
        );
      }
    }

    if (serverIdWatch) {
      replacedContent = replacedContent.replace(
        "{serverName}",
        servers?.items.find((server) => server.id === Number(serverIdWatch))
          ?.name || "",
      );
    }

    if (ageWatch) {
      replacedContent = replacedContent.replace("{age}", String(ageWatch));
    }
    if (experienceWatch) {
      replacedContent = replacedContent.replace(
        "{experience}",
        experienceWatch,
      );
    }

    if (reasonWatch) {
      replacedContent = replacedContent.replace("{reason}", reasonWatch);
    }
    form.setValue("content", replacedContent);
  }, [
    category,
    user,
    serverIdWatch,
    ageWatch,
    experienceWatch,
    reasonWatch,
    servers,
  ]);

  async function onSubmit(data: CreateApplicationThreadFormSchemaInputs) {
    console.log(data);
    const response = await createApplicantThreadAction(data);
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
        description: response.validationError,
      });
    } else {
      if (response?.data) {
        form.reset();
        router.push(
          `/forum/${slugify(response?.data?.title)}-${response?.data?.id}`,
        );
        toast({
          variant: "success",
          title: "Sukces!",
          description: "Pomyslnie utworzono temat",
        });
      } else {
        toast({
          variant: "destructive",
          title: "Oh nie. Wystapil bład",
          description: "Nieznany błąd",
        });
      }
    }
  }
  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
        <FormField
          control={form.control}
          name="title"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Tytuł</FormLabel>
              <FormControl>
                <Input placeholder="Tytuł" {...field} readOnly={true} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="server_id"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Serwer</FormLabel>
              <Select onValueChange={field.onChange} defaultValue={field.value}>
                <FormControl>
                  <SelectTrigger>
                    <SelectValue placeholder="Wybierz serwer" />
                  </SelectTrigger>
                </FormControl>
                <SelectContent>
                  {servers &&
                    servers.items.map((server, i) => (
                      <SelectItem key={i} value={String(server.id)}>
                        {server.name}
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
          name="question_age"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Wiek</FormLabel>
              <FormControl>
                <Input
                  placeholder="Wiek"
                  {...field}
                  type="number"
                  onChange={(e) =>
                    field.onChange(
                      Number.isNaN(parseInt(e.target.value))
                        ? 0
                        : parseInt(e.target.value),
                    )
                  }
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="question_experience"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Doświadczenie</FormLabel>
              <FormControl>
                <MarkdownEditor {...field} height="200px" />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="question_reason"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Dlaczego chcesz zostać administratorem?</FormLabel>
              <FormControl>
                <MarkdownEditor {...field} height="200px" />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="content"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Treść</FormLabel>
              <FormControl>
                <MarkdownEditor
                  {...field}
                  height={"500px"}
                  enablePreview={false}
                  readOnly={true}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit" className="text-white">
          Napisz wątek
        </Button>
      </form>
    </Form>
  );
}
