import { UserOut } from "sharkservers-sdk";
import UserAvatar from "./avatar";
import Username from "./username";
import user from "@/hooks/user";
import OnlineStatus from "./online-status";
import RoleBadge from "./role-badge";
import { dateFormatter, dateTimeFormatter } from "@/lib/utils";
import { MessageSquare, MessagesSquare } from "lucide-react";
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "../ui/tooltip";


interface IUserInfo {
    user: UserOut,
    className?: string | undefined
    avatarClassName?: string | undefined
    usernameClassName?: string | undefined
    badgeClassName?: string | undefined
    onlineStatusClassName?: string | undefined
}

export default function UserInfo({ user, className, avatarClassName, usernameClassName, badgeClassName, onlineStatusClassName }: IUserInfo) {
    if (!user) return
    const { avatar, username, display_role, last_online, created_at, threads_count, posts_count } = user;
    return (
        <div className={className ? className : "flex flex-col items-center text-center"}>
            <UserAvatar
                avatar={avatar}
                username={username}
                className={avatarClassName ? avatarClassName : "h-12 w-12 mx-auto"}
            />
            <div className="flex">
                <Username
                    user={...user}
                    className={usernameClassName ? usernameClassName : "mt-2"}
                />
                <OnlineStatus last_online_date={last_online} />
            </div>
            <RoleBadge {...display_role} />
            <div className="mt-2 grid grid-cols-2 gap-4">
                <TooltipProvider>
                    <Tooltip>
                        <TooltipTrigger>
                            <div className="flex">
                                <MessageSquare className="w-4 h-4" />
                                <span className="ml-1 text-slate-500 text-xs">
                                    {threads_count}
                                </span>
                            </div>
                            </TooltipTrigger>
                        <TooltipContent>
                            <p>Liczba tematów</p>
                        </TooltipContent>
                    </Tooltip>
                </TooltipProvider>
                <TooltipProvider>
                    <Tooltip>
                        <TooltipTrigger>
                            <div className="flex">
                                <MessagesSquare className="w-4 h-4" />
                                <span className="ml-1 text-slate-500 text-xs">
                                    {posts_count}
                                </span>
                            </div>
                        </TooltipTrigger>
                        <TooltipContent>
                            <p>Liczba postów</p>
                        </TooltipContent>
                    </Tooltip>
                </TooltipProvider>
            </div>
        </div>

    )

}