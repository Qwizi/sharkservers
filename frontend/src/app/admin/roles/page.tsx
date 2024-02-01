import { DataTable } from "@/components/admin/data-table";
import { columns } from "@/components/admin/roles/columns";
import Pagination from "@/components/pagination";
import { sharkApi } from "@/lib/server-api";

export default async function AdminRolesPage({
  searchParams,
}: {
  searchParams: { [key: string]: string | string[] | undefined };
}) {
  const api = await sharkApi();
  let page = searchParams["page"] ? Number(searchParams["page"]) : 1;
  const roles = await api.adminRoles.adminGetRoles(page, 10);
  return (
    <>
      <DataTable columns={columns} data={roles.items} />
      <Pagination total={roles.total} size={roles.size} />
    </>
  );
}
