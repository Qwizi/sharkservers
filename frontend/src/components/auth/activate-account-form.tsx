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
import useApi from "@/hooks/api";
import { activateUserAction } from "@/actions";
import { ActivationCodeSchemaInputs } from "@/schemas";


const formSchema = z.object({
    code: z.string().min(5).max(5)
})


export default function ActivateAccountForm() {
    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            code: "",
        },
    })
    const api = useApi()

    async function onSubmit(data: ActivationCodeSchemaInputs) {
        const response = await activateUserAction(data)
        if (response.serverError) {
            toast({
                variant: "destructive",
                title: "Ups. Coś poszło nie tak",
                description: response.serverError === "Bad request" ? "Nie poprawny kod" : response.serverError
            })
        } else {
            toast({
                variant: "success",
                title: "Sukces!",
                description: "Pomyślnie aktywowano konto"
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
                <Button type="submit">Aktywuj konto</Button>
            </form>
        </Form>
    )
}