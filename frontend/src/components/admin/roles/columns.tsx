"use client";
import { RoleOut } from "sharkservers-sdk";
import { ColumnDef } from "@tanstack/react-table";
import ActionMenuRole from "./action-menu-role";

export const columns: ColumnDef<RoleOut>[] = [
  {
    accessorKey: "id",
    header: "Id",
  },
  {
    accessorKey: "name",
    header: "Name",
  },
  {
    id: "actions",
    cell: ({ row }) => {
      const role = row.original;

      return (
        <>
          <ActionMenuRole {...role} />
        </>
      );
    },
  },
];
