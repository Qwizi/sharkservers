import { DataTable } from "@/components/admin/data-table";
import { columns } from "@/components/admin/users/columns";
import Pagination from "@/components/pagination";
import { sharkApi } from "@/lib/server-api";

export default async function AdminUsersPage({
  searchParams,
}: {
  searchParams: { [key: string]: string | string[] | undefined };
}) {
  const api = await sharkApi();
  let page = searchParams["page"] ? Number(searchParams["page"]) : 1;
  const users = await api.adminUsers.adminGetUsers(page, 10);
  return (
    <>
      <DataTable columns={columns} data={users.items} />
      <Pagination total={users.total} size={users.size} />
    </>
  );
}
