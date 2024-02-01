import { ThreadActionEnum } from "sharkservers-sdk"
import { Badge } from "../ui/badge"

interface IThreadBadges {
    categoryName: string,
    is_closed: boolean,
    is_pinned: boolean,
    serverName?: string | undefined,
    status?: string | undefined
}

export default function ThreadBadges({ categoryName, is_closed, is_pinned, serverName, status }: IThreadBadges) {

    const ClosedStatusBadge = () => {
        if (is_closed) {
            return <Badge variant="destructive">Zamknięty</Badge>
        }
        return <Badge variant="outline">Otwarty</Badge>
        
    }

    const PinnedStatusBadge = () => {
        if (!is_pinned) return
        return (
            <Badge  className="bg-yellow-400 text-white">Wątek przypiety</Badge>
        )
    }

    const CategoryNameBadge = () => {
        return (
            <Badge className="text-white">{categoryName}</Badge>
        )
    }

    const ServerNameBadge = () => {
        if (!serverName) return
        return <Badge variant="outline">{serverName}</Badge>
    }

    const ThreadStatusBadge = () => {
        if (!status) return
        switch(status) {
            case "approved":
                return <Badge className="bg-green-700 text-white">Zaakceptowany</Badge>
            case "rejected":
                return <Badge variant="destructive">Odrzucony</Badge>
            default:
                return <Badge variant="outline">Nie rozpatrzony</Badge>
        }
    }

    return (
        <div>
            <CategoryNameBadge />
            <ServerNameBadge />
            <ClosedStatusBadge />
            <PinnedStatusBadge />
            <ThreadStatusBadge />
        </div>
    )
}