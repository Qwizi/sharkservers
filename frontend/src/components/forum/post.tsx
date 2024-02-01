import { PostOut } from "sharkservers-sdk";
import Username from "../users/username";
import { useEffect, useState } from "react";
import MarkdownPreview from '@uiw/react-markdown-preview';
import UpdatePostForm from "./update-post-form";
import RoleBadge from "../users/role-badge";
import PostActionMenu from "./post-action-menu";
import UserAvatar from "../users/avatar";
import UserInfo from "../users/user-info";
import PostLikeButton from "./post-like-button";
import useApi from "@/hooks/api";
import useUser from "@/hooks/user";
import { Separator } from "../ui/separator";


export default function Post({ ...props }: PostOut) {
    //@ts-ignore
    const { id, author, content, threadAuthorId } = props
    const [editPost, setEditPost] = useState(false)
    const [liked, setLiked] = useState(false)
    const [likes, setLikes] = useState()
    const api = useApi()
    const { user } = useUser()



    function userLikePost(likes) {
        let userLike = false
        likes.items.map((like, i) => {
            if (user.id == like.author.id) {
                userLike = true
            }
        })
        return userLike
    }

    useEffect(() => {
        const getLikes = async () => {
            const response = await api.forum.getPostLikes(id)
            setLikes(response)
            if (userLikePost(response)) {
                setLiked(true)
            }
        }
        getLikes().catch(console.error)
    }, [liked]);
    if (!author || !content || !likes) return

    return (
        <div id={`post-${id}`} className="rounded-[0.5rem] border bg-background shadow mt-5">
            <div className="p-10 w-full flex flex-col md:flex-row gap-10">
                <div className="flex flex-col items-center w-full md:w-1/6  rounded-[0.5rem]  p-4 text-center h-[250px]">
                    <UserInfo
                        user={...author}
                        avatarClassName="h-15 w-15  mx-auto"
                    />
                </div>
                <div className="flex flex-col rounded-[0.5rem] p-2 w-full">
                    <div className="ml-auto flex w-full justify-between">
                        <div className="flex flex-col w-full">
                            {editPost && editPost ? (
                                <UpdatePostForm content_prop={content} authorId={author.id} postId={id} setEditPost={setEditPost} />
                            ) : (
                                <div className="prose dark:prose-invert">
                                    <MarkdownPreview source={content} />
                                </div>

                            )}

                            <div className="ml-auto flex flex-col w-full justify-end mt-32">
                                <Separator />
                                <div className="float-right">
                                    <span className="text-sm">Polubien {likes.total}</span> <PostLikeButton postId={id} liked={liked} setLiked={setLiked} />
                                </div>


                            </div>

                        </div>
                        <PostActionMenu
                            postId={id}
                            authorId={author?.id}
                            setEditPost={setEditPost}
                            editPost={editPost}
                        />

                    </div>
                </div>
            </div>
        </div>
    )
}