import { ThreadOut } from "sharkservers-sdk";
import { Card } from "../ui/card";
import { Avatar, AvatarFallback, AvatarImage } from "../ui/avatar";
import { title } from "@uiw/react-md-editor";
import slugify from "slugify";
import Username from "../users/username";
import Link from "next/link";
import { dateTimeFormatter } from "@/lib/utils";

export default function LastThread({ ...props }: ThreadOut) {
    const { id, title, created_at, author } = props;
    return (
        <div className={"p-2"}>
            <div className="flex">
                <div className="w-20">
                    <Avatar className="h-12 w-12 ">
                        <AvatarImage src={author?.avatar} alt={`@${author?.username}`} />
                        <AvatarFallback>{author?.username}</AvatarFallback>
                    </Avatar>

                </div>

                <div className="w-80">
                    <h4 className="text-xl whitespace-normal "><Link href={`/forum/${slugify(title)}-${id}`}>{title}</Link></h4>
                    <div>

                        <span className="text-sm text-m">przez</span> <Username user={...author} />
                    </div>
                    <div>
                        <span className="text-slate-500 text-xs">{dateTimeFormatter.format(new Date(created_at))}</span>
                    </div>

                </div>

            </div>

        </div>
    )
}