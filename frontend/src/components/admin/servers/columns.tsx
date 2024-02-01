"use client";
import { ServerOut } from "sharkservers-sdk";
import { ColumnDef } from "@tanstack/react-table";
import ActionMenuServer from "./action-menu-server";

export const columns: ColumnDef<ServerOut>[] = [
  {
    accessorKey: "id",
    header: "Id",
  },
  {
    accessorKey: "name",
    header: "Name",
  },
  {
    accessorKey: "ip",
    header: "Ip",
  },
  {
    accessorKey: "port",
    header: "Port",
  },
  {
    id: "actions",
    cell: ({ row }) => {
      const server = row.original;

      return (
        <>
          <ActionMenuServer {...server} />
        </>
      );
    },
  },
];
