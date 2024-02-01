"use client";
import "@uiw/react-md-editor/markdown-editor.css";

import { useState } from "react";
import {
  CategoryOut,
  CategoryTypeEnum,
  Page_CategoryOut_,
  Page_ServerOut_,
} from "sharkservers-sdk";
import { Separator } from "@/components/ui/separator";
import CreateNormalThreadForm from "./create-thread-normal-form";
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { useRouter } from "next/navigation";
import CreateApplicationThreadForm from "./create-thread-application-form";

interface ICreateThread {
  categories: Page_CategoryOut_;
  category?: undefined | CategoryOut;
  servers?: undefined | Page_ServerOut_;
}

export default function CreateThread({
  categories,
  servers,
  category,
}: ICreateThread) {
  const router = useRouter();
  return (
    <div className="rounded-[0.5rem] border bg-background shadow">
      <div className="space-y-6 p-10 md:block">
        <div className="space-y-0.5">
          <h2 className="text-2xl font-bold tracking-tight">Nowy wątek</h2>
          <p className="text-muted-foreground">Utwórz nowy wątek</p>
        </div>
        <Separator />
      </div>
      <div className="p-10 w-full">
        Kategoria:
        <Select
          onValueChange={(value) => {
            router.push(`/forum/create?category=${value}`);
          }}
          defaultValue={category?.id ? String(category?.id) : undefined}
        >
          <SelectTrigger>
            <SelectValue placeholder="Wybierz kategorie" />
          </SelectTrigger>
          <SelectContent>
            <SelectGroup>
              {categories &&
                categories.items.map((category) => {
                  return (
                    <SelectItem value={String(category.id)} key={category.id}>
                      {category.name}
                    </SelectItem>
                  );
                })}
            </SelectGroup>
          </SelectContent>
        </Select>
        {category?.type === CategoryTypeEnum.PUBLIC ? (
          <CreateNormalThreadForm category={category} />
        ) : null}
        {servers && category?.type === CategoryTypeEnum.APPLICATION ? (
          <CreateApplicationThreadForm category={category} servers={servers} />
        ) : null}
      </div>
    </div>
  );
}
