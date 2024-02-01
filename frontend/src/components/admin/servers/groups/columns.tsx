"use client";
import { GroupOut } from "sharkservers-sdk";
import { ColumnDef } from "@tanstack/react-table";

export const columns: ColumnDef<GroupOut>[] = [
  {
    accessorKey: "id",
    header: "Id",
  },
  {
    accessorKey: "name",
    header: "Name",
  },
  {
    accessorKey: "flags",
    header: "Flags",
  },
  {
    accessorKey: "immunity_level",
    header: "immunity_level",
  },
  {
    id: "actions",
    cell: ({ row }) => {
      const group = row.original;

      return <></>;
    },
  },
];
