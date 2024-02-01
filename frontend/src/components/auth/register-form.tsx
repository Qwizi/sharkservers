'use client';
import { SubmitHandler, useForm } from "react-hook-form";
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
import { useRouter } from "next/navigation";
import SharkApi from "@/lib/api";
import { useToast } from "@/components/ui/use-toast"

import * as ReCAPTCHA from "react-google-recaptcha";
import { useRef } from "react";
import useApi from "@/hooks/api";
import { registerUserAction } from "@/actions"


export const registerFormSchema = z.object({
    username: z.string().min(2).max(32).regex(new RegExp('^[a-zA-Z0-9_-]+$'), "Nazwa użytkownika musi zawierac tylko litery, cyfry oraz znaki specjalne - _"),
    email: z.coerce.string().email(),
    password: z.string().min(8),
    password2: z.string().min(8)
})
.refine((data) => data.password === data.password2, {
    message: "Hasła nie sa takie same",
    path: ["password"],
})

export type RegisterUserInputs = z.infer<typeof registerFormSchema>

interface IRegisterForm {
    setOpenDialog: Function
}


export default function RegisterForm({setOpenDialog}: IRegisterForm) {
    const router = useRouter()
    const form = useForm<z.infer<typeof registerFormSchema>>({
        resolver: zodResolver(registerFormSchema),
        defaultValues: {
            username: "",
            email: "",
            password: "",
            password2: ""
        },
    })
    const { toast } = useToast()

    const registerUser: SubmitHandler<RegisterUserInputs> = async data => {
        const response = await registerUserAction(data)
        console.log(response.validationError)
        if (response.serverError) {
            toast({
                variant: "destructive",
                title: "Ups. Coś poszło nie tak",
                description: response.serverError
            })
        } else {
            router.push("/auth/activate-account?registration=true")
        }
    }

    return (
        <Form {...form}>
            <form onSubmit={form.handleSubmit(registerUser)} className="space-y-8">
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
                    name="email"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>Email</FormLabel>
                            <FormControl>
                                <Input type="email" {...field} placeholder="username@website.pl" {...field} />
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
                <Button className="g-recaptcha" data-sitekey="6LcfKN0nAAAAAEldDutKmu8OMlmiLgFJQsRkLYdG" type="submit" data-action='submit'>Zarejestruj się</Button>
            </form>
        </Form>
    )
}