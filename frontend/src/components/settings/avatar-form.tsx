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
import { changeAvatarSchema, ChangeAvatarSchemaInputs } from "@/schemas";
import { changeAvatarAction } from "@/actions";


const formSchema = z.object({
    avatar:  z.any()
})


export default function AvatarForm() {
    const { data: session, update } = useSession()
    const form = useForm<z.infer<typeof changeAvatarSchema>>({
        resolver: zodResolver(changeAvatarSchema),
    })
    const api = useApi()

    async function onSubmit(data: ChangeAvatarSchemaInputs) {
        //!!TODO Zmien na serverAction
        try {
            const formData = new FormData();
            formData.append("file", data.avatar[0]);
            const response = await api.users.uploadUserAvatar({
                avatar: data.avatar
            })
            const userResponse = await api.users.getLoggedUser()
            console.log(userResponse)
            await update({
                ...session,
                user: {
                    ...session?.user,
                    avatar: userResponse.avatar
                }
            })
            console.log(response)
            toast({
                variant: "default",
                title: "Success",
                description: "Zaaktualizwano avatar!"
            })
        } catch (e) {
            console.log(e)
            toast({
                variant: "destructive",
                title: "Wystapił bład",
                description: e.message
            })
        }
        
    }

    return (
        <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
                <FormField
                    control={form.control}
                    name="avatar"
                    render={({ field: { value, onChange, ...field }}) => (
                        <FormItem>
                            <FormLabel>Avatar</FormLabel>
                            <FormControl>
                                <Input {...field} type="file" value={value?.fileName}
                                onChange={(event) => {
                                    onChange(event.target.files[0]);
                                }}
                                />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    )}
                />
                <Button type="submit">Przeslij</Button>
            </form>
        </Form>
    )
}