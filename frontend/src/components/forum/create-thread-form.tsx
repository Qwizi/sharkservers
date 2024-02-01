"use client";
import { zodResolver } from "@hookform/resolvers/zod";
import dynamic from "next/dynamic";
import { z } from "zod";
import { Button } from "../ui/button";
import {
  FormField,
  FormItem,
  FormLabel,
  FormControl,
  FormMessage,
  Form,
} from "../ui/form";
import { Input } from "../ui/input";
import { useForm } from "react-hook-form";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "../ui/select";
import {
  CategoryOut,
  CategoryTypeEnum,
  Page_CategoryOut_,
  Page_ServerOut_,
  Page_UserOut_,
} from "sharkservers-sdk";
import slugify from "slugify";
import { useRouter } from "next/navigation";
import { toast } from "../ui/use-toast";
import useApi from "@/hooks/api";
import { useEffect, useState } from "react";
import useUser from "@/hooks/user";
import useCategory from "@/hooks/category";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "../ui/dialog";
import {
  CreateForumCategorySchema,
  CreateNormalThreadSchema,
  CreateThreadSchema,
} from "@/schemas";
import { createNormalThreadAction } from "@/actions";

const MarkdownEditor = dynamic(
  () => import("@uiw/react-markdown-editor").then((mod) => mod.default),
  { ssr: false },
);

interface ICreateThreadNormalForm {
  categories: Page_CategoryOut_;
  category?: CategoryOut | undefined;
  servers?: Page_ServerOut_ | undefined;
}

export default function CreateThreadForm({
  categories,
  category,
  servers,
}: ICreateThreadNormalForm) {
  const router = useRouter();
  const { user } = useUser();
  const normalForm = useForm<z.infer<typeof CreateNormalThreadSchema>>({
    resolver: zodResolver(CreateNormalThreadSchema),
    defaultValues: {
      title: "",
      content: "",
      category: category?.id?.toString(),
    },
  });
  const applicationForm = useForm<z.infer<typeof CreateThreadSchema>>({
    resolver: zodResolver(CreateThreadSchema),
    defaultValues: {
      title: `Podanie na administratora - ${user?.username}`,
      content: `Podanie na administratora - ${user?.username}`,
      question_age: 0,
      question_experience: "",
      question_reason: "",
      category: category?.id?.toString(),
    },
  });
  const api = useApi();

  async function onSubmitNormalThread(
    data: z.infer<typeof CreateNormalThreadSchema>,
  ) {
    const response = await createNormalThreadAction(data);
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
        description: response.validationError,
      });
    } else {
      toast({
        variant: "success",
        title: "Sukces!",
        description: "Pomyslnie utworzono użytkownika",
      });
      normalForm.reset();
      const title = response?.data?.title;
      router.push(`/forum/${slugify(title)}-${response?.data?.id}`);
    }
  }

  async function onSubmit(data: z.infer<typeof CreateThreadSchema>) {
    //const response = await createThreadAction(data)
  }

  useEffect(() => {
    if (category?.type == CategoryTypeEnum.APPLICATION) {
      applicationForm.setValue(
        "title",
        `Podanie na administratora - ${user?.username}`,
      );
      applicationForm.setValue(
        "content",
        `Podanie na administratora - ${user?.username}`,
      );
    } else {
      applicationForm.reset();
    }
  }, [category]);

  if (category?.type == CategoryTypeEnum.APPLICATION) {
    return (
      <>
        <Form {...applicationForm}>
          <form
            onSubmit={applicationForm.handleSubmit(onSubmit)}
            className="space-y-8"
          >
            <FormField
              control={applicationForm.control}
              name="category"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Kategoria</FormLabel>
                  <Select
                    onValueChange={(value) => {
                      field.onChange(value);
                      router.push(`/forum/create?category=${value}`);
                    }}
                    defaultValue={field.value}
                  >
                    <FormControl>
                      <SelectTrigger>
                        <SelectValue
                          placeholder="Wybierz kategorie"
                          defaultValue={category?.id}
                        />
                      </SelectTrigger>
                    </FormControl>
                    <SelectContent>
                      {categories &&
                        categories.items.map((category, i) => (
                          <SelectItem key={i} value={String(category.id)}>
                            {category.name}
                          </SelectItem>
                        ))}
                    </SelectContent>
                  </Select>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={applicationForm.control}
              name="server_id"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Serwer</FormLabel>
                  <Select onValueChange={field.onChange} defaultValue="1">
                    <FormControl>
                      <SelectTrigger>
                        <SelectValue placeholder="Select a verified email to display" />
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
              control={applicationForm.control}
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
              control={applicationForm.control}
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
              control={applicationForm.control}
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
            <Button type="submit" className="text-white">
              Napisz wątek
            </Button>
          </form>
        </Form>
      </>
    );
  }

  return (
    <Form {...normalForm}>
      <form
        onSubmit={normalForm.handleSubmit(onSubmitNormalThread)}
        className="space-y-8"
      >
        <FormField
          control={normalForm.control}
          name="category"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Kategoria</FormLabel>
              <Select
                onValueChange={(value) => {
                  field.onChange(value);
                  router.push(`/forum/create?category=${value}`);
                }}
                defaultValue={field.value}
              >
                <FormControl>
                  <SelectTrigger>
                    <SelectValue
                      placeholder="Wybierz kategorie"
                      defaultValue={category?.id}
                    />
                  </SelectTrigger>
                </FormControl>
                <SelectContent>
                  {categories &&
                    categories.items.map((category, i) => (
                      <SelectItem key={i} value={String(category.id)}>
                        {category.name}
                      </SelectItem>
                    ))}
                </SelectContent>
              </Select>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={normalForm.control}
          name="title"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Tytuł</FormLabel>
              <FormControl>
                <Input placeholder="Tytuł" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={normalForm.control}
          name="content"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Treść</FormLabel>
              <FormControl>
                <MarkdownEditor
                  readOnly={
                    category?.type === CategoryTypeEnum.APPLICATION
                      ? true
                      : false
                  }
                  {...field}
                  height={
                    category?.type === CategoryTypeEnum.APPLICATION
                      ? "50px"
                      : "500px"
                  }
                  enablePreview={false}
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
