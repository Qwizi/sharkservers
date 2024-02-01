import { DataTable } from "@/components/admin/data-table";
import { columns } from "@/components/admin/servers/columns";
import Pagination from "@/components/pagination";
import { sharkApi } from "@/lib/server-api";

export default async function AdminServersPage({
  searchParams,
}: {
  searchParams: { [key: string]: string | string[] | undefined };
}) {
  const api = await sharkApi();
  let page = searchParams["page"] ? Number(searchParams["page"]) : 1;
  const servers = await api.servers.getServers(undefined, undefined, page, 10);
  return (
    <>
      <DataTable columns={columns} data={servers.items} />
      <Pagination total={servers.total} size={servers.size} />
    </>
  );
}
