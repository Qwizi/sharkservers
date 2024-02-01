import CreateServerForm from "@/components/admin/servers/create-server-form";

export default async function AdminCreateServerPage() {
  return (
    <div>
      <h1 className="text-3xl font-semibold">Dodaj serwer</h1>
      <CreateServerForm />
    </div>
  );
}
