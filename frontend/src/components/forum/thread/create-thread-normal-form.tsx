"use client";

import { createNormalThreadAction } from "@/actions";
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
import {
  CreateNormalThreadSchema,
  CreateNormalThreadSchemaInputs,
} from "@/schemas";
import { zodResolver } from "@hookform/resolvers/zod";

import MarkdownEditor from "@uiw/react-markdown-editor";
import { useRouter } from "next/navigation";
import router from "next/router";
import { useEffect } from "react";
import { useForm } from "react-hook-form";
import {
  CategoryOut,
  CategoryTypeEnum,
  Page_CategoryOut_,
} from "sharkservers-sdk";
import slugify from "slugify";

interface CreateNormalThreadFormProps {
  category?: CategoryOut;
}

export default function CreateNormalThreadForm({
  category,
}: CreateNormalThreadFormProps) {
  const router = useRouter();
  const form = useForm<CreateNormalThreadSchemaInputs>({
    resolver: zodResolver(CreateNormalThreadSchema),
    defaultValues: {
      title: "",
      content: "",
      category: category?.id ? String(category.id) : undefined,
    },
  });

  async function onSubmit(data: CreateNormalThreadSchemaInputs) {
    console.log(data);
    const response = await createNormalThreadAction(data);
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

  useEffect(() => {
    if (category) {
      form.setValue("category", String(category.id));
    }
  }, [category]);

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
                <Input placeholder="Tytuł" {...field} />
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
