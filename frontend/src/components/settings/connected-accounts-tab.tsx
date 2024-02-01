'use client'
import { useRouter } from "next/navigation";
import { Button } from "../ui/button";
import { Separator } from "../ui/separator";
import useUser from "@/hooks/user";
import PlayerInfo from "../users/player-info";
import Image from "next/image"
export default function ConnectedAccountTab() {
    const { player } = useUser()
    console.log(player)
    const router = useRouter()
    return (
        <div className="space-y-6">
            <div>
                <h3 className="text-lg font-medium">Połączone konta</h3>
                <p className="text-sm text-muted-foreground">
                    Połącz swoje konto z kontami społecznościowymi
                </p>
            </div>
            <Separator />
            <div className="grid grid-cols-1 gap-4">
                {player ? (
                    <div className="flex flex-col">
                        Steam: <PlayerInfo player={...player} usernameClassName="text-xs"/>
                    </div>
                    
                ) : <Image 
                    src="/images/steam_button.png" 
                    alt="Login to steam" 
                    width="180" 
                    height="35" 
                    onClick={() => router.push("/settings/connected-accounts/steam")}
                    className="hover:cursor-pointer"
                    />

                }

            </div>
        </div>
    )
}