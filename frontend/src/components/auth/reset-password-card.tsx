'use client'
import { useState } from "react";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "../ui/card";
import ResetPasswordForm from "./reset-password-form";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import ConfirmResetPasswordForm from "./confirm-reset-password-form";
import ResetPasswordTab from "./reset-password-tab";

export default function ResetPasswordCard() {
    const [tab, setTab] = useState("e-mail");

    return (
        <>
            <Card>
                <CardHeader>
                    <CardTitle>
                        Zresetuj hasło
                    </CardTitle>
                </CardHeader>
                <CardContent>
                    <ResetPasswordTab tab={tab} setTab={setTab}/>
                </CardContent>
            </Card>
        </>
    )
}