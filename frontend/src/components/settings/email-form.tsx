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
import useUser from "@/hooks/user";
import { EmailSchemaInputs, emailSchema } from "@/schemas";
import { requestChangeEmailAction } from "@/actions";


const formSchema = z.object({
    email: z.coerce.string().email(),
})

interface IEmailForm {
    setOpen: Function
}


export default function EmailForm({setOpen}: IEmailForm) {
    const { data: session, update } = useSession()
    const {user} = useUser()
    const form = useForm<z.infer<typeof emailSchema>>({
        resolver: zodResolver(emailSchema),
        defaultValues: {
            email: "",
        },
    })
    const api = useApi()

    async function onSubmit(data: EmailSchemaInputs, setOpen: Function) {
        // Do something with the form values.
        // ✅ This will be type-safe and validated.
        // console.log(data)
        // try {
        //     const response = await api.users.requestChangeUserEmail({
        //         email: data.email
        //     })
        //     console.log(response)
        //     setOpen(true)
        // } catch(e) {
        //     console.log(e)
        //     let errorMessage = "Wystapil nieoczkiwany blad"
        //     toast({
        //         variant: "destructive",
        //         title: "Wystapił bład",
        //         description: errorMessage
        //     })
        // }
        const response = await requestChangeEmailAction(data)
        console.log(response)

        if (response.serverError) {
            toast({
                variant: "destructive",
                title: "Oh nie. Wystapil bład",
                description: response.serverError
            })
        } else {
            setOpen(true)
        }
    }

    return (
        <Form {...form}>
            <form onSubmit={form.handleSubmit((e) => onSubmit(e, setOpen))} className="space-y-8">
                <FormField
                    control={form.control}
                    name="email"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>E-mail</FormLabel>
                            <FormControl>
                                <Input {...field} defaultValue={user?.email}/>
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    )}
                />
                <Button type="submit">Wyślij email</Button>
            </form>
        </Form>
    )
}