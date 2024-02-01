'use client'
import Image from "next/image"
import { Avatar, AvatarFallback, AvatarImage } from "../ui/avatar"
import { Page_PostOut_, Page_ThreadOut_, UserOut } from "sharkservers-sdk"
import { Card, CardContent, CardHeader } from "../ui/card"
import Username from "../users/username"
import { Badge } from "../ui/badge"

interface ProfileInterface {
    user: UserOut,
    posts: Page_PostOut_,
    threads: Page_ThreadOut_,
}

export default function Profile({ ...props }: ProfileInterface) {
    const {user, posts, threads} = props
    const { id, username, avatar, display_role, created_at } = user
    return (
        <div className="flex flex-col">
            <div className="h-[200px] w-full bg-slate-700">

            </div>
            
            <div className="border p-4 grid grid-cols-4">
                <div className="flex flex-col mt-[-60px] ml-10 w-[150px] text-center">
                    <Avatar className="h-[100px] w-[100px] mx-auto">
                        <AvatarImage src={avatar} className="mx-auto" alt="@shadcn" width="100px" height="120" />
                        <AvatarFallback>{username}</AvatarFallback>
                    </Avatar>
                    <Username user={...user}/>
                    <Badge className="w-full" variant="outline" style={{ color: display_role?.color }}>{display_role?.name}</Badge>
                </div>
                <div>
                    Postów: {posts.total}
                </div>
                <div>
                    Tematów: {threads.total}
                </div>
                <div>
                    123
                </div>
            </div>
            <div className="grid mt-10 grid-cols-2">
                <div className="w-3/4">
                    <Card>
                        <CardContent>
                            <CardHeader>
                                Informacje
                            </CardHeader>
                            Dołączył: {created_at}
                        </CardContent>
                        
                    </Card>
                </div>

                <div className="w-full">
                <Card>
                        <CardContent>
                            <CardHeader>
                                Informacje
                            </CardHeader>
                            123
                        </CardContent>
                        
                    </Card>
                </div>
            </div>
        </div>
    )
}