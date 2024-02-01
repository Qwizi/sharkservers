"use client";
import { UserOutWithEmail } from "sharkservers-sdk";
import { ColumnDef } from "@tanstack/react-table";

import ActionMenuUser from "./action-menu-user";

export const columns: ColumnDef<UserOutWithEmail>[] = [
  {
    accessorKey: "id",
    header: "Id",
  },
  {
    accessorKey: "username",
    header: "Username",
  },
  {
    accessorKey: "email",
    header: "Email",
  },
  {
    accessorKey: "is_superuser",
    header: "Superuser",
  },
  {
    accessorKey: "is_activated",
    header: "Activated",
  },
  {
    id: "actions",
    cell: ({ row }) => {
      const user = row.original;

      return (
        <>
          <ActionMenuUser {...user} />
        </>
      );
    },
  },
];
