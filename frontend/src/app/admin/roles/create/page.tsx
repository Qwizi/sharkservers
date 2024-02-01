import CreateRoleForm from "@/components/admin/roles/create-role-form";
import { sharkApi } from "@/lib/server-api";
import { notFound } from "next/navigation";

export default async function AdminCreateRole() {
  try {
    const api = await sharkApi();
    const scopes = await api.adminScopes.adminGetScopes();
    return (
      <div>
        <h1 className="text-3xl font-bold">Utwórz role</h1>
        <div className="mt-8">
          <CreateRoleForm scopes={scopes} />
        </div>
      </div>
    );
  } catch (error) {
    console.log(error);
    return <></>;
  }
}
