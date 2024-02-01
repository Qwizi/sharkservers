'use client';

import { useState } from "react";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "../ui/card";
import RegisterForm from "./register-form";
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from "@/components/ui/dialog"
import { ContextMenu, ContextMenuTrigger, ContextMenuContent, ContextMenuItem } from "@radix-ui/react-context-menu";
import { Button } from "../ui/button";
import ActivateAccountForm from "./activate-account-form";
import Link from "next/link";

export function RegisterCard() {
    const [openDialog, setOpenDialog] = useState(false)
    return (
        <>
            <Card>
                <CardHeader>
                    <CardTitle>
                        Zarejestruj się
                    </CardTitle>
                </CardHeader>
                <CardContent>
                    <RegisterForm setOpenDialog={setOpenDialog} />
                </CardContent>
                <CardFooter>
                Posiadasz konto? <Link href="/auth/login">  <span className="ml-1 text-blue-600">Zaloguj się</span></Link>
            </CardFooter>
            </Card>
        </>

    )
}