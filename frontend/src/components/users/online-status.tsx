import {
    Tooltip,
    TooltipContent,
    TooltipProvider,
    TooltipTrigger,
} from "@/components/ui/tooltip"

interface IOnlineStatus {
    last_online_date: Date
}

export default function OnlineStatus({ last_online_date }: IOnlineStatus) {
    const lastUserOnlineDate = new Date(last_online_date)
    const currentDate = new Date()
    const timeDifference = currentDate.getTime() - lastUserOnlineDate.getTime();
    // 15 minutes
    const online = timeDifference <= 900_000

    if (online) {
        return (
            <div>
                <TooltipProvider>
                    <Tooltip>
                        <TooltipTrigger>
                            <span className="animate-ping ml-2 h-2 w-2 align-middle mt-4 rounded-full bg-green-400 opacity-75 float-right "></span>
                        </TooltipTrigger>
                        <TooltipContent>
                            Online
                        </TooltipContent>
                    </Tooltip>
                </TooltipProvider>

            </div>
        )
    }

    return (
        <div>
            <TooltipProvider>
                <Tooltip>
                    <TooltipTrigger>
                        <span className="ml-1 h-2 w-2 align-middle mt-4 rounded-full bg-red-400 opacity-75 float-right "></span>
                    </TooltipTrigger>
                    <TooltipContent>
                        Offline
                    </TooltipContent>
                </Tooltip>
            </TooltipProvider>

        </div>
    )
}