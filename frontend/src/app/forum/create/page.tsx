import { authOptions } from "@/app/api/auth/[...nextauth]/route";
import CreateThread from "@/components/forum/thread/create-thread";
import SharkApi, { authApi } from "@/lib/api";
import { sharkApi } from "@/lib/server-api";
import { Session, getServerSession } from "next-auth";
import { notFound, redirect } from "next/navigation";
import { CategoryTypeEnum } from "sharkservers-sdk";

export default async function CreateThreadPage({
  searchParams,
}: {
  searchParams: { [key: string]: string | string[] | undefined };
}) {
  const session: Session | null = await getServerSession(authOptions);
  if (!session?.user?.player) {
    return redirect("/settings/connected-accounts");
  }
  try {
    const api = await sharkApi();
    const categories = await api.forum.getCategories(undefined, 100, "id");
    const categoryId = searchParams["category"]
      ? searchParams["category"]
      : undefined;

    if (categoryId) {
      const categoryObj = await api.forum.getCategory(Number(categoryId));
      if (categoryObj.type === CategoryTypeEnum.APPLICATION) {
        const servers = await api.servers.getServers(
          undefined,
          undefined,
          1,
          100,
        );
        return (
          <CreateThread
            categories={categories}
            category={categoryObj}
            servers={servers}
          />
        );
      }
      return <CreateThread categories={categories} category={categoryObj} />;
    }

    return <CreateThread categories={categories} />;
  } catch (e) {
    notFound();
  }
}
