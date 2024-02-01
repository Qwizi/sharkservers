import { DataTable } from "@/components/admin/data-table";
import { columns } from "@/components/admin/forum-categories/columns";
import Pagination from "@/components/pagination";
import { sharkApi } from "@/lib/server-api";

export default async function AdminForumCategoriesPage({
  searchParams,
}: {
  searchParams: { [key: string]: string | string[] | undefined };
}) {
  const api = await sharkApi();
  let page = searchParams["page"] ? Number(searchParams["page"]) : 1;
  const categories = await api.forum.getCategories(page, 10);
  return (
    <>
      <DataTable columns={columns} data={categories.items} />
      <Pagination total={categories.total} size={categories.size} />
    </>
  );
}
