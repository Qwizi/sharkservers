'use client'
import { ThreadOut } from "sharkservers-sdk";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "../ui/card";
import { Avatar, AvatarFallback, AvatarImage } from "../ui/avatar";
import Username from "../users/username";
import Link from "next/link";
import slugify from "slugify";
import { dateTimeFormatter } from "@/lib/utils";
import { Badge } from "../ui/badge";
import ThreadBadges from "./thread-badges";
import useCategory from "@/hooks/category";
import { Separator } from "../ui/separator";


export default function Thread({ ...props }: ThreadOut) {
    const { id, title, author, created_at, is_pinned, post_count, is_closed, category, status, server } = props
    const { isApplicationCategory } = useCategory()
    return (
        <Card className={is_pinned ? "border border-blue-400 p-4 animate-pulse" : "p-4 h-[250px]"}>
            <div className="flex">
                <Avatar className="h-12 w-12">
                    <AvatarImage src={author?.avatar} alt={`@${author?.username}`} />
                    <AvatarFallback>{author?.username}</AvatarFallback>
                </Avatar>
                <div className="flex flex-col ml-5">
                    <span><Username user={...author} /> </span>
                    <span className="text-slate-500">{dateTimeFormatter.format(new Date(created_at))}</span>
                </div>
            </div>
            <div>
                <h4 className="text-2xl p-2 mt-2"><Link href={`/forum/${slugify(title)}-${id}`}>{title}</Link></h4>
            </div>
            <div className="flex flex-col mt-10 p-4">
                <Separator />
                <div>
                    Postów: {post_count}
                </div>
                <div>
                <ThreadBadges
                        categoryName={category?.name}
                        is_closed={is_closed}
                        is_pinned={is_pinned}
                        serverName={server ? server.name : ""}
                        status={isApplicationCategory(category) ? status : undefined}
                    />
                </div>
            </div>

        </Card>
    )
}