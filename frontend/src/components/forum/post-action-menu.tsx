import useUser from "@/hooks/user";
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuSeparator, DropdownMenuTrigger } from "../ui/dropdown-menu";
import { Button } from "../ui/button";
import { GripHorizontal } from "lucide-react";
import useApi from "@/hooks/api";
import { useRouter } from "next/navigation";
import { toast } from "../ui/use-toast";

interface IPostActionMenu {
    postId: number | undefined;
    authorId: number | undefined;
    setEditPost: Function
    editPost: boolean
}


export default function PostActionMenu({ postId, authorId, setEditPost, editPost }: IPostActionMenu) {
    const { user, isAuthor, hasScope } = useUser()
    const api = useApi()
    const router = useRouter()

    if (
        !postId ||
        !authorId ||
        !user

    )
        return


    async function deletePost(postId: number) {
        try {

            const response = await api.adminForum.adminDeletePost(postId)
            console.log(response)
            router.refresh()
            toast({
                className: "bg-green-700",
                title: "Pomyślnie usunięto post",
                description: `Post o id ${postId} został pomyślnie usunięty`
            })
        } catch (e) {
            console.log(e)
            toast({
                variant: "destructive",
                title: "Wystapił błąd!",
                description: e.message
            })
        }
    }

    if (user.is_superuser || hasScope(user.roles, "posts:delete")) {
        return (
            <DropdownMenu>
                <DropdownMenuTrigger asChild>
                    <Button variant="secondary" className="float-right">
                        <span className="sr-only">Akcje</span>
                        <GripHorizontal className="h-2 w-2" />
                    </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end">
                    <DropdownMenuItem
                        onClick={(e) => setEditPost(!editPost)}
                    >
                        Edytuj
                    </DropdownMenuItem>
                    <DropdownMenuSeparator />
                    <DropdownMenuItem
                        onClick={(e) => deletePost(postId)}
                        className="text-red-600"
                    >
                        Usuń
                    </DropdownMenuItem>
                </DropdownMenuContent>
            </DropdownMenu>
        )
    } else {
        if (!isAuthor(authorId) || !hasScope(user.roles, "posts:update")) return
        return (
            <DropdownMenu>
                <DropdownMenuTrigger asChild>
                    <Button variant="secondary" className="float-right">
                        <span className="sr-only">Akcje</span>
                        <GripHorizontal className="h-2 w-2" />
                    </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end">
                    <DropdownMenuItem
                        onClick={(e) => setEditPost(!editPost)}
                    >
                        Edytuj
                    </DropdownMenuItem>
                </DropdownMenuContent>
            </DropdownMenu>
        )
    }
}