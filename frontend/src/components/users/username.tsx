'use client'
import Link from "next/link";
import {
    HoverCard,
    HoverCardContent,
    HoverCardTrigger,
} from "@/components/ui/hover-card"
import UserAvatar from "./avatar";
import RoleBadge from "./role-badge";
import { UserOut } from "sharkservers-sdk";
import OnlineStatus from "./online-status";
import UserInfo from "./user-info";
import PlayerInfo from "./player-info";
import { Separator } from "../ui/separator";

interface IUsername {
    user: UserOut
    className?: string | undefined
}
export default function Username({ user, className }: IUsername) {
    const {player} = user
    return (
        <HoverCard >
            <HoverCardTrigger className={className} key={user.id} href={`/profile/${user.id}-${user.username}`} style={{ color: user.display_role?.color }}>
                {user.username}
            </HoverCardTrigger>
            <HoverCardContent className={player ? "w-[250px] h-[350px]" : "w-[250px] h-[200px]"}>
                <UserInfo user={...user} />
                {player && (
                    <>
                    <Separator className="mt-4 mb-4"/>
                    <PlayerInfo player={...player}  avatarClassName="rounded-none"/>
                    </>
                    
                )}
            </HoverCardContent>
        </HoverCard>

    )
}