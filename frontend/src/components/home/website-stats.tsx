'use client'
import { MessageSquare, MessagesSquare, Users } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";
import { UserOut } from "sharkservers-sdk";
import { Avatar, AvatarFallback, AvatarImage } from "../ui/avatar";
import Username from "../users/username";
import { dateTimeFormatter } from "@/lib/utils";
import UserAvatar from "../users/avatar";

interface IWebsiteStats {
    users_total: number;
    threads_total: number
    posts_total: number
    last_user: UserOut
}



export default function WebsiteStats({ users_total, threads_total, posts_total, last_user }: IWebsiteStats) {

    return (
        <div className="
            mt-32 
            mb-10 
            grid
            grid-cols-1
            md:grid-cols-4 
            md:justify-between 
            md:justify-items-between
        ">
            <div className="flex">
                <div className="p-4 bg-primary rounded-[0.5rem] h-16 w-16">
                    <MessageSquare className="w-8 h-8 mx-auto" />
                </div>
                <div className="flex flex-col">
                    <div className="align-middle mt-[10px] pl-[30px] text-xl">{threads_total}</div>
                    <div className="align-middle mt-[10px] pl-[30px] text-sm">Napisanych tematów</div>
                </div>
            </div>
            <div className="flex">
                <div className="p-4 bg-primary rounded-[0.5rem] h-16 w-16">
                    <MessagesSquare className="w-8 h-8" />
                </div>
                <div className="flex flex-col">
                    <div className="align-middle mt-[10px] pl-[30px] text-xl">{posts_total}</div>
                    <div className="align-middle mt-[10px] pl-[30px] text-sm">Napisanych postów</div>
                </div>
            </div>
            <div className="flex">
                <div className="p-4 bg-primary rounded-[0.5rem] h-16 w-16">
                    <Users className="w-8 h-8" />
                </div>
                <div className="flex flex-col">
                    <div className="align-middle mt-[10px] pl-[30px] text-xl">{users_total}</div>
                    <div className="align-middle mt-[10px] pl-[30px] text-sm">Użytkowników</div>
                </div>
            </div>
            <div className="flex">
                {last_user ? (
                    <>
                        <div className="mt-[15px]">
                            <UserAvatar avatar={last_user.avatar} username={last_user.username} className="h-12 w-12" />
                        </div>
                        <div className="flex flex-col">
                            <div className="align-middle mt-[10px] pl-[30px] text-xl">
                                <Username user={...last_user} />
                            </div>
                            <div className="align-middle mt-[10px] pl-[30px] text-sm">
                                <span className="text-slate-500">Dołączył {dateTimeFormatter.format(new Date(last_user.created_at))}</span>
                            </div>
                        </div>
                    </>
                ) : null}

            </div>
        </div>
    )

}