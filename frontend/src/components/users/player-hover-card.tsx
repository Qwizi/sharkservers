import { Player_OOJ } from "sharkservers-sdk"
import { HoverCard, HoverCardContent, HoverCardTrigger } from "../ui/hover-card"
import user from "@/hooks/user"
import UserInfo from "./user-info"
import { Badge } from "../ui/badge"
import PlayerInfo from "./player-info"

interface IUserInfo {
    player: Player_OOJ,
    className?: string | undefined
    avatarClassName?: string | undefined
    usernameClassName?: string | undefined
    badgeClassName?: string | undefined
    onlineStatusClassName?: string | undefined
}


export default function PlayerHoverCard({ player, className, avatarClassName }: IUserInfo) {
    const { id, steamid32 } = player
    return (
        <HoverCard >
            <HoverCardTrigger className={className} key={id}>
                <Badge variant="outline" className="text-white text-xs">{steamid32}</Badge>
            </HoverCardTrigger>
            <HoverCardContent className="w-[200px] h-[150px]">
                <PlayerInfo player={...player} />
            </HoverCardContent>
        </HoverCard>
    )
}