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
import SharkApi from "@/lib/api";
import { toast } from "../ui/use-toast";
import { useSession } from "next-auth/react";
import useApi from "@/hooks/api";
import { changeUsernameAction } from "@/actions";
import { ChangeUsernameSchemaInputs } from "@/schemas";


const formSchema = z.object({
    username: z.string().min(2).max(32).regex(new RegExp('^[a-zA-Z0-9_-]+$'), "Nazwa użytkownika musi zawierac tylko litery, cyfry oraz znaki specjalne - _"),
})


export default function UsernameForm() {
    const { data: session, update } = useSession()
    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            username: session?.user?.username,
        },
    })
    const api = useApi()

    async function onSubmit(data: ChangeUsernameSchemaInputs) {
        const response = await changeUsernameAction(data)
        if (response.serverError) {
            toast({
                variant: "destructive",
                title: "Oh nie. Wystapil bład",
                description: response.serverError === "Bad request" ? "Podana nazwa użytkownika jest już zajeta" : response.serverError
            })
        } else {
            await update({
                ...session,
                user: {
                    ...session?.user,
                    username: data.username
                }
            })
            toast({
                variant: "success",
                title: "Sukces!",
                description: "Pomyslnie zaaktualizowano nazwe użytkownika"
            })
        }
        // Do something with the form values.
        // ✅ This will be type-safe and validated.
        // try {
        //     const response = await api.users.changeUserUsername({
        //         username: data.username
        //     })
        //     await update({
        //         ...session,
        //         user: {
        //             ...session?.user,
        //             username: data.username
        //         }
        //     })
        //     toast({
        //         variant: "default",
        //         title: "Sukces!",
        //         description: "Pomyslnie zaaktualizowano nazwe użytkownika"
        //     })
        // } catch(e) {
        //     let errorMessage = "Wystapil nieoczekiwany blad"
        //     if (e.status == 400) {
        //         errorMessage = "Podana nazwa uzytkownika jest niedostępna"
        //     }
        //     console.log(e)
        //     toast({
        //         variant: "destructive",
        //         title: "Oh nie. Wystapil bład",
        //         description: errorMessage
        //     })
        // }
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
                                <Input {...field} defaultValue={session?.user?.username} />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    )}
                />
                <Button type="submit">Aktualizuj</Button>
            </form>
        </Form>
    )
}