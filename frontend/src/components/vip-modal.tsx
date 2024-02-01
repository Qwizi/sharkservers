'use client'
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from "@/components/ui/dialog"
import { useVipModal } from "@/hooks/use-vip-modal"
import { Badge } from "./ui/badge"
import { Button } from "./ui/button"
import { Zap } from "lucide-react"
import useApi from "@/hooks/api"
import { useRouter } from "next/navigation"

export const VipModal = () => {
    const vipModal = useVipModal()
    const api = useApi()
    const router = useRouter()

    async function onCLick() {
        try {
            const sub_data = await api.subscryption.getSubscryption()
            console.log(sub_data.url)
            router.push(sub_data.url)
        } catch (e) {
            console.log(e)
        }
    }

    return (
        <Dialog open={vipModal.isOpen} onOpenChange={vipModal.onClose}>
            <DialogContent>
                <DialogHeader>
                    <DialogTitle className="flex justify-center items-center flex-col gap-y-4 pb-2">
                        <div className="flex items-center gap-x-2 font-bold py-1">
                            Ulepsz konto do pakietu <Badge variant={"vip"}>VIP</Badge>
                        </div>
                    </DialogTitle>
                    <DialogDescription>
                        
                    </DialogDescription>
                </DialogHeader>
                <DialogFooter>
                    <Button
                        variant={"vip"}
                        size="lg"
                        className="w-full"
                        onClick={() => onCLick()}
                    >
                        Ulepsz
                        <Zap className="w-4 h-4 ml-2 fill-white"/>
                    </Button>
                </DialogFooter>
            </DialogContent>
        </Dialog>
    )
}