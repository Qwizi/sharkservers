'use client'
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select"
import { Page_CategoryOut_, Server_QGM } from "sharkservers-sdk"
import { Form, FormControl, FormDescription, FormField, FormItem, FormLabel, FormMessage } from "../ui/form"
import { Link } from "lucide-react"
import { Button } from "../ui/button"
import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import { z } from "zod"
import { toast } from "../ui/use-toast"
import { useRouter, useSearchParams } from "next/navigation"
import useCategory from "@/hooks/category"

interface IForumFilters {
    categories: Page_CategoryOut_,
    servers: {
        items: Server_QGM[],
        total: number,
        page?: number,
        size?: number,
        pages?: number
    }
}

const FormSchema = z.object({
    closed: z.string().optional(),
    server: z.string().optional(),
    order_by: z.string().optional(),
    status: z.string().optional()
})

export default function ForumFilters({ categories, servers }: IForumFilters) {
    const router = useRouter()
    const searchParams = useSearchParams()
    const form = useForm<z.infer<typeof FormSchema>>({
        resolver: zodResolver(FormSchema),
        defaultValues: {
            closed: "false",
            server: undefined,
            order_by: "-id",
            status: ""
        },
    })
    const { isApplicationCategoryMany } = useCategory(categories)
    const categoryId = Number(searchParams.get("category"))

    function onSubmit(data: z.infer<typeof FormSchema>) {
        console.log(data)
        let url = `/forum?`

        if (categoryId > 0) {
            url += `category=${categoryId}`
        }

        if (data.closed) {
            url += `&closed=${data.closed}`
        }
        if (data.server && Number(data.server) > 0) {
            url += `&server=${data.server}`
        }
        if (data.order_by) {
            url += `&order_by=${data.order_by}`
        }
        if (data.status) {
            url += `&status=${data.status}`
        }
        router.push(url)
    }
    return (
        <div className="border p-4 rounded-sm">
            <h4>Filtry</h4>
            <Form {...form}>
                <form onSubmit={form.handleSubmit(onSubmit)} className="w-full grid gap-4 grid-cols-1 md:grid-cols-3">
                    <FormField
                        control={form.control}
                        name="closed"
                        render={({ field }) => (
                            <FormItem>
                                <FormLabel>Wątek zamknięty?</FormLabel>
                                <Select onValueChange={field.onChange} defaultValue={field.value}>
                                    <FormControl>
                                        <SelectTrigger>
                                            <SelectValue placeholder="Wątek zamknięty" />
                                        </SelectTrigger>
                                    </FormControl>
                                    <SelectContent>
                                        <SelectItem value="true">Tak</SelectItem>
                                        <SelectItem value="false">Nie</SelectItem>
                                    </SelectContent>
                                </Select>
                                <FormMessage />
                            </FormItem>
                        )}
                    />

                    {isApplicationCategoryMany(categoryId) && (
                        <>
                            <FormField
                                control={form.control}
                                name="status"
                                render={({ field }) => (
                                    <FormItem>
                                        <FormLabel>Status</FormLabel>
                                        <Select onValueChange={field.onChange} defaultValue={"pending"}>
                                            <FormControl>
                                                <SelectTrigger>
                                                    <SelectValue placeholder="Status" />
                                                </SelectTrigger>
                                            </FormControl>
                                            <SelectContent>
                                                <SelectItem value="pending">Oczekujacy</SelectItem>
                                                <SelectItem value="approved">Zaakcepotwany</SelectItem>
                                                <SelectItem value="rejected">Odrzucony</SelectItem>
                                            </SelectContent>
                                        </Select>
                                        <FormMessage />
                                    </FormItem>
                                )}
                            />
                            <FormField
                                control={form.control}
                                name="server"
                                render={({ field }) => (
                                    <FormItem>
                                        <FormLabel>Server</FormLabel>
                                        <Select onValueChange={field.onChange} defaultValue="0">
                                            <FormControl>
                                                <SelectTrigger>
                                                    <SelectValue placeholder="Serwer" />
                                                </SelectTrigger>
                                            </FormControl>
                                            <SelectContent>
                                                <SelectItem value="0">Brak</SelectItem>
                                                {servers && servers.items.map((server, i) =>
                                                    <SelectItem key={i} value={String(server.id)}>{server.name}</SelectItem>
                                                )}

                                            </SelectContent>
                                        </Select>
                                        <FormMessage />
                                    </FormItem>
                                )}
                            />
                        </>

                    )}
                    <FormField
                        control={form.control}
                        name="order_by"
                        render={({ field }) => (
                            <FormItem>
                                <FormLabel>Sortuj</FormLabel>
                                <Select onValueChange={field.onChange} defaultValue="-id">
                                    <FormControl>
                                        <SelectTrigger>
                                            <SelectValue placeholder="Filtruj po" />
                                        </SelectTrigger>
                                    </FormControl>
                                    <SelectContent>
                                        <SelectItem value="-id">ID malejaco</SelectItem>
                                        <SelectItem value="id">ID rosnąco</SelectItem>
                                    </SelectContent>
                                </Select>
                                <FormMessage />
                            </FormItem>
                        )}
                    />
                    <div>
                        <Button type="submit" className="text-white mt-8">Zapisz</Button>
                    </div>

                </form>
            </Form>
        </div>
    )
}