import useApi from "@/hooks/api";
import useUser from "@/hooks/user";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "../ui/form";
import MarkdownEditor from "@uiw/react-markdown-editor";
import { useRouter } from "next/navigation";
import slugify from "slugify";
import { toast } from "../ui/use-toast";
import { ThreadOut } from "sharkservers-sdk";
import { Button } from "../ui/button";

const formSchema = z.object({
    content: z.string().min(2),
})


export default function ThreadDetailCreatePost({...props }: ThreadOut) {
    const { authenticated, user, hasScope } = useUser()
    const api = useApi()
    const router = useRouter()
    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            content: "",
        },
    })
    const {id, title} = props

    async function onSubmit(data: z.infer<typeof formSchema>) {
        // Do something with the form values.
        // ✅ This will be type-safe and validated.
        try {
            const response = await api.forum.createPost({
                content: data.content,
                thread_id: id
            })
            const postsReq = await api.forum.getPosts(id, undefined, 10)
            console.log(postsReq)
            if (postsReq.total >= 10) {
                const url = `/forum/${slugify(title)}-${id}?page=${postsReq.pages}`
                await router.push(url)
                await router.refresh()
            } else {
                await router.refresh()
                await router.refresh()
            }

            toast({
                className: "bg-green-700",
                title: "Pomyślnie dodano post!",
                description: `Twój post został pomyślnie dodany.`
            })

        } catch (e) {
            console.log(e)
            toast({
                variant: "destructive",
                title: "Wystąpił błąd!",
                description: e.message
            })
        }
    }

    if (!authenticated || !user.roles || !hasScope(user.roles, "posts:create")) return

    return (
        <div className="rounded-[0.5rem] border bg-background shadow mt-10 p-4">
            <Form {...form}>
                <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
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
        </div>
    )
}