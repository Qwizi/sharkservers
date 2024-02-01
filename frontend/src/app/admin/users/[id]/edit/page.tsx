import EditUserForm from "@/components/admin/users/edit-user-form";
import { sharkApi } from "@/lib/server-api";
import { notFound } from "next/navigation";

export default async function AdminEditUserPage({
  params,
  searchParams,
}: {
  params: { id: number };
  searchParams: { [key: string]: string | string[] | undefined };
}) {
  try {
    const api = await sharkApi();
    const user = await api.adminUsers.adminGetUser(params.id);
    const roles = await api.adminRoles.adminGetRoles();
    return <EditUserForm user={user} roles={roles} />;
  } catch (error) {
    console.log(error);
    return notFound();
  }
}
