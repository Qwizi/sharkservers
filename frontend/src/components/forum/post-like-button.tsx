'use client'
import useUser from "@/hooks/user";
import { Button } from "../ui/button";
import { useState } from "react";
import useApi from "@/hooks/api";
import { useRouter } from "next/navigation";
import { ThumbsDown, ThumbsUp } from "lucide-react";

interface IPostLikeButton {
    postId: number | undefined;
    liked: boolean | undefined;
    setLiked: Function;
}

export default function PostLikeButton({postId, liked, setLiked}: IPostLikeButton) {
    const {authenticated, user} = useUser()
    const api = useApi()
    const router = useRouter()

    if (!authenticated || !user || !postId) return

    async function likePost(postId: number) {
        try {
            if (liked) {
                const response = await api.forum.dislikePost(postId)
                console.log(response)
            } else {
                const response = await api.forum.likePost(postId)
                console.log(response)
            }
            
            setLiked(!liked)
            router.refresh()
        } catch(e) {
            console.log(e)
        }
    }

    if (liked) return <Button variant="outline" onClick={(e) => likePost(postId)}><ThumbsDown className="w-4 h-4" /></Button>
    return <Button variant="outline" onClick={(e) => likePost(postId)}><ThumbsUp className="w-4 h-4" /></Button>
}