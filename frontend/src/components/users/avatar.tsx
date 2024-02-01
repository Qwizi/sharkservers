import { Avatar, AvatarFallback, AvatarImage } from "../ui/avatar"

interface IUserAvatar {
    avatar: string | undefined,
    username: string | undefined,
    className: string
}

export default function UserAvatar({ avatar, username, className }: IUserAvatar) {
    return (
        <Avatar className={className}>
            <AvatarImage src={avatar} alt="@shadcn" />
            <AvatarFallback>{username}</AvatarFallback>
            
        </Avatar>
    )
}