'use client'
import useApi from "@/hooks/api";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "../ui/form";
import { Input } from "../ui/input";
import { Button } from "../ui/button";
import { toast } from "../ui/use-toast";
import { useEffect } from "react";

const formSchema = z.object({
    email: z.string().email()
})

interface IResetPasswordForm {
    setTab: Function;
    defaultEmail?: string | undefined
    disabledEmailField?: boolean | undefined
}

export default function ResetPasswordForm({setTab, defaultEmail, disabledEmailField}: IResetPasswordForm) {
    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            email: defaultEmail,
        },
    })
    const api = useApi()

    useEffect(() => {
        if (!defaultEmail) return
        form.setValue("email", defaultEmail)
    }, [defaultEmail])

    async function onSubmit(data: z.infer<typeof formSchema>) {
        try {
            const response = api.auth.forgotPasswordRequest({email: data.email})
            console.log(response)
            setTab("confirm")
            toast({
                variant: "default",
                title: "Sukces!",
                description: "Pomyślnie wysłano e-mail z kodem aktywacyjnym"
            })
        } catch(e) {
            console.log(e)
            toast({
                variant: "destructive",
                title: "Uh oh! Wystąpil bład.",
                description: e.message,
                //action: <ToastAction altText="Try again">Try again</ToastAction>,
              })
        }
    }

    if (!defaultEmail) return

    return (
        <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
                <FormField
                    control={form.control}
                    name="email"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>E-mail</FormLabel>
                            <FormControl>
                                <Input defaultValue={defaultEmail} {...field} 
                                    type="email"
                                    disabled={disabledEmailField}
                                    
                                />
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
