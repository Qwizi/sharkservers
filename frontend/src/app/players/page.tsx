import Pagination from "@/components/pagination"
import { UserCard } from "@/components/users/card"
import SharkApi, { authApi } from "@/lib/api"
import { Page_UserOut_ } from "sharkservers-sdk"
import {notFound} from "next/navigation"
import { PlayerCard } from "@/components/users/player-card"
import { sharkApi } from "@/lib/server-api"

export const dynamic = 'force-dynamic'

export default async function PlayersPage({
    searchParams,
}: {
searchParams: { [key: string]: string | string[] | undefined };
}) {
    const api = await sharkApi()
    let page = searchParams["page"] ? Number(searchParams["page"]) : 1
    const players_data: any = await api.players.getPlayers(page, 12)
    console.log(api)
    return (
        <section>
            <div className="grid grid-cols-1 lg:grid-cols-4 gap-4">
            {players_data.items.map((player, i) =>
                <PlayerCard key={i} {...player} />
            )}
            </div>
            <Pagination total={players_data.total} size={12}/>
        </section>
    )
}
