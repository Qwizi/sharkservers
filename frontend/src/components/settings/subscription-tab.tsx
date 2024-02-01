'use client'

import useUser from "@/hooks/user"
import { Badge } from "../ui/badge"
import { Button } from "../ui/button"
import { Separator } from "../ui/separator"
import useApi from "@/hooks/api"
import { useRouter } from "next/navigation"

export default function SubscriptionTab() {
    const api = useApi()
    const {isVip} = useUser()
    const router = useRouter()


    async function onClick() {
        try {
            const sub_data = await api.subscryption.getSubscryption()
            console.log(sub_data.url)
            router.push(sub_data.url)
        } catch (e) {
            console.log(e)
        }
    }

    return (
        <div className="space-y-6">
            <div>
            <div className="flex items-center gap-x-2 font-bold py-1">
                    <h3 className="text-lg font-medium">Subscrypcja </h3> <Badge variant="vip">VIP</Badge>
                </div>
                <p className="text-sm text-muted-foreground">
                    Aktualnie nie posiadasz żadnej subscrypcji
                </p>
            </div>
            <Separator />
            
            <Button variant={"vip"} onClick={() => onClick()}>{isVip ? "Zarządzaj subscrypcja": "Ulepsz konto"}</Button>
        </div>
    )
}