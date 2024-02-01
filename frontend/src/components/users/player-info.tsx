import { Player_OOJ, UserOut } from "sharkservers-sdk";
import UserAvatar from "./avatar";
import { TooltipProvider, Tooltip, TooltipTrigger, TooltipContent } from "@radix-ui/react-tooltip";
import { MessageSquare, MessagesSquare } from "lucide-react";
import Link from "next/link";
import { Badge } from "../ui/badge";
import Image from "next/image";

interface IUserInfo {
    player: Player_OOJ,
    className?: string | undefined
    avatarClassName?: string | undefined
    usernameClassName?: string | undefined
    badgeClassName?: string | undefined
    onlineStatusClassName?: string | undefined
}

export default function PlayerInfo({ player, className, avatarClassName, usernameClassName, badgeClassName, onlineStatusClassName }: IUserInfo) {
    const { avatar, username, steamid32, steamrep_profile, profile_url } = player
    return (
        <div className={className ? className : "flex flex-col items-center text-center"}>
            <UserAvatar
                avatar={avatar}
                username={username}
                className={avatarClassName ? avatarClassName : "h-12 w-12 mx-auto"}
            />
            <div className="flex">
                {username}
            </div>
            <div className="mt-2 grid grid-cols-1 gap-4">
                <div>
                    <Badge variant="outline" className="text-white text-xs">{steamid32}</Badge>
                </div>
            </div>
            <div className="mt-2 grid grid-cols-2 gap-4">
                <div>
                    <Badge className="text-white">
                        <Link href={profile_url}>Profil</Link>
                    </Badge>
                </div>
                <div>
                    <Badge className="text-white"><Link href={steamrep_profile?.profile_url}>SteamRep</Link></Badge>
                </div>
            </div>
        </div>
    )
}