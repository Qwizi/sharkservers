import CreateForumCategoryForm from "@/components/admin/forum-categories/create-category-form";
import CreateServerForm from "@/components/admin/servers/create-server-form";

export default async function AdminCreateForumCategoryPage() {
  return (
    <div>
      <h1 className="text-3xl font-semibold">Dodaj kategorie</h1>
      <CreateForumCategoryForm />
    </div>
  );
}
