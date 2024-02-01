'use client'
import { useState } from "react";
import ResetPasswordTab from "../auth/reset-password-tab";
import { Separator } from "../ui/separator";
import useUser from "@/hooks/user";

export default function PasswordTab() {
    const [tab, setTab] = useState("e-mail")
    const {user} = useUser()
    return (
        <div className="space-y-6">
            <div>
                <h3 className="text-lg font-medium">Zmień hasło</h3>
                <p className="text-sm text-muted-foreground">
                    Zaaktualizuj swoje hasło
                </p>
            </div>
            <Separator />
            <ResetPasswordTab 
                tab={tab} 
                setTab={setTab}
                defaultEmail={user?.email}
                disabledEmailField={true}
            />
        </div>
    )
}