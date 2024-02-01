'use client'

import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import { z } from "zod"
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "../ui/form"
import { Button } from "../ui/button"
import { Input } from "../ui/input"
import { useEffect, useState } from "react"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../ui/select"

const formSchema = z.object({
    message: z.string().min(2).max(500)
})

export default function CreateMessageForm({ sendJsonMessage }: any) {
    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            message: "",
        },
    })

    async function onSubmit(data: z.infer<typeof formSchema>) {
        console.log(data.message)
        form.setValue("message", "")
        sendJsonMessage({
            event: "send_message",
            data: data.message
        })
    }

    useEffect(() => {
        form.watch((value, { name, type }) => {
            if (name == "message") {
                if (value?.message?.includes("@")) {
                    console.log("Jest malpa")
                    
                }
            }
        });
    }, [form.watch])

    return (
        <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">

                <FormField
                    control={form.control}
                    name="message"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>Wiadomosc</FormLabel>
                            <FormControl>
                                <Input {...field} />


                            </FormControl>
                            <FormMessage />

                        </FormItem>
                    )}
                />
                <Button type="submit">Wyslij</Button>
            </form>
        </Form>
    )
}