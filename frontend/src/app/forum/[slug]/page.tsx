import ThreadDetail from "@/components/forum/thread-detail";
import SharkApi, { authApi } from "@/lib/api";
import { sharkApi } from "@/lib/server-api";
import { notFound } from "next/navigation";

export const dynamic = 'force-dynamic'


export default async function ThreadDetailPage({
    params,
    searchParams,
}: {
    params: { slug: string };
    searchParams: { [key: string]: string | string[] | undefined };
}) {
    try {
        const api = await sharkApi()
        let slugSplit = params.slug.split("-")
        let threadId = Number(slugSplit[slugSplit.length - 1]);
        const page = searchParams["page"] ? Number(searchParams["page"]) : 1
        const [
            thread,
            posts
        ] = await Promise.all([
            api.forum.getThread(threadId),
            api.forum.getPosts(threadId, page, 10, "id")
        ])
        return (
            <ThreadDetail thread={...thread} posts={posts} />
        )
    } catch (e) {
        console.log(e)
        return notFound()
    }
}