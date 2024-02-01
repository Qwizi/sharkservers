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
import { useState } from "react";
import { useSession } from "next-auth/react";
import useApi from "@/hooks/api";
import useUser from "@/hooks/user";
import { ActivationCodeSchema, ActivationCodeSchemaInputs } from "@/schemas";
import { confirmChangeEmailAction } from "@/actions";

const formSchema = z.object({
    code: z.string().min(5).max(5)
})

interface IConfirmEmailCode {
    setOpen: Function
}

export default function ConfirmEmailCode({ setOpen }: IConfirmEmailCode) {
    const { update, data: session } = useSession()
    const { user } = useUser()
    const api = useApi()
    const form = useForm<z.infer<typeof ActivationCodeSchema>>({
        resolver: zodResolver(ActivationCodeSchema),
        defaultValues: {
            code: "",
        },
    })

    async function onSubmit(data: ActivationCodeSchemaInputs, setOpen: Function) {
        const response = await confirmChangeEmailAction(data)
        console.log(response)
        if (response.serverError) {
            toast({
                variant: "destructive",
                title: "Oh nie. Wystapil bład",
                description: response.serverError === "Bad Request" ? "Nie poprawny kod" : response.serverError
            })
        } else {
            await update({
                ...session,
                user: {
                    ...session?.user,
                    email: response?.data?.email
                }
            })
            setOpen(false)
            toast({
                variant: "success",
                title: "Sukces!",
                description: "Pomyślnie zmieniono adres email"
            })
        }
    }

    return (
        <Form {...form}>
            <form onSubmit={form.handleSubmit((e) => onSubmit(e, setOpen))} className="space-y-8">
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
                <Button type="submit">
                    Potwierdz zmiane
                </Button>
            </form>
        </Form>
    )
}