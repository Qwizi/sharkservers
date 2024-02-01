'use client'
import { UserOut } from "sharkservers-sdk"
import { Card, CardHeader } from "../ui/card"
import PlayerInfo from "./player-info"

export function PlayerCard({ ...props }: any) {    
    return (
      <Card className="">
        <CardHeader className="items-center">
          <PlayerInfo player={...props} avatarClassName="w-28 h-28"/>
        </CardHeader>
      </Card>
    )
  }