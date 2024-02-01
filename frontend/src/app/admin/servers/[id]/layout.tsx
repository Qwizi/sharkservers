import AdminServerLayout from "@/components/admin/servers/layout-server";

export default function AdminLayoutPage({
  children,
}: {
  children: React.ReactNode;
}) {
  return <AdminServerLayout>{children}</AdminServerLayout>;
}
