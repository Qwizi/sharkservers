'use client';
import { useForm } from "react-hook-form";
import * as z from "zod"
import { zodResolver } from "@hookform/resolvers/zod"
import {
    Form,
    FormControl,
    FormDescription,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { Button } from "../ui/button";
import {signIn, SignInResponse} from "next-auth/react";
import { toast } from "../ui/use-toast";
import { useRouter, useSearchParams } from "next/navigation";
import { useEffect } from "react";




const formSchema = z.object({
    username: z.string().min(2).max(32).regex(new RegExp('^[a-zA-Z0-9_-]+$'), "Nazwa użytkownika musi zawierac tylko litery, cyfry oraz znaki specjalne - _"),
    password: z.string().min(8),
})


export default function LoginForm() {
    const router = useRouter()
    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            username: "",
        },
    })
    const searchPararms = useSearchParams()
    
    useEffect(() => {
        const errorParam = searchPararms.get("error")
        console.log(errorParam)
        if (errorParam == "CredentialsSignin") {
            const timeout = setTimeout(() => {
                toast({
                    variant: "destructive",
                    title: "Wystapił problem",
                    description: "Nie poprawny login/hasło"
                })
            }, 0)
        
            return (() => clearTimeout(timeout))
        }
    }, [searchPararms, toast])

    async function onSubmit(values: z.infer<typeof formSchema>) {
        // Do something with the form values.
        // ✅ This will be type-safe and validated.
        const response: SignInResponse | undefined = await signIn("credentials", {
            username: values.username,
            password: values.password,
            redirect: true
        })
        console.log(response)
        
    }

    return (
        <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
            <FormField
                    control={form.control}
                    name="username"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>Nazwa użytkownika</FormLabel>
                            <FormControl>
                                <Input placeholder="nazwa użytkownika" {...field} />
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
                <Button type="submit">Zaloguj się</Button>
            </form>
        </Form>
    )
}