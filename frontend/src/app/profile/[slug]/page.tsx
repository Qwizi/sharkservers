import Profile from "@/components/profile/profile";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import SharkApi, { authApi } from "@/lib/api";
import { sharkApi } from "@/lib/server-api";
import Image from "next/image"
import { notFound } from "next/navigation";

export default async function UserProfilePage({
    params,
    searchParams,
}: {
    params: { slug: string };
    searchParams: { [key: string]: string | string[] | undefined };
}) {
    try {
        let user_id = Number(params.slug.split("-")[0])
        let slug_username = params.slug.split("-")[1]
        const api = await sharkApi()
        const user = await api.users.getUser(user_id)
        if (slug_username == undefined || slug_username.toLowerCase() !== user.username.toLowerCase()) {
            notFound()
        }
        const threads_data = await api.users.getUserThreads(user_id)
        const posts_data = await api.users.getUserPosts(user_id)
        return (
            <Profile user={...user} threads={threads_data} posts={posts_data}/>
        )
    } catch(e) {
        notFound()
        return
    }
    
}