'use client'

import useApi from "@/hooks/api"
import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import { z } from "zod"
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "../ui/form"
import { Button } from "../ui/button"
import { Input } from "../ui/input"
import { toast } from "../ui/use-toast"
import { useRouter } from "next/navigation"

const formSchema = z.object({
    code: z.string().min(5).max(5),
    password: z.string().min(8),
    password2: z.string().min(8)
}).refine((data) => data.password === data.password2, {
    message: "Hasła nie sa takie same",
    path: ["password"],
})

export default function ConfirmResetPasswordForm() {
    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            code: "",
            password: "",
            password2: ""
        },
    })
    const router = useRouter()
    const api = useApi()



    async function onSubmit(data: z.infer<typeof formSchema>) {
        try {
            const response = await api.auth.resetPassword({
                code: data.code,
                password: data.password,
                password2: data.password2
            })
            console.log(response)
            toast({
                variant: "default",
                title: "Sukces!",
                description: "Pomyślnie zresetowano hasło"
            })
            router.push("/")
        } catch (e) {
            console.log(e)
            toast({
                variant: "destructive",
                title: "Uh oh! Wystąpil bład.",
                description: e.message,
                //action: <ToastAction altText="Try again">Try again</ToastAction>,
            })
        }
    }

    return (
        <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
                <FormField
                    control={form.control}
                    name="code"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>Kod aktywacyjny</FormLabel>
                            <FormControl>
                                <Input {...field} />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    )}
                />
                <FormField
                    control={form.control}
                    name="password"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>Hasło</FormLabel>
                            <FormControl>
                                <Input type="password" {...field} placeholder="hasło" {...field} />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    )}
                />
                <FormField
                    control={form.control}
                    name="password2"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>Powtórz hasło</FormLabel>
                            <FormControl>
                                <Input type="password" {...field} placeholder="hasło" {...field} />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    )}
                />
                <Button type="submit">Resetuj hasło</Button>
            </form>
        </Form>
    )
}