import ForumContainer from "@/components/forum/forum-container";
import ForumFilters from "@/components/forum/forum-filters";
import Pagination from "@/components/pagination";
import SharkApi, { authApi } from "@/lib/api";
import { sharkApi } from "@/lib/server-api";


export const dynamic = 'force-dynamic'

export default async function ForumPage({
    searchParams,
}: {
    searchParams: { [key: string]: string | string[] | undefined };
}) {
    const api = await sharkApi()
    const page = searchParams["page"] ? Number(searchParams["page"]) : 1
    const category = searchParams["category"] ? Number(searchParams["category"]) : undefined
    const server = searchParams["server"] ? Number(searchParams["server"]) : undefined
    const order_by = searchParams["order_by"] ? String(searchParams["order_by"]) : "-id"
    const status = searchParams["status"] ? searchParams["status"] : undefined
    const closed = searchParams["closed"] ? searchParams["closed"] : false

    const [
        categoriesResult,
        threadsResult,
        lastThreadsResult,
        serversResult
    ] = await Promise.allSettled([
        //@ts-ignore
        api.forum.getCategories(undefined, 100, "id"),
        api.forum.getThreads(page, 10, order_by, category, server, status, closed),
        api.forum.getThreads(page, 5, "-id"),
        api.servers.getServers()
    ])

    const categories = categoriesResult.status === "rejected" ? null : categoriesResult.value
    const threads = threadsResult.status === "rejected" ? null : threadsResult.value
    const lastThreads = lastThreadsResult.status === "rejected" ? null : lastThreadsResult.value
    const servers = serversResult.status === "rejected" ? null : serversResult.value

    if (!categories || !threads || !lastThreads || !servers) return
    return (
        
        <>
            <ForumFilters categories={categories} servers={servers}/>
            <ForumContainer categories={categories} threads={threads} last_threads={lastThreads}/>
            <Pagination total={threads.total} />
        </>
        
    )
}