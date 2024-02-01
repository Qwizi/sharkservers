import { DataTable } from "@/components/admin/data-table";
import { columns } from "@/components/admin/scopes/columns";
import Pagination from "@/components/pagination";
import { sharkApi } from "@/lib/server-api";

export default async function AdminScopesPage({
  searchParams,
}: {
  searchParams: { [key: string]: string | string[] | undefined };
}) {
  const api = await sharkApi();
  let page = searchParams["page"] ? Number(searchParams["page"]) : 1;
  const scopes = await api.adminScopes.adminGetScopes(page, 10);
  return (
    <>
      <DataTable columns={columns} data={scopes.items} />
      <Pagination total={scopes.total} size={scopes.size} />
    </>
  );
}
