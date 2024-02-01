import Chat from "@/components/chat/chat";
import ForumContainer from "@/components/forum/forum-container";
import LastPlayers from "@/components/home/last-players";
import WebsiteStats from "@/components/home/website-stats";
import ServersTable from "@/components/servers/servers-table";
import LastOnlineUsers from "@/components/users/last-online-users";
import {sharkApi} from "@/lib/server-api";
import { ApiClient } from "sharkservers-sdk";


export const dynamic = 'force-dynamic'


async function fetchData(api: ApiClient) {
  const [
    serversResult,
    categoriesResult,
    threadsResult,
    lastThreadsResult,
    postsResult,
    usersResult,
    lastOnlineUsersResultsResult,
    lastPlayersResult
  ] = await Promise.allSettled([
    api.servers.getServersStatus(),
    api.forum.getCategories(undefined, 100, "id"),
    api.forum.getThreads(undefined, 10, "-id"),
    api.forum.getThreads(undefined, 5, "-id"),
    api.forum.getPosts(undefined, undefined, 10, "-id"),
    api.users.getUsers(undefined, 1, "-id"),
    api.users.getLastOnlineUsers(undefined, 100),
    api.players.getPlayers(undefined, 15)
  ])
  const servers = serversResult.status === "rejected" ? null : serversResult.value
  const categories = categoriesResult.status === "rejected" ? null : categoriesResult.value
  const threads = threadsResult.status === "rejected" ? null : threadsResult.value
  const lastThreads = lastThreadsResult.status === "rejected" ? null : lastThreadsResult.value
  const posts = postsResult.status === "rejected" ? null : postsResult.value
  const users = usersResult.status === "rejected" ? null : usersResult.value
  const lastOnlineUsers = lastOnlineUsersResultsResult.status === "rejected" ? null : lastOnlineUsersResultsResult.value
  const lastPlayers = lastPlayersResult.status === "rejected" ? null : lastPlayersResult.value
  return {
    servers,
    categories,
    threads,
    lastThreads,
    posts,
    users,
    lastOnlineUsers,
    lastPlayers
  }
}

export default async function Home() {
  const api = await sharkApi()
  const {
    servers,
    categories,
    threads,
    lastThreads,
    posts,
    users,
    lastOnlineUsers,
    lastPlayers
  } = await fetchData(api)
  return (
    <>
      {servers && (
        <ServersTable data={...servers} />
      )}
      
      <Chat />
      {lastPlayers && (
        <LastPlayers players_data={lastPlayers} />
      )}
      <ForumContainer categories={categories} threads={threads} last_threads={lastThreads} />
      
      {lastOnlineUsers && (
        <LastOnlineUsers {...lastOnlineUsers} />
      )}
      <WebsiteStats users_total={users ? users.total : 0} threads_total={threads ? threads.total : 0} posts_total={posts ? posts.total : 0} last_user={users ? users.items[0] : null} />
    </>
  )
}
