import { DataTable } from "@/components/admin/data-table";
import { columns } from "@/components/admin/servers/groups/columns";
import { sharkApi } from "@/lib/server-api";
import { notFound } from "next/navigation";

export default async function AdminServerDetailPage({
  params,
  searchParams,
}: {
  params: { id: number };
  searchParams: { [key: string]: string | string[] | undefined };
}) {
  async function detailsTab(server) {
    return <>Server details {server.name}</>;
  }

  async function groupsTab(api, server) {
    const groups = await api.adminServersAdminGroups.adminGetServerAdminsGroups(
      params.id,
    );
    return (
      <>
        <DataTable columns={columns} data={groups.items} />
      </>
    );
  }

  try {
    const api = await sharkApi();
    let tab = searchParams["tab"] || "details";
    const server = await api.adminServers.adminGetServer(params.id);
    switch (tab) {
      case "details":
        return detailsTab(server);
      case "groups":
        return groupsTab(api, server);
      default:
        return notFound();
    }
  } catch (error) {
    console.log(error);
    return notFound();
  }
}
