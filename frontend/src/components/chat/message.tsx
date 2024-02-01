import { UserOut } from "sharkservers-sdk"
import UserAvatar from "../users/avatar"
import Username from "../users/username"
import { dateTimeFormatter } from "@/lib/utils"

interface IChatMessage {
    id: number,
    message: string
    author: UserOut,
    created_at: string
}

export default function ChatMessage({ ...props }: IChatMessage) {
    const { id, message, author, created_at } = props
    if (!id || !message || !author) return

    return (
        <div className="flex flex-col md:flex-row text-center relative gap-4 px-4 py-4 border-b">
            <div className="hidden md:block">
                <UserAvatar
                    avatar={author.avatar}
                    username={author.username}
                    className="h-8 w-8"
                />

            </div>
            <div className="">
                <Username user={...author} />
            </div>
            <div className="">
                {message}
            </div>
            <div className="absolute right-0">
                <span className="text-slate-500 hidden md:block">{dateTimeFormatter.format(new Date(created_at))}</span>
            </div>
        </div>
    )
}