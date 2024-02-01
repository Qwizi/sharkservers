import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import { z } from "zod"
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "../ui/form"
import { Button } from "../ui/button"
import dynamic from "next/dynamic"
import { toast } from "../ui/use-toast"
import { useSession } from "next-auth/react"
import { useRouter } from "next/navigation"
import useApi from "@/hooks/api"
import useUser from "@/hooks/user"

const MarkdownEditor = dynamic(
    () => import("@uiw/react-markdown-editor").then((mod) => mod.default),
    { ssr: false }
);

const formSchema = z.object({
    content: z.string().min(2),
})

interface IUpdatePostForm {
    postId: number
    authorId: number
    content_prop: string
    setEditPost: Function
}

export default function UpdatePostForm({ postId, authorId, content_prop, setEditPost }: IUpdatePostForm) {
    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            content: content_prop,
        },
    })
    const { data: session, status } = useSession()
    const router = useRouter()
    const api = useApi()
    const { isAuthor } = useUser()

    async function onSubmit(data: z.infer<typeof formSchema>, postId: number, authorId: number, setEditPost: Function) {
        try {
            const response =
                isAuthor(authorId)
                    ? await api.forum.updatePost(postId, {
                        content: data.content,
                    })
                    : await api.adminForum.adminUpdatePost({
                        content: data.content
                    })

            console.log(response)
            toast({
                className: "bg-green-700",
                title: "Pomyślnie zaaktualizowano post",
                description: ``
            })
            setEditPost(false)
            router.refresh()
        } catch (e) {
            toast({
                variant: "destructive",
                title: "Wystapił błąd!",
                description: e.message
            })
        }
    }

    return (
        <Form {...form}>
            <form onSubmit={form.handleSubmit((e) => onSubmit(e, postId, authorId, setEditPost))} className="space-y-8">
                <FormField
                    control={form.control}
                    name="content"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>Treść wiadomosci</FormLabel>
                            <FormControl>
                                <MarkdownEditor height="250px" {...field} value={field.value} />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    )}
                />

                <Button type="submit">Dodaj odpowiedź</Button>
            </form>
        </Form>
    )
}