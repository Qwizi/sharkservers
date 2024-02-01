'use client'
import UserAvatar from "../users/avatar";

export default function LastPlayers({ players_data }: any) {
    return (
        <div className="h-full w-full rounded-[inherit] mt-10">
            <h3 className="text-2xl font-semibold leading-none tracking-tight flex">Gracze</h3>
            {players_data?.total > 0 ? players_data.items.map((player, i) =>
                <UserAvatar
                    key={i}
                    avatar={player.avatar}
                    username={player.username}
                    className={"h-12 w-12 mt-5"}
                />
            ) : <p>Brak graczy</p>}
        </div>
    )
}