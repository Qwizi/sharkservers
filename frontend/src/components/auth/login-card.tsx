'use client'
import Link from "next/link";
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from "../ui/card";
import LoginForm from "./login-form";
import RegisterForm from "./register-form";
export default function LoginCard() {
    return (
        <Card>
            <CardHeader>
                <CardTitle>
                    Zaloguj się
                </CardTitle>
            </CardHeader>
            <CardContent>
                <LoginForm />
            </CardContent>
            <CardFooter className="flex flex-col items-start">
                <div>Zapomniales hasła?
                    <Link href="/auth/reset-password"><span className="ml-1 text-blue-600">Zresetuj hasło </span></Link>
                </div>
                <div>
                Nie posiadasz konta?<Link href="/auth/register"><span className="ml-1 text-blue-600">Zarejestruj się </span></Link>
                </div>
            </CardFooter>
        </Card>
    )
}