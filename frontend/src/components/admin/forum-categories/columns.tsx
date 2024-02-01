"use client";
import { CategoryOut } from "sharkservers-sdk";
import { ColumnDef } from "@tanstack/react-table";
import ActionMenuCategory from "./action-menu-category";

export const columns: ColumnDef<CategoryOut>[] = [
  {
    accessorKey: "id",
    header: "Id",
  },
  {
    accessorKey: "name",
    header: "Nazwa",
  },
  {
    accessorKey: "type",
    header: "Typ kategorii",
  },
  {
    accessorKey: "threads_count",
    header: "Ilosc tematow",
  },
  {
    id: "actions",
    cell: ({ row }) => {
      const category = row.original;

      return (
        <>
          <ActionMenuCategory {...category} />
        </>
      );
    },
  },
];
