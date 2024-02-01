import EditServerForm from "@/components/admin/servers/edit-server-form";
import EditUserForm from "@/components/admin/users/edit-user-form";
import { sharkApi } from "@/lib/server-api";
import { notFound } from "next/navigation";

export default async function AdminEditServerPage({
  params,
  searchParams,
}: {
  params: { id: number };
  searchParams: { [key: string]: string | string[] | undefined };
}) {
  try {
    const api = await sharkApi();
    const user = await api.servers.getServer(params.id);
    return <EditServerForm server={user} />;
  } catch (error) {
    console.log(error);
    return notFound();
  }
}
